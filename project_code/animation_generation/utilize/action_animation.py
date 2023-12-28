# Main function of action animation
import os
import numpy as np
import graph_transformation as gt
# import skeleton_visualization
import shutil
from pathlib import Path
import json
from tqdm import tqdm
from skeleton_visualization import visualization_prime
from scipy.interpolate import PchipInterpolator, PPoly, CubicSpline
from supersmoother import SuperSmoother, LinearSmoother
from sklearn.preprocessing import MinMaxScaler

########################################################################
#############################CONFIGURATIONS#############################
########################################################################

########################Basic configurations########################

input_folder_path = r'demo\skeletons'
# output_foler_path = r'code\demo\onim_file'
output_foler_path = r'demo\animations'
# output_foler_path = r'resources\[scripts]\animation\stream'
# Original .onim file
template_file_path = r'code\animation_generation\template\origin.onim'
frame_rate = 30.0
correction_num = 0
interplation_interval = 6 # 1 defalt
SequenceFrameLimit = 512
smooth = True

# The rotation (euler and quat) in world coordsys is changed by parent node
# The rotation in local coordsys is not change, only depend on node itself
# The calculation of rotation in parent coordsys has two methods: 
# 1. calculate euler in local directly, requires calculate coord in local coordsys, which need the TM of parent node
# 2. calculate euler in world and convert into local, requires coord in world, and rotation of parent 

########################GTA bone configuration########################
# Bone code list in GTA
# -: static
bone_code_coco = [
    '0', # 0: SKEL_ROOT (coco)
    '4089',  # # 1:'SKEL_L_Finger01' (coco)
    '4090',  # # 2:'SKEL_L_Finger02' (coco)
    '4137',  # # 3:'SKEL_L_Finger31' (coco)
    '4138',   # # 4:'SKEL_L_Finger32' (coco)
    '4153',  # # 5:'SKEL_L_Finger41' (coco)
    '4154',  # # 6:'SKEL_L_Finger42' (coco)
    '4169',  # # 7:'SKEL_L_Finger11' (coco)
    '4170',  # # 8:'SKEL_L_Finger12' (coco)
    '4185',  # # 9:'SKEL_L_Finger21' (coco)
    '4186',  # # 10:'SKEL_L_Finger22' (coco)
    '10706', # 11:'SKEL_R_Clavicle' (ntu)
    '11816', # 12:'SKEL_Pelvis' (-)
    '14201', # 13:'SKEL_L_Foot' (coco)
    '18905', # 14:'SKEL_L_Hand' (coco)
    '23553', # 15:'SKEL_Spine0' (-)
    '24816', # 16:'SKEL_Spine1' (ntu)
    '24817', # 17:'SKEL_Spine2' (-)
    '24818', # 18:'SKEL_Spine3' (ntu)   
    '26610',  # 19:'SKEL_L_Finger00' (coco)
    '26611', # 20:'SKEL_L_Finger10' (coco)
    '26612', # 21:'SKEL_L_Finger20' (coco)
    '26613', # 22:'SKEL_L_Finger30' (coco)
    '26614', # 23:'SKEL_L_Finger40' (coco)
    '28252', # 24:'SKEL_R_Forearm' (ntu)
    '31086', # 25:'SKEL_Head' (coco)
    '36864', # 26:'SKEL_R_Calf' (ntu)
    '39317', # 27:'SKEL_Neck_1' (-)
    '40269', # 28:'SKEL_R_UpperArm' (ntu)
    '45509', # 29:'SKEL_L_UpperArm' (ntu)
    '51826', # 30:'SKEL_R_Thigh' (ntu)
    '52301', # 31:'SKEL_R_Foot' (coco)
    '57005', # 32:'SKEL_R_Hand' (coco)
    '57597', # 33:'SKEL_Spine_Root' 
    '58271', # 34:'SKEL_L_Thigh' (ntu)
    '58866',  # 35:'SKEL_R_Finger00' (coco)
    '58867', # 36:'SKEL_R_Finger10' (coco)
    '58868', # 37:'SKEL_R_Finger20' (coco)
    '58869', # 38:'SKEL_R_Finger30' (coco)
    '58870', # 39:'SKEL_R_Finger40' (coco)
    '61163', # 40:'SKEL_L_Forearm' (ntu)
    '63931', # 41:'SKEL_L_Calf' (ntu)
    '64016',  # 42:'SKEL_R_Finger01' (coco)
    '64017',  # 43:'SKEL_R_Finger02' (coco)
    '64064',  # 44:'SKEL_R_Finger31' (coco)
    '64065',  # 45:'SKEL_R_Finger32' (coco)
    '64080',  # 46:'SKEL_R_Finger41' (coco)
    '64081',  # 47:'SKEL_R_Finger42' (coco)
    '64096',  # 48:'SKEL_R_Finger11' (coco)
    '64097',  # 49:'SKEL_R_Finger12' (coco)
    '64112',  # 50'SKEL_R_Finger21' (coco)
    '64113',  # 51:'SKEL_R_Finger22' (coco)
    '64729', # 52:'SKEL_L_Clavicle' (ntu)
]
bone_name_coco = [
    'SKEL_ROOT',
    'SKEL_L_Finger01',
    'SKEL_L_Finger02',
    'SKEL_L_Finger31',
    'SKEL_L_Finger32',
    'SKEL_L_Finger41',
    'SKEL_L_Finger42',
    'SKEL_L_Finger11',
    'SKEL_L_Finger12',
    'SKEL_L_Finger21',
    'SKEL_L_Finger22',
    'SKEL_R_Clavicle',
    'SKEL_Pelvis',
    'SKEL_L_Foot',
    'SKEL_L_Hand',
    'SKEL_Spine0',
    'SKEL_Spine1',
    'SKEL_Spine2',
    'SKEL_Spine3',
    'SKEL_L_Finger00',
    'SKEL_L_Finger10',
    'SKEL_L_Finger20',
    'SKEL_L_Finger30',
    'SKEL_L_Finger40',
    'SKEL_R_Forearm',
    'SKEL_Head',
    'SKEL_R_Calf',
    'SKEL_Neck_1',
    'SKEL_R_UpperArm',
    'SKEL_L_UpperArm',
    'SKEL_R_Thigh',
    'SKEL_R_Foot',
    'SKEL_R_Hand',
    'SKEL_Spine_Root',
    'SKEL_L_Thigh',
    'SKEL_R_Finger00',
    'SKEL_R_Finger10',
    'SKEL_R_Finger20',
    'SKEL_R_Finger30',
    'SKEL_R_Finger40',
    'SKEL_L_Forearm',
    'SKEL_L_Calf',
    'SKEL_R_Finger01',
    'SKEL_R_Finger02',
    'SKEL_R_Finger31',
    'SKEL_R_Finger32',
    'SKEL_R_Finger41',
    'SKEL_R_Finger42',
    'SKEL_R_Finger11',
    'SKEL_R_Finger12',
    'SKEL_R_Finger21',
    'SKEL_R_Finger22',
    'SKEL_L_Clavicle',
    ]
bone_code_ntu = [
    # body
    '10706', # 0: SKEL_R_Clavicle (ntu)
    '11816', # 1: SKEL_Pelvis -
    '23553', # 2: SKEL_Spine0 -
    '24816', # 3: SKEL_Spine1  (ntu)
    '24817', # 4: SKEL_Spine2 -
    '24818', # 5: SKEL_Spine3  (ntu)
    '28252', # 6: SKEL_R_Forearm  (ntu)
    '36864', # 7: SKEL_R_Calf  (ntu)
    '40269', # 8: SKEL_R_UpperArm  (ntu)
    '45509', # 9: SKEL_L_UpperArm  (ntu)
    '51826', # 10: SKEL_R_Thigh  (ntu)
    '57597', # 11: SKEL_Spine_Root -
    '58271', # 12: SKEL_L_Thigh  (ntu)
    '61163', # 13: SKEL_L_Forearm  (ntu)
    '63931', # 14: SKEL_L_Calf  (ntu)
    '64729', # 15: SKEL_L_Clavicle (ntu)
]
# Bones which is relative static, need to be expected from writing into .onim file
bond_expection = [
    '11816', # 1: SKEL_Pelvis -
    '23553', # 2: SKEL_Spine0 -
    '24817', # 4: SKEL_Spine2 -
    '57597', # 11: SKEL_Spine_Root -
]


# Euler angles of fixed node 
# world coordsys
euler_root = np.array([0,0,-180])
euler_pelvis = np.array([180,90,0])
euler_spine_root = np.array([-180, -90, 0])
euler_spine0 = np.array([90.0, -84.542, 90.0])
# euler_spine1 = np.array([90.0, -89.63, 90.0])
# euler_spine2 = np.array([90.0, -86.898, 90.0])
# euler_clavicle_l = np.array([-175.55, 13.314, 18.674])
# euler_clavicle_r = np.array([-4.451, 13.314, 161.326])
# local coordsys
euler_root_local = euler_root 
euler_spine_root_local = np.array([-90, -90, 90])
euler_pelvis_local = np.array([90,90,90])
euler_spine0_local = np.array([180.0, -180.0, 174.542])
euler_spine2_local = np.array([0.001, 0, -2.733])
euler_clavicle_l_local = np.array([128.719, -67.204, -127.179])
euler_clavicle_r_local = np.array([-128.719, 67.204, -127.18])
# quat of root node
quat_root = gt.euler_to_quat(euler_root)
# Fingers left
euler_finger_l_00_local_x = -10.344
euler_finger_l_10_local_x = -80.618
euler_finger_l_20_local_x = -90.362
euler_finger_l_30_local_x = -103.827
euler_finger_l_40_local_x = -113.726
# Fingers right
euler_finger_r_00_local_x = -10.344
euler_finger_r_10_local_x = -80.618
euler_finger_r_20_local_x = -90.362
euler_finger_r_30_local_x = -103.827
euler_finger_r_40_local_x = -66.274

############################################################
########################DATA READING########################
############################################################

# Read skeleton coordinates from .skeleton file of NTU
def read_skeleton(file):
    with open(file, 'r') as f: 
        skeleton_sequence = {} # dict
        skeleton_sequence['numFrame'] = int(f.readline()) # Read the first line in ".skeleton" file (frame num)
        skeleton_sequence['frameInfo'] = []
        
        for t in range(skeleton_sequence['numFrame']): # Every frame
            frame_info = {} 
            frame_info['numBody'] = int(f.readline()) # body num
            frame_info['bodyInfo'] = []
            
            for m in range(frame_info['numBody']): # Every body
                body_info = {} 
                body_info_key = [ 
                    'bodyID', 'clipedEdges', 'handLeftConfidence',
                    'handLeftState', 'handRightConfidence', 'handRightState',
                    'isResticted', 'leanX', 'leanY', 'trackingState'
                ]
                body_info = {
                    k: float(v) 
                    for k, v in zip(body_info_key, f.readline().split()) 
                }
                
                body_info['numJoint'] = int(f.readline()) # joint num
                body_info['jointInfo'] = []
                
                for v in range(body_info['numJoint']): # Every joint
                    joint_info_key = [ 
                        'x', 'y', 'z', 'depthX', 'depthY', 'colorX', 'colorY',
                        'orientationW', 'orientationX', 'orientationY',
                        'orientationZ', 'trackingState'
                    ]
                    joint_info = {
                        k: float(v) 
                        for k, v in zip(joint_info_key, f.readline().split()) 
                    }
                    body_info['jointInfo'].append(joint_info) 
                
                frame_info['bodyInfo'].append(body_info) 
            skeleton_sequence['frameInfo'].append(frame_info) 
    return skeleton_sequence

# Read the xyz coordinates from the skeleton sequence
# data: 3(xyz) × frame_num × 25(joint_num) × max_body
def read_xyz_skel(file, max_body=2, num_joint=25):
    seq_info = read_skeleton(file) 
    data = np.zeros((3, seq_info['numFrame'], num_joint, max_body)) # 3(xyz) × frame_num × 25(joint_num) × max_body  
    for n, f in enumerate(seq_info['frameInfo']): # Each frame 
        for m, b in enumerate(f['bodyInfo']): # Each body
            for j, v in enumerate(b['jointInfo']): # Each joint
                if m < max_body and j < num_joint:
                    data[:, n, j, m] = [v['x'], v['y'], v['z']] # Save x, y, z coordinates
                else:
                    pass
    return data

# Read the xyz coordinates from the json file
# data: 3(xyz) x frame_num x 133(joint_num) x 1(human_num)
def read_xyz_json(json_path, frame=None):
    seq_info = json.load(open(json_path))
    if frame == None:
        data = np.zeros((3, len(seq_info), 133, 1)) # 3 x frame_num x 133(joint_num) x human_num
        for f, frame in enumerate(seq_info):
            for k, joints in enumerate(frame['instances']['keypoints']):
                data[:, f, k, 0] = joints
    else:
        data = np.zeros((3, 1, 133, 1))
        for k, joints in enumerate(seq_info[frame]['instances']['keypoints']):
            data[:,0,k,0] = joints
    return data


# Load data from .skeleton file (ntu) or json file (coco)
def load_data(file_path, frame=None):
    print(file_path.split('.')[-1])
    if file_path.split('.')[-1] == 'json':
        return read_xyz_json(file_path, frame)
    if file_path.split('.')[-1] == 'skeleton':
        return read_xyz_skel(file_path)
    
###############################################################
########################DATA PREPROCESSING#####################
###############################################################

# Correct coordinates into game coordsys
# Input: 3 x frame_num x joint_num x human_num
# Output: 3 x joint_num x frame_num
def coordinate_correction(coordinates):
    axis_num, frame_num, bone_num, human_num = np.shape(coordinates)
    coordinates_prime = np.zeros((axis_num, bone_num, frame_num))
    for f in range(0, frame_num):
        for b in range(0, bone_num):
            x = coordinates[0,f,b,0]
            y = coordinates[1,f,b,0]
            z = coordinates[2,f,b,0]
            if bone_num == 25:
                coordinates_prime[0][b][f] = x
                coordinates_prime[1][b][f] = z
                coordinates_prime[2][b][f] = y
            if bone_num == 133:
                coordinates_prime[0][b][f] = x/1000
                coordinates_prime[1][b][f] = z/1000
                coordinates_prime[2][b][f] = -y/1000
    # offset = (coordinates_prime[:,0,0]+coordinates_prime[:,1,0])/2
    offset = coordinates_prime[:,0,0].copy()
    for f in range(frame_num):
        for b in range(bone_num):
            coordinates_prime[:,b,f] -= offset
    return coordinates_prime

# Rotate the body to make it to be vertical to the ground
# axis_num * bone_num * frame_num
def rotate_body(coordinates):
    axis_num, bone_num, frame_num = np.shape(coordinates)
    vet_spine_init = coordinates[:,1,0] - coordinates[:,0,0]
    angle = gt.calculate_angle_plane(vet_spine_init, np.array([0,1,0]))
    RM_x = gt.calculate_RM_x(angle)
    for f in range(0,frame_num):
        for b in range(0,bone_num):
            coordinates[:,b,f] = np.dot(np.mat(coordinates[:,b,f]),RM_x)
    return coordinates
    

######################################################
########################ANIMATION#####################
######################################################
# 1. Quaternions of each node in world coordsys (target node, parent node, child node)
# 2. Quaternions of each node in local coordsys (parent quaternion, target quaternion both in world coordsys)


# Convert quaternions of world coordsys in the list into local coordsys
def quat_list_world_to_local(quat_list):
    # Adjacent joints label
    # From parent to child 
    trunk = [1, 2, 3, 4, 5, 6]
    left_arm = [5, 10, 11, 12, 13]
    right_arm = [5, 15, 16, 17, 18]
    left_leg = [0, 20, 21]
    right_leg = [0, 25, 26]

    quat_list_local = np.zeros(np.shape(quat_list))

    # Root
    quat_list_local[0,:] = gt.worldQuat_to_localQuat(
        quat_world=quat_list[0,:],
        quat_parent_world=quat_root)
    quat_list_local[1,:] = gt.euler_to_quat(euler_spine_root)
    # Trunk
    for i in range(1,len(trunk)):
        quat_list_local[trunk[i],:] = gt.worldQuat_to_localQuat(
            quat_world=quat_list[trunk[i],:],
            quat_parent_world=quat_list[trunk[i-1],:])
    # Left arm
    for i in range(1,len(left_arm)):
        quat_list_local[left_arm[i],:] = gt.worldQuat_to_localQuat(
            quat_world=quat_list[left_arm[i],:],
            quat_parent_world=quat_list[left_arm[i-1],:])
    # Right arm
    for i in range(1,len(right_arm)):
        quat_list_local[right_arm[i],:] = gt.worldQuat_to_localQuat(
            quat_world=quat_list[right_arm[i],:],
            quat_parent_world=quat_list[right_arm[i-1],:])
    # Left leg
    for i in range(1,len(left_leg)):
        quat_list_local[left_leg[i],:] = gt.worldQuat_to_localQuat(
            quat_world=quat_list[left_leg[i],:],
            quat_parent_world=quat_list[left_leg[i-1],:])
    # Right leg
    for i in range(1,len(right_leg)):
        quat_list_local[right_leg[i],:] = gt.worldQuat_to_localQuat(
            quat_world=quat_list[right_leg[i],:],
            quat_parent_world=quat_list[right_leg[i-1],:])
    
    for i in range(0, np.shape(quat_list_local)[0]):
        if any(quat_list_local[i,:]) == 0:
            quat_list_local[i,:] = np.array([0,0,0,1])
    return quat_list_local

# Generate the position list in world
# coord_list: 3 * frame_num
# pos_list: frame_num * 3
def generate_pos_list(coord_list, frame_num_interpolated, flag=False):
    pos_list = np.zeros([frame_num_interpolated, np.shape(coord_list)[0]])
    if flag:
        for i in range(0,np.shape(coord_list)[1]):
        # for i in range(np.shape(coord_list)[1]-1,np.shape(coord_list)[1]):
            # pos_list[i,0] = -coord_list[0,i]
            # pos_list[i,1] = -coord_list[1,i]
            # pos_list[i,2] = coord_list[2,i]
            pos_list[i,0] = -coord_list[0,0]
            pos_list[i,1] = -coord_list[1,0]
            pos_list[i,2] = coord_list[2,0]
    # pos_list = animation_interpolation(np.array([pos_list]), frame_num_interpolated)[0]
    return pos_list

# Calculate the euler of centeral structure (spine, neck)
def calculate_euler_center_local(coord_up_l, coord_up_r, coord_down_l, coord_down_r, vet_baseline, coord_parent, euler_parent):
    TM_parent = gt.calculate_TM(coord=coord_parent, euler=euler_parent)
    vet_up = coord_up_l - coord_up_r
    vet_down = coord_down_l - coord_down_r
    vet_up_parent = gt.worldCoordSys_to_localCoordSys(vet_up, TM_parent)
    vet_down_parent = gt.worldCoordSys_to_localCoordSys(vet_down, TM_parent)
    vet_baseline_parent = gt.worldCoordSys_to_localCoordSys(vet_baseline, TM_parent)
    vet_up_x0y, vet_up_y0z, vet_up_z0x = gt.calculate_projection_plane(vet_up_parent)
    vet_down_x0y, vet_down_y0z, vet_down_z0x = gt.calculate_projection_plane(vet_down_parent)
    angle_x = gt.calculate_angle_direct(vet_down_y0z, vet_up_y0z)
    angle_y = gt.calculate_angle_direct(vet_down_z0x, vet_up_z0x)
    vet_center = gt.calculate_midpoint([coord_up_l, coord_up_r]) - gt.calculate_midpoint([coord_down_l, coord_down_r])
    vet_center_parent = gt.worldCoordSys_to_localCoordSys(vet_center, TM_parent)
    vet_baseline_x0y = gt.calculate_projection_plane(vet_baseline_parent)[0]
    vet_center_x0y = gt.calculate_projection_plane(vet_center_parent)[0]
    angle_z = gt.calculate_angle_direct(vet_baseline_x0y, vet_center_x0y)
    return np.array([angle_x, angle_y, angle_z]) 

# Calculate the euler angle of one-dimension joint in local coordsys
# coord: target joint
# coord_parent: the parent joint of joint coord
# coord_child: the child joint of joint coord
# All joints are in 3d world coordsys
def calculate_euler_1d_local(coord_parent, coord_target, coord_child, euler_parent): 
    TM_parent = gt.calculate_TM(coord_parent, euler_parent)
    coord_parent_parent = np.array([0,0,0])
    coord_target_parent = gt.worldCoordSys_to_localCoordSys(
        coord_child_world=coord_target,
        TM_parent=TM_parent)
    coord_child_parent = gt.worldCoordSys_to_localCoordSys(
        coord_child_world=coord_child,
        TM_parent=TM_parent)   
    vet_1_parent = coord_target_parent - coord_parent_parent
    vet_2_parent = coord_child_parent - coord_target_parent
    angle_z = gt.calculate_angle(vet_1_parent, vet_2_parent)
    if vet_2_parent[1] < 0:
        angle_z = -angle_z
    return np.array([0,0,angle_z])

# Calculate Euler angleof three-dimension joint in local coordsys
def calculate_euler_3d_local(coord_parent, coord_target, coord_child, coord_ref, euler_parent):
    TM_parent = gt.calculate_TM(coord_parent, euler_parent)
    # coord_parent_parent = np.array([0,0,0])
    coord_target_parent = gt.worldCoordSys_to_localCoordSys(
        coord_child_world=coord_target,
        TM_parent=TM_parent)
    coord_child_parent = gt.worldCoordSys_to_localCoordSys(
        coord_child_world=coord_child,
        TM_parent=TM_parent)  
    coord_ref_parent = gt.worldCoordSys_to_localCoordSys(
        coord_child_world=coord_ref,
        TM_parent=TM_parent)
    euler = gt.calculate_euler_by_coord(
        p1=coord_target_parent,
        p2=coord_child_parent,
        p3=coord_ref_parent)
    return euler

# Adjust thigh bones
def euler_adjust(euler):
    angle_x = euler[0]
    if angle_x > 0:
        angle_x = angle_x - 180
    if angle_x < 0:
        angle_x = angle_x + 180
    return np.array([angle_x, euler[1], euler[2]])

# Generate quat list in local coordsys
def generate_quat_list_local(coord_list):
    bone_num = np.shape(coord_list)[1] 

    ###################ntu###################
        
    ###################coco###################
    if bone_num == 133:
        # List of euler angle in world coordsys
        euler_list_local = np.zeros((len(bone_code_coco), 3))
        # List of quaternion in world coordsys
        quat_list_local = np.zeros((len(bone_code_coco), 4))
        ##################Trunk##################
        # SKEL_ROOT (facing direction)
        coord_hip_l = coord_list[:,11]
        coord_hip_r = coord_list[:,12]
        coord_hip = gt.calculate_midpoint([coord_hip_l, coord_hip_r])
        euler_root = np.array([0,0,gt.calculate_angle_direct(
            np.array([1,0]), 
            gt.calculate_projection_plane(coord_hip_r-coord_hip_l)[0])
            ])
        euler_root_local = euler_root
        euler_list_local[0,:] = euler_root_local
        # SKEL_Pelvis (static)
        euler_list_local[12,:] = euler_pelvis_local
        euler_pelvis = gt.localEuler_to_worldEuler(
            euler_child_local=euler_pelvis_local,
            euler_parent_world=euler_root)
        # SKEL_Spine_Root (static)
        euler_list_local[33,:] = euler_spine_root_local
        euler_spine_root = gt.localEuler_to_worldEuler(
            euler_child_local=euler_spine_root_local,
            euler_parent_world=euler_root)
        # SKEL_Spine0-3 (center)
        coord_shoulder_l = coord_list[:,5]
        coord_shoulder_r = coord_list[:,6]
        euler_spine_local = calculate_euler_center_local(
            coord_shoulder_l, coord_shoulder_r, coord_hip_l, coord_hip_r, np.array([0,0,1]), 
            coord_hip, euler_spine_root)
        # SKEL_Spine0
        euler_spine0_local = euler_spine_local/4 # spine0
        euler_spine0 = gt.localEuler_to_worldEuler(
            euler_child_local=euler_spine0_local,
            euler_parent_world=euler_spine_root)
        euler_list_local[15,:] = euler_spine0_local
        # SKEL_Spine1
        euler_spine1_local = euler_spine_local/4 # spine1
        euler_spine1 = gt.localEuler_to_worldEuler(
            euler_child_local=euler_spine1_local,
            euler_parent_world=euler_spine0)
        euler_list_local[16,:] = euler_spine1_local
        # SKEL_Spine2
        euler_spine2_local = euler_spine_local/4 # spine1
        euler_spine2 = gt.localEuler_to_worldEuler(
            euler_child_local=euler_spine2_local,
            euler_parent_world=euler_spine1)
        euler_list_local[17,:] = euler_spine2_local
        # SKEL_Spine3
        euler_spine3_local = euler_spine_local/4 # spine1
        euler_spine3 = gt.localEuler_to_worldEuler(
            euler_child_local=euler_spine3_local,
            euler_parent_world=euler_spine2)
        euler_list_local[18,:] = euler_spine3_local
        # SKEL_Neck_1 & SKEL_Head (center)
        coord_ear_l = coord_list[:,3]
        coord_ear_r = coord_list[:,4]
        coord_neck = gt.calculate_midpoint([coord_shoulder_l, coord_shoulder_r])
        vet_neck_baseline = coord_neck - coord_hip
        euler_head_local = calculate_euler_center_local(coord_ear_l, coord_ear_r, coord_shoulder_l, coord_shoulder_r, vet_neck_baseline, 
                                                        coord_neck, euler_spine3)
        euler_list_local[27,:] = euler_head_local/2 # neck
        euler_list_local[25,:] = euler_head_local/2 # head
        

        ##################Limbs##################
        # Arms
        coord_elbow_l = coord_list[:,7]
        coord_wrist_l = coord_list[:,9]
        coord_elbow_r = coord_list[:,8]
        coord_wrist_r = coord_list[:,10]
        # SKEL_L_Clavicle (static)
        euler_list_local[52,:] = euler_clavicle_l_local # clavicle_l static
        euler_clavicle_l = gt.localEuler_to_worldEuler(
            euler_child_local=euler_clavicle_l_local,
            euler_parent_world=euler_spine3)
        # SKEL_R_Clavicle (static)
        euler_list_local[11,:] = euler_clavicle_r_local # clavicle_l static
        euler_clavicle_r = gt.localEuler_to_worldEuler(
            euler_child_local=euler_clavicle_r_local,
            euler_parent_world=euler_spine3)
        # SKEL_L_UpperArm (3)
        euler_upperarm_l_local = calculate_euler_3d_local(
            coord_parent=gt.calculate_midpoint([coord_shoulder_l, coord_shoulder_r]),
            coord_target=coord_shoulder_l,
            coord_child=coord_elbow_l,
            coord_ref=coord_wrist_l,
            euler_parent=euler_clavicle_l)
        euler_list_local[29,:] = euler_upperarm_l_local
        euler_upperarm_l = gt.localEuler_to_worldEuler(
            euler_child_local=euler_upperarm_l_local,
            euler_parent_world=euler_clavicle_l)
        # SKEL_R_UpperArm (3)
        euler_upperarm_r_local = calculate_euler_3d_local(
            coord_parent=gt.calculate_midpoint([coord_shoulder_l, coord_shoulder_r]),
            coord_target=coord_shoulder_r,
            coord_child=coord_elbow_r,
            coord_ref=coord_wrist_r,
            euler_parent=euler_clavicle_r)
        euler_list_local[28,:] = euler_upperarm_r_local
        euler_upperarm_r = gt.localEuler_to_worldEuler(
            euler_child_local=euler_upperarm_r_local,
            euler_parent_world=euler_clavicle_r)
        # SKEL_L_Forearm (1)
        # elbow only have single dimention freedom, only need angle-z in local coordsys
        euler_forearm_l_local = calculate_euler_1d_local(
            coord_parent=coord_shoulder_l,
            coord_target=coord_elbow_l,
            coord_child=coord_wrist_l,
            euler_parent=euler_upperarm_l)
        euler_list_local[40,:] = euler_forearm_l_local
        euler_forearm_l = gt.localEuler_to_worldEuler(
            euler_child_local=euler_forearm_l_local,
            euler_parent_world=euler_upperarm_l)
        # SKEL_R_Forearm (1)
        # elbow only have single dimention freedom, only need angle-z in local coordsys
        euler_forearm_r_local = calculate_euler_1d_local(
            coord_parent=coord_shoulder_r,
            coord_target=coord_elbow_r,
            coord_child=coord_wrist_r,
            euler_parent=euler_upperarm_r)
        euler_list_local[24,:] = euler_forearm_r_local
        euler_forearm_r = gt.localEuler_to_worldEuler(
            euler_child_local=euler_forearm_r_local, 
            euler_parent_world=euler_upperarm_r)
        # Legs
        coord_knee_l = coord_list[:,13]
        coord_ankle_l = coord_list[:,15] 
        coord_knee_r = coord_list[:,14]
        coord_ankle_r = coord_list[:,16]
        coord_foot_l_1 = coord_list[:,17]
        coord_foot_l_2 = coord_list[:,18]
        coord_foot_l = gt.calculate_midpoint([coord_foot_l_1, coord_foot_l_2])
        coord_foot_r_1 = coord_list[:,20]
        coord_foot_r_2 = coord_list[:,21]
        coord_foot_r = gt.calculate_midpoint([coord_foot_r_1, coord_foot_r_2])
        # SKEL_L_Thigh (3) and SKEL_L_Calf (1)
        coord_hip_mid = gt.calculate_midpoint([coord_hip_l, coord_hip_r])
        length_hip = np.linalg.norm(coord_hip_l-coord_hip_r)
        coord_pelvis = np.array([coord_hip_mid[0], coord_hip_mid[1], 0.5*length_hip+coord_hip_mid[2]]) 
        # coord_pelvis = coord_hip_mid
        euler_thigh_l_local = calculate_euler_3d_local(
            coord_parent=coord_pelvis,
            coord_target=coord_hip_l,
            coord_child=coord_knee_l,
            coord_ref=coord_foot_l,
            euler_parent=euler_pelvis)
        euler_list_local[34,:] = euler_thigh_l_local
        euler_thigh_l = gt.localEuler_to_worldEuler(
            euler_child_local=euler_thigh_l_local,
            euler_parent_world=euler_pelvis)
        euler_calf_l_local = calculate_euler_1d_local(
            coord_parent=coord_hip_l,
            coord_target=coord_knee_l,
            coord_child=coord_ankle_l,
            euler_parent=euler_thigh_l)
        euler_list_local[41,:] = euler_calf_l_local
        euler_calf_l = gt.localEuler_to_worldEuler(
            euler_child_local=euler_calf_l_local,
            euler_parent_world=euler_thigh_l)
        # SKEL_R_Thigh (3) and SKEL_R_Calf (1) 
        euler_thigh_r_local = calculate_euler_3d_local(
            coord_parent=coord_pelvis,
            coord_target=coord_hip_r,
            coord_child=coord_knee_r,
            coord_ref=coord_foot_r,
            euler_parent=euler_pelvis)
        euler_list_local[30,:] = euler_thigh_r_local
        euler_thigh_r = gt.localEuler_to_worldEuler(
            euler_child_local=euler_thigh_r_local,
            euler_parent_world=euler_pelvis)
        euler_calf_r_local = calculate_euler_1d_local(
            coord_parent=coord_hip_r,
            coord_target=coord_knee_r,
            coord_child=coord_ankle_r,
            euler_parent=euler_thigh_r)
        euler_list_local[26,:] = euler_calf_r_local
        euler_calf_r = gt.localEuler_to_worldEuler(
            euler_child_local=euler_calf_r_local,
            euler_parent_world=euler_thigh_r) 
    
        ##################Hands and feet##################
        # Left hand
        coord_finger_l_00 = coord_list[:,92]
        coord_finger_l_01 = coord_list[:,93]
        coord_finger_l_02 = coord_list[:,94]
        coord_finger_l_03 = coord_list[:,95]
        coord_finger_l_10 = coord_list[:,96]
        coord_finger_l_11 = coord_list[:,97]
        coord_finger_l_12 = coord_list[:,98]
        coord_finger_l_13 = coord_list[:,99]
        coord_finger_l_20 = coord_list[:,100]
        coord_finger_l_21 = coord_list[:,101]
        coord_finger_l_22 = coord_list[:,102]
        coord_finger_l_23 = coord_list[:,103]
        coord_finger_l_30 = coord_list[:,104]
        coord_finger_l_31 = coord_list[:,105]
        coord_finger_l_32 = coord_list[:,106]
        coord_finger_l_33 = coord_list[:,107]
        coord_finger_l_40 = coord_list[:,108]
        coord_finger_l_41 = coord_list[:,109]
        coord_finger_l_42 = coord_list[:,110]
        coord_finger_l_43 = coord_list[:,111]
        # Right hand
        coord_finger_r_00 = coord_list[:,113]
        coord_finger_r_01 = coord_list[:,114]
        coord_finger_r_02 = coord_list[:,115]
        coord_finger_r_03 = coord_list[:,116]
        coord_finger_r_10 = coord_list[:,117]
        coord_finger_r_11 = coord_list[:,118]
        coord_finger_r_12 = coord_list[:,119]
        coord_finger_r_13 = coord_list[:,120]
        coord_finger_r_20 = coord_list[:,121]
        coord_finger_r_21 = coord_list[:,122]
        coord_finger_r_22 = coord_list[:,123]
        coord_finger_r_23 = coord_list[:,124]
        coord_finger_r_30 = coord_list[:,125]
        coord_finger_r_31 = coord_list[:,126]
        coord_finger_r_32 = coord_list[:,127]
        coord_finger_r_33 = coord_list[:,128]
        coord_finger_r_40 = coord_list[:,129]
        coord_finger_r_41 = coord_list[:,130]
        coord_finger_r_42 = coord_list[:,131]
        coord_finger_r_43 = coord_list[:,132]
        # SKEL_L_Hand
        coord_hand_mid_l = gt.calculate_midpoint([
            coord_finger_l_00,coord_finger_l_10,coord_finger_l_20,
            coord_finger_l_30,coord_finger_l_40])
        euler_hand_l_local = calculate_euler_3d_local(
            coord_parent=coord_elbow_l,
            coord_target=coord_wrist_l,
            coord_child=coord_hand_mid_l,
            coord_ref=coord_finger_l_00,
            euler_parent=euler_forearm_l)
        euler_list_local[14,:] = euler_hand_l_local
        euler_hand_l = gt.localEuler_to_worldEuler(
            euler_child_local=euler_hand_l_local,
            euler_parent_world=euler_forearm_l)
        # SKEL_R_Hand
        coord_hand_mid_r = gt.calculate_midpoint([
            coord_finger_r_00, coord_finger_r_10,coord_finger_r_20,
            coord_finger_r_30,coord_finger_r_40])
        euler_hand_r_local = calculate_euler_3d_local(
            coord_parent=coord_elbow_r,
            coord_target=coord_wrist_r,
            coord_ref=coord_finger_r_00,
            coord_child=coord_hand_mid_r,
            euler_parent=euler_forearm_r)
        euler_list_local[32,:] = euler_hand_r_local
        euler_hand_r = gt.localEuler_to_worldEuler(
            euler_child_local=euler_hand_r_local,
            euler_parent_world=euler_forearm_r)

        # Finger 0
        # SKEL_L_Finger00 (3)
        euler_finger_l_00_local =  calculate_euler_3d_local(
            coord_parent=coord_wrist_l,
            coord_target=coord_finger_l_00,
            coord_child=coord_finger_l_01,
            coord_ref=coord_finger_l_02,
            euler_parent=euler_hand_l)
        euler_finger_l_00_local[0] = euler_finger_l_00_local_x
        euler_list_local[19,:] = euler_finger_l_00_local
        euler_finger_l_00 = gt.localEuler_to_worldEuler(
            euler_child_local=euler_finger_l_00_local,
            euler_parent_world=euler_hand_l)
        # SKEL_R_Finger00 (3)
        euler_finger_r_00_local = calculate_euler_3d_local(
            coord_parent=coord_wrist_r,
            coord_target=coord_finger_r_00,
            coord_child=coord_finger_r_01,
            coord_ref=coord_finger_r_02,
            euler_parent=euler_hand_r)
        euler_finger_r_00_local[0] = euler_finger_r_00_local_x
        euler_list_local[35,:] = euler_finger_r_00_local
        euler_finger_r_00 = gt.localEuler_to_worldEuler(
            euler_child_local=euler_finger_r_00_local,
            euler_parent_world=euler_hand_r)
        # SKEL_L_Finger01 (1) 
        euler_finger_l_01_local = calculate_euler_1d_local(
            coord_parent=coord_finger_l_00,
            coord_target=coord_finger_l_01,
            coord_child=coord_finger_l_02,
            euler_parent=euler_finger_l_00)
        euler_list_local[1,:] = euler_finger_l_01_local
        euler_finger_l_01 = gt.localEuler_to_worldEuler(
            euler_child_local=euler_finger_l_01_local,
            euler_parent_world=euler_finger_l_00)
        # SKEL_R_Finger01 (1)
        euler_finger_r_01_local = calculate_euler_1d_local(
            coord_parent=coord_finger_r_00,
            coord_target=coord_finger_r_01,
            coord_child=coord_finger_r_02,
            euler_parent=euler_finger_r_00)
        euler_list_local[42,:] = euler_finger_r_01_local
        euler_finger_r_01 = gt.localEuler_to_worldEuler(
            euler_child_local=euler_finger_r_01_local,
            euler_parent_world=euler_finger_r_00)
        # SKEL_L_Finger02 (1)
        euler_finger_l_02_local = calculate_euler_1d_local(
            coord_parent=coord_finger_l_01,
            coord_target=coord_finger_l_02,
            coord_child=coord_finger_l_03,
            euler_parent=euler_finger_l_01)
        euler_list_local[2,:] = euler_finger_l_02_local
        # SKEL_R_Finger02 (1)
        euler_finger_r_02_local = calculate_euler_1d_local(
            coord_parent=coord_finger_r_01,
            coord_target=coord_finger_r_02,
            coord_child=coord_finger_r_03,
            euler_parent=euler_finger_r_01)
        euler_list_local[43,:] = euler_finger_r_02_local

        # Finger 1
        # SKEL_L_Finger10 (3)
        euler_finger_l_10_local = calculate_euler_3d_local(
            coord_parent=coord_wrist_l,
            coord_target=coord_finger_l_10,
            coord_child=coord_finger_l_11,
            coord_ref=coord_finger_l_12,
            euler_parent=euler_hand_l)
        euler_finger_l_10_local[0] = euler_finger_l_10_local_x
        euler_list_local[20,:] = euler_finger_l_10_local
        euler_finger_l_10 = gt.localEuler_to_worldEuler(
            euler_child_local=euler_finger_l_10_local,
            euler_parent_world=euler_hand_l)
        # SKEL_R_Finger10 (3)
        euler_finger_r_10_local = calculate_euler_3d_local(
            coord_parent=coord_wrist_r,
            coord_target=coord_finger_r_10,
            coord_child=coord_finger_r_11,
            coord_ref=coord_finger_r_12,
            euler_parent=euler_hand_r)
        euler_finger_r_10_local[0] = euler_finger_r_10_local_x
        euler_list_local[36,:] = euler_finger_r_10_local
        euler_finger_r_10 = gt.localEuler_to_worldEuler(
            euler_child_local=euler_finger_r_10_local,
            euler_parent_world=euler_hand_r)
        # SKEL_L_Finger11 (1) 
        euler_finger_l_11_local = calculate_euler_1d_local(
            coord_parent=coord_finger_l_10,
            coord_target=coord_finger_l_11,
            coord_child=coord_finger_l_12,
            euler_parent=euler_finger_l_10)
        euler_list_local[7,:] = euler_finger_l_11_local
        euler_finger_l_11 = gt.localEuler_to_worldEuler(
            euler_child_local=euler_finger_l_11_local,
            euler_parent_world=euler_finger_l_10)
        # SKEL_R_Finger11 (1)
        euler_finger_r_11_local = calculate_euler_1d_local(
            coord_parent=coord_finger_r_10,
            coord_target=coord_finger_r_11,
            coord_child=coord_finger_r_12,
            euler_parent=euler_finger_r_10)
        euler_list_local[48,:] = euler_finger_r_11_local
        euler_finger_r_11 = gt.localEuler_to_worldEuler(
            euler_child_local=euler_finger_r_11_local,
            euler_parent_world=euler_finger_r_10)
        # SKEL_L_Finger12 (1)
        euler_finger_l_12_local = calculate_euler_1d_local(
            coord_parent=coord_finger_l_11,
            coord_target=coord_finger_l_12,
            coord_child=coord_finger_l_13,
            euler_parent=euler_finger_l_11)
        euler_list_local[8,:] = euler_finger_l_12_local
        # SKEL_R_Finger12 (1)
        euler_finger_r_12_local = calculate_euler_1d_local(
            coord_parent=coord_finger_r_11,
            coord_target=coord_finger_r_12,
            coord_child=coord_finger_r_13,
            euler_parent=euler_finger_r_11)
        euler_list_local[49,:] = euler_finger_r_12_local

        # Finger 2
        # SKEL_L_Finger20 (3)
        euler_finger_l_20_local = calculate_euler_3d_local(
            coord_parent=coord_wrist_l,
            coord_target=coord_finger_l_20,
            coord_child=coord_finger_l_21,
            coord_ref=coord_finger_l_22,
            euler_parent=euler_hand_l)
        euler_finger_l_20_local[0] = euler_finger_l_20_local_x
        euler_list_local[21,:] = euler_finger_l_20_local
        euler_finger_l_20 = gt.localEuler_to_worldEuler(
            euler_child_local=euler_finger_l_20_local,
            euler_parent_world=euler_hand_l)
        # SKEL_R_Finger20 (3)
        euler_finger_r_20_local = calculate_euler_3d_local(
            coord_parent=coord_wrist_r,
            coord_target=coord_finger_r_20,
            coord_child=coord_finger_r_21,
            coord_ref=coord_finger_r_22,
            euler_parent=euler_hand_r)
        euler_finger_r_20_local[0] = euler_finger_r_20_local_x
        euler_list_local[37,:] = euler_finger_r_20_local
        euler_finger_r_20 = gt.localEuler_to_worldEuler(
            euler_child_local=euler_finger_r_20_local,
            euler_parent_world=euler_hand_r)
        # SKEL_L_Finger21 (1) 
        euler_finger_l_21_local = calculate_euler_1d_local(
            coord_parent=coord_finger_l_20,
            coord_target=coord_finger_l_21,
            coord_child=coord_finger_l_22,
            euler_parent=euler_finger_l_20)
        euler_list_local[9,:] = euler_finger_l_21_local
        euler_finger_l_21 = gt.localEuler_to_worldEuler(
            euler_child_local=euler_finger_l_21_local,
            euler_parent_world=euler_finger_l_20)
        # SKEL_R_Finger21 (1)
        euler_finger_r_21_local = calculate_euler_1d_local(
            coord_parent=coord_finger_r_20,
            coord_target=coord_finger_r_21,
            coord_child=coord_finger_r_22,
            euler_parent=euler_finger_r_20)
        euler_list_local[50,:] = euler_finger_r_21_local
        euler_finger_r_21 = gt.localEuler_to_worldEuler(
            euler_child_local=euler_finger_r_21_local,
            euler_parent_world=euler_finger_r_20)
        # SKEL_L_Finger22 (1)
        euler_finger_l_22_local = calculate_euler_1d_local(
            coord_parent=coord_finger_l_21,
            coord_target=coord_finger_l_22,
            coord_child=coord_finger_l_23,
            euler_parent=euler_finger_l_21)
        euler_list_local[10,:] = euler_finger_l_22_local
        # SKEL_R_Finger22 (1)
        euler_finger_r_22_local = calculate_euler_1d_local(
            coord_parent=coord_finger_r_21,
            coord_target=coord_finger_r_22,
            coord_child=coord_finger_r_23,
            euler_parent=euler_finger_r_21)
        euler_list_local[51,:] = euler_finger_r_22_local

        # Finger 3
        # SKEL_L_Finger30 (3)
        euler_finger_l_30_local = calculate_euler_3d_local(
            coord_parent=coord_wrist_l,
            coord_target=coord_finger_l_30,
            coord_child=coord_finger_l_31,
            coord_ref=coord_finger_l_32,
            euler_parent=euler_hand_l)
        euler_finger_l_30_local[0] = euler_finger_l_30_local_x
        euler_list_local[22,:] = euler_finger_l_30_local
        euler_finger_l_30 = gt.localEuler_to_worldEuler(
            euler_child_local=euler_finger_l_30_local,
            euler_parent_world=euler_hand_l)
        # SKEL_R_Finger30 (3)
        euler_finger_r_30_local = calculate_euler_3d_local(
            coord_parent=coord_wrist_r,
            coord_target=coord_finger_r_30,
            coord_child=coord_finger_r_31,
            coord_ref=coord_finger_r_32,
            euler_parent=euler_hand_r)
        euler_finger_r_30_local[0] = euler_finger_r_30_local_x
        euler_list_local[38,:] = euler_finger_r_30_local
        euler_finger_r_30 = gt.localEuler_to_worldEuler(
            euler_child_local=euler_finger_r_30_local,
            euler_parent_world=euler_hand_r)
        # SKEL_L_Finger31 (1) 
        euler_finger_l_31_local = calculate_euler_1d_local(
            coord_parent=coord_finger_l_30,
            coord_target=coord_finger_l_31,
            coord_child=coord_finger_l_32,
            euler_parent=euler_finger_l_30)
        euler_list_local[3,:] = euler_finger_l_31_local
        euler_finger_l_31 = gt.localEuler_to_worldEuler(
            euler_child_local=euler_finger_l_31_local,
            euler_parent_world=euler_finger_l_30)
        # SKEL_R_Finger31 (1)
        euler_finger_r_31_local = calculate_euler_1d_local(
            coord_parent=coord_finger_r_30,
            coord_target=coord_finger_r_31,
            coord_child=coord_finger_r_32,
            euler_parent=euler_finger_r_30)
        euler_list_local[44,:] = euler_finger_r_31_local
        euler_finger_r_31 = gt.localEuler_to_worldEuler(
            euler_child_local=euler_finger_r_31_local,
            euler_parent_world=euler_finger_r_30)
        # SKEL_L_Finger32 (1)
        euler_finger_l_32_local = calculate_euler_1d_local(
            coord_parent=coord_finger_l_31,
            coord_target=coord_finger_l_32,
            coord_child=coord_finger_l_33,
            euler_parent=euler_finger_l_31)
        euler_list_local[4,:] = euler_finger_l_32_local
        # SKEL_R_Finger32 (1)
        euler_finger_r_32_local = calculate_euler_1d_local(
            coord_parent=coord_finger_r_31,
            coord_target=coord_finger_r_32,
            coord_child=coord_finger_r_33,
            euler_parent=euler_finger_r_31)
        euler_list_local[45,:] = euler_finger_r_32_local

        # Finger 4
        # SKEL_L_Finger40 (3)
        euler_finger_l_40_local = calculate_euler_3d_local(
            coord_parent=coord_wrist_l,
            coord_target=coord_finger_l_40,
            coord_child=coord_finger_l_41,
            coord_ref=coord_finger_l_42,
            euler_parent=euler_hand_l)
        euler_finger_l_40_local[0] = euler_finger_l_40_local_x
        euler_list_local[23,:] = euler_finger_l_40_local
        euler_finger_l_40 = gt.localEuler_to_worldEuler(
            euler_child_local=euler_finger_l_40_local,
            euler_parent_world=euler_hand_l)
        # SKEL_R_Finger40 (3)
        euler_finger_r_40_local = calculate_euler_3d_local(
            coord_parent=coord_wrist_r,
            coord_target=coord_finger_r_40,
            coord_child=coord_finger_r_41,
            coord_ref=coord_finger_r_42,
            euler_parent=euler_hand_r)
        euler_finger_r_40_local[0] = euler_finger_r_40_local_x
        euler_list_local[39,:] = euler_finger_r_40_local
        euler_finger_r_40 = gt.localEuler_to_worldEuler(
            euler_child_local=euler_finger_r_40_local,
            euler_parent_world=euler_hand_r)
        # SKEL_L_Finger41 (1) 
        euler_finger_l_41_local = calculate_euler_1d_local(
            coord_parent=coord_finger_l_40,
            coord_target=coord_finger_l_41,
            coord_child=coord_finger_l_42,
            euler_parent=euler_finger_l_40)
        euler_list_local[5,:] = euler_finger_l_41_local
        euler_finger_l_41 = gt.localEuler_to_worldEuler(
            euler_child_local=euler_finger_l_41_local,
            euler_parent_world=euler_finger_l_40)
        # SKEL_R_Finger41 (1)
        euler_finger_r_41_local = calculate_euler_1d_local(
            coord_parent=coord_finger_r_40,
            coord_target=coord_finger_r_41,
            coord_child=coord_finger_r_42,
            euler_parent=euler_finger_r_40)
        euler_list_local[46,:] = euler_finger_r_41_local
        euler_finger_r_41 = gt.localEuler_to_worldEuler(
            euler_child_local=euler_finger_r_41_local,
            euler_parent_world=euler_finger_r_40)
        # SKEL_L_Finger42 (1)
        euler_finger_l_42_local= calculate_euler_1d_local(
            coord_parent=coord_finger_l_41,
            coord_target=coord_finger_l_42,
            coord_child=coord_finger_l_43,
            euler_parent=euler_finger_l_41)
        euler_list_local[6,:] = euler_finger_l_42_local
        # SKEL_R_Finger42 (1)
        euler_finger_r_42_local = calculate_euler_1d_local(
            coord_parent=coord_finger_r_41,
            coord_target=coord_finger_r_42,
            coord_child=coord_finger_r_43,
            euler_parent=euler_finger_r_41)
        euler_list_local[47,:] = euler_finger_r_42_local

        # Left foot
        # SKEL_L_Foot
        euler_foot_l_local = calculate_euler_1d_local(
            coord_parent=coord_knee_l,
            coord_target=coord_ankle_l,
            coord_child=coord_foot_l,
            euler_parent=euler_calf_l)
        euler_list_local[13,:] = euler_foot_l_local
        # SKEL_R_Foot
        euler_foot_r_local = calculate_euler_1d_local(
            coord_parent=coord_knee_r,
            coord_target=coord_ankle_r,
            coord_child=coord_foot_r,
            euler_parent=euler_calf_r)
        euler_list_local[31,:] = euler_foot_r_local

    # Transform euler angle into quaternion
    for euler, i in zip(euler_list_local, range(0,np.shape(euler_list_local)[0])):
        if any(euler) == 0:
            quat_list_local[i,:] = np.array([0,0,0,1])
        else:
            quat_list_local[i,:] = gt.euler_to_quat(euler)
    return quat_list_local

# Correct the quaternions in different frames
# quat_list: frame_num * 4
def quat_correction(quat_list):
    euler_list = np.zeros([np.shape(quat_list)[0], 3])
    for quat, i in zip(quat_list, range(0,np.shape(quat_list)[0])):
        euler_list[i,:] = gt.quat_to_euler(quat)
    for i in range(1, np.shape(euler_list)[0]-1):
        euler0 = euler_list[i-1]
        euler1 = euler_list[i]
        euler2 = euler_list[i+1]
        if abs(euler1[0]-euler0[0])>5 or abs(euler2[0]-euler1[0]<5):
            euler1[0] = (euler0[0] + euler2[0]) /2 
        if abs(euler1[1]-euler0[1])>5 or abs(euler2[1]-euler1[1]<5):
            euler1[1] = (euler0[1] + euler2[1]) /2 
        if abs(euler1[2]-euler0[2])>5 or abs(euler2[2]-euler1[0]<5):
            euler1[2] = (euler0[2] + euler2[2]) /2 
    for euler, i in zip(euler_list, range(0,np.shape(euler_list)[0])):
        quat_list[i,:] = gt.euler_to_quat(euler)
    return quat_list

# Animation Interpolation
# animation_list: node number * frame number * 4 (quat)
def animation_interpolation(animation_list, interplation_interval, distance_threshold=2, pointwise=False):
    if interplation_interval == 1:
        return animation_list
    node_num, frame_num, quat_div = np.shape(animation_list)
    if frame_num == 1:
        return animation_list
    if pointwise == False:
        return interpolation(animation_list, interplation_interval)
    # Generate distance list
    dis_list = []
    seq_list_prime = []
    index = 0
    for frame in range(1, frame_num):
        distance_sum = 0
        for bone in range(node_num):
            distance_sum += gt.calculate_angular_distance(animation_list[bone,frame-1,:], animation_list[bone,frame,:]) 
            distance_sum = distance_sum/(bone+1)
        dis_list.append(distance_sum)
    
    dis_list = gt.min_max_norm(np.array(dis_list))
    print(dis_list)
    index = 0
    seq_list_prime = []
    for frame, dis in enumerate(dis_list):
        if dis >= 0.5:
            if index < frame-1:
                print(index, frame-1)
                seq_list_prime.append(interpolation(animation_list[:,index:frame,:], interplation_interval))
                print(frame-1, frame)
                seq_list_prime.append(interpolation(animation_list[:,frame-1:frame+1,:], interplation_interval*int(dis*4)))
            if index == frame-1:
                print(frame-1, frame)
                seq_list_prime.append(interpolation(animation_list[:,frame-1:frame+1,:], interplation_interval*int(dis*4)))
            index = frame
    if index != frame:
        print(index, frame)
        seq_list_prime.append(interpolation(animation_list[:,index:frame+1,:], interplation_interval))
   
    for seq in seq_list_prime:
        print(np.shape(seq))
    
    animation_list_prime = np.concatenate(seq_list_prime, axis=1)
    
    return animation_list_prime

def interpolation(seq, interplation_interval):
    node_num, frame_num, quat_div = np.shape(seq)    
    if frame_num == 1:
        return seq
    x = np.linspace(0, frame_num, frame_num*interplation_interval)
    seq_prime = np.zeros([node_num, frame_num*interplation_interval, quat_div])
    for node in range(node_num):
        for q in range(quat_div):
            interpolant = PchipInterpolator(range(frame_num), seq[node, :, q])
            seq_prime[node, :, q] = interpolant(x)
    return seq_prime

# Data smoother
# bone_num x frame_num x 4
def animation_smoother(animation_list, smooth=True):
    if not smooth:
        return animation_list
    node_num, frame_num, quat_div = np.shape(animation_list)
    print(node_num, frame_num, quat_div)
    if frame_num == 1:
        return animation_list
    x = np.linspace(0, frame_num, frame_num)
    animation_list_prime = np.zeros([node_num, frame_num, quat_div])
    ss = SuperSmoother()
    for node in range(node_num):
        for q in range(quat_div):
            ss.fit(x, animation_list[node,:,q])
            animation_list_prime[node,:,q] = ss.predict(x)
    
    return animation_list_prime 

###############################################################
########################FILE GENERATION########################
###############################################################

# Generate bone rotation block
def generate_rot_block(bone_code, rot_list):
    block = []
    block.append('		BoneRotation Float4 %s\n' %bone_code)
    block.append('		{\n')
    block.append('			FramesData SingleChannel\n')
    block.append('			{\n')
    for rot in rot_list:
        block.append('				%f %f %f %f\n' %(rot[0],rot[1],rot[2],rot[3]))
        # block.append('				%f %f %f %f\n' %(rot_list[28,0],rot_list[28,1],rot_list[28,2],rot_list[28,3]))
    block.append('			}\n')
    block.append('		}\n')
    return block

# Generate bone position block
def generate_pos_block(bone_code, pos_list):
    block = []
    block.append('		BonePosition Float3 %s\n' %bone_code)
    block.append('		{\n')
    block.append('			FramesData SingleChannel\n')
    block.append('			{\n')
    for pos in pos_list:
        block.append('				%f %f %f\n' %(pos[0],pos[1],pos[2]))
    block.append('			}\n')
    block.append('		}\n')
    return block

# Write .onim file
def write_onim_file(template_file_path, new_file_path, pos_block, animation_list):
    print("Generating onim file:", new_file_path.split('\\')[-1])
    # Animation information
    _, frame_num, _ = np.shape(animation_list)
    print(np.shape(animation_list))
    # Generate new .onim file
    shutil.copyfile(template_file_path, new_file_path)
    # Read file
    f = open(new_file_path)
    lines = f.readlines()
    f.close()
    # Modify file
    for line, i in zip(lines, range(0,len(lines))):
        # Modify fundimental information 
        if 'Frames ' in line:
            lines[i] = '	Frames %d\n' %frame_num
        if 'SequenceFrameLimit ' in line:
            lines[i] = '	SequenceFrameLimit %d\n' %frame_num
        if 'Duration' in line:
            lines[i] = '	Duration %f\n' %(frame_num/frame_rate)
        if 'Sequences ' in line:
            lines[i] = '	Sequences %d\n' %frame_num
        # Add bone position block
        if 'Animation' in line:
            lines[i+2:i+2] = pos_block
    # Insert rotation information
    for i, code in enumerate(bone_code_coco):
        block = generate_rot_block(bone_code=code, rot_list=animation_list[i,:,:])
        lines[len(lines)-2:len(lines)-2] = block

    # for i in range(len(bone_code_coco)):
    #     print(bone_name_coco[i], gt.quat_to_euler(animation_list[i,-1,:]))
    
    f = open(new_file_path, 'w')
    f.writelines(lines)
    f.close()

# Generate .onim file
# coordinate_prime: the coordinate list after correction with multiple frames
# Axis * joint * frame
def generate_onim_file(coordinate_prime, new_file_path, start_frame=0, animation_movement=False):
    
    # Calculate frame number of animation
    _, bone_num, frame_num = np.shape(coordinate_prime)

    # Initalize list of quaternions of animation in all frames
    # node number * frame number * 4 (quat)
    # ntu layout
    if bone_num == 25:
        animation_list = np.zeros((len(bone_code_ntu), frame_num, 4))
    if bone_num == 133:
        animation_list = np.zeros((len(bone_code_coco), frame_num, 4))
    # Generate animation list
    for f in range(0, frame_num):
        print('Generating frame', f)
        # Generate quat list in local coordsys
        quat_list_local = generate_quat_list_local(coordinate_prime[:,:,f]) # bone_num x 4
        # Rearrange quat list layout
        # Each quat in quat_list_local
        for q in range(0,np.shape(quat_list_local)[0]):
            animation_list[q,f,:] = quat_list_local[q,:] # bone_num x frame_num x 4

    # Skeleton Interpolation
    animation_list = animation_interpolation(animation_list, interplation_interval=interplation_interval, pointwise=False) 

    # Animation smoother
    animation_list = animation_smoother(animation_list, smooth=smooth)

    frame_num_interpolated = np.shape(animation_list)[1]

    # generate position list (root node)
    # Default staric (flag=False)
    pos_list = generate_pos_list(coordinate_prime[:,0,:], frame_num_interpolated, animation_movement)

    # Animation segmentation
    for frame in range(0, frame_num_interpolated, SequenceFrameLimit):
        # Last sequence
        if (frame+SequenceFrameLimit) > (frame_num_interpolated-1):
            # Construct new file path 
            new_file = new_file_path.split('.onim')[0]+'_'+str(frame)+'-'+str(frame_num_interpolated-1)+'_'+str(frame_num_interpolated-frame)+'.'+new_file_path.split('.')[-1]
            pos_block = generate_pos_block('0', pos_list[frame:frame_num_interpolated,:])
            write_onim_file(template_file_path, new_file, pos_block, animation_list[:,frame:frame_num_interpolated,:])
        else:
            # Construct new file path 
            new_file = new_file_path.split('.onim')[0]+'_'+str(frame)+'-'+str(frame+SequenceFrameLimit-1)+'_'+str(SequenceFrameLimit)+'.'+new_file_path.split('.')[-1]
            pos_block = generate_pos_block('0', pos_list[frame:(frame+SequenceFrameLimit),:])
            write_onim_file(template_file_path, new_file, pos_block, animation_list[:,frame:(frame+SequenceFrameLimit),:])


    # for i in range(frame_num_interpolated):
    #     print(i, gt.quat_to_euler(animation_list[0,i,:]))
    

if __name__ == "__main__":
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
        
        






