# Graph transformation toolbox 

import numpy as np
import math
from scipy.spatial.transform import Rotation as R
# import skeleton_visualization

##################################################################################
########################ROTATION MATRIX, EULER, QUATERNION########################
##################################################################################

########################Quaternion and rotation matrix########################

# Quaternion to rotation matrix
def quat_to_RM(quat):
    quat = np.mat(quat)
    r = R.from_quat(quat)
    rm = r.as_matrix()
    return rm[0]

# Rotation matirx to quaternion
def RM_to_quat(rm):
    rm = np.mat(rm)
    r = R.from_matrix(rm)
    quat = r.as_quat()
    return quat

########################Quaternion and euler angle########################

# Euler angle to quaternion
def euler_to_quat(euler):
    r4 = R.from_euler('xyz', euler, degrees=True)
    quat = r4.as_quat()
    return quat

# Quaternion to euler angle
def quat_to_euler(quat):
    r = R.from_quat(quat)
    euler = r.as_euler('xyz', degrees=True)
    return euler

########################Rotation matrix and euler angle########################

# Euler angle to rotation matirx
def euler_to_RM(euler):
    r4 = R.from_euler('xyz', euler, degrees=True)
    rm = r4.as_matrix()
    return rm

########################Quternion and axis&angle########################

# Axis and angle to quaternion
def axis_angle_to_quat(axis, angle):
    angle = np.radians(angle)
    return np.array([
        axis[0]*np.sin(angle/2), axis[1]*np.sin(angle/2), axis[2]*np.sin(angle/2), np.cos(angle/2) 
    ])

#####################################################################
########################QUATERNION OPERATIONS########################
#####################################################################

# quat = (x, y, z, w)
# Obtain the conjugate of quaternion 
def quat_conj(quat):
    return np.array([
        -quat[0], -quat[1], -quat[2], quat[3]
    ])

# Obtain the inverse of quaternion
def quat_inv(quat):
    # Sharing of quaternion
    quat_star = np.array([-quat[0], -quat[1], -quat[2], quat[3]])
    # Norm square of quaternion
    quat_norm_square = np.dot(quat, quat)
    quat_I = quat_star / quat_norm_square
    return quat_I

# Product of quaternions
# (x,y,z,w)
def quat_prod(quat_1, quat_2):
    
    w1 = quat_1[3]
    w2 = quat_2[3]
    v1 = np.array([quat_1[0],quat_1[1],quat_1[2]])
    v2 = np.array([quat_2[0],quat_2[1],quat_2[2]])
    
    w = w1*w2 - np.dot(v1, v2)
    v = w1*v2 + w2*v1 + np.cross(v1, v2)
    q = np.array([v[0], v[1], v[2], w])
    return q

    # x1 = quat_1[0]
    # y1 = quat_1[1]
    # z1 = quat_1[2]
    # w1 = quat_1[3]

    # x2 = quat_1[0]
    # y2 = quat_1[1]
    # z2 = quat_1[2]
    # w2 = quat_1[3]   

    # w = (w1 * w2) - (x1 * x2) - (y1 * y2) - (z1 * z2)
    # x = (w1 * x2) + (x1 * w2) + (y1 * z2) - (z1 * y2)
    # y = (w1 * y2) - (x1 * z2) + (y1 * w2) + (z1 * x2)
    # z = (w1 * z2) + (x1 * y2) - (y1 * x2) + (z1 * w2)

    # return np.array(
    #     [x,y,z,w]
    # )

# Calculate the distance between two quats
def calculate_angular_distance(q1, q2):
    if (q1==q2).all():
        return 0
    return 2*np.arccos(quat_prod(q1, quat_conj(q2))[-1])

##########################################################################
##################MATRIX, VECTOR, COORDINATE OPERATIOINS##################
##########################################################################

########################Coordinate or node########################

# # Calculate the midpoint between two points 
# def calcualte_midpoint_2(p1, p2):
#     return (p1+p2)/2 

# # Calculate the midpoint between three points
# def calcualte_midpoint_3(p1, p2, p3):
#     return (p1+p2+p3)/3

# Calculate the midpoint of multiple points
def calculate_midpoint(point_list):
    sum_value = 0
    for point in point_list:
        sum_value += point
    return sum_value/len(point_list)

# Convert coordinate into quaternion format
def coord_to_quat(coord):
    if np.shape(coord) != 4:
        return np.insert(coord, 3, 0, axis=0)
    else: 
        return coord
    
# Calculate the normal vector of a plane formed by three points
def calculate_nor_vet_by_points(p1, p2, p3):
    for i in range(0,3):
        if p1[i]==p2[i]==p3[i]:
            return False
    v1 = p2 - p1
    v2 = p3 - p2
    return np.cross(v1, v2)

########################Matrix########################

# Convert matrix into homogeneous 
def to_homo(mat):

    # Is quaternion
    if np.shape(mat) == (4,):
        return mat
    # Is coordinate matrix and not homogeneous
    if np.shape(mat)[0]==1 and np.shape(mat)[1]==3:
        # Add "1" at the end of coordinate
        return np.insert(mat, 3, 1, axis=1)
    # Is a 4X3 transform matrix
    if np.shape(mat)[0]==4 and np.shape(mat)[1]==3:
        # Add [0,0,0,1] as a new column
        return np.insert(mat, 3, np.array([0,0,0,1]), axis=1)
    # Is a 3X4 matrix
    if np.shape(mat)[0]==3 and np.shape(mat)[1]==4:
        # Add [0,0,0,1] as a new row
        return np.insert(mat, 3, np.array([0,0,0,1]), axis=0)
    # Is a 3X3 matrix
    if np.shape(mat)[0]==3 and np.shape(mat)[1]==3:
        # Add [0,0,0] as a new row
        mat = np.insert(mat, 3, np.array([0,0,0]), axis=0)
        # Add [0,0,0,1] as a new column
        return np.insert(mat, 3, np.array([0,0,0,1]), axis=1)
    # Is homogeneous
    else: 
        return mat
    
# Calculate the transformation matrix (TM) of a node 
# coord: the coordinate of node, euler: the euler angle of node, RM: the rotation matrix of node 
# TM = (RM_I  0)
#      (coord 1）4X4
def calculate_TM(coord, euler):
    RM = quat_to_RM(euler_to_quat(euler))
    RM_I = np.linalg.inv(RM)
    coord = np.mat(coord)
    TM = np.insert(RM_I, 3, coord, axis=0)
    return to_homo(TM)

########################Vector########################

# Min max normalization
def min_max_norm(list):
    return (list - list.min())/(list.max()-list.min())

# normalization of vector 
def normalization(vet):
    norm = np.linalg.norm(vet)
    if norm == 0:
        return vet
    return vet/norm

# Calculate the projection of a vector onto a plane
# Result in 3d
def calculate_projection(vet, nor_vet): # nor_vet is the unit normal vector of the plane
    proj = vet - np.dot(vet, nor_vet)*nor_vet
    return proj

# Calculate the projection of a 3d vector onto the coordinate plane
# Result in 2d
def calculate_projection_plane(vet):
    # Calculate the projections
    proj_x0y = calculate_projection(vet, np.array([0,0,1])).take([0,1])
    proj_y0z = calculate_projection(vet, np.array([1,0,0])).take([1,2])
    proj_z0x = calculate_projection(vet, np.array([0,1,0])).take([2,0])
    return proj_x0y, proj_y0z, proj_z0x

# Calculate the angle between two vectors in 3d
def calculate_angle(vet_1, vet_2):
    cos_theta = np.dot(vet_1, vet_2)
    sin_theta = np.linalg.norm(np.cross(vet_1, vet_2))
    # if np.cross(vet_1, vet_2) > 0:
    return np.degrees(np.arctan2(sin_theta, cos_theta))
    # if np.cross(vet_1, vet_2) < 0:
    #     return -np.degrees(np.arctan2(sin_theta, cos_theta))
    # vet_1_norm = np.linalg.norm(vet_1)
    # vet_2_norm = np.linalg.norm(vet_2)
    # cos_theta = np.dot(vet_1, vet_2) / (vet_1_norm*vet_2_norm)
    # theta = np.degrees(np.arccos(cos_theta))
    # if abs(theta) > 90:
    #     return theta-180
    # return theta

# Calculate the angle from vet1 to vet2 in 2d
def calculate_angle_direct(vet_1, vet_2):
    cos_theta = np.dot(vet_1, vet_2)
    sin_theta = np.linalg.norm(np.cross(vet_1, vet_2))
    if np.cross(vet_1, vet_2) > 0:
        return np.degrees(np.arctan2(sin_theta, cos_theta))
    if np.cross(vet_1, vet_2) < 0:
        return -np.degrees(np.arctan2(sin_theta, cos_theta))


# Calculate the angle between vector and plane
# vet: target vector, nor_vet: the normal vector of the plane
def calculate_angle_plane(vet, nor_vet):
    vet_proj = calculate_projection(vet, nor_vet)
    return calculate_angle(vet, vet_proj)

# Calculate the angle between the projrctions of two vectors on a plane
# vet_nor: the normal vector of the plane
def calculate_angle_proj(vet1, vet2, vet_nor): 
    vet1_proj = calculate_projection(vet1, vet_nor).take([0,1])
    vet2_proj = calculate_projection(vet2, vet_nor).take([0,1])
    if np.cross(vet1_proj, vet2_proj) > 0:
        return calculate_angle(vet1_proj, vet2_proj)
    if np.cross(vet1_proj, vet2_proj) < 0:
        return -calculate_angle(vet1_proj, vet2_proj)
    else: return 0

# Return the central symmety angle 
def central_sym(angle):
    if angle > 0:
        return -(180.0-angle)
    if angle < 0:
        return (180.0-abs(angle))
    else:
        return 0.0

def calculate_explementary_angle(angle):
    if angle > 0:
        return angle - 180
    if angle <= 0:
        return angle + 180
    

######################################################################
########################TRANSFORMATION TOOLBOX########################
######################################################################


# Convert coordinate from world coordsys into local coordsys
def worldCoordSys_to_localCoordSys(coord_child_world, TM_parent):
    coord_child_world = np.mat(coord_child_world)
    coord_child_world_homo = to_homo(coord_child_world)
    TM_parent_I = np.linalg.inv(TM_parent)
    # coord_child_local_homo = coord_child_world_homo * TM_parent_homo_I
    prod = np.dot(coord_child_world_homo, TM_parent_I).A[0]
    return prod[:3]

# Convert quaternion from world coordsys into local coordsys
# quat_local = quat_parent_world_I * quat_world
def worldQuat_to_localQuat(quat_world, quat_parent_world):
    return normalization(quat_prod(quat_inv(quat_parent_world), quat_world))

# Convert world euler into local euler
def worldEuler_to_localEuler(euler_child_world, euler_parent_world):
    quat_child_world = euler_to_quat(euler_child_world)
    quat_parent_world = euler_to_quat(euler_parent_world)
    quat_child_local = worldQuat_to_localQuat(quat_child_world, quat_parent_world)
    return quat_to_euler(quat_child_local)

# Convert euler angle from local into world 
def localEuler_to_worldEuler(euler_child_local, euler_parent_world): 
    quat_child_local = euler_to_quat(euler_child_local)
    quat_parent_world = euler_to_quat(euler_parent_world)
    quat_child_world = quat_prod(quat_parent_world, quat_child_local)
    return quat_to_euler(quat_child_world)

##################################################################
########################CALCULATE ROTATION########################
##################################################################

# Calcualte the rotation matrix by inital vector and direction vector
# v0: inital vector, v1: direction vector
def calculate_rm_by_vet(v0, v1):
    v0 = normalization(v0)
    v1 = normalization(v1)
    axis, theta = calculate_axis_angle_by_vet(v0, v1) 
    I = np.mat([[1,0,0],
               [0,1,0],
               [0,0,1]])
    N = np.mat(axis)
    return np.cos(theta)*I + (1-np.cos(theta))*np.dot(N.T, N) + np.sin(theta)*np.mat([[0,-N[0,2], N[0,1]],
                                                                                     [N[0,2], 0, -N[0,0]],
                                                                                     [-N[0,1], N[0,0], 0]])

# Calculate the euler angle of vector by parent coordinate and child coordinate
# p1: target point, p2: child point, p3: reference point (child point of child point) 
# child_node_num: the munber of child node of p1 (number of p2)
def calculate_euler_by_coord(p1, p2, p3=np.array([0,0,0])):
    vet = normalization(p2-p1) # 1X3
    # Reference vector for calculation
    vet_ref = normalization(p3-p2) # 1X3
    # If p2 has no child node (no p3), reference vector is vet itself
    if p3.all() == 0:
        vet_ref = vet
    vet_ref_mat = np.mat(vet_ref).T # 3X1

    # z angle is the angle between the projection of vet on xOy and x positive axis, [-180, 180]
    proj_x0y, _, proj_z0x = calculate_projection_plane(vet)
    
    angle_z = calculate_angle_direct(np.array([1,0]), proj_x0y)
    # # y>0, angle_z +
    # if vet[1] > 0:
    #     angle_z = angle_z
    # # y<0, angle_z -
    # if vet[1] <0:
    #     angle_z = -angle_z
    rm_z = calculate_RM_z(angle_z)
    rm_z_I = np.linalg.inv(rm_z)

    vet_z = normalization(np.dot(rm_z_I, vet).T)

    print('vet_z:', vet_z)
    print('p1', p1)
    p2_z = normalization(p1 + vet_z)
    print('p2_z:', p2_z)
    p3_z = normalization(p2_z + vet_z)
    print('p3_z', p3_z)
    # y angle is the angle between vet and xOy plane (look from xOz plane), -z is positive, [-90,90]
    # angle_y = calculate_angle_direct(np.array([0,1]), proj_z0x)
    angle_y = calculate_angle_plane(vet, nor_vet=np.array([0,0,1]))
    # z<0, angle_y +
    if vet[2]<0:
        angle_y = angle_y
    # z>0, angle_y -
    if vet[2]>0:
        angle_y = -angle_y
    rm_y = calculate_RM_y(angle_y)
    rm_y_I = np.linalg.inv(rm_y)
    rm = np.dot(rm_z, rm_y)
    rm_I = np.linalg.inv(rm)


    # x angle
    if p3.all() == 0:
        angle_x = 0
    else:
        # Calculate the inital reference vector 
        vet_ref_init = normalization(np.dot(rm_I, vet_ref_mat).T).A
        print(vet_ref_init)
        vet_ref_init_yOz = calculate_projection_plane(vet_ref_init)[1]
        # The angle between the projection of vet_ref_init onto yOz plane and y positive axis
        angle_x = calculate_angle_direct(np.array([1,0]), vet_ref_init_yOz)
        
        if vet_ref_init[0,1] < 0:
            angle_x = calculate_explementary_angle(angle_x)


    return np.array([float(format(angle_x, '.3f')), float(format(angle_y, '.3f')), float(format(angle_z, '.3f'))])

# Calculate the euler angle in local coordsys
# p0: the inital point of local coordsys
# p1: the point of euler angle
# p2: the child point of p1, for calculating target vector
# p3: the child point of p2, for calculating reference vector 
def calculate_euler_local(p0, p1, p2, p3, euler_p0):
    # Calculate the transform matrix (TM) of p0
    TM_p0 = calculate_TM(coord=p0, euler=euler_p0)
    coord_p1_p0 = worldCoordSys_to_localCoordSys(coord_child_world=p1, TM_parent=TM_p0)
    coord_p2_p0 = worldCoordSys_to_localCoordSys(coord_child_world=p2, TM_parent=TM_p0)
    coord_p3_p0 = worldCoordSys_to_localCoordSys(coord_child_world=p3, TM_parent=TM_p0)
    # The euler angle of p1 in the local coordsys of p0
    euler_p1_p0 = calculate_euler_by_coord(coord_p1_p0, coord_p2_p0, coord_p3_p0)
    return euler_p1_p0

# Calculate the rotation matrix by x-axis and angle
def calculate_RM_x(angle):
    angle = math.radians(angle)
    return np.array([
        [1,0,0],
        [0, math.cos(angle), -math.sin(angle)],
        [0, math.sin(angle), math.cos(angle)]
    ])

# Calculate the rotation matrix by y-axis and angle
def calculate_RM_y(angle):
    angle = math.radians(angle)
    return np.array([
        [math.cos(angle), 0, math.sin(angle)],
        [0, 1, 0],
        [-math.sin(angle), 0, math.cos(angle)]
    ])

# Calculate the rotation matrix by z-axis and angle
def calculate_RM_z(angle):
    angle = math.radians(angle)
    return np.array([
        [math.cos(angle), -math.sin(angle), 0],
        [math.sin(angle), math.cos(angle), 0],
        [0, 0, 1]
    ])

# Calculate the axis and angle of rotation by quaternion
def calculate_axis_angle_by_quat(quat):
    angle = 2*(np.arccos(quat[3]))
    axis = np.array([
        quat[0]/np.sin(angle/2), quat[1]/np.sin(angle/2), quat[2]/np.sin(angle/2)
    ])
    return axis, np.degrees(angle) 

# Calculate the axis and angle of rotation by rotation matrix
def calculate_axis_angle_by_RM(rm):
    trace = np.trace(rm)
    angle = np.arccos((trace-1)/2)
    return angle

# Calculate the new coordinate after rotation by quaternion
def calculate_coord_by_quat(coord, quat):
    norm = np.linalg.norm(coord)
    quat = normalization(quat)
    coord = coord_to_quat(coord)
    quat_I = quat_inv(quat)
    res = normalization(quat_prod(quat_prod(quat, coord), quat_I))
    if abs(res[3]) < 1e-16:
        return norm * res.take([0,1,2])
    return False

# Calculate the rotation axis and angle from vetcor_1 to vector_2
def calculate_axis_angle_by_vet(vet_1, vet_2): # vectors of same body part in adjacent frames
    axis = np.outer(vet_1, vet_2)[0]
    theta = np.degrees(np.arccos(np.inner(vet_1, vet_2)/(np.linalg.norm(vet_1)*np.linalg.norm(vet_2))))
    return axis, theta

# Calculate the quaternion by two connected nodes
# p1: parent node; p2: child node
def calculate_quat_by_coord(p1, p2):
    # Direction vecter
    vet = normalization(p2-p1)
    # Inital vector
    vet_init = np.array([1,0,0])
    # Rotation axis orthogonal to the plane formed by two vectors
    axis = normalization(np.cross(vet_init, vet))
    # Rotation angle
    dot = np.dot(vet_init, vet)
    angle = math.acos(dot)
    # vet_dir and vet_init are in collinear
    if angle == 0 or angle == math.pi:
        return False
    else: 
        return normalization([
            axis[0]*math.sin(angle/2), 
            axis[1]*math.sin(angle/2), 
            axis[2]*math.sin(angle/2), 
            math.cos(angle/2)
        ])

# Correct the angle x with offset
def angle_correction(angle, offset):
    return abs(angle) - offset


if __name__ == "__main__":

    p1 = np.array([0.236,	0.175,	0.365])
    p2 = np.array([0.51,	0.175,	0.365])
    p3 = np.array([0.467,	0.43,	0.365])
    print(p2-p1)
    print(p3-p1)
    # "KE111FA9070E850A"











    
