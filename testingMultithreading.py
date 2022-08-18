import time
from time import sleep
import threading

# The idea in this file is to simply test whether or not
# Python multithreading works. 

class Coordinates:
    def __init__(self, num):
        self.number = num

a = Coordinates(0)

def iterateNumber():
    while True:
        a.number = a.number + 1
        sleep(1)

def printNumber():
    while True:
        print(a.number)
        sleep(5)

thread1 = threading.Thread(target=iterateNumber, args=())
thread2 = threading.Thread(target=printNumber, args=())


thread1.start()
thread2.start()