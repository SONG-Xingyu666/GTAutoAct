from run_jointformer import train
import run_jointformer
from data.h3wb.utils.utils import json_loader, json_loader_part
import numpy as np
from common.h36m_dataset import Human36mDataset
import argparse
import torch
import torch.nn as nn
import torch.backends.cudnn as cudnn
from models.jointformer import JointTransformer
import os.path as path
from common.log import Logger, savefig
import datetime
import os
from torch.utils.tensorboard import SummaryWriter
from common.generators import PoseGenerator
from torch.utils.data import DataLoader, random_split
import sys
import csv
from common.utils import AverageMeter, lr_decay, save_ckpt, model_load_2_3
import random
from data.h3wb.utils.utils import draw_skeleton
import json

joints_num = 133

action_list = ["Directions",
                "Discussion",
                "Eating",
                "Greeting",
                "Phoning",
                "Photo",
                "Posing",
                "Purchases",
                "Sitting",
                "SittingDown",
                "Smoking",
                "Waiting",
                "WalkDog",
                "Walking",
                "WalkTogether"]


def train_worker(data_path, downsample=1, num_layers=4, dropout=0, 
                 hid_dim=128, intermediate=False, spatial_encoding=False,
                 pred_dropout=0.0, embedding_type='conv', no_error_prediction=False,
                 d_inner=512, lr=1.0e-3, resume='', evaluate='', checkpoint='checkpoint',
                 batch_size=64, num_workers=8, epochs=100, lr_decay=100000, lr_gamma=0.96,
                 max_norm=True, snapshot=5):
    # Loading data
    print('==> Loading dataset...')
    # poses_2d: 80000x[1,133,2]
    # poses_3d: 80000x[1,133,3]
    poses_2d, poses_3d = json_loader_part(data_path=data_path)
    actions = []
    names = []
    with open(path.join(data_path, 'image_list.csv')) as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            names.append(row[0])
            actions.append(row[1])
    # actions = actions[:10]
    # names = names[:10]
    # Generate pose datasets
    dataset = PoseGenerator(poses_3d=poses_3d, 
                            poses_2d=poses_2d, 
                            actions=actions,
                            datasets='h3wb')
    
    train_dataset, valid_dataset = random_split(
        dataset=dataset, lengths=[int(0.8*len(dataset)), len(dataset)-int(0.8*len(dataset))])

    train_loader = DataLoader(dataset=train_dataset, batch_size=batch_size, 
                             shuffle=True, num_workers=num_workers, 
                             sampler=None, pin_memory=True)
    valid_loader = DataLoader(dataset=valid_dataset, batch_size=batch_size, 
                             shuffle=True, num_workers=num_workers, 
                             sampler=None, pin_memory=True)

    
    # Create model
    stride = downsample
    cudnn.benchmark = True
    model = JointTransformer(num_joints_in=joints_num, n_layers=num_layers, encoder_dropout=dropout, 
                             d_model=hid_dim, intermediate=intermediate, spatial_encoding=spatial_encoding, 
                             pred_dropout=pred_dropout, embedding_type=embedding_type, 
                             error_prediction=not no_error_prediction, d_inner=d_inner, n_head=8).cuda()
    print("==> Total parameters: {:.2f}M".format(sum(p.numel() for p in model.parameters()) / 1000000.0))
    criterion = nn.MSELoss(reduction='mean').cuda()
    optimizer = torch.optim.AdamW(model.parameters(), lr=lr)

    # Optionally resume from a checkpoint
    if resume or evaluate:
        ckpt_path = (resume if resume else evaluate)

        if path.isfile(ckpt_path):
            print("==> Loading checkpoint '{}'".format(ckpt_path))
            ckpt = torch.load(ckpt_path)
            start_epoch = ckpt['epoch']
            error_best = ckpt['error']
            glob_step = ckpt['step']
            lr_now = ckpt['lr']
            model.load_state_dict(ckpt['state_dict'])
            optimizer.load_state_dict(ckpt['optimizer'])
            print("==> Loaded checkpoint (Epoch: {} | Error: {})".format(start_epoch, error_best))

            if resume:
                ckpt_dir_path = path.dirname(ckpt_path)
                logger = Logger(path.join(ckpt_dir_path, 'log.txt'), resume=True)
        else:
            raise RuntimeError("==> No checkpoint found at '{}'".format(ckpt_path))
    else:
        start_epoch = 0
        error_best = None
        glob_step = 0
        lr_now = lr
        ckpt_dir_path = path.join(checkpoint, datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S"))

        if not path.exists(ckpt_dir_path):
            os.makedirs(ckpt_dir_path)
            print('==> Making checkpoint dir: {}'.format(ckpt_dir_path))

        logger = Logger(os.path.join(ckpt_dir_path, 'log.txt'))
        # logger.file.write('{}'.format(args))
        logger.file.write('\n')
        logger.file.flush()
        logger.set_names(['epoch', 'lr', 'loss_train', 'error_eval_p1', 'error_eval_p2'])
        visualizer = SummaryWriter(log_dir=ckpt_dir_path)
    
    # Data pre-processing
    # poses_train, poses_train_2d, actions_train, names_train = fetch(subjects_train, dataset, keypoints, action_filter, stride, image_names=image_names)

    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, epochs * len(train_loader))

    for epoch in range(start_epoch, epochs):
        print('\nEpoch: %d | LR: %.8f' % (epoch + 1, lr_now))

        # Train for one epoch
        epoch_loss, lr_now, glob_step = train(train_loader, model, criterion, optimizer, lr, lr_now,
                                              glob_step, lr_decay, lr_gamma, max_norm=max_norm, 
                                              intermediate=intermediate, scheduler=scheduler, visualizer=visualizer,
                                              error_prediction=not no_error_prediction)

        # Evaluate
        error_eval_p1, error_eval_p2 = run_jointformer.evaluate(valid_loader, model, intermediate=intermediate)

        # Update log file
        visualizer.add_scalar('Train/{}'.format('loss'), epoch_loss, global_step=glob_step)
        visualizer.add_scalar('Train/{}'.format('lr'), lr_now, global_step=glob_step)
        if intermediate:
            for k in range(num_layers):
                visualizer.add_scalar('Test/{}{}'.format('MPJPE', k), error_eval_p1[k].avg, global_step=glob_step)
                visualizer.add_scalar('Test/{}{}'.format('P-MPJPE', k), error_eval_p2[k].avg, global_step=glob_step)
            error_eval_p1 = error_eval_p1[-1].avg
            error_eval_p2 = error_eval_p2[-1].avg
        else:
            visualizer.add_scalar('Test/{}'.format('MPJPE'), error_eval_p1, global_step=glob_step)
            visualizer.add_scalar('Test/{}'.format('P-MPJPE'), error_eval_p2, global_step=glob_step)
        logger.append([epoch + 1, lr_now, epoch_loss, error_eval_p1, error_eval_p2])

        # Save checkpoint
        if error_best is None or error_best > error_eval_p1:
            error_best = error_eval_p1
            save_ckpt({'epoch': epoch + 1, 'lr': lr_now, 'step': glob_step, 'state_dict': model.state_dict(),
                       'optimizer': optimizer.state_dict(), 'error': error_eval_p1}, ckpt_dir_path, suffix='best')

        if (epoch + 1) % snapshot == 0:
            save_ckpt({'epoch': epoch + 1, 'lr': lr_now, 'step': glob_step, 'state_dict': model.state_dict(),
                       'optimizer': optimizer.state_dict(), 'error': error_eval_p1}, ckpt_dir_path)

    logger.close()
    logger.plot(['loss_train', 'error_eval_p1'])
    savefig(path.join(ckpt_dir_path, 'log.eps'))
    visualizer.close()
    return

# input: poses_2d (list): n*tensor[1,133,2]
# output: poses_3d (list): n*tensor[1,133,3]
# make sure n < 970 due to the cuda memory 
def prediction(poses_2d, ckpt_path, output_path, num_layers=4, dropout=0, 
                 hid_dim=128, intermediate=False, spatial_encoding=False,
                 pred_dropout=0.0, embedding_type='conv', no_error_prediction=False,
                 d_inner=512, lr=1.0e-3):
    if not path.exists(output_path):
        os.makedirs(output_path)
    print("==> 3D skeletons will be saved at '{}'".format(output_path))
    model = JointTransformer(num_joints_in=joints_num, n_layers=num_layers, encoder_dropout=dropout, 
                             d_model=hid_dim, intermediate=intermediate, spatial_encoding=spatial_encoding, 
                             pred_dropout=pred_dropout, embedding_type=embedding_type, 
                             error_prediction=not no_error_prediction, d_inner=d_inner, n_head=8).cuda()
    optimizer = torch.optim.AdamW(model.parameters(), lr=lr)
    if path.isfile(ckpt_path):
        print("==> Loading checkpoint '{}'".format(ckpt_path))
        ckpt = torch.load(ckpt_path)
        start_epoch = ckpt['epoch']
        error_best = ckpt['error']
        model.load_state_dict(ckpt['state_dict'])
        optimizer.load_state_dict(ckpt['optimizer'])
        print("==> Loaded checkpoint (Epoch: {} | Error: {})".format(start_epoch, error_best))
    else:
        raise RuntimeError("==> No checkpoint found at '{}'".format(ckpt_path))
    poses_3d = []
    print("==> Predicting total: {}".format(len(poses_2d)))
    for i, pose_2d in enumerate(poses_2d):
        print("==> Predicting pose {}".format(i))
        pose_2d = pose_2d.cuda()
        pose_3d, _, _ = model(pose_2d, None)
        pose_3d = pose_3d.cpu()
        poses_3d.append(pose_3d)
    print("==> Predicting finished")
    text = []
    for frame, pose_3d in enumerate(poses_3d):
        pose_3d = pose_3d[0].tolist()
        text.append({'frame_id':frame, 'instances':{'keypoints': pose_3d}})
    output_json_path = os.path.join(output_path, 'res_3d.json')
    f = open(output_json_path, 'w')
    text = json.dumps(text, indent=2)
    f.write(text)
    f.close()

    return poses_3d
        


if __name__ == '__main__':
    data_path = r''
    ckpt_path = r''
    output_path = r'demo'
    # train_worker(data_path=data_path, epochs=200)
    # _, poses_2d = json_loader(data_path=data_path, task=1, type='test')
    # poses_2d = poses_2d[:1]
    poses_2d = [torch.tensor([json.load(open(r'overall0440.json'))[0]['keypoints']])]

    poses_3d = prediction(poses_2d=poses_2d, ckpt_path=ckpt_path, output_path=output_path) 
    print(np.shape(poses_3d[0]))
    draw_skeleton(poses_3d[0].detach(), plt_show=True, save_path=output_path)

