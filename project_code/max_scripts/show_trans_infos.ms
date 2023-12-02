pelvis = getNodeByName "SKEL_Pelvis"
thigh_l = getNodeByName "SKEL_L_Thigh"
thigh_r = getNodeByName "SKEL_R_Thigh"
spine = getNodeByName "SKEL_Spine_Root"
spine1 = getNodeByName "SKEL_Spine1"
forearm_r = getNodeByName "SKEL_R_Forearm"
calf_l = getNodeByName "SKEL_L_Calf"
calf_r = getNodeByName "SKEL_R_Calf"

animate on

(

at time 0(


    -- Obtain the coordinate in world coordsys
    coord_pelvis = pelvis.pos
    coord_thigh_l = thigh_l.pos
    coord_thigh_r = thigh_r.pos
    coord_calf_l = calf_l.pos
    coord_calf_r = calf_r.pos
    format "coord_pelvis: [%]\n" coord_pelvis
    format "coord_thigh_l: [%]\n" coord_thigh_l
    format "coord_calf_l: [%]\n" coord_calf_l
    format "coord_calf_r: [%]\n" coord_calf_r

    -- -- Obtain the quat in world coordsys
    -- quat_pelvis = pelvis.rotation
    -- quat_thigh_l = thigh_l.rotation
    -- quat_thigh_r = thigh_r.rotation
    -- quat_spine = spine.rotation
    -- format "quat_pelvis: [%]\n" quat_pelvis
    -- format "quat_thigh_l: [%]\n" quat_thigh_l
    -- format "quat_thigh_r: [%]\n" quat_thigh_r
    -- format "quat_spine: [%]\n" quat_spine

    -- quat = forearm_r.rotation
    -- format "quat: [%]\n" quat



)
)
