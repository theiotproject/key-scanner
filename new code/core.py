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
def comparing(pas,code):
    f=open("/etc/magic.guid","r")
    var=f.read()
    var=var[:-1]
    if str(pas)==str(var):
        syslog.syslog(syslog.LOG_INFO,"SCANNED MATCHING MAGIC CODE")
        pub(topic,(str(pas+">"+ser_nm+">"+"Opened using magic code"+">"+str(datetime.datetime.now())+">"+"1"+">"+code)))
        opening(pas,code)
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
def com(start,end,now):
    try:
        start=datetime.datetime.strptime(str(start), "%Y-%m-%d %H:%M:%S")
        end=datetime.datetime.strptime(str(end), "%Y-%m-%d %H:%M:%S")
    except:
        return False
    return start <= now <= end
def deserialize(code):
    try:
        list2=code.split(";;")
        print(list2)
        #list2[0]+=";;"
        code=list2[0]
        list1=code.split(":")
        list=code.split(";")
        print (list)
        
        if 1:
            
            hashlist=list2[1].split(":")
            sign=hashlist[1]
            sign=sign[:-1]
            print(code+";;J384CP1S")
            signature=hash(code+";;J384CP1S")
            print("sign: ",sign)
            sublist=list[0].split(":")
            command=sublist[0]
            GUID=sublist[2]
            datestart=str(list[1])[3:]
            dateend=str(list[2])[3:]
            gates=list[3].split(":")
            #gates[1]+=",salt"
            print("gates: ",gates)
            gateslist=gates[1].split(",")
            return command, GUID, datestart, gateslist, dateend,signature,sign
        elif len(list1)==2:
            command=list1[0]
            GUID=list1[1]
            datestart=0
            dateend=0
            gates=0
            gateslist=0
            return command, GUID, datestart, gateslist, dateend, 0,0
        else:
            
            return "none",0,0,0,0,0,0
    except:
        print("exception")
        return "none",0,0,0,0,0,0
def start(code):
    command, GUID, datestart,gateslist,dateend, signature,sign = deserialize(code)
    
    print("signr: ", signature)
    if str(sign) == signature:
        if command=="OPEN":
            today=datetime.datetime.now()
            yrs=datestart
            yrend=dateend
            if isValidGUID(GUID):
                if com(yrs,yrend,today):
                    if check_num(gateslist):
                            pub(topic,(str(GUID+">"+ser_nm+">"+"Correct code"+">"+str(datetime.datetime.now())+">"+"1"+">"+code)))
                            opening(GUID,code)
                            return True
                    else:
                        pub(topic,(str(GUID+">"+ser_nm+">"+"Code doesnt contain correct gate"+">"+str(datetime.datetime.now())+">"+"0"+">"+code)))
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
                comparing(GUID,code)
                return True
            else:
                return False

        elif command=="none":
            return False
    else:
                pub(topic,(str(GUID+">"+ser_nm+">"+"Kod nie zawiera poprawnego podpisu"+">"+str(datetime.datetime.now())+">"+"0"+">"+code)))
                return False
def hash(code):
    code=bytes(code, 'utf-8')
    code=hashlib.sha256(code)
    #code=code.hexdigest()
    return code.hexdigest()
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
            pas+=";"
            print(pas)
            
            syslog.syslog(syslog.LOG_INFO,"Scanned code "+pas)
            if start(pas):
                syslog.syslog(syslog.LOG_INFO,"SCANNED CODE IS A VALID VIRTUAL KEY")
            elif pas[:4]!="OPEN":
                syslog.syslog(syslog.LOG_INFO,"SCANNED CODE DOES NOT MATCH ANYTHNG")
                pub(topic,(str(" "+">"+ser_nm+">"+"Code does not match anything"+">"+str(datetime.datetime.now())+">"+"0"+">"+pas)))

        
             
except :
    if chinp(shot)==0:
                down(shot)
    ser.close()
    syslog.syslog(syslog.LOG_WARNING,"SCRIPT TERMINATED")
    client_end(client)
    ser.close()
cleanup()   
    
    
	
        
	
	
	
	


