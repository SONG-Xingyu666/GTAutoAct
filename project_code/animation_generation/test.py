bone_code_coco = [
    '4089',  # 0: 'SKEL_L_Finger01' (coco)
    '4090',  # 1: 'SKEL_L_Finger02' (coco)
    '4137',  # 2: 'SKEL_L_Finger31' (coco)
    '4138',  # 3: 'SKEL_L_Finger32' (coco)
    '4153',  # 4: 'SKEL_L_Finger41' (coco)
    '4154',  # 5: 'SKEL_L_Finger42' (coco)
    '4169',  # 6: 'SKEL_L_Finger11' (coco)
    '4170',  # 7: 'SKEL_L_Finger12' (coco)
    '4185',  # 8: 'SKEL_L_Finger21' (coco)
    '4186',  # 9: 'SKEL_L_Finger22' (coco)
    '10706', #10: 'SKEL_R_Clavicle' (ntu)
    '11816', #11: 'SKEL_Pelvis' (-)
    '14201', #12: 'SKEL_L_Foot' (coco)
    '18905', #13: 'SKEL_L_Hand' (coco)
    '23553', #14: 'SKEL_Spine0' (-)
    '24816', #15: 'SKEL_Spine1' (ntu)
    '24817', #16: 'SKEL_Spine2' (-)
    '24818', #17: 'SKEL_Spine3' (ntu)   
    '26610', #18: 'SKEL_L_Finger00' (coco)
    '26611', #19: 'SKEL_L_Finger10' (coco)
    '26612', #20: 'SKEL_L_Finger20' (coco)
    '26613', #21: 'SKEL_L_Finger30' (coco)
    '26614', #22: 'SKEL_L_Finger40' (coco)
    '28252', #23: 'SKEL_R_Forearm' (ntu)
    '31086', #24: 'SKEL_Head' (coco)
    '36864', #25: 'SKEL_R_Calf' (ntu)
    '39317', #26: 'SKEL_Neck_1' (-)
    '40269', #27: 'SKEL_R_UpperArm' (ntu)
    '45509', #28: 'SKEL_L_UpperArm' (ntu)
    '51826', #29: 'SKEL_R_Thigh' (ntu)
    '52301', #30: 'SKEL_R_Foot' (coco)
    '57005', #31: 'SKEL_R_Hand' (coco)
    '57597', #32: 'SKEL_Spine_Root' 
    '58271', #33: 'SKEL_L_Thigh' (ntu)
    '58866', #34: 'SKEL_R_Finger00' (coco)
    '58867', #35: 'SKEL_R_Finger10' (coco)
    '58868', #36: 'SKEL_R_Finger20' (coco)
    '58869', #37: 'SKEL_R_Finger30' (coco)
    '58870', #38: 'SKEL_R_Finger40' (coco)
    '61163', #39: 'SKEL_L_Forearm' (ntu)
    '63931', #40: 'SKEL_L_Calf' (ntu)
    '64016', #41: 'SKEL_R_Finger01' (coco)
    '64017', #42: 'SKEL_R_Finger02' (coco)
    '64064', #43: 'SKEL_R_Finger31' (coco)
    '64065', #44: 'SKEL_R_Finger32' (coco)
    '64080', #45: 'SKEL_R_Finger41' (coco)
    '64081', #46: 'SKEL_R_Finger42' (coco)
    '64096', #47: 'SKEL_R_Finger11' (coco)
    '64097', #48: 'SKEL_R_Finger12' (coco)
    '64112', #49 'SKEL_R_Finger21' (coco)
    '64113', #50: 'SKEL_R_Finger22' (coco)
    '64729', #51: 'SKEL_L_Clavicle' (ntu)
]

        # Coordinates list
        coord_spine_base = coord_list[:,0]
        coord_spine_middle = coord_list[:,1]
        coord_neck = coord_list[:,2]
        coord_head = coord_list[:,3]
        coord_shoulder_r = coord_list[:,4]
        coord_elbow_r = coord_list[:,5]
        coord_wrist_r = coord_list[:,6]
        coord_hand_r = coord_list[:,7]
        coord_shoulder_l = coord_list[:,8]
        coord_elbow_l = coord_list[:,9]
        coord_wrist_l = coord_list[:,10]
        coord_hand_l = coord_list[:,11]
        coord_hip_r = coord_list[:,12]
        coord_knee_r = coord_list[:,13]
        coord_ankle_r = coord_list[:,14]
        coord_foot_r = coord_list[:,15]
        coord_hip_l = coord_list[:,16]
        coord_knee_l = coord_list[:,17]
        coord_ankle_l = coord_list[:,18]
        coord_foot_l = coord_list[:,19]
        coord_spine = coord_list[:,20]
        coord_hand_tip_r = coord_list[:,21]
        coord_thumb_r = coord_list[:,22]
        coord_hand_tip_l = coord_list[:,23]
        coord_thumb_l = coord_list[:,24]

        # List of euler angle in world coordsys
        euler_list_local = np.zeros((len(bone_code_ntu),3))
        # List of quaternion in world coordsys
        quat_list_local = np.zeros((len(bone_code_ntu),4))

        # SKEL_Pelvis (fixed)
        euler_list_local[1,:] = euler_pelvis_local
        # SKEL_Spine_Root
        euler_list_local[11,:] = euler_spine_root_local
        # SKEL_Spine0
        euler_list_local[2,:] = euler_spine0_local
        # SKEL_Spine1
        euler_spine1 = graph_transformation.calculate_euler_by_coord(
            p1=coord_spine_base,
            p2=coord_spine_middle,
            p3=coord_spine)
        euler_spine1_local = graph_transformation.worldEuler_to_localEuler(euler_spine1, euler_spine0)
        euler_list_local[3,:] = euler_spine1_local
        # SKEL_Spine2
        euler_list_local[4,:] = euler_spine2_local
        # SKEL_Spine3
        euler_spine3 = graph_transformation.calculate_euler_by_coord(
            p1=coord_spine_middle,
            p2=coord_spine,
            p3=graph_transformation.calcualte_midpoint_2(coord_shoulder_l, coord_shoulder_r))
        euler_spine2 = graph_transformation.localEuler_to_worldEuler(euler_spine2_local, euler_spine1)
        euler_spine3_local = graph_transformation.worldEuler_to_localEuler(euler_spine3, euler_spine2)
        angle_x =  graph_transformation.calculate_angle_proj(coord_shoulder_r-coord_shoulder_l, coord_hip_r-coord_hip_l, vet_nor=np.array([0,0,1]))
        # if abs(angle_x) > 90:
        #     angle_x = 90 - abs(angle_x)
        if (coord_shoulder_l-coord_shoulder_r)[2] > 0:
            angle_x = -angle_x
        euler_spine3_local[0] = angle_x
        euler_list_local[5,:] = euler_spine3_local
        euler_spine3 = graph_transformation.localEuler_to_worldEuler(euler_spine3_local, euler_spine2)
        # SKEL_Neck_1
        # euler_neck = graph_transformation.calculate_euler_by_coord(
        #     p1=coord_neck,
        #     p2=coord_head,)
        # euler_list[6,:] = euler_neck

        # Left arm
        # SKEL_L_Clavicle
        euler_list_local[15,:] = euler_clavicle_l_local
        euler_clavicle_l = graph_transformation.localEuler_to_worldEuler(euler_clavicle_l_local, euler_spine3)
        # SKEL_L_UpperArm
        # euler_upperarm_l_local = graph_transformation.calculate_euler_local(p0=coord_spine,p1=coord_shoulder_l,p2=coord_elbow_l,p3=coord_wrist_l,euler_p0=euler_clavicle_l)
        # euler_list_local[11,:] = euler_upperarm_l_local
        euler_upperarm_l = graph_transformation.calculate_euler_by_coord(
            p1=coord_shoulder_l,
            p2=coord_elbow_l,
            p3=coord_wrist_l)
        euler_list_local[9,:] = graph_transformation.worldEuler_to_localEuler(euler_upperarm_l, euler_clavicle_l) 
        # SKEL_L_Forearm
        # elbow only have single dimention freedom, only need angle-z in local coordsys
        euler_list_local[13,:] = np.array([0,0,graph_transformation.calculate_angle(coord_elbow_l-coord_shoulder_l, coord_wrist_l-coord_elbow_l)])
        # SKEL_L_Hand
        # euler_hand_l = graph_transformation.calculate_euler_by_coord(
        #     p1=coord_wrist_l,
        #     p2=coord_hand_l,
        #     p3=coord_thumb_l)
        # euler_list[13,:] = euler_hand_l

        # Right arm
        # SKEL_R_Clavicle
        euler_list_local[0,:] = euler_clavicle_r_local
        euler_clavicle_r = graph_transformation.localEuler_to_worldEuler(euler_clavicle_r_local, euler_spine3)
        # SKEL_R_UpperArm
        # euler_upperarm_r_local = graph_transformation.calculate_euler_local(p0=coord_spine,p1=coord_shoulder_r,p2=coord_elbow_r,p3=coord_wrist_r,euler_p0=euler_clavicle_r)
        # euler_list_local[16,:] = euler_upperarm_r_local
        euler_upperarm_r = graph_transformation.calculate_euler_by_coord(
            p1=coord_shoulder_r,
            p2=coord_elbow_r,
            p3=coord_wrist_r)
        euler_upperarm_r_local = graph_transformation.worldEuler_to_localEuler(euler_upperarm_r, euler_clavicle_r) 
        euler_list_local[8,:] = euler_upperarm_r_local
        # SKEL_R_Forearm
        euler_list_local[6,:] = np.array([0,0,graph_transformation.calculate_angle(coord_elbow_r-coord_shoulder_r, coord_wrist_r-coord_elbow_r)])
        # SKEL_R_Hand
        # euler_hand_r = graph_transformation.calculate_euler_by_coord(
        #     p1=coord_wrist_r,
        #     p2=coord_hand_r,
        #     p3=coord_thumb_r)
        # euler_list[18,:] = euler_hand_r

        # Left leg
        # SKEL_L_Thigh
        euler_thigh_l = graph_transformation.calculate_euler_by_coord(
            p1=coord_hip_l,
            p2=coord_knee_l,
            p3=coord_ankle_l)
        euler_list_local[12,:] = graph_transformation.worldEuler_to_localEuler(
            np.array([graph_transformation.central_sym(euler_thigh_l[0]),euler_thigh_l[1],euler_thigh_l[2]]),
            euler_pelvis)
        # SKEL_L_Calf
        euler_list_local[14,:] = np.array([0,0,-graph_transformation.calculate_angle(coord_knee_l-coord_hip_l, coord_ankle_l-coord_knee_l)])

        # Right leg
        # SKEL_R_Thigh
        euler_thigh_r = graph_transformation.calculate_euler_by_coord(
            p1=coord_hip_r,
            p2=coord_knee_r,
            p3=coord_ankle_r)
        euler_list_local[10,:] = graph_transformation.worldEuler_to_localEuler(
            np.array([graph_transformation.central_sym(euler_thigh_r[0]),euler_thigh_r[1],euler_thigh_r[2]]),
            euler_pelvis)
        # SKEL_R_Calf
        euler_list_local[7,:] = np.array([0,0,-graph_transformation.calculate_angle(coord_knee_r-coord_hip_r, coord_ankle_r-coord_knee_r)])