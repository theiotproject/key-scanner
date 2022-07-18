import time
import serial
import os

ser = serial.Serial(
        port='/dev/pts/3', 
        baudrate = 9600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=1
)
var=input()+"b"
ser.write(bytes(var,"utf-8"))
time.sleep(1)