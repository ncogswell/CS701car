# Motor Controls
# Drive: w- forward, x- backward, e- stop
# Turn: a- left, d- right, s- stop
# z- full stop, q- quit

import RPi.GPIO as GPIO
from time import sleep

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

current_state = 'e','s'

def set_state_drive(a):
    global current_state
    x,y = current_state
    current_state = a,y

def set_state_turn(a):
    global current_state
    x,y = current_state
    current_state = x,a

def drive(dir):
  print("drive dir = ",dir)
  set_state_drive(dir)
  if dir == "w":
    GPIO.output(Motor2A,GPIO.HIGH)
    GPIO.output(Motor2B,GPIO.LOW)
    GPIO.output(Motor2E,GPIO.HIGH)
    print("drive forward")
  elif dir == "x":
    GPIO.output(Motor2A,GPIO.LOW)
    GPIO.output(Motor2B,GPIO.HIGH)
    GPIO.output(Motor2E,GPIO.HIGH)
    print("drive back")
  else: 
    GPIO.output(Motor2E,GPIO.LOW)
    GPIO.output(Motor2A,GPIO.LOW)
    GPIO.output(Motor2B,GPIO.LOW)

def turn(dir):
  print("turn dir = ", dir) 
  set_state_turn(dir)
  if dir == "s":
    GPIO.output(Motor1E,GPIO.LOW)
  elif dir == "a":
    GPIO.output(Motor2E,GPIO.LOW)
    sleep(.2)
    GPIO.output(Motor1A,GPIO.LOW)
    GPIO.output(Motor1B,GPIO.HIGH)
    GPIO.output(Motor1E,GPIO.HIGH)
    sleep(.4)
    GPIO.output(Motor2E,GPIO.HIGH)
  else:
    GPIO.output(Motor2E,GPIO.LOW)
    sleep(.2)
    GPIO.output(Motor1A,GPIO.HIGH)
    GPIO.output(Motor1B,GPIO.LOW)
    GPIO.output(Motor1E,GPIO.HIGH)
    sleep(.4)
    GPIO.output(Motor2E,GPIO.HIGH)

def full_stop():
  print("full_stop")
  GPIO.output(Motor1E,GPIO.LOW)
  GPIO.output(Motor2A,GPIO.LOW)
  GPIO.output(Motor2B,GPIO.LOW)
  GPIO.output(Motor2E,GPIO.LOW)

dir = input()

while dir != "q":

  if dir in {"w","e","x"}:
    drive(dir)
  elif dir in {"a","s","d"}:
    turn(dir)
  elif dir == "z":
    full_stop()
  print (current_state)

  dir = input()

full_stop()

GPIO.cleanup()
