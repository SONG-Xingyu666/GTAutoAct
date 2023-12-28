# Visualization of results on NTU dataset 
import os
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import action_animation as aa
import sys
import torch
 
######################################################################
#############################LOADING DATA#############################
######################################################################

########################Reading from .skeleton file########################
# Reading skeleton data
# Input: .skeleton file
def read_skeleton(file):
    with open(file, 'r') as f: # open file (.skeleton)
        skeleton_sequence = {} # initialize skeleton_sequence
        skeleton_sequence['numFrame'] = int(f.readline()) # read .skeleton first line (frame number)
        skeleton_sequence['frameInfo'] = []
        
        for t in range(skeleton_sequence['numFrame']): # Every frame 
            frame_info = {} # Initialize frame_info
            frame_info['numBody'] = int(f.readline()) # Read .skeleton next line (body number)
            frame_info['bodyInfo'] = []
            
            for m in range(frame_info['numBody']): # Every body 
                body_info = {} # Initialize body_info
                body_info_key = [
                    'bodyID', 'clipedEdges', 'handLeftConfidence',
                    'handLeftState', 'handRightConfidence', 'handRightState',
                    'isResticted', 'leanX', 'leanY', 'trackingState'
                ]
                body_info = {
                    k: float(v) # key:k, value: v
                    for k, v in zip(body_info_key, f.readline().split()) # Zip key and value
                }
                
                body_info['numJoint'] = int(f.readline()) # Joint number
                body_info['jointInfo'] = []
                
                for v in range(body_info['numJoint']): # Every joint (25)
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
 
########################Reading from coordinate list########################
# Read coordiante of x, y, z
def read_xyz(file, max_body=2, num_joint=25):
    seq_info = read_skeleton(file)
    # Initialize data: xyz(3) × frame_num × joint_num(25) × max_body  
    data = np.zeros((3, seq_info['numFrame'], num_joint, max_body)) 
    for n, f in enumerate(seq_info['frameInfo']): # Each frame
        for m, b in enumerate(f['bodyInfo']): # Each body
            for j, v in enumerate(b['jointInfo']): # Each joint
                if m < max_body and j < num_joint:
                    data[:, n, j, m] = [v['x'], v['y'], v['z']] 
                else:
                    pass
    return data
 
########################################################################
#############################PLAT FUNCTIONS#############################
########################################################################

########################For .skeleton file########################

# Print in 2D
def Print2D(num_frame, point, arms, rightHand, leftHand, legs, body):
    
    # 求坐标最大值
    xmax = np.max(point[0, :, :, :])
    xmin = np.min(point[0, :, :, :]) 
    ymax = np.max(point[1, :, :, :])
    ymin = np.min(point[1, :, :, :])
    zmax = np.max(point[2, :, :, :])
    zmin = np.min(point[2, :, :, :])
    
    n = 0     # 从第n帧开始展示
    m = num_frame   # 到第m帧结束，n<m<row
    plt.figure()
    plt.ion()
    for i in range(n, m):
        plt.cla() # # Clear axis, 即清除当前图形中的当前活动轴, 其他轴不受影响
 
        # 画出两个body所有关节
        plt.scatter(point[0, i, :, :], point[1, i, :, :], c='red', s=40.0) # c: 颜色;  s: 大小
 
        # 连接第一个body的关节，形成骨骼
        plt.plot(point[0, i, arms, 0], point[1, i, arms, 0], c='green', lw=2.0)
        plt.plot(point[0, i, rightHand, 0], point[1, i, rightHand, 0], c='green', lw=2.0) # c: 颜色;  lw: 线条宽度 
        plt.plot(point[0, i, leftHand, 0], point[1, i, leftHand, 0], c='green', lw=2.0)
        plt.plot(point[0, i, legs, 0], point[1, i, legs, 0], c='green', lw=2.0)
        plt.plot(point[0, i, body, 0], point[1, i, body, 0], c='green', lw=2.0)
 
        # 连接第二个body的关节，形成骨骼
        plt.plot(point[0, i, arms, 1], point[1, i, arms, 1], c='green', lw=2.0)
        plt.plot(point[0, i, rightHand, 1], point[1, i, rightHand, 1], c='green', lw=2.0)
        plt.plot(point[0, i, leftHand, 1], point[1, i, leftHand, 1], c='green', lw=2.0)
        plt.plot(point[0, i, legs, 1], point[1, i, legs, 1], c='green', lw=2.0)
        plt.plot(point[0, i, body, 1], point[1, i, body, 1], c='green', lw=2.0)
 
        plt.text(xmax, ymax+0.2, 'frame: {}/{}'.format(i, num_frame-1)) # 文字说明
        plt.xlim(xmin-0.5, xmax+0.5) # x坐标范围
        plt.ylim(ymin-0.3, ymax+0.3) # y坐标范围
        plt.pause(0.001) # 停顿延时

    plt.ioff() 
    plt.show()

# Print in 3D   
def Print3D(num_frame, point, arms, rightHand, leftHand, legs, body):
    # Maximum and minimum of coordinate 
    xmax = np.max(point[0, :, :, 0])
    xmin = np.min(point[0, :, :, 0]) 
    ymax = np.max(point[1, :, :, 0])
    ymin = np.min(point[1, :, :, 0])
    zmax = np.max(point[2, :, :, 0])
    zmin = np.min(point[2, :, :, 0])    
    
    n = 0 # Print from frame n 
    m = num_frame # Prent by frame m, n<m<row
    fig = plt.figure()
    plt.ion()
    # for i in range(0,1):
    for i in range(n, m):
        plt.cla() # Clear axis
 
        plot3D = plt.subplot(projection = '3d')
        # plot3D.view_init(120, -90) # Change the view 
        plot3D.view_init(0, 0)
        Expan_Multiple = 1 # Coordinate scaling factor
        
        # Every body joints
        # c: color, s: scale
        plot3D.scatter3D(point[0, i, :, :]*Expan_Multiple, point[1, i, :, :]*Expan_Multiple, point[2, i, :, :], c='red', s=40.0) 
 
        # Connect joints of first body
        # c: color, lw: line width 
        plot3D.plot(point[0, i, arms, 0]*Expan_Multiple, point[1, i, arms, 0]*Expan_Multiple, point[2, i, arms, 0], c='green', lw=2.0)
        plot3D.plot(point[0, i, rightHand, 0]*Expan_Multiple, point[1, i, rightHand, 0]*Expan_Multiple, point[2, i, rightHand, 0], c='green', lw=2.0) 
        plot3D.plot(point[0, i, leftHand, 0]*Expan_Multiple, point[1, i, leftHand, 0]*Expan_Multiple, point[2, i, leftHand, 0], c='green', lw=2.0)
        plot3D.plot(point[0, i, legs, 0]*Expan_Multiple, point[1, i, legs, 0]*Expan_Multiple, point[2, i, legs, 0], c='green', lw=2.0)
        plot3D.plot(point[0, i, body, 0]*Expan_Multiple, point[1, i, body, 0]*Expan_Multiple, point[2, i, body, 0], c='green', lw=2.0)
 
        # Connect joints of second body
        # plot3D.plot(point[0, i, arms, 1]*Expan_Multiple, point[1, i, arms, 1]*Expan_Multiple, point[2, i, arms, 1], c='green', lw=2.0)
        # plot3D.plot(point[0, i, rightHand, 1]*Expan_Multiple, point[1, i, rightHand, 1]*Expan_Multiple, point[2, i, rightHand, 1], c='green', lw=2.0)
        # plot3D.plot(point[0, i, leftHand, 1]*Expan_Multiple, point[1, i, leftHand, 1]*Expan_Multiple, point[2, i, leftHand, 1], c='green', lw=2.0)
        # plot3D.plot(point[0, i, legs, 1]*Expan_Multiple, point[1, i, legs, 1]*Expan_Multiple, point[2, i, legs, 1], c='green', lw=2.0)
        # plot3D.plot(point[0, i, body, 1]*Expan_Multiple, point[1, i, body, 1]*Expan_Multiple, point[2, i, body, 1], c='green', lw=2.0)
 
        # plot3D.text(xmax-0.3, ymax+1.1, zmax+0.3, 'frame: {}/{}'.format(i, num_frame-1)) # Text description
        plot3D.set_xlim3d(-0.5, 0.5) 
        plot3D.set_ylim3d(ymin-0.3, ymax+0.3) 
        plot3D.set_zlim3d(zmin-0.3, zmax+0.3) 
        plt.pause(0.001) 
    plot3D.set_xlabel('x')
    plot3D.set_ylabel('y')
    plot3D.set_zlabel('z')
    plt.ioff() 
    plt.show() 

########################For coordinate list########################

# Print in 3D for coordinate prime
# points: Axis * joint * frame
def draw_skeleton_ntu(num_frame, point, arms, rightHand, leftHand, legs, body):
    
    # Maximum and minimum of coordinate 
    xmax = np.max(point[0, :, :])
    xmin = np.min(point[0, :, :]) 
    ymax = np.max(point[1, :, :])
    ymin = np.min(point[1, :, :])
    zmax = np.max(point[2, :, :])
    zmin = np.min(point[2, :, :])   
    
    n = 0 # Print from frame n 
    m = num_frame # Print by frame m, n<m<row
    fig = plt.figure()
    plt.ion()

    # for i in range(0,1):
    for i in range(n, m):
        plt.cla() # Clear axis

        plot3D = plt.subplot(projection = '3d')
        plot3D.view_init(0, 0) # Change the view 
        
        Expan_Multiple = 1 # Coordinate scaling factor
        
        # Every body joints
        # c: color, s: scale
        plot3D.scatter(point[0, :, i]*Expan_Multiple, point[1, :, i]*Expan_Multiple, point[2, :, i], c='red', s=40.0) 
 
        # Connect joints of first body
        # c: color, lw: line width 
        plot3D.plot(point[0, arms, i]*Expan_Multiple, point[1, arms, i]*Expan_Multiple, point[2, arms, i], c='green', lw=2.0)
        plot3D.plot(point[0, rightHand, i]*Expan_Multiple, point[1, rightHand, i]*Expan_Multiple, point[2, rightHand, i], c='green', lw=2.0) 
        plot3D.plot(point[0, leftHand, i]*Expan_Multiple, point[1, leftHand, i]*Expan_Multiple, point[2, leftHand, i], c='green', lw=2.0)
        plot3D.plot(point[0, legs, i]*Expan_Multiple, point[1, legs, i]*Expan_Multiple, point[2, legs, i], c='green', lw=2.0)
        plot3D.plot(point[0, body, i]*Expan_Multiple, point[1, body, i]*Expan_Multiple, point[2, body, i], c='green', lw=2.0)
 
        # plot3D.text(xmax-0.3, ymax+1.1, zmax+0.3, 'frame: {}/{}'.format(i, num_frame-1)) # Text description
        plot3D.set_xlim3d(-0.6, 0.6) 
        plot3D.set_ylim3d(-0.6, 0.6) 
        plot3D.set_zlim3d(zmin-0.3, zmax+0.3) 
        plt.pause(0.1) 

    plot3D.set_xlabel('x')
    plot3D.set_ylabel('y')
    plot3D.set_zlabel('z')
    plt.ioff() 
    plt.show() 

def get_limb(X, Y, Z=None, id1=0, id2=1):
    if Z is not None:
        return np.concatenate((np.expand_dims(X[id1], 0), np.expand_dims(X[id2], 0)), 0), \
               np.concatenate((np.expand_dims(Y[id1], 0), np.expand_dims(Y[id2], 0)), 0), \
               np.concatenate((np.expand_dims(Z[id1], 0), np.expand_dims(Z[id2], 0)), 0)
    else:
        return np.concatenate((np.expand_dims(X[id1], 0), np.expand_dims(X[id2], 0)), 0), \
               np.concatenate((np.expand_dims(Y[id1], 0), np.expand_dims(Y[id2], 0)), 0)

# draw wholebody skeleton
# conf: which joint to draw, conf=None draw all
# 1 x 133 x 3
def draw_skeleton_coco(vec, fig, conf=None, pointsize=None, figsize=None, plt_show=True, save_path=None, inverse_z=False,
                  fakebbox=False, background=None):
    _, keypoint, d = vec.shape
    if keypoint==133:
        X = vec
        if (d == 3) or ((d==2) and (background==None)):
            X = X - (X[:,11:12,:]+X[:, 12:13,:])/2.0
        X=X.numpy()
        list_branch_head = [(0,1),(1,3),(0,2),(2,4), (59,64), (65,70),(71, 82),
                            (71,83),(77,87),(77,88),(88,89),(89,90),(71,90)]
        for i in range(16):
            list_branch_head.append((23+i, 24+i))
        for i in range(4):
            list_branch_head.append((40+i, 41+i))
            list_branch_head.append((45+i, 46+i))
            list_branch_head.append((54+i, 55+i))
            list_branch_head.append((83+i, 84+i))
        for i in range(3):
            list_branch_head.append((50+i, 51+i))
        for i in range(5):
            list_branch_head.append((59+i, 60+i))
            list_branch_head.append((65+i, 66+i))
        for i in range(11):
            list_branch_head.append((71+i, 72+i))

        list_branch_left_arm = [(5,7),(7,9),(9,91),(91,92),(93,96),(96,100),(100,104),(104,108),(91,108)]
        for i in range(3):
            list_branch_left_arm.append((92+i,93+i))
            list_branch_left_arm.append((96+i,97+i))
            list_branch_left_arm.append((100+i,101+i))
            list_branch_left_arm.append((104+i,105+i))
            list_branch_left_arm.append((108+i,109+i))
        list_branch_right_arm = [(6,8),(8,10),(10,112),(112,113),(114,117),(117,121),(121,125),(125,129),(112,129)]
        for i in range(3):
            list_branch_right_arm.append((113+i, 114+i))
            list_branch_right_arm.append((117+i, 118+i))
            list_branch_right_arm.append((121+i, 122+i))
            list_branch_right_arm.append((125+i, 126+i))
            list_branch_right_arm.append((129+i, 130+i))
        list_branch_body = [(5,6),(6,12),(11,12),(5,11)]
        list_branch_right_foot = [(12,14),(14,16),(16,20),(16,21),(16,22)]
        list_branch_left_foot = [(11,13),(13,15),(15,17),(15,18),(15,19)]
    else:
        print('Not implemented this skeleton')
        return 0

    if d==3:
        # fig = plt.figure()
        if figsize is not None:
            fig.set_size_inches(figsize,figsize)
        ax = fig.add_subplot(111, projection='3d')
        ax.elev = 10
        ax.grid(False)
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_zlabel('z')
        ax.set_xlim3d(0.75, -0.7500) 
        ax.set_ylim3d(0.7500, -0.7500) 
        ax.set_zlim3d(-0.750, 0.750) 
        # ax.set_xlim3d(-0.6, 0.6) 
        # ax.set_ylim3d(-0.6, 0.6) 
        # ax.set_zlim3d(0.3, 0.3) 

        if inverse_z:
            zdata = -X[0, :, 2]
        else:
            zdata = X[0, :, 2]
        xdata = X[0, :, 0]
        ydata = X[0, :, 1]
        if conf is not None:
            xdata*=conf[0,:].numpy()
            ydata*=conf[0,:].numpy()
            zdata*=conf[0,:].numpy()
        if pointsize is None:
            ax.scatter(xdata, ydata, zdata, c='r')
        else:
            ax.scatter(xdata, ydata, zdata, s=pointsize, c='r')

        if fakebbox:
            max_range= np.array([xdata.max() - xdata.min(), ydata.max() - ydata.min(), zdata.max() - zdata.min()]).max()
            Xb = 0.5 * max_range * np.mgrid[-1:2:2, -1:2:2, -1:2:2][0].flatten() + 0.5 * (xdata.max() + xdata.min())
            Yb = 0.5 * max_range * np.mgrid[-1:2:2, -1:2:2, -1:2:2][1].flatten() + 0.5 * (ydata.max() + ydata.min())
            Zb = 0.5 * max_range * np.mgrid[-1:2:2, -1:2:2, -1:2:2][2].flatten() + 0.5 * (zdata.max() + zdata.min())

            for xb, yb, zb in zip(Xb, Yb, Zb):
                ax.plot([xb], [yb], [zb], 'w')

            if background is not None:
                WidthX = Xb[7] - Xb[0]
                WidthY = Yb[7] - Yb[0]
                WidthZ = Zb[7] - Zb[0]
                arr = np.array(background.getdata()).reshape(background.size[1], background.size[0], 3).astype(float)
                arr = arr / arr.max()
                stepX, stepZ = WidthX / arr.shape[1], WidthZ / arr.shape[0]

                X1 = np.arange(0, -Xb[0]+Xb[7], stepX)
                Z1 = np.arange(Zb[7], Zb[0], -stepZ)
                X1, Z1 = np.meshgrid(X1, Z1)
                Y1 = Z1 * 0.0 + Zb[7] + 0.01
                ax.plot_surface(X1, Y1, Z1, rstride=1, cstride=1, facecolors=arr, shade=False)

        for (id1, id2) in list_branch_head:
            if ((conf is None) or ((conf[0,id1]>0.0) and (conf[0,id2]>0.0))):
                x, y, z = get_limb(xdata, ydata, zdata, id1, id2)
                ax.plot(x, y, z, color='red')
        for (id1, id2) in list_branch_body:
            if ((conf is None) or ((conf[0, id1] > 0.0) and (conf[0, id2] > 0.0))):
                x, y, z = get_limb(xdata, ydata, zdata, id1, id2)
                ax.plot(x, y, z, color='orange')
        for (id1, id2) in list_branch_left_arm:
            if ((conf is None) or ((conf[0,id1]>0.0) and (conf[0,id2]>0.0))):
                x, y, z = get_limb(xdata, ydata, zdata, id1, id2)
                ax.plot(x, y, z, color='blue')
        for (id1, id2) in list_branch_right_arm:
            if ((conf is None) or ((conf[0,id1]>0.0) and (conf[0,id2]>0.0))):
                x, y, z = get_limb(xdata, ydata, zdata, id1, id2)
                ax.plot(x, y, z, color='violet')
        for (id1, id2) in list_branch_left_foot:
            if ((conf is None) or ((conf[0,id1]>0.0) and (conf[0,id2]>0.0))):
                x, y, z = get_limb(xdata, ydata, zdata, id1, id2)
                ax.plot(x, y, z, color='cyan')
        for (id1, id2) in list_branch_right_foot:
            if ((conf is None) or ((conf[0,id1]>0.0) and (conf[0,id2]>0.0))):
                x, y, z = get_limb(xdata, ydata, zdata, id1, id2)
                ax.plot(x, y, z, color='pink')
        if plt_show:
            plt.show()
        if save_path is not None:
            fig.savefig(save_path)
            plt.close()


#####################################################################################
#############################MAIN VISUALZATION FUNCTIONS#############################
#####################################################################################

########################For .skeleton file########################

# Visualization main function
# Read from .skeleton file
def visualization(data_path):
    sys.path.extend(['../'])  # Extend path

    point = read_xyz(data_path)   

    print('Read Data Done!')
    num_frame = point.shape[1] # frame_num
    print(point.shape)  # xyz(3) × frame_num × joint_num(25) × max_body  

    # Adjacent joints label
    arms = [23, 11, 10, 9, 8, 20, 4, 5, 6, 7, 21] # 23 <-> 11 <-> 10 ...
    rightHand = [11, 24] # 11 <-> 24
    leftHand = [7, 22] # 7 <-> 22
    legs = [19, 18, 17, 16, 0, 12, 13, 14, 15] # 19 <-> 18 <-> 17 ...
    body = [3, 2, 20, 1, 0]  # 3 <-> 2 <-> 20 ...
    
    #Print2D(num_frame, point, arms, rightHand, leftHand, legs, body)  # 2D visualization 
    Print3D(num_frame, point, arms, rightHand, leftHand, legs, body) # 3D visualization

########################For coordinate list########################

# Visualization for NTU layout (12 joints)
def visualization_ntu(coordinate_list):
    num_frame = coordinate_list.shape[2] # frame_num
    # Adjacent joints label
    arms = [23, 11, 10, 9, 8, 20, 4, 5, 6, 7, 21] # 23 <-> 11 <-> 10 ...
    rightHand = [11, 24] # 11 <-> 24
    leftHand = [7, 22] # 7 <-> 22
    legs = [19, 18, 17, 16, 0, 12, 13, 14, 15] # 19 <-> 18 <-> 17 ...
    body = [3, 2, 20, 1, 0]  # 3 <-> 2 <-> 20 ...
    draw_skeleton_ntu(num_frame, coordinate_list, arms, rightHand, leftHand, legs, body)
 
# Visualzation for coco layout (133 joints)
def visualization_coco(coordinate_list):
    _, joint_num, frame_num = np.shape(coordinate_list)
    # fig = plt.figure()
    # plt.ion()
    skeleton = torch.zeros(1,133,3)
    fig = plt.figure()
    plt.ion()
    for i in range(frame_num):
    # for i in range(24, 25):
    # for i in range(1):
        plt.cla()
        plot3D = plt.subplot(projection = '3d')
        plot3D.view_init(0, 180) # Change the view 

        coord = coordinate_list[:,:,i]
        for j in range(joint_num):
            skeleton[0,j,0] = coord[0,j]
            skeleton[0,j,1] = coord[1,j]
            skeleton[0,j,2] = coord[2,j]
        plt.title('Frame: %i' %i)
        draw_skeleton_coco(skeleton, fig, pointsize=2, figsize=10 )
        plt.pause(0.001) 
    plt.ioff() 
    plt.show() 

# Visualization for coordinate after correction 
# Input: coordinate_list: Axis * joint * frame
def visualization_prime(coordinate_list):
    # Joint_num = 25 (NTU layout)
    if coordinate_list.shape[1] == 25:
        visualization_ntu(coordinate_list)
    # Joint_num = 133 (COCO layout)
    if coordinate_list.shape[1] == 133:
        visualization_coco(coordinate_list)

    
if __name__ == "__main__":
    skeleton_coordinates = aa.read_xyz_json(r'code\demo\skeleton_json\res_3d.json')
    # skeleton_coordinates = aa.read_xyz_json(r'code\demo\skeleton_json\S1_Images_Greeting.58860488.json', 28)
    coordinate_prime = aa.coordinate_correction(skeleton_coordinates)
    
    visualization_prime(coordinate_prime)