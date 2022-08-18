# Importing Libraries for GPS Navigation
import serial
from pyubx2 import UBXReader
from shapely.geometry import Point, Polygon
import threading

# Setup for GPS Navigation
stream = serial.Serial("/dev/ttyACM0", 38400, timeout=3)
ubr = UBXReader(stream)

# Importing Libraries for Robot Movement
import RPi.GPIO as GPIO
from time import sleep

# Setup for Robot Movement
AN1 = 12
AN2 = 13
DIG2 = 24
DIG1 = 26

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(17, GPIO.OUT)
GPIO.setup(AN2, GPIO.OUT)
GPIO.setup(AN1, GPIO.OUT)
GPIO.setup(DIG2, GPIO.OUT)
GPIO.setup(DIG1, GPIO.OUT)
p1 = GPIO.PWM(DIG1, 100)
p2 = GPIO.PWM(DIG2, 100)
pwm = GPIO.PWM(17, 50)

def forward(x):
    print("Forward")
    GPIO.output(AN1, GPIO.HIGH)
    GPIO.output(AN2, GPIO.HIGH)
    p1.start(0)
    p2.start(0)
    sleep(x)
    stop()

def right(x):
    print("Right")
    GPIO.output(AN1, GPIO.HIGH)
    GPIO.output(AN2, GPIO.HIGH)
    p1.start(100)
    p2.start(0)
    sleep(x)
    stop()

def left(x):
    print("Left")
    GPIO.output(AN1, GPIO.HIGH)
    GPIO.output(AN2, GPIO.HIGH)
    p1.start(0)
    p2.start(100)
    sleep(x)
    stop()

def back(x):
    print("Backward")
    GPIO.output(AN1, GPIO.HIGH)
    GPIO.output(AN2, GPIO.HIGH)
    p1.start(100)
    p2.start(100)
    sleep(x)
    stop()

def stop():
    print("Stop")
    GPIO.output(AN1, GPIO.LOW)
    GPIO.output(AN2, GPIO.LOW)
    p1.start(0)
    p2.start(0)

def end():
    print("End")
    GPIO.output(AN1, GPIO.LOW)
    GPIO.output(AN2, GPIO.LOW)
    pwm.stop()
    p1.start(0)
    p2.start(0)
    sleep(1)

# Main Function

lat1 = 40.554697539
long1 = -74.394024133

lat2 = 40.554660827
long2 = -74.393967461

lat3 = 40.554709854
long3 = -74.393926932

lat4 = 40.554740111
long4 = -74.393990068

coordinates = [(lat1, long1), (lat2, long2), (lat3, long3), (lat4, long4)]
polygon = Polygon(coordinates)

class RobotLocation:
    def __init__(self, lat_, lon_, hAcc_):
        self.lat = lat_
        self.lon = lon_
        self.hAcc = hAcc_

(raw_data, parsed_data) = ubr.read()
data = RobotLocation(parsed_data.lat, parsed_data.lon, parsed_data.hAcc)

def getCoordinates():
    while True:
        (raw_data, parsed_data) = ubr.read()
        data.lat = parsed_data.lat
        data.lon = parsed_data.lon
        data.hAcc = parsed_data.hAcc
        print("Iterating: " + str(parsed_data.lat) + " " + str(parsed_data.lon) + " " + str(parsed_data.hAcc))
        sleep(1)

thread1 = threading.Thread(target=getCoordinates, args=())
thread1.start()

while True:

    point = Point(data.lat, data.lon)

    if (data.hAcc > 60):
        print("Accuracy: " + str(data.hAcc))
        print("Latitude: " + str(data.lat))
        print("Longitude: " + str(data.lon))
        print("Horizontal Accuracy is not high enough.")
        sleep(10)

    elif (point.within(polygon)):
        forward(0.05)
        print("Accuracy: " + str(data.hAcc))
        print("Latitude: " + str(data.lat))
        print("Longitude: " + str(data.lon))
        print("Moving Forward")

    elif(point.within(polygon) == False):
        stop()
        left(3)
        forward(3)
        print("Accuracy: " + str(data.hAcc))
        print("Latitude: " + str(data.lat))
        print("Longitude: " + str(data.lon))
        print("Moving Left")