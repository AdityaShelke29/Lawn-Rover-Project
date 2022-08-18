# Importing Libraries for GPS Navigation
import serial
from pyubx2 import UBXReader
from shapely.geometry import Point, Polygon

# Setup for GPS Navigation
stream = serial.Serial("COM3", 38400, timeout=3)
ubr = UBXReader(stream)

# Importing Libraries for Robot Movement
from time import sleep

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

while True:
    (raw_data, parsed_data) = ubr.read()
    point = Point(parsed_data.lat, parsed_data.lon)

    if (parsed_data.hAcc > 60):
        print("Accuracy: " + str(parsed_data.hAcc))
        print("Latitude: " + str(parsed_data.lat))
        print("Longitude: " + str(parsed_data.lon))
        print("Horizontal Accuracy is not high enough.")

    elif (point.within(polygon)):
        print("Accuracy: " + str(parsed_data.hAcc))
        print("Latitude: " + str(parsed_data.lat))
        print("Longitude: " + str(parsed_data.lon))
        print("Moving Forward")
        sleep(1)

    elif(point.within(polygon) == False):
        print("Accuracy: " + str(parsed_data.hAcc))
        print("Latitude: " + str(parsed_data.lat))
        print("Longitude: " + str(parsed_data.lon))
        print("Moving Left")
        sleep(1)