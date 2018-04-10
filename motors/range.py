import RPi.GPIO as GPIO
import time

def dist():
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    while GPIO.input(ECHO)==0:
        pulse_start = time.time() 

    while GPIO.input(ECHO)==1:
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start

    distance = pulse_duration * 17150

    distance = round(distance, 2)
    print ("Distance:", distance, "cm")

    return distance

if __name__ == '__main__':
    GPIO.setmode(GPIO.BOARD)

    TRIG = 3
    ECHO = 5

    GPIO.setup(TRIG,GPIO.OUT)
    GPIO.setup(ECHO,GPIO.IN)

    print ("Distance Measurement In Progress")

    try:
        while True:
            dist()
            time.sleep(.25)
                                                 
    except KeyboardInterrupt:
        print("\nMeasurement stopped by User")

    GPIO.output(TRIG, False)
    print ("Waiting For Sensor To Settle")
    time.sleep(2)
    print ("Done")

    GPIO.cleanup()
