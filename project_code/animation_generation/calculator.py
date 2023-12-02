# Calculator for testing algorithms 

import numpy as np
import math
from numpy.linalg import matrix_rank 
import scipy
import action_animation as aa
import graph_transformation as gt
from supersmoother import SuperSmoother, LinearSmoother


bone_code_coco = [
    '0',     # :0 'SKEL_ROOT' (coco)
    '4089',  #  1'SKEL_L_Finger01' (coco)a
    '4090',  #  2'SKEL_L_Finger02' (coco)a
    '4137',  #  3'SKEL_L_Finger31' (coco)a
    '4138',  #  4'SKEL_L_Finger32' (coco)a
    '4153',  #  5'SKEL_L_Finger41' (coco)a
    '4154',  #  6'SKEL_L_Finger42' (coco)a
    '4169',  #  7'SKEL_L_Finger11' (coco)a
    '4170',  #  8'SKEL_L_Finger12' (coco)a
    '4185',  #  9'SKEL_L_Finger21' (coco)a
    '4186',  #  10'SKEL_L_Finger22' (coco)a
    '10706', #  11 'SKEL_R_Clavicle' (ntu)a
    '11816', #  12 'SKEL_Pelvis' (-)a
    '14201', #  13 'SKEL_L_Foot' (coco)a
    '18905', #  14 'SKEL_L_Hand' (coco)a
    '23553', #  15 'SKEL_Spine0' (-)a
    '24816', #  16 'SKEL_Spine1' (ntu)a
    '24817', #  17 'SKEL_Spine2' (-)a
    '24818', #  18 'SKEL_Spine3' (ntu)   a
    '26610', #  19 'SKEL_L_Finger00' (coco)a
    '26611', #  20 'SKEL_L_Finger10' (coco)a
    '26612', #  21 'SKEL_L_Finger20' (coco)a
    '26613', #  22 'SKEL_L_Finger30' (coco)a
    '26614', #  23 'SKEL_L_Finger40' (coco)a
    '28252', #  24 'SKEL_R_Forearm' (ntu)a
    '31086', #  25 'SKEL_Head' (coco)a
    '36864', #  26 'SKEL_R_Calf' (ntu)a
    '39317', #  27 'SKEL_Neck_1' (-)a
    '40269', #  28 'SKEL_R_UpperArm' (ntu)a
    '45509', #  29 'SKEL_L_UpperArm' (ntu)a
    '51826', #  30 'SKEL_R_Thigh' (ntu)a
    '52301', #  31 'SKEL_R_Foot' (coco)a
    '57005', #  32 'SKEL_R_Hand' (coco)a
    '57597', #  33 'SKEL_Spine_Root' a
    '58271', #  34 'SKEL_L_Thigh' (ntu)a
    '58866', #  35 'SKEL_R_Finger00' (coco)a
    '58867', #  36 'SKEL_R_Finger10' (coco)a
    '58868', #  37 'SKEL_R_Finger20' (coco)a
    '58869', #  38 'SKEL_R_Finger30' (coco)a
    '58870', #  39 'SKEL_R_Finger40' (coco)a
    '61163', #  40 'SKEL_L_Forearm' (ntu)a
    '63931', #  41 'SKEL_L_Calf' (ntu)a
    '64016', #  42 'SKEL_R_Finger01' (coco)a
    '64017', #  43 'SKEL_R_Finger02' (coco)a
    '64064', #  44 'SKEL_R_Finger31' (coco)a
    '64065', #  45 'SKEL_R_Finger32' (coco)a
    '64080', #  46 'SKEL_R_Finger41' (coco)a
    '64081', #  47 'SKEL_R_Finger42' (coco)a
    '64096', #  48 'SKEL_R_Finger11' (coco)a
    '64097', #  49 'SKEL_R_Finger12' (coco)a
    '64112', #  50 'SKEL_R_Finger21' (coco)a
    '64113', #  51 'SKEL_R_Finger22' (coco)a
    '64729', #  52 'SKEL_L_Clavicle' (ntu)a
]

# coord_shoulder_l = np.array([0.365, 0.159, 0.313])
# coord_shoulder_r = np.array([0.003,0.287, 0.423])
# coord_hip_l = np.array([0.096, 0.007, -0.092])
# coord_hip_r = np.array([-0.096, 0.007, -0.092])
# vet_baseline = np.array([0,0,1])
# # coord_hip = gt.calculate_midpoint([coord_hip_l, coord_hip_r])
# coord_hip = np.array([0, 0.007, -0.019])
# euler_hip = np.array([-180, -90, 0])
# aa.calculate_euler_center_local(
#     coord_up_l=coord_shoulder_l,
#     coord_up_r=coord_shoulder_r, 
#     coord_down_l=coord_hip_l,
#     coord_down_r=coord_hip_r,
#     vet_baseline=vet_baseline,
#     coord_parent=coord_hip,
#     euler_parent=euler_hip)

# def make_test_set(N=200, rseed_x=None, rseed_y=None):
#     """Code to generate the test set from Friedman 1984"""
#     rng_x = np.random.RandomState(rseed_x)
#     rng_y = np.random.RandomState(rseed_y)
#     x = rng_x.rand(N)
#     dy = x
#     y = np.sin(2 * np.pi * (1 - x) ** 2) + dy * rng_y.randn(N)
#     return x, y, dy

# t, y, dy = make_test_set(rseed_x=0, rseed_y=1)
# print(t)
# print(y)
# print(dy)

SKEL_ROOT [  0.           0.         -35.93670258]
SKEL_L_Finger01 [ 0.          0.         -8.68761025]
SKEL_L_Finger02 [  0.           0.         113.30361922]
SKEL_L_Finger31 [  0.           0.         -79.99183388]
SKEL_L_Finger32 [   0.            0.         -137.05126408]
SKEL_L_Finger41 [  0.           0.         -16.38936089]
SKEL_L_Finger42 [   0.            0.         -137.00231375]
SKEL_L_Finger11 [   0.            0.         -123.35212589]
SKEL_L_Finger12 [  0.          0.        -68.1204633]
SKEL_L_Finger21 [   0.            0.         -108.68333499]
SKEL_L_Finger22 [  0.           0.         166.03529843]
SKEL_R_Clavicle [-128.719   67.204 -127.18 ]
SKEL_Pelvis [-0. 90.  0.]
SKEL_L_Foot [ 0.          0.         82.57898492]
SKEL_L_Hand [-99.6422262   22.26949089 -25.92407062]
SKEL_Spine0 [-29.44374961  -3.25693175  -2.67942565]
SKEL_Spine1 [-29.44374961  -3.25693175  -2.67942565]
SKEL_Spine2 [-29.44374961  -3.25693175  -2.67942565]
SKEL_Spine3 [-29.44374961  -3.25693175  -2.67942565]
SKEL_L_Finger00 [  68.54150292  -46.05961844 -118.97866507]
SKEL_L_Finger10 [-14.21171155 -66.38841666 -88.89819683]
SKEL_L_Finger20 [ -28.09988141  -41.03714014 -105.55508515]
SKEL_L_Finger30 [ -35.11011731  -58.97993972 -101.24619847]
SKEL_L_Finger40 [-74.32996376 -24.95758592 -88.09843117]
SKEL_R_Forearm [  0.           0.         164.27221576]
SKEL_Head [  1.48130468 -23.5212783   -1.34042613]
SKEL_R_Calf [  0.           0.         -25.60909917]
SKEL_Neck_1 [  1.48130468 -23.5212783   -1.34042613]
SKEL_R_UpperArm [  27.39695657   72.45054799 -178.91754363]
SKEL_L_UpperArm [ -7.66549412 -10.58142187 -33.90486717]
SKEL_R_Thigh [ 54.39571698 -13.39580433  33.51433358]
SKEL_R_Foot [ 0.          0.         72.73866125]
SKEL_R_Hand [ 54.21914973 -33.01409922  -0.0662087 ]
SKEL_Spine_Root [  0. -90.   0.]
SKEL_L_Thigh [15.17180083  4.22386501 13.63307432]
SKEL_R_Finger00 [-29.06496074 -15.43037019 175.19995047]
SKEL_R_Finger10 [-70.52232939  33.59265373 164.47728634]
SKEL_R_Finger20 [-122.34084362  -13.52446036   94.96762064]
SKEL_R_Finger30 [-137.25769695  -49.96975614   71.43813597]
SKEL_R_Finger40 [  6.52107865 -64.02229037 -69.73800393]
SKEL_L_Forearm [ 0.          0.         96.50775571]
SKEL_L_Calf [0.        0.        5.8833231]
SKEL_R_Finger01 [   0.           0.        -177.7597496]
SKEL_R_Finger02 [  0.           0.         156.23332757]
SKEL_R_Finger31 [ 0.          0.         -3.05719182]
SKEL_R_Finger32 [  0.           0.         -94.89585898]
SKEL_R_Finger41 [  0.           0.         -79.12969386]
SKEL_R_Finger42 [   0.            0.         -152.13224531]
SKEL_R_Finger11 [   0.            0.         -122.02767222]
SKEL_R_Finger12 [  0.           0.         174.36250838]
SKEL_R_Finger21 [  0.           0.         -56.39924403]
SKEL_R_Finger22 [  0.          0.        155.0627823]
SKEL_L_Clavicle [ 128.719  -67.204 -127.179]