# GTAutoAct Auto-Collection

import pydirectinput
import time
import math
import pyautogui
import matplotlib.pyplot as plt 
import cv2
import numpy as np
import random
import os
from mpl_toolkits.mplot3d import Axes3D 
from PIL import ImageGrab
# from auto_recording import change_screen_to_game


#############################################################################
# CONFIGURATIONS
#############################################################################
time_interval = 1
duration = 2.0
animation_command = '/ani'
camera_command = '/cam'
search_command = 'h'
next_animation_command = 'down'
play_animation_command = 'x'


#############################################################################
# BASIC FUNCTIONS
#############################################################################

def change_screen_to_game():
    pyautogui.keyDown('alt')
    pyautogui.keyDown('tab')
    pyautogui.keyUp('tab')
    time.sleep(0.01)
    pyautogui.keyUp('alt')
    time.sleep(0.01)

# Calculate coordinates of vector with magnitude and angle
def calculate_coords(magnitude, angle): # angle in 0-360
    angle = math.pi*(angle/180)
    x = magnitude * math.cos(angle)
    y = magnitude * math.sin(angle)
    return x, y

# Press button and hold for a period of time
def press_button(button, time_interval):
    pydirectinput.keyDown(button)
    time.sleep(time_interval)
    pydirectinput.keyUp(button)

# Recording the screen
def screen_record(duration, path):
    '''
    recording screen in a specific time
    duration: video time
    path: path of saving video
    '''
    flag=False # flag for stop recording  
    screen = ImageGrab.grab()  
    width, height = screen.size  
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  
    video = cv2.VideoWriter(path, fourcc, 30, (width, height))  
    start_time = cv2.getTickCount()
    i = 0
    
    play_animation()
    while (cv2.getTickCount() - start_time) / cv2.getTickFrequency() < duration:
        frame = ImageGrab.grab()
        #frame = pyautogui.screenshot()
        frame = cv2.cvtColor(np.array(frame), cv2.COLOR_RGB2BGR) # convert RGB to BGR
        video.write(frame)
        print(i)
        i += 1

    print("Recording finish")
    print("Input video path is", path)

    video.release()
    cv2.destroyAllWindows()

# Create folder
def create_folder(path, name):
    dir_path = os.path.join(path, name)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    return dir_path


#############################################################################
# MODE SETSTINGS
#############################################################################

# Set player mode to to camera mode 
def set_camera_mode():
    pydirectinput.press('t')
    pydirectinput.typewrite(camera_command)
    pydirectinput.press('enter')
    pydirectinput.press('enter')
    pydirectinput.press('backspace')

# Set camera mode to player mode
def set_player_mode():
    pydirectinput.press('t')
    pydirectinput.typewrite(camera_command)
    pydirectinput.press('enter')
    pydirectinput.press('enter')
    pydirectinput.press('backspace')

# Set animation mode open
# both at player mode and camera mode are fine
def set_animation_mod():
    pydirectinput.press('t')
    pydirectinput.typewrite(animation_command)
    pydirectinput.press('enter')


#############################################################################
# ENVIRONMENT SETTINGS (in any mode)
#############################################################################

# Go to next location in the location list
def goto_next_location():
    pydirectinput.press(']')

# Go to random location in the location list
def goto_random_location():
    pydirectinput.press('[')

# Change the weather in game
def change_weather():
    pydirectinput.press('F9')

# Change the player ped in game
def change_ped():
    pydirectinput.press('F10')

# Change the time of the day in game
def change_time():
    pydirectinput.press('F11')

#############################################################################
# ANIMATION SETTINGS (in animation mode)
#############################################################################
# Play animation
def play_animation():
    pydirectinput.press(play_animation_command)

# Wait animation to finish (for recording) 
def wait_animation_finish(duration):
    time.sleep(duration)

# Go to next animation
def next_animation():
    pydirectinput.press('down')

# go to last animation
def last_animation():
    pydirectinput.press('up')

# search animation (animation mode)
def search_animation(keyword):
    pydirectinput.press(search_command)
    pydirectinput.typewrite(keyword)
    pydirectinput.press('enter')

    # Go to the first search result
    pydirectinput.press(next_animation_command)

# Get animation duration from the txt file from animation path
def get_animation_info(animation_path):
    duration = 0
    
    while duration < 1:

        # To write the duration of animation
        play_animation()

        # If animation information not been writen, play it again
        while not os.path.exists(r'animation_lists\text.txt'):
            play_animation()
        # Open txt file
        animation = open(r'animation_lists\text.txt', 'r')

        # Get animation dictionary, name and duration
        line = animation.readline().strip()
        info = line.split(' ')
        dict = info[0]
        anim = info[1]
        duration = float(info[2])
        animation.close()
        os.remove(animation_path)
        if duration < 1:
            next_animation()



    return dict, anim, duration
    
# Delete animation information txt file
def delete_animation_info():
    if os.path.exists(r'animation_lists\text.txt'):
        os.remove(r'animation_lists\text.txt')


#############################################################################
# CAMERA SETSTINGS (in camera mode)
#############################################################################
# Focue the camera to player
def cam_focus_player():
    pydirectinput.press(',')

# Releace the camera focus of player
def cam_release_focus_player():
    pydirectinput.press('.')

# Move camera at X-axis (right and left)
# right is positive, left is negative
def cam_move_x(time_x): 
    if time_x > 0:
        pydirectinput.keyDown('d')
        time.sleep(time_x)
        pydirectinput.keyUp('d') # move right 
    if time_x < 0:
        pydirectinput.keyDown('a')
        time.sleep(abs(time_x))
        pydirectinput.keyUp('a') # move left


# Move camera at Y-axis (front and back)
# front is postive, back is negative
def cam_move_y(time_y): 
    if time_y > 0:
        pydirectinput.keyDown('w')
        time.sleep(time_y)
        pydirectinput.keyUp('w') # move front
    if time_y < 0:
        pydirectinput.keyDown('s')
        time.sleep(abs(time_y))
        pydirectinput.keyUp('s') # move back

# Move camera at Z-axis (up and down)
# up is postive, down is negative
def cam_move_z(time_z): 
    if time_z > 0:
        pydirectinput.keyDown('space')
        time.sleep(time_z)
        pydirectinput.keyUp('space') # move up 
    if time_z < 0:
        pydirectinput.keyDown('ctrl')
        time.sleep(abs(time_z))
        pydirectinput.keyUp('ctrl') # move down

# reset camera to initial postition (in camera mode)
def cam_reset():
    set_camera_mode()
    pydirectinput.press('enter')
    pydirectinput.press('enter')
    pydirectinput.press('backspace')




#############################################################################
# MOVE CAMERA (in camera mode)
#############################################################################
# Random Camera Moving (RCM)
def RCM(duration, path, postition_num):
    magnitude = 0.001
    # magnitude_delta = 0.05
    angle = random.uniform(0, 360)
    # angle_delta = 50
    x = 0.0
    y = 0.0
    z = 0.0
    x_list = [0.0]
    y_list = [0.0]
    z_list = [0.0] 
    for index in range(1, postition_num+1):
        
        x_new, y_new = calculate_coords(magnitude, angle)

        angle_delta = random.uniform(60, 120)
        magnitude_delta = random.uniform(-0.3, 0.3)
        x_delta = x_new - x
        y_delta = y_new - y
        z_delta = random.uniform(-0.1, 0.3)

        cam_move_x(x_delta)
        cam_move_y(y_delta)
        cam_move_z(z_delta)
        
        x = x_new
        y = y_new
        z = z + z_delta
        magnitude += magnitude_delta
        angle += angle_delta

        output_path = path + '_p' + str(index) + '.mp4'

        screen_record(duration, output_path)
        change_time()
        change_weather()
        change_ped()
        x_list.append(x)
        y_list.append(y)
        z_list.append(z)
        time.sleep(0.2)
        

    set_player_mode()
    # print(x_list)
    # print(y_list)
    # print(z_list)
    # fig = plt.figure()
    # ax = Axes3D(fig)
    # ax.plot3D(x_list, y_list, z_list, c='r')
    # plt.show()

#############################################################################
# OBTAINING ANIMATION INFORAMTION
#############################################################################

def obtain_animation_info_ingame(animation_info_path, keyword):
    # Search animation by keywords
    # search_animation(keyword)

    while get_animation_info(animation_info_path) == None:
        next_animation()
    # Get animation information
    dict, anim, duration = get_animation_info(animation_info_path)

    return dict, anim, duration

def obtain_animation_info_bylist(animation_info_path):
    animation_info = open(animation_info_path)    
    lines = animation_info.readlines()


def recording_animation(output_dir, dict, anim, duration, location_num, postition_num):
    # Create output path
    output_path = output_dir + '\\' + anim

    for i in range(1, location_num+1):
        
        output_path_loc = output_path + '_l' + str(i)
        # turn to camera mode
        set_camera_mode()
        # focus camera to player
        cam_focus_player()
        # camera spiral up movement 
        RCM(duration, output_path_loc, postition_num)
        # Move to next location 
        goto_next_location()
        # Change weahther
        change_weather()
        # Change time
        change_time()
        # Change ped
        change_ped()
        
        time.sleep(0.5)



if __name__ == '__main__':
    #############################################################################
    # VARIABLE DECLARATIOIN
    #############################################################################

    output_dir = r'videos'

    # For in game animation information obtaining  
    
    animation_info_path = r'resources\[scripts]\animation\client\animations.lua'
    

    # For by list animation information obtaining
    keyword = 'H36M'
    postition_num = 3
    location_num = 4
    animation_num = 284

    #############################################################################
    # ANIMATION CONFIGURATION
    #############################################################################

    # change to game
    change_screen_to_game()


    # turn on animation mode
    set_animation_mod()
    
    # Create folder for animations of same keyword
    output_dir = create_folder(output_dir, keyword)

    #############################################################################
    # OBTAINING INFORMATION, PLAYING ANIMATION, RECORDING, TRIMMING, LABELING
    #############################################################################
    
    f = open(animation_info_path)
    anim_list = f.readlines()


    for i in range(1, animation_num):
        # Using all animations list, obtaining animation information in game    
        print(anim_list[i])

        # dict, anim, duration = obtain_animation_info_ingame(animation_info_path, keyword)
        dict = anim_list[i].split('\'')[1]
        anim = anim_list[i].split('\'')[3]
        duration = float(anim_list[i].split('\'')[5])
        animation_name = anim
        animation_dir = create_folder(output_dir, animation_name)
        recording_animation(animation_dir, dict, anim, duration, location_num, postition_num)
        next_animation()


    #############################################################################
    # FINISH
    #############################################################################
    

    # turn off animation mode
    set_animation_mod()



