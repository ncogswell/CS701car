import numpy as np
import cv2

cam = cv2.VideoCapture(0)
s, im = cam.read() #captures image
cv2.imwrite("testimg.bmp", im) #writes image to disk
