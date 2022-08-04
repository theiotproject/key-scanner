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

try:
        while 1:
                #print(GPIO.input(26))
                time.sleep(0.5)
                if GPIO.input(26)==1:
                        os.system("./test")
except:
        ser2.flushOutput()
        ser2.flushInput()
        ser2.close()
