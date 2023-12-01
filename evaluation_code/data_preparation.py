import os
import random
import shutil
import argparse
import csv
import cv2
import os
import re

# Header of annotation
HEADER = ['label', 'name', 'time_start','time_end','split']

ANNOTATION_DIR_NAME = 'annotations'
TRAIN_DIR_NAME = 'videos_train'
VAL_DIR_NAME = 'videos_val'
TEST_DIR_NAME = 'videos_test'

TRAIN_ANNOTATION_NAME = 'kinetics_train.csv'
VAL_ANNOTATION_NAME = 'kinetics_val.csv'
TEST_ANNOTATION_NAME = 'kinetics_test.csv'

def parse_args():
    
    parser = argparse.ArgumentParser(description='Data preparation')
    parser.add_argument('input_path', help='Input path of raw data')
    parser.add_argument('output_path', help='Output path of raw data')
    
    args = parser.parse_args()

    return args

def create_dir(path):
    if not os.path.exists(path):
        os.mkdir(path)

def move_files_random(input_path, output_path, move_rate):
    files = os.listdir(input_path)
    total_num = len(files)
    move_number = int(total_num * move_rate)
    file_num_list = random.sample(range(0, total_num), move_number)

    index = 0
    for file in files:
        if index in file_num_list:
            from_path = os.path.join(input_path, file)
            to_path = os.path.join(output_path, file)
            print('File from', from_path, 'move to', to_path)
            shutil.copy(from_path, to_path)
        index += 1

def split_from_train(train_path, val_path, test_path, val_rate):
    class_list = os.listdir(train_path)
    
    # Create class dir for val and test
    for cls in class_list:
        create_dir(os.path.join(val_path, cls))
        create_dir(os.path.join(test_path, cls))
        move_files_random(os.path.join(train_path, cls), os.path.join(val_path, cls), val_rate)


def generate_split(input_path, output_path):
    if not os.path.exists(output_path):
        os.mkdir(output_path)
    val_rate=0.2
    train_path = os.path.join(output_path, 'videos_train')
    val_path = os.path.join(output_path, 'videos_val')
    if not os.path.exists(train_path):
        os.mkdir(train_path)
    if not os.path.exists(val_path):
        os.mkdir(val_path)

    class_list = os.listdir(input_path)
    for cls in class_list:
        train_cls_path = os.path.join(train_path, cls)
        val_cls_path = os.path.join(val_path, cls)
        if not os.path.exists(train_cls_path):
            os.mkdir(train_cls_path)
        if not os.path.exists(val_cls_path):
            os.mkdir(val_cls_path)
        input_cls_path = os.path.join(input_path, cls)
        files = os.listdir(input_cls_path)
        total_num = len(files)
        move_number = int(total_num * val_rate)
        file_num_list = random.sample(range(0, total_num), move_number)

        index = 0
        for file in files:
            from_path = os.path.join(input_cls_path, file)
            if index in file_num_list:
                to_path = os.path.join(val_cls_path, file)
                print('Val File from', from_path, 'move to', to_path)
                shutil.copy(from_path, to_path)
            else:
                to_path = os.path.join(train_cls_path, file)
                print('Val File from', from_path, 'move to', to_path)
                shutil.copy(from_path, to_path)
            index += 1

# Get video frame number
def get_video_frame_num(video_path):

    # Capture video
    cap = cv2.VideoCapture(video_path)

    # Obtain video information
    frame_num = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    
    # print('frame number:', frame_num)
    return int(frame_num)

# Write information into csv
def write_csv(csv_path, info):
    with open(csv_path, 'a+') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(info)


# Get video information in a specific split
# Split: training dataset, validation dataset, testing dataset
def write_vidInfo_csv(split_path, annotation_path, split):

    # Write header into csv
    if split == 'train':
        # Get train csv path
        train_anno_path = os.path.join(annotation_path, TRAIN_ANNOTATION_NAME)
        # Write video information into csv file
        write_csv(train_anno_path, HEADER)

    elif split == 'val':
        # Get val csv path
        val_anno_path = os.path.join(annotation_path, VAL_ANNOTATION_NAME)
        write_csv(val_anno_path, HEADER)

    elif split == 'test':
        # Get test csv path
        test_anno_path = os.path.join(annotation_path, TEST_ANNOTATION_NAME)
        write_csv(test_anno_path, HEADER)


    # Get all classes of dataset
    class_list = os.listdir(split_path)

    for cls in class_list:
        # 1. Get video label
        label = cls
        # Get class path
        cls_path = os.path.join(split_path, cls)
        # Get video list of the class
        vid_list = os.listdir(cls_path)

        for vid in vid_list:
            # 2. Get video Name
            video_name = vid.split('.mp4')[0]
            # 3. Get start_frame
            start_frame = 0
            # Get video path
            vid_path = os.path.join(cls_path, vid)
            # 4. Get end_frame
            end_frame = get_video_frame_num(vid_path) - 1
            # Composite to video info
            info = [label, video_name, start_frame, end_frame, split]
            print(info)
            # Write into csv
            if split == 'train':
                # Get train csv path
                train_anno_path = os.path.join(annotation_path, TRAIN_ANNOTATION_NAME)
                # Write video information into csv file
                write_csv(train_anno_path, info)
            elif split == 'val':
                # Get val csv path
                val_anno_path = os.path.join(annotation_path, VAL_ANNOTATION_NAME)
                write_csv(val_anno_path, info)
            elif split == 'test':
                # Get test csv path
                test_anno_path = os.path.join(annotation_path, TEST_ANNOTATION_NAME)
                write_csv(test_anno_path, info)

def generate_annotation(dataset_path):
    annotation_path = os.path.join(dataset_path, ANNOTATION_DIR_NAME)
    if not os.path.exists(annotation_path):
        os.mkdir(annotation_path)
    train_path = os.path.join(dataset_path, TRAIN_DIR_NAME)
    val_path = os.path.join(dataset_path, VAL_DIR_NAME)
    
    write_vidInfo_csv(train_path, annotation_path, 'train')
    write_vidInfo_csv(val_path, annotation_path, 'val')



def write_vid_info(vid_dir_path, list_path):
    f = open(list_path, 'a')
    
    cls_list = os.listdir(vid_dir_path)

    index = 0
    info = []
    for cls in cls_list:

        vid_path = os.path.join(vid_dir_path, cls)
        vid_list = os.listdir(vid_path)
        for vid in vid_list:
            f.write(cls)
            f.write('/')
            f.write(vid)
            f.write(' ')
            f.write(str(index))
            f.write('\n')
        index += 1

    f.close()


def generate_videoList(dataset_path):

    val_vid_list_path = os.path.join(dataset_path, 'kinetics400_val_list_videos.txt')
    val_vid_path = os.path.join(dataset_path, 'videos_val')

    train_vid_list_path = os.path.join(dataset_path, 'kinetics400_train_list_videos.txt') 
    train_vid_path = os.path.join(dataset_path, 'videos_train')

    write_vid_info(val_vid_path, val_vid_list_path)
    write_vid_info(train_vid_path, train_vid_list_path)


def main():
    args = parse_args()
    generate_split(args.input_path, args.output_path)
    generate_annotation(args.output_path)
    generate_videoList(args.output_path)