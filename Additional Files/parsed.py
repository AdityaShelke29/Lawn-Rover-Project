# This additional function allows for data from the ZED - F9P to be procesed by the serial
# and the pyubx2 libraries, and printed as raw data and parsed data in the python window.
# Note that COM3 is the port for Windows, while /dev/ttyACM0 is the port for the Raspberry Pi.

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