import time
import serial
import os

ser = serial.Serial(
        port='/dev/ttyS90',
        baudrate = 9600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=1
)
ser2 = serial.Serial(
        port='/dev/ttyACM0', 
        baudrate = 9600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=1
)
counter=0
try:
        while 1:
                x=ser2.readline()
                ser.write(x)
                time.sleep(1)
except :
        ser.close()
        ser2.close()

