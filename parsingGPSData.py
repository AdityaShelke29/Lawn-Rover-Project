import serial
from pyubx2 import UBXReader

stream = serial.Serial("COM3", 38400, timeout=3)
ubr = UBXReader(stream)

while True:
    (raw_data, parsed_data) = ubr.read()
    print("\n")
    print(raw_data)
    print("\n")
    print(parsed_data.lon)