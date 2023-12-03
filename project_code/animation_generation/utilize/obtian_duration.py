# Obtain the duration of animation
import os

onim_folder = r'resources\onim_files'
onim_files = os.listdir(onim_folder)
for file in onim_files:
    if file.split('.')[-1] == 'onim':
        file_path = os.path.join(onim_folder, file)
        f = open(file_path)
        line = f.readline()
        line = f.readline()
        line = f.readline()
        line = f.readline()
        frame_num = int(line[-4:-1])
        new_name = file_path.split('.')[0] + '_' + str(frame_num) + '.'+ file_path.split('.')[1]
        print(new_name)
        f.close()
        os.rename(file_path, new_name)

