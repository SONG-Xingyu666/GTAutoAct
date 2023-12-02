import cv2
import numpy as np
import pyautogui
import time
from datetime import datetime
import argparse

def record_screen(output_file, fps, duration):
    # Get screen size
    screen_size = (pyautogui.size().width, pyautogui.size().height)
    
    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(output_file, fourcc, fps, screen_size)
    
    # Record the screen
    start_time = time.time()
    count = 0
    while True:
        # Take screenshot
        img = pyautogui.screenshot()
        count += 1
        
        # Convert screenshot to numpy array
        frame = np.array(img)
        
        # Convert BGR to RGB
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Write the frame
        out.write(frame)
        
        # Show the frame
        cv2.imshow("Screen Recorder", frame)
        
        # Break the loop if 'q' is pressed or if the duration has passed
        if cv2.waitKey(1) == ord('q') or (time.time() - start_time > duration):
            break
    
    # Release the VideoWriter and close windows
    out.release()
    cv2.destroyAllWindows()
    print(count)
if __name__ == "__main__":
    # parser = argparse.ArgumentParser(description="Screen Recorder")
    # parser.add_argument("--output", type=str, default="output.avi", help="Output video file")
    # parser.add_argument("--fps", type=int, default=30, help="Frames per second")
    # parser.add_argument("--duration", type=int, default=10, help="Duration of recording in seconds")
    # args = parser.parse_args()
    output_file = r'videos/test.mp4'
    fps = 30
    duration = 5
    record_screen(output_file, fps, duration)
