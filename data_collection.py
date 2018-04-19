## Casey Astiz and Nick Cogswell 701
## Script to collect data and label simulateously

#range.py
#run.py
#capture_video_data.py

import numpy as np
import cv2
#from range.py import dist


def main():
    """
    Main will simulatenously collect data from the ultrasonic 
    sensor, camera, and direction commands to create input
    data matrices combined with direction labels.
    """
    data = [] #a list of data points stored as tuples

    while input() != "q":
        image = take_picture()
        dist = dist()
        print(dist)
        combined_input = image + dist
        #label = run.py
        label = 0
        #add new data point to dataset
        data.append((combined_input,label)) 
    #print(len(data))
    return data #maybe instead of return, need to write to local dir

def take_picture():
    """takes a picture at the current moment to be labeled in main"""
    cam = cv2.VideoCapture(0)
    s, im = cam.read() #captures image
    #cv2.imwrit("test.bmp", im) #writes image to disk
    gray_image = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    temp = np.array(gray_image)
#    print(temp.shape)
    flattened = temp.flatten()
#    print(flattened.shape)
    return flattened


main()

