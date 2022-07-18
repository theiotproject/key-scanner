import time
import serial
import os
#import virtual.py

#os.system("socat -d -d pty,raw,echo=0 pty,raw,echo=0")
#time.sleep(5)
ser = serial.Serial(
        port='/dev/pts/3', #Replace ttyS0 with ttyAM0 for Pi1,Pi2,Pi0
        baudrate = 9600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=1
)
var=input()+"b"
ser.write(bytes(var,"utf-8"))