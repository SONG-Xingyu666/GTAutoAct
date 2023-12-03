import os
import shutil

in_path = r'C:\FMServer\cfx-server-data-master\data\H3WB_skeleton'
out_path = r'C:\FMServer\cfx-server-data-master\demo\skeletons'

skel_list = os.listdir(in_path)
for skel in skel_list:
    angle = skel.split('.')[1]
    if angle == '60457274':
        in_file_path = os.path.join(in_path, skel)
        out_file_path = os.path.join(out_path, skel)
        print(out_file_path)
        shutil.copy(in_file_path, out_file_path)
