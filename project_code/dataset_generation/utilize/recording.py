
from PIL import ImageGrab
import numpy as np
import cv2
import datetime
from pynput import keyboard
import threading
flag=False  # Stop recording
def video_record():

    name = datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S') # Current time
    p = ImageGrab.grab()  # Current screen
    a, b = p.size  # Screen size
    fourcc = cv2.VideoWriter_fourcc(*'MP4V')  # Code type
    video = cv2.VideoWriter('%s.mp4'%name, fourcc, 25, (a, b))  
    while True:
        im = ImageGrab.grab()
        imm=cv2.cvtColor(np.array(im), cv2.COLOR_RGB2BGR)
        video.write(imm)
        if flag:
            print("Finish!")
            break
    video.release()
def on_press(key):

    global flag
    if key == keyboard.Key.f5:
        flag=True
        print("stop monitor!")
        return False  
 
if __name__=='__main__':
    th=threading.Thread(target=video_record)
    th.start()
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()