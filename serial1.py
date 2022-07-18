import time
import re
import serial
import RPi.GPIO as GPIO
import syslog
from datetime import datetime
from datetime import date
import datetime as dt  

shot=2
GPIO.setwarnings(False)
ser = serial.Serial(
    port='/dev/pts/2',
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
        syslog.syslog(syslog.LOG_WARNING,"SCANNED MATCHING MAGIC CODE")
        opening()
    else:
        print("nie zgadza sie")
        syslog.syslog(syslog.LOG_WARNING,"SCANNED CODE DOES NOT MATCH MAGIC FILE")
def opening():
    GPIO.output(shot, False)
    print("lock opened")
    #print(GPIO.input(shot))
    syslog.syslog(syslog.LOG_INFO,"LOCK OPENED")
    time.sleep(30)
    GPIO.output(shot,True)
    syslog.syslog(syslog.LOG_INFO,"LOCK CLOSED")
    print("Lock closed")

def isNowInTimePeriod(startTime, endTime, nowTime): 
    if startTime < endTime: 
        return nowTime >= startTime and nowTime <= endTime 
    else: 
        return nowTime >= startTime or nowTime <= endTime 

def validate(code):
    if len(code)==30:
        e=datetime.now()
        if datetime.strptime(code[2:10], '%y-%m-%d').date()==date.today():
            if isNowInTimePeriod (dt.time(e.hour,e.minute-1), dt.time(e.hour,e.minute+1), dt.time(int(code[11]+code[12]),int(code[14]+code[15]))):
                print("Correct virtual key")
                opening_key()
                return True
        else:
            return False
    else: 
        return False
def opening_key():
    GPIO.output(shot, False)
    print("lock opened")
    syslog.syslog(syslog.LOG_INFO,"LOCK OPENED")
    time.sleep(15)
    GPIO.output(shot,True)
    syslog.syslog(syslog.LOG_INFO,"LOCK CLOSED")
    print("Lock closed")

try:
    while 1:
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(shot,GPIO.OUT)
        if(GPIO.input(shot)==0):
            GPIO.output(shot,True)
        inp=ser.readline()
        pas=inp.decode("utf-8")
        pas=pas[0:-1]
        if pas!="":
            print(pas)
            syslog.syslog(syslog.LOG_INFO,"Scanned code "+pas)
            if isValidGUID(pas)==True:
                comparing(pas)
            elif validate(pas):
                syslog.syslog(syslog.LOG_INFO,"SCANNED CODE IS A VALID VIRTUAL KEY")
            else:
                syslog.syslog(syslog.LOG_INFO,"SCANNED CODE DOES NOT MATCH ANYTHNG")
            
                
except :
    if(GPIO.input(shot)==0):
                GPIO.output(shot,True)
                
    syslog.syslog(syslog.LOG_WARNING,"SCRIPT TERMINATED")
GPIO.cleanup()    
    
    
	
        
	
	
	
	


