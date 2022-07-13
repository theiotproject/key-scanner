import time
import re
import serial
import RPi.GPIO as GPIO
import syslog
import requests



shot=2

ser = serial.Serial(
    port='/dev/ttyACM0',
    baudrate = 9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)

def isValidGUID(str):
    regex = "^[{]?[0-9a-fA-F]{8}" + "-([0-9a-fA-F]{4}-)" + "{3}[0-9a-fA-F]{12}[}]?$"
    p = re.compile(regex)
    if (str == None):
        return False
    if(re.search(p, str)):
        return True
    else:
        return False
def comparing(pas):
    f=open("/etc/magic.guid","r")
    var=f.read()
    var=var[:-1]
    if str(pas)==str(var):
        opening()
        syslog.syslog(syslog.LOG_WARNING,"SCANNED MATCHING MAGIC CODE")
    else:
        print("nie zgadza sie")
        syslog.syslog(syslog.LOG_WARNING,"SCANNED CODE DOES NOT MATCH MAGIC FILE")
def opening():
    GPIO.output(shot, False)
    print("lock opened")
    syslog.syslog(syslog.LOG_INFO,"LOCK OPENED")
    time.sleep(30)
    GPIO.output(shot,True)
    syslog.syslog(syslog.LOG_INFO,"LOCK CLOSED")
    print("Lock closed")
    GPIO.cleanup()
while 1:
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(shot,GPIO.OUT)
    inp=ser.readline()
    pas=inp.decode("utf-8")
    pas=pas[0:-1]
    if pas!="":
        #print(pas)
        syslog.syslog(syslog.LOG_INFO,"Scanned code "+pas)
        if isValidGUID(pas)==True:
            comparing(pas)
        else:
            print("kod nie zawiera GUID")
            syslog.syslog(syslog.LOG_WARNING,"SCANNED CODE IS NOT GUID")
GPIO.cleanup()    
    
    
	
        
	
	
	
	


