import os
import numpy as np
from utilize.action_animation import load_data, coordinate_correction, generate_onim_file


if __name__ == "__main__":

    input_folder_path = r'demo\skeletons'
    output_foler_path = r'demo\animations'

    # frame = -1
    frame = None
    animation_movement = False
    input_folder = input_folder_path
    file_list = os.listdir(input_folder)
    out_folder = output_foler_path
    for file in file_list:
        skeleton_path = os.path.join(input_folder, file)
        onim_path = os.path.join(out_folder, file.split('.json')[0] + '.onim')
        # Read coordinates
        skeleton_coordinates = load_data(skeleton_path, frame) 
        # Correct coordinates
        coordinate_prime = coordinate_correction(skeleton_coordinates) # Axis * joint * frame
        # coordinate_prime = rotate_body(coordinate_prime)
        # Generate onim file
        frame_num = np.shape(coordinate_prime)[2]
        print('Frame number:', frame_num)

        generate_onim_file(coordinate_prime, onim_path, frame)

        # visualization_prime(coordinate_prime)