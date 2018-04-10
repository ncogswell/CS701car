import threading
from time import sleep

a = ''

def loop():
    try:
        while a != 'q':
            print("data point")
            sleep(1)
    except KeyboardInterrupt:
        print("Done")

def usr():
    global a
    a = input()
    while a != 'q':
        print(a)
        a = input()

thread = threading.Thread(target=loop)
thread.start()

usr()
