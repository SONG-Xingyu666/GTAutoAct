# Tool for automatically video recording (training dataset for temporal action prediction)
'''
  Game: <Assassin's Creed Unity> or <Assassin's Creed Syndicate>
  Tool: 'Steam', 'Extremeinjector', 'pyautogui', 'pydirectinput'
  Method: Simulating the 'keyboard' operation
      (1) Using the 'extreme injector' and video recording toolkit in Windows 11
      (2) Rotate free camera for identical 'scenario'
'''

import time
import os
import sys
import math

import pyautogui
import pydirectinput

import cv2

#-------------------------------------------------------------
# Keyboard mapping of keypad
class Keys:
  NUM4 = 'numpad4'
  NUM5 = 'numpad5'
  NUM6 = 'numpad6'
  NUM8 = 'numpad8'
pydirectinput.KEYBOARD_MAPPING[Keys.NUM4] = 0x4B
pydirectinput.KEYBOARD_MAPPING[Keys.NUM5] = 0x4C
pydirectinput.KEYBOARD_MAPPING[Keys.NUM6] = 0x4D
pydirectinput.KEYBOARD_MAPPING[Keys.NUM8] = 0x48

#-------------------------------------------------------------

#---------------------------------------------------------------
'''
  The part that need to be changed when recording for other scenarios
'''
# Parameters of dataset generation
video_type = 'ACU_squat_'  # The action type that need to be recorded
result_path = 'C:/Users/lizha/Videos/Captures/'
index_initial = 1  # The initial index of recorded videos
rotate_angle = 30  # The angle that would be rotated each time
radiu_camera = 1.8  # The radiu of rotating cameras


# Action sequences for recording: The most important!!!!
'''
  Format: [action1, duration time1, action2, duration time2, ...]
'''
action_sequence = ['s', 4, 'w', 4]

#---------------------------------------------------------------

# Shift to the <Steam> interface
pyautogui.keyDown('alt')
pyautogui.keyDown('tab')
pyautogui.keyUp('tab')
time.sleep(0.01)
pyautogui.keyUp('alt')
time.sleep(0.01)


# for i in range(1, 64671):
#   pydirectinput.keyDown('down')
#   time.sleep(0.000001)
#   pydirectinput.keyUp('down')


for i in range(148891, 200000):


  pydirectinput.keyDown('enter')

  time.sleep(0.00005)
  pydirectinput.keyUp('enter')

  pydirectinput.keyDown('down')
  time.sleep(0.00005)
  pydirectinput.keyUp('down')






# The outer loop of video recording

'''


  #Prerequisite: 

     (1) Pre-open the free camera in game

     (2) Set the free camera to the most right side

     (3) Determining the 'action_sequence'4

'''

# for i in range(180 // rotate_angle):

#   # Video recording
#   pyautogui.hotkey('win', 'g')  # Open the 'Windows 10 XBOX' for video recording
#   time.sleep(2)
#   pyautogui.hotkey('win', 'alt', 'r')  # Hotkey of "video recording"
#   time.sleep(2)
#   pyautogui.click()  # Exit 'Windows 10 XBOX' and begin to video recording
#   time.sleep(1)

#   # Conducting the 'action seqeunce'
#   for j in range(0, len(action_sequence), 2):
#     pydirectinput.keyDown(action_sequence[j])
#     time.sleep(action_sequence[j + 1])
#     pydirectinput.keyUp(action_sequence[j])

#   # End the procedure of video recording and obtain video data
#   pyautogui.hotkey('win', 'alt', 'r')  

#   # Rotate the angle of free camera
#   pydirectinput.keyDown('right')
#   time.sleep(1)
#   pydirectinput.keyUp('right')

#   pydirectinput.keyDown('numpad4')
#   #win32api.keybd_event(52, 0x4B, 0, 0)
#   time.sleep((radiu_camera + 1) * math.sin(math.radians(rotate_angle)))
#   #win32api.keybd_event(52, 0x4B, win32con.KEYEVENTF_KEYUP, 0)
#   pydirectinput.keyUp('numpad4')

#   pydirectinput.keyDown('numpad5')
#   #win32api.keybd_event(56, 0x48, 0, 0)
#   time.sleep((radiu_camera + 1) * (1 - math.cos(math.radians(rotate_angle))))
#   #win32api.keybd_event(56, 0x48, win32con.KEYEVENTF_KEYUP, 0)
#   pydirectinput.keyUp('numpad5')

#   time.sleep(5)


# Assign video numbers to each obtained video
# video_list = os.listdir(result_path)

# # Count the number of videos that have been collected
# video_collect_num = 0
# for vis_name in video_list:
#   if video_type in vis_name:
#     video_collect_num = video_collect_num + 1

# # Assign video numbers
# video_collect_current = 1
# for vis_name in video_list:
#   if video_type not in vis_name:
#     os.rename(result_path + vis_name, result_path + video_type + str(video_collect_current + video_collect_num + index_initial) + '.mp4')
#     video_collect_current = video_collect_current + 1

