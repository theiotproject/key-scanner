#!/usr/bin/env python3
import RPi.GPIO as GPIO
import os
import time
import serial
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(26,GPIO.IN)
ser2 = serial.Serial(
                port='/dev/ttyACM0', 
                baudrate = 9600,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS,
                timeout=1
        )
pom=0
try:
        while 1:
                #print(GPIO.input(26))
                time.sleep(1)
                if pom==1:
                        os.system("./test")
                        ser2.write
                if GPIO.input(26)!=pom:
                        pom=(not pom)
except KeyboardInterrupt:
        ser2.flushOutput()
        ser2.flushInput()
        ser2.close()
