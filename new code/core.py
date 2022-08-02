import time
import re
import serial
import syslog
from datetime import datetime
import datetime
import paho.mqtt.client as mqttClient
import json
from datetime import date
import pin 

from pin import *
import hashlib

ser = serial.Serial(
    port='/dev/ttyS91',
    baudrate = 9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)
fb=open("/etc/point")
temp=fb.read()
temp=temp[:-1]
if temp=="test":
    
    from pythonlogtest import *

elif temp=="dev":
    import pythonlogdev
    from pythonlogdev import pub
    from pythonlogdev import on_connect
    from pythonlogdev import client_end
ser_nm="9238420983"
topic="/iotlocks/v1/{}/event".format(ser_nm)
shot=14
fel()
teamid="fbdn7y4"
def time_in_range(start, end, current):
     if start <= end:
        return start <= current <= end
     else:
        return start <= current or current <= end
def regg(text):
    regex="[A-Z0-9]{10}"
   
    if(re.search(regex, text)):
        return True
    else:
        return False

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
        pub(topic,(str(pas+">"+ser_nm+">"+"Opened using magic code"+">"+str(datetime.datetime.now())+">"+"1"+">"+pas)))
        opening(pas,pas)
    else:
        print("nie zgadza sie")
        syslog.syslog(syslog.LOG_WARNING,"SCANNED CODE DOES NOT MATCH MAGIC FILE")


def opening(GUID,code):
    up(shot)
    print("lock opened")
    syslog.syslog(syslog.LOG_INFO,"LOCK OPENED")
    time.sleep(10)
    down(shot)
    syslog.syslog(syslog.LOG_INFO,"LOCK CLOSED")
    print("Lock closed")

def time_in_range(start, end, current):
     if start <= end:
        return start <= current <= end
     else:
        return start <= current or current <= end

def check_num(list):
    pom=0
    if len(list)>1:
        for x in list:
            if x==ser_nm:
                pom=1
                return True
    else:
        if list[0]==ser_nm:
            pom=1
            return True
            
    if pom==0:
            return False

def validate_time(datestr,current,list):
    print(datestr)
    print(int(datestr[11]+datestr[12]),int(datestr[14]+datestr[15]),0)
    ctime=datetime.time(int(datestr[11]+datestr[12]),int(datestr[14]+datestr[15]),0)
    if(current.minute==00):
        print("00")
        start = datetime.time(current.hour-1, 59, 0)
        end = datetime.time(current.hour, current.minute+1, 59)
        if (time_in_range(start, end, ctime)):
            if check_num(list):
                return True
        else:
            return False
           
    elif(current.minute==59):
        start = datetime.time(current.hour, current.minute-1, 0)
        end = datetime.time(current.hour+1, 00, 59)
        if (time_in_range(start, end, ctime)):
            if check_num(list):
                return True
        else:
            return False
            
    else:
        start = datetime.time(current.hour, current.minute-1, 0)
        end = datetime.time(current.hour, current.minute+1, 59)
        print(start, end)
        if (time_in_range(start, end, ctime)):
            if check_num(list):
                return True
        else:
            return False
def deserialize(code):
    list=code.split(";")
    if len(list)==4:
        sublist=list[0].split(":")
        command=sublist[0]
        GUID=sublist[2]
        datestr=str(list[1])[3:]
        gates=list[2].split(":")
        gateslist=gates[1].split(",")
        print(list)
        print("command ", command)
        print(GUID)
        print(datestr)
        print(gateslist)
        return command, GUID, datestr, gateslist
    elif len(list)==1:
        list=code.split(":")
        command=list[0]
        GUID=list[1]
        datestr=0
        gateslist=0
        return command, GUID, datestr, gateslist
        



def start(code):
    command, GUID, datestr,gateslist= deserialize(code)
    if command=="OPEN":
        current = datetime.datetime.now().time()
        today=date.today()
        yr=datestr[:10]
        if isValidGUID(GUID):
            print(isValidGUID(GUID))
            if yr==str(today):
                if validate_time(datestr,current,gateslist):
                        pub(topic,(str(GUID+">"+ser_nm+">"+"Correct code"+">"+str(datetime.datetime.now())+">"+"1"+">"+code)))
                        opening(GUID,code)
                        return True
                else:
                    pub(topic,(str(GUID+">"+ser_nm+">"+"Code expired"+">"+str(datetime.datetime.now())+">"+"0"+">"+code)))
                    return False
            else:
                pub(topic,(str(GUID+">"+ser_nm+">"+"Code expired"+">"+str(datetime.datetime.now())+">"+"0"+">"+code)))
                return False
        else:
            pub(topic,(str(GUID+">"+ser_nm+">"+"Kod nie zawiera poprawnego GUID"+">"+str(datetime.datetime.now())+">"+"0"+">"+code)))
            return False
    elif command=="WIFI":
        print("placeholder WIFI")
        return True
    elif command=="MAGIC":
        if isValidGUID(GUID):
            comparing(GUID)
            return True
        else:
            return False
        
    else:
        return False


def hash(code):
    code=bytes(code, 'utf-8')
    code=hashlib.sha256(code)
    code=code.hexdigest()
    return code




def opening_key():
    up()
    print("lock opened")
    syslog.syslog(syslog.LOG_INFO,"LOCK OPENED")
    time.sleep(15)
    down()
    syslog.syslog(syslog.LOG_INFO,"LOCK CLOSED")
    print("Lock closed")
try:
    while 1:
        ser.flushInput()
        sett(shot)
        if(chinp(shot)==0):
            down(shot)
        inp=ser.readline()
        pas=inp.decode("utf-8")
        pas=pas[0:-1]
        if pas!="":
            print(pas)
            syslog.syslog(syslog.LOG_INFO,"Scanned code "+pas)
            #client.publish("dev>pub",(str(datetime.datetime.now())+": SCANNED CODE: "+str(pas)))
            if start(pas):
                
                syslog.syslog(syslog.LOG_INFO,"SCANNED CODE IS A VALID VIRTUAL KEY")
            elif pas[:4]!="OPEN":
                syslog.syslog(syslog.LOG_INFO,"SCANNED CODE DOES NOT MATCH ANYTHNG")
                pub(topic,(str(" "+">"+ser_nm+">"+"Code does not match anything"+">"+str(datetime.datetime.now())+">"+"0"+">"+pas)))
                print("nie pasuje")
             
except :
    if chinp(shot)==0:
                down(shot)
    ser.close()
    syslog.syslog(syslog.LOG_WARNING,"SCRIPT TERMINATED")
    client_end(client)
    ser.close()
cleanup()   
    
    
	
        
	
	
	
	


