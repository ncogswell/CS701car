# Motor Controls
# Drive: w- forward, x- backward, e- stop
# Turn: a- left, d- right, s- stop
# z- full stop, q- quit

import RPi.GPIO as GPIO
import time
import numpy as np
import cv2
import threading
import csv
import os

# Initialization
GPIO.setmode(GPIO.BOARD)
 
Motor1A = 16
Motor1B = 18
Motor1E = 22
 
Motor2A = 19
Motor2B = 21
Motor2E = 23
 
GPIO.setup(Motor1A,GPIO.OUT)
GPIO.setup(Motor1B,GPIO.OUT)
GPIO.setup(Motor1E,GPIO.OUT)
 
GPIO.setup(Motor2A,GPIO.OUT)
GPIO.setup(Motor2B,GPIO.OUT)
GPIO.setup(Motor2E,GPIO.OUT)

TRIG = 3
ECHO = 5

GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)

current_state = 'e','s'


# Driving Method
def set_state_drive(a):
    global current_state
    x,y = current_state
    current_state = a,y

def set_state_turn(a):
    global current_state
    x,y = current_state
    current_state = x,a

def drive(dir):
    #print("drive dir = ",dir)
    set_state_drive(dir)
    if dir == "w":
        GPIO.output(Motor2A,GPIO.HIGH)
        GPIO.output(Motor2B,GPIO.LOW)
        GPIO.output(Motor2E,GPIO.HIGH)
    elif dir == "x":
        GPIO.output(Motor2A,GPIO.LOW)
        GPIO.output(Motor2B,GPIO.HIGH)
        GPIO.output(Motor2E,GPIO.HIGH)
    else: 
        GPIO.output(Motor2E,GPIO.LOW)
        GPIO.output(Motor2A,GPIO.LOW)
        GPIO.output(Motor2B,GPIO.LOW)

def turn(dir):
    #print("turn dir = ", dir) 
    set_state_turn(dir)
    if dir == "s":
        GPIO.output(Motor1E,GPIO.LOW)
    elif dir == "a":
        GPIO.output(Motor2E,GPIO.LOW)
        time.sleep(.2)
        GPIO.output(Motor1A,GPIO.LOW)
        GPIO.output(Motor1B,GPIO.HIGH)
        GPIO.output(Motor1E,GPIO.HIGH)
        time.sleep(.4)
        GPIO.output(Motor2E,GPIO.HIGH)
    else:
        GPIO.output(Motor2E,GPIO.LOW)
        time.sleep(.2)
        GPIO.output(Motor1A,GPIO.HIGH)
        GPIO.output(Motor1B,GPIO.LOW)
        GPIO.output(Motor1E,GPIO.HIGH)
        time.sleep(.4)
        GPIO.output(Motor2E,GPIO.HIGH)

def full_stop():
    #print("full_stop")
    GPIO.output(Motor1E,GPIO.LOW)
    GPIO.output(Motor2A,GPIO.LOW)
    GPIO.output(Motor2B,GPIO.LOW)
    GPIO.output(Motor2E,GPIO.LOW)

# Range Sensor Methods
def dist():
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    pulse_start = time.time() 
    while GPIO.input(ECHO)==0:
        pulse_start = time.time() 

    pulse_end = time.time() 
    while GPIO.input(ECHO)==1:
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start

    distance = pulse_duration * 17150

    distance = round(distance, 2)

    return distance

# Webcam Methods
def take_picture():
    """takes a picture at the current moment to be labeled in main"""
    cam = cv2.VideoCapture(0)
    s, im = cam.read() #captures image
    #gray_image = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    #temp = np.array(gray_image)
    temp = np.array(im)
#    print(temp.shape)
    flattened = temp.flatten()
#    print(flattened.shape)
    return flattened

# Data Collection Methods
def collect_data():
    while dir != "q":
        global data
        start_time = time.time()
        image = take_picture().tolist()
        d = dist()
        print(d)
        image.append(d)
        data.append([image, dir])
        end_time = time.time()
        if end_time - start_time < 1 :
            time.sleep(1)

def collect_data2():
    global data_size
    global dist_array
    cam = cv2.VideoCapture(0)
    while dir != "q":
        s, im = cam.read()
        name = "imgs/" + str(data_size) + ".bmp"
        cv2.imwrite(name, im)
        d = dist()
        print(d)
        dist_array.append([d,current_state])
        data_size = data_size + 1
        time.sleep(.2)

def save_data():
    global data
    for filename in os.listdir('imgs'):
        index = int(filename[:-4])
        if index < data_size:
            print (filename, " ", index, " ", dist_array[index])
            distance, direction = dist_array[index]
            im = cv2.imread(filename)
            temp = np.array(im)
            flattened = temp.flatten()
            print (flattened.tolist())
            data.append([flattened.tolist().append(direction),direction])

# Start Data Collection
dir = "z"
data = [] #a list of data points stored as tuples
dist_array = []
data_size = 0

thread = threading.Thread(target=collect_data2, name="data_collection")
thread.start()

# Start Driving
while dir != "q":

    dir = input()
    if dir in {"w","e","x"}:
        drive(dir)
    elif dir in {"a","s","d"}:
        turn(dir)
    elif dir == "z":
        full_stop()


# GPIO cleanup
full_stop()

GPIO.output(TRIG, False)
print ("Waiting For Sensor To Settle")
time.sleep(2)
print ("Done")


GPIO.cleanup()

# Write data to file to be read in on another computer
save_data()

csvfile = "training_data.csv"

with open(csvfile, "w") as output:
    writer = csv.writer(output, lineterminator='\n')
    writer.writerows(data)
