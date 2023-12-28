-- 1: Base of the spine
bone_1_main = getNodeByName "SKEL_Spine_Root"
bone_1_minor = getNodeByName "SKEL_Pelvis"
bone_0 = getNodeByName "IK_Root"
-- 2: Middle of the spine
bone_2 = getNodeByName "SKEL_Spine2"
-- 3: Neck
bone_3 = getNodeByName "SKEL_Neck_1"
-- 4: Head
bone_4 = getNodeByName "SKEL_Head"
-- 5: Left shoulder
bone_5 = getnodebyname "SKEL_L_UpperArm"
-- 9: Right shoulder
bone_9 = getNodeByName "SKEL_R_UpperArm"
-- 6: Left elbow 
-- MH_L_Elbow is as the same coordinate as SKEL_L_UpperArm
bone_6_main = getNodeByName "SKEL_L_Forearm" 
bone_6_minor = getNodeByName "MH_L_Elbow"
-- 10: Right elbow
-- MH_R_Elbow is as the same coordinate as SKEL_R_UpperArm
bone_10_main = getNodeByName "SKEL_R_Forearm"
bone_10_minor = getNodeByName "MH_R_Elbow"
-- 7: Left wrist 
-- RB_L_ForeArmRoll is in the midlle of hand and elbow
bone_7_main = getNodeByName "SKEL_L_Hand"
bone_7_minor = getNodeByName "RB_L_ForeArmRoll"
-- 11: Right wrist 
-- RB_R_ForeArmRoll is in the midlle of hand and elbow
bone_11_main = getNodeByName "SKEL_R_Hand"
bone_11_minor = getNodeByName "RB_R_ForeArmRoll"
-- 8: Left hand
-- The relative coordinate of fingers should be fixed 
bone_8_main = getNodeByName "PH_L_Hand"
bone_8_minor = getNodeByName "IK_L_Hand"
finger_L_00 = getNodeByName "SKEL_L_Finger00"
finger_L_10 = getNodeByName "SKEL_L_Finger10"
finger_L_20 = getNodeByName "SKEL_L_Finger20"
finger_L_30 = getNodeByName "SKEL_L_Finger30"
finger_L_40 = getNodeByName "SKEL_L_Finger40"
delta_L_00 = finger_L_00.pos - bone_8_main.pos
delta_L_10 = finger_L_10.pos - bone_8_main.pos
delta_L_20 = finger_L_20.pos - bone_8_main.pos
delta_L_30 = finger_L_30.pos - bone_8_main.pos
delta_L_40 = finger_L_40.pos - bone_8_main.pos
finger_L_01 = getNodeByName "SKEL_L_Finger01"
finger_L_11 = getNodeByName "SKEL_L_Finger11"
finger_L_21 = getNodeByName "SKEL_L_Finger21"
finger_L_31 = getNodeByName "SKEL_L_Finger31"
finger_L_41 = getNodeByName "SKEL_L_Finger41"
delta_L_01 = finger_L_01.pos - bone_8_main.pos
delta_L_11 = finger_L_11.pos - bone_8_main.pos
delta_L_21 = finger_L_21.pos - bone_8_main.pos
delta_L_31 = finger_L_31.pos - bone_8_main.pos
delta_L_41 = finger_L_41.pos - bone_8_main.pos
finger_L_02 = getNodeByName "SKEL_L_Finger02"
finger_L_12 = getNodeByName "SKEL_L_Finger12"
finger_L_22 = getNodeByName "SKEL_L_Finger22"
finger_L_32 = getNodeByName "SKEL_L_Finger32"
finger_L_42 = getNodeByName "SKEL_L_Finger42"
delta_L_02 = finger_L_02.pos - bone_8_main.pos
delta_L_12 = finger_L_12.pos - bone_8_main.pos
delta_L_22 = finger_L_22.pos - bone_8_main.pos
delta_L_32 = finger_L_32.pos - bone_8_main.pos
delta_L_42 = finger_L_42.pos - bone_8_main.pos
-- 12: Right hand 
-- The relative coordinate of fingers should be fixed 
bone_12_main = getNodeByName "PH_R_Hand"
bone_12_minor = getNodeByName "IK_R_Hand"
finger_R_00 = getNodeByName "SKEL_R_Finger00"
finger_R_10 = getNodeByName "SKEL_R_Finger10"
finger_R_20 = getNodeByName "SKEL_R_Finger20"
finger_R_30 = getNodeByName "SKEL_R_Finger30"
finger_R_40 = getNodeByName "SKEL_R_Finger40"
delta_R_00 = finger_R_00.pos - bone_12_main.pos
delta_R_10 = finger_R_10.pos - bone_12_main.pos
delta_R_20 = finger_R_20.pos - bone_12_main.pos
delta_R_30 = finger_R_30.pos - bone_12_main.pos
delta_R_40 = finger_R_40.pos - bone_12_main.pos
finger_R_01 = getNodeByName "SKEL_R_Finger01"
finger_R_11 = getNodeByName "SKEL_R_Finger11"
finger_R_21 = getNodeByName "SKEL_R_Finger21"
finger_R_31 = getNodeByName "SKEL_R_Finger31"
finger_R_41 = getNodeByName "SKEL_R_Finger41"
delta_R_01 = finger_R_01.pos - bone_12_main.pos
delta_R_11 = finger_R_11.pos - bone_12_main.pos
delta_R_21 = finger_R_21.pos - bone_12_main.pos
delta_R_31 = finger_R_31.pos - bone_12_main.pos
delta_R_41 = finger_R_41.pos - bone_12_main.pos
finger_R_02 = getNodeByName "SKEL_R_Finger02"
finger_R_12 = getNodeByName "SKEL_R_Finger12"
finger_R_22 = getNodeByName "SKEL_R_Finger22"
finger_R_32 = getNodeByName "SKEL_R_Finger32"
finger_R_42 = getNodeByName "SKEL_R_Finger42"
delta_R_02 = finger_R_02.pos - bone_12_main.pos
delta_R_12 = finger_R_12.pos - bone_12_main.pos
delta_R_22 = finger_R_22.pos - bone_12_main.pos
delta_R_32 = finger_R_32.pos - bone_12_main.pos
delta_R_42 = finger_R_42.pos - bone_12_main.pos
-- 22: Tip of the left hand
-- The coordinate22 should be the coordinate of finger22 
finger_L_10 = getNodeByName "SKEL_L_Finger10"
finger_L_20 = getNodeByName "SKEL_L_Finger20"
finger_L_30 = getNodeByName "SKEL_L_Finger30"
finger_L_40 = getNodeByName "SKEL_L_Finger40"
finger_L_11 = getNodeByName "SKEL_L_Finger11"
finger_L_21 = getNodeByName "SKEL_L_Finger21"
finger_L_31 = getNodeByName "SKEL_L_Finger31"
finger_L_41 = getNodeByName "SKEL_L_Finger41"
finger_L_12 = getNodeByName "SKEL_L_Finger12"
finger_L_22 = getNodeByName "SKEL_L_Finger22"
finger_L_32 = getNodeByName "SKEL_L_Finger32"
finger_L_42 = getNodeByName "SKEL_L_Finger42"
-- 24: Tip of the right hand
-- 23: Left thumb
-- 25: Right thumb
-- 13: Left hip
-- RB_L_ThighRoll is as the same coordinate as SKEL_L_Thigh
bone_13_main = getNodeByName "SKEL_L_Thigh"
bone_13_minor = getNodeByName "RB_L_ThighRoll"
-- 17: Right hip
-- RB_R_ThighRoll is as the same coordinate as SKEL_R_Thigh
bone_17_main = getNodeByName "SKEL_R_Thigh"
bone_17_minor = getNodeByName "RB_R_ThighRoll"
-- 14: Left Knee
-- MH_L_Knee is as the same coordinate as SKEL_L_Calf
bone_14_main = getNodeByName "SKEL_L_Calf"
bone_14_minor = getNodeByName "MH_L_Knee"
-- 18: Right Knee
-- MH_R_Knee is as the same coordinate as SKEL_R_Calf
bone_18_main = getNodeByName "SKEL_R_Calf"
bone_18_minor = getNodeByName "MH_R_Knee"
-- 15: Left ankle
bone_15 = getNodeByName "SKEL_L_Foot"
-- 19: Right ankle  
bone_19 = getNodeByName "SKEL_R_Foot"
-- 16: Left foot
-- PH_L_Foot is as the same coordinate as IK_L_Foot
bone_16_up = getNodeByName "SKEL_L_Toe0"
bone_16_down = getNodeByName "IK_L_Foot"
bone_16_down_minor = getNodeByName "PH_L_Foot"
-- 20: Right foot
-- PH_R_Foot is as the same coordinate as IK_R_Foot
bone_20_up = getNodeByName "SKEL_R_Toe0"
bone_20_down = getNodeByName "IK_R_Foot"
bone_20_down_minor = getNodeByName "PH_R_Foot"
-- 21: Spine
-- The middle of SKEL_L_Clavicle and SKEL_R_Clavicle
bone_21_L = getNodeByName "SKEL_L_Clavicle"
bone_21_R = getNodeByName "SKEL_R_Clavicle"
bone_21_interval = (bone_21_L.pos.x - bone_21_R.pos.x)/2
print(bone_21_L.pos)
print(bone_21_interval)
print(bone_21_R.pos)

animate on

(

at time 0(
  -- Base of the spine
  bone_1_main.pos=[0.00482835,0.038598,-0.1347898]
  bone_1_minor.pos=[0.00482835,0.038598,-0.1347898]
  bone_0.pos=[0.00482835,0.038598,-0.1347898]
  -- Middle of the spine
  bone_2.pos=[-0.02633815,-0.038788,0.1414218]
  -- Neck 
  bone_3.pos=[-0.05793885,-0.126541,0.4132445]
  -- Head
  bone_4.pos=[-0.00880515,-0.161764,0.5360415]
  -- Left shoulder
  bone_5.pos=[0.09666325,-0.048518,0.2958541]
  -- Left elbow
  bone_6_main.pos=[0.12126025,0.071779,0.0849397]
  bone_6_minor.pos=[0.12126025,0.071779,0.0849397]
  -- Left wrist
  bone_7_main.pos=[0.09270375,-0.143593,0.0425575]
  bone_7_minor.pos=(bone_6_main.pos+bone_7_main.pos)/2
  -- Left hand
  bone_8_main.pos=[0.02551285,-0.134349,0.0020459]
  bone_8_minor.pos=[0.02551285,-0.134349,0.0020459]
  finger_L_00.pos=bone_8_main.pos+delta_L_00
  finger_L_10.pos=bone_8_main.pos+delta_L_10
  finger_L_20.pos=bone_8_main.pos+delta_L_20
  finger_L_30.pos=bone_8_main.pos+delta_L_30
  finger_L_40.pos=bone_8_main.pos+delta_L_40
  finger_L_01.pos=bone_8_main.pos+delta_L_01
  finger_L_11.pos=bone_8_main.pos+delta_L_11
  finger_L_21.pos=bone_8_main.pos+delta_L_21
  finger_L_31.pos=bone_8_main.pos+delta_L_31
  finger_L_41.pos=bone_8_main.pos+delta_L_41
  finger_L_02.pos=bone_8_main.pos+delta_L_02
  finger_L_12.pos=bone_8_main.pos+delta_L_12
  finger_L_22.pos=bone_8_main.pos+delta_L_22
  finger_L_32.pos=bone_8_main.pos+delta_L_32
  finger_L_42.pos=bone_8_main.pos+delta_L_42
  -- Right shoulder
  bone_9.pos=[-0.11524495,-0.188631,0.2861754]
  -- Right elbow
  bone_10_main.pos=[-0.01552355,-0.360986,0.2305318]
  bone_10_minor.pos=[-0.01552355,-0.360986,0.2305318]
  -- Right wrist
  bone_11_main.pos=[0.05257885,-0.343207,0.3982644]
  bone_11_minor.pos=[0.05257885,-0.343207,0.3982644]
  -- Right hand
  bone_12_main.pos=[0.05775925,-0.319748,0.4655187]
  bone_12_minor.pos=[0.05775925,-0.319748,0.4655187]
  finger_R_00.pos=bone_12_main.pos+delta_R_00
  finger_R_10.pos=bone_12_main.pos+delta_R_10
  finger_R_20.pos=bone_12_main.pos+delta_R_20
  finger_R_30.pos=bone_12_main.pos+delta_R_30
  finger_R_40.pos=bone_12_main.pos+delta_R_40
  finger_R_01.pos=bone_12_main.pos+delta_R_01
  finger_R_11.pos=bone_12_main.pos+delta_R_11
  finger_R_21.pos=bone_12_main.pos+delta_R_21
  finger_R_31.pos=bone_12_main.pos+delta_R_31
  finger_R_41.pos=bone_12_main.pos+delta_R_41
  finger_R_02.pos=bone_12_main.pos+delta_R_02
  finger_R_12.pos=bone_12_main.pos+delta_R_12
  finger_R_22.pos=bone_12_main.pos+delta_R_22
  finger_R_32.pos=bone_12_main.pos+delta_R_32
  finger_R_42.pos=bone_12_main.pos+delta_R_42
  -- Left hip
  bone_13_main.pos=[0.05844615,0.036508,-0.1303165]
  bone_13_minor.pos=[0.05844615,0.036508,-0.1303165]
  -- Left knee
  bone_14_main.pos=[0.02407985,0.155176,-0.4394675]
  bone_14_minor.pos=[0.02407985,0.155176,-0.4394675]
  -- Left ankle
  bone_15.pos=[-0.01602435,0.303192,-0.7160519]
  -- Left feet 
  bone_16_up.pos=[0.03622685,0.210606,-0.7727775]
  bone_16_down.pos=[0.03622685,0.210606,-0.7727775]
  bone_16_down_minor.pos=[0.03622685,0.210606,-0.7727775]
  -- Right hip
  bone_17_main.pos=[-0.04524785,-0.023158,-0.1424932]
  bone_17_minor.pos=[-0.04524785,-0.023158,-0.1424932]
  -- Right knee
  bone_18_main.pos=[-0.09522615,0.04103,-0.4231509]
  bone_18_minor.pos=[-0.09522615,0.04103,-0.4231509]
  -- Right ankle
  bone_19.pos=[-0.12430215,0.199462,-0.7372387]
  -- Right foot
  bone_20_up.pos=[-0.07821235,0.219406,-0.8004258]
  bone_20_down.pos=[-0.07821235,0.219406,-0.8004258]
  bone_20_down_minor.pos=[-0.07821235,0.219406,-0.8004258]
  -- Spine
  bone_21_L.pos=[-0.05006005+bone_21_interval,-0.102827,0.3458432]
  bone_21_R.pos=[-0.05006005-bone_21_interval,-0.102827,0.3458432]

)


)


