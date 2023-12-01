ann_file_test = 'data/kinetics400/kinetics400_val_list_videos.txt'
ann_file_train = 'data/kinetics400/kinetics400_train_list_videos.txt'
ann_file_val = 'data/kinetics400/kinetics400_val_list_videos.txt'
data_root = 'data/kinetics400/videos_train'
data_root_val = 'data/kinetics400/videos_val'
dataset_type = 'VideoDataset'
default_hooks = dict(
    checkpoint=dict(
        interval=1, max_keep_ckpts=5, save_best='auto', type='CheckpointHook'),
    logger=dict(ignore_last=False, interval=20, type='LoggerHook'),
    param_scheduler=dict(type='ParamSchedulerHook'),
    runtime_info=dict(type='RuntimeInfoHook'),
    sampler_seed=dict(type='DistSamplerSeedHook'),
    sync_buffers=dict(type='SyncBuffersHook'),
    timer=dict(type='IterTimerHook'))
default_scope = 'mmaction'
env_cfg = dict(
    cudnn_benchmark=False,
    dist_cfg=dict(backend='nccl'),
    mp_cfg=dict(mp_start_method='fork', opencv_num_threads=0))
launcher = 'none'
load_from = None
log_level = 'INFO'
log_processor = dict(by_epoch=True, type='LogProcessor', window_size=20)
model = dict(
    backbone=dict(
        conv1_kernel=(
            1,
            7,
            7,
        ),
        conv1_stride_t=1,
        depth=50,
        inflate=(
            0,
            0,
            1,
            1,
        ),
        lateral=False,
        norm_eval=False,
        out_indices=(
            2,
            3,
        ),
        pool1_stride_t=1,
        pretrained='torchvision://resnet50',
        type='ResNet3dSlowOnly'),
    cls_head=dict(
        average_clips='prob',
        consensus=dict(dim=1, type='AvgConsensus'),
        dropout_ratio=0.5,
        in_channels=2048,
        init_std=0.01,
        num_classes=400,
        spatial_type='avg',
        type='TPNHead'),
    data_preprocessor=dict(
        format_shape='NCTHW',
        mean=[
            123.675,
            116.28,
            103.53,
        ],
        std=[
            58.395,
            57.12,
            57.375,
        ],
        type='ActionDataPreprocessor'),
    neck=dict(
        aux_head_cfg=dict(loss_weight=0.5, out_channels=400),
        downsample_cfg=dict(downsample_scale=(
            1,
            1,
            1,
        )),
        in_channels=(
            1024,
            2048,
        ),
        level_fusion_cfg=dict(
            downsample_scales=(
                (
                    1,
                    1,
                    1,
                ),
                (
                    1,
                    1,
                    1,
                ),
            ),
            in_channels=(
                1024,
                1024,
            ),
            mid_channels=(
                1024,
                1024,
            ),
            out_channels=2048),
        out_channels=1024,
        spatial_modulation_cfg=dict(
            in_channels=(
                1024,
                2048,
            ), out_channels=2048),
        temporal_modulation_cfg=dict(downsample_scales=(
            8,
            8,
        )),
        type='TPN',
        upsample_cfg=dict(scale_factor=(
            1,
            1,
            1,
        ))),
    test_cfg=dict(fcn_test=True),
    train_cfg=None,
    type='Recognizer3D')
optim_wrapper = dict(
    clip_grad=dict(max_norm=40, norm_type=2),
    optimizer=dict(
        lr=0.01, momentum=0.9, nesterov=True, type='SGD', weight_decay=0.0001))
param_scheduler = [
    dict(
        begin=0,
        by_epoch=True,
        end=150,
        gamma=0.1,
        milestones=[
            75,
            125,
        ],
        type='MultiStepLR'),
]
randomness = dict(deterministic=False, diff_rank_seed=False, seed=None)
resume = False
test_cfg = dict(type='TestLoop')
test_dataloader = dict(
    batch_size=4,
    dataset=dict(
        ann_file='data/kinetics400/kinetics400_val_list_videos.txt',
        data_prefix=dict(video='data/kinetics400/videos_val'),
        pipeline=[
            dict(type='DecordInit'),
            dict(
                clip_len=8,
                frame_interval=8,
                num_clips=10,
                test_mode=True,
                type='SampleFrames'),
            dict(type='DecordDecode'),
            dict(scale=(
                -1,
                256,
            ), type='Resize'),
            dict(crop_size=256, type='ThreeCrop'),
            dict(input_format='NCTHW', type='FormatShape'),
            dict(type='PackActionInputs'),
        ],
        test_mode=True,
        type='VideoDataset'),
    num_workers=4,
    persistent_workers=True,
    sampler=dict(shuffle=False, type='DefaultSampler'))
test_evaluator = dict(type='AccMetric')
test_pipeline = [
    dict(type='DecordInit'),
    dict(
        clip_len=8,
        frame_interval=8,
        num_clips=10,
        test_mode=True,
        type='SampleFrames'),
    dict(type='DecordDecode'),
    dict(scale=(
        -1,
        256,
    ), type='Resize'),
    dict(crop_size=256, type='ThreeCrop'),
    dict(input_format='NCTHW', type='FormatShape'),
    dict(type='PackActionInputs'),
]
train_cfg = dict(
    max_epochs=150, type='EpochBasedTrainLoop', val_begin=1, val_interval=10)
train_dataloader = dict(
    batch_size=8,
    dataset=dict(
        ann_file='data/kinetics400/kinetics400_train_list_videos.txt',
        data_prefix=dict(video='data/kinetics400/videos_train'),
        pipeline=[
            dict(type='DecordInit'),
            dict(
                clip_len=8, frame_interval=8, num_clips=1,
                type='SampleFrames'),
            dict(type='DecordDecode'),
            dict(type='RandomResizedCrop'),
            dict(keep_ratio=False, scale=(
                224,
                224,
            ), type='Resize'),
            dict(flip_ratio=0.5, type='Flip'),
            dict(type='ColorJitter'),
            dict(input_format='NCTHW', type='FormatShape'),
            dict(type='PackActionInputs'),
        ],
        type='VideoDataset'),
    num_workers=4,
    persistent_workers=True,
    sampler=dict(shuffle=True, type='DefaultSampler'))
train_pipeline = [
    dict(type='DecordInit'),
    dict(clip_len=8, frame_interval=8, num_clips=1, type='SampleFrames'),
    dict(type='DecordDecode'),
    dict(type='RandomResizedCrop'),
    dict(keep_ratio=False, scale=(
        224,
        224,
    ), type='Resize'),
    dict(flip_ratio=0.5, type='Flip'),
    dict(type='ColorJitter'),
    dict(input_format='NCTHW', type='FormatShape'),
    dict(type='PackActionInputs'),
]
val_cfg = dict(type='ValLoop')
val_dataloader = dict(
    batch_size=8,
    dataset=dict(
        ann_file='data/kinetics400/kinetics400_val_list_videos.txt',
        data_prefix=dict(video='data/kinetics400/videos_val'),
        pipeline=[
            dict(type='DecordInit'),
            dict(
                clip_len=8,
                frame_interval=8,
                num_clips=1,
                test_mode=True,
                type='SampleFrames'),
            dict(type='DecordDecode'),
            dict(scale=(
                -1,
                256,
            ), type='Resize'),
            dict(crop_size=224, type='CenterCrop'),
            dict(type='ColorJitter'),
            dict(input_format='NCTHW', type='FormatShape'),
            dict(type='PackActionInputs'),
        ],
        test_mode=True,
        type='VideoDataset'),
    num_workers=4,
    persistent_workers=True,
    sampler=dict(shuffle=False, type='DefaultSampler'))
val_evaluator = dict(type='AccMetric')
val_pipeline = [
    dict(type='DecordInit'),
    dict(
        clip_len=8,
        frame_interval=8,
        num_clips=1,
        test_mode=True,
        type='SampleFrames'),
    dict(type='DecordDecode'),
    dict(scale=(
        -1,
        256,
    ), type='Resize'),
    dict(crop_size=224, type='CenterCrop'),
    dict(type='ColorJitter'),
    dict(input_format='NCTHW', type='FormatShape'),
    dict(type='PackActionInputs'),
]
vis_backends = [
    dict(type='LocalVisBackend'),
]
visualizer = dict(
    type='ActionVisualizer', vis_backends=[
        dict(type='LocalVisBackend'),
    ])
work_dir = 'work_dir\\tpn_H36M_gta'
