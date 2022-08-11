import sys
import time
import os
import re
import serial
import syslog
from datetime import datetime
import datetime
import paho.mqtt.client as mqttClient
import json
from datetime import date
import pin 
from firstconf import *

from pin import *
import hashlib
def conff():
    try:
        f=open("/etc/KeyScannerconf/magic.guid","r")
        magic=f.read()
        f.close()
        f=open("/etc/KeyScannerconf/teamcode","r")
        team=f.read()
        f.close()
        f=open("/etc/KeyScannerconf/serialnm","r")
        serialnm=f.read()
        
        f.close()
        return team,magic,serialnm
    except:
        return "","",""
    
ser = serial.Serial(
    port='/dev/ttyS91',
    baudrate = 9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)
fb=open("/etc/KeyScannerconf/point")
temp=fb.read()
temp=temp[:-1]
if temp=="test":
    
    from pythonLogControl import *

elif temp=="dev":
    import pythonLogControl
    from pythonLogControl import pub
    from pythonLogControl import on_connect
    from pythonLogControl import client_end
#ser_nm="9238420983"

teamcode, magic,ser_nm = conff() 
syslog.syslog(syslog.LOG_INFO,f"{teamcode},{ser_nm},{magic}")
topic="/iotlocks/v1/{}/event".format(ser_nm)
shot=14
fel()
def regg(text):
    regex="[A-Z0-9]{10}"
   
    if(re.search(regex, text)):
        return True
    else:
        return False
#/etc/magic.guid
#/etc/blacklist
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
    syslog.syslog(syslog.LOG_INFO,(f"{magic}+{pas}"))
    if str(pas)==str(magic):
        now=str(datetime.datetime.now())
        syslog.syslog(syslog.LOG_INFO,"SCANNED MATCHING MAGIC CODE")
        pub(topic,(str(f"{pas}>{ser_nm}>Opened using magic code>{now}>1>{code}")))
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
def blacklist(GUID):
    syslog.syslog(syslog.LOG_INFO,"17")
    f=open("/etc/KeyScannerconf/blacklist","r")
    for index, line in enumerate(f):
                if GUID==line:
                    syslog.syslog(syslog.LOG_INFO,"18")
                    return False
    syslog.syslog(syslog.LOG_INFO,"20")
    return True

def com(start,end,now):
    try:
        start=datetime.datetime.strptime(str(start), "%Y-%m-%d %H:%M:%S")
        end=datetime.datetime.strptime(str(end), "%Y-%m-%d %H:%M:%S")
    except:
        return False
    return start <= now <= end

def deserialize(code):
    syslog.syslog(syslog.LOG_INFO,"7")
    try:
        try:
            list2=code.split(";;")
        except:
            syslog.syslog(syslog.LOG_INFO,"no nie poszło")
        print(list2)
        #list2[0]+=";;"
        code=list2[0]
        list=code.split(";")
        print (list)
        code1=code[:-1]
        list1=code1.split(":")
        syslog.syslog(syslog.LOG_INFO,"8")
        syslog.syslog(syslog.LOG_INFO,f"len,{len(list)},{len(list1)}")
        if len(list)==4:
            syslog.syslog(syslog.LOG_INFO,"11")
            hashlist=""
            sign=""
            signature=hash(code+";;"+teamcode)
            if list2[1]!="":
                hashlist=list2[1].split(":")
                sign=hashlist[1]
                sign=sign[:-1]
            else:
                sign=""
            sublist=list[0].split(":")
            syslog.syslog(syslog.LOG_INFO,"12")
            command=sublist[0]
            GUID=sublist[2]
            datestart=str(list[1])[3:]
            dateend=str(list[2])[3:]
            gates=list[3].split(":")
            syslog.syslog(syslog.LOG_INFO,"14")
            #gates[1]+=",salt"
            print("gates: ",gates)
            print("przed splitem")
            gateslist=gates[1].split(",")
            print("po splicie",gateslist)
        
            return command, GUID, datestart, gateslist, dateend,signature,sign
        elif len(list1)==2 and len(list)!=3:
            syslog.syslog(syslog.LOG_INFO,"13")
            command=list1[0]
            GUID=list1[1]
            datestart=0
            dateend=0
            gates=0
            gateslist=0
            return command, GUID, datestart, gateslist, dateend, "",""
        elif len(list)==3:
            sl=list[0].split(":")
            syslog.syslog(syslog.LOG_INFO,"hehe")
            command=sl[0]
            syslog.syslog(syslog.LOG_INFO,f"{command}")
            if command=="CONF":
                syslog.syslog(syslog.LOG_INFO,"config")
                f=open("/etc/KeyScannerconf/magic.guid","w")
                f.write(sl[1])
                f.close()
                os.system("chmod 0444 /etc/KeyScannerconf/magic.guid",)
                f=open("/etc/KeyScannerconf/teamcode","w")
                f.write(list[1])
                f.close()
                os.system("chmod 0444 /etc/KeyScannerconf/teamcode")
                f=open("/etc/KeyScannerconf/serialnm","w")
                f.write(list[2])
                f.close()
                os.system("chmod 0444 /etc/KeyScannerconf/serialnm")
                return "none",0,0,0,0,0,0
            
        else:
            
            return "none",0,0,0,0,0,0
        
    except:
        print("exception")
        return "none",0,0,0,0,0,0
def start(code):
    command, GUID, datestart,gateslist,dateend, signature,sign = deserialize(code)
    syslog.syslog(syslog.LOG_INFO,"15")
    #syslog.syslog(syslog.LOG_INFO,gateslist)
    #signature=str(signature)
    #syslog.syslog(syslog.LOG_INFO,("signr: ", signature)) 
    today=datetime.datetime.now()
    syslog.syslog(syslog.LOG_INFO,"16")
    yrs=datestart
    syslog.syslog(syslog.LOG_INFO,"17")
    yrend=dateend
    syslog.syslog(syslog.LOG_INFO,"18")
    now=str(datetime.datetime.now())
    syslog.syslog(syslog.LOG_INFO,"19")
    if blacklist(GUID):
        syslog.syslog(syslog.LOG_INFO,"2")
        if str(sign) == signature:
            syslog.syslog(syslog.LOG_INFO,"3")
            if command=="OPEN":
                syslog.syslog(syslog.LOG_INFO,"4")
                if isValidGUID(GUID):
                    syslog.syslog(syslog.LOG_INFO,"5")
                    if com(yrs,yrend,today):
                        syslog.syslog(syslog.LOG_INFO,"6")
                        if check_num(gateslist):
                                syslog.syslog(syslog.LOG_INFO,"9")
                                pub(topic,(str(f"{GUID}>{ser_nm}>Correct code>{now}>1>"+code)))
                                opening(GUID,code)
                                return True
                        else:
                            pub(topic,(str(f"{GUID}>{ser_nm}>Code doesnt contain correct gate>{now}>0>{code}")))
                    else:
                        pub(topic,(str(f"{GUID}>{ser_nm}>Code expired>{now}>0>{code}")))
                        return False
                else:
                    pub(topic,(str(f"{GUID}>{ser_nm}>Kod nie zawiera poprawnego GUID>{now}>0>{code}")))
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
                    pub(topic,(str(f"{GUID}>{ser_nm}>Kod nie zawiera poprawnego podpisu>{now}>0>{code}")))
                    return False
    else:
        pub(topic,(str(f"{GUID}>{ser_nm}>Kod znajduje się na czarnej liście>{now}>0>{code}")))
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
            syslog.syslog(syslog.LOG_INFO,"1")
            syslog.syslog(syslog.LOG_INFO,pas)
            if start(pas):
                syslog.syslog(syslog.LOG_INFO,"SCANNED CODE IS A VALID VIRTUAL KEY")
            elif pas[:4]!="OPEN":
                syslog.syslog(syslog.LOG_INFO,"SCANNED CODE DOES NOT MATCH ANYTHNG")
                pub(topic,(str(" "+">"+ser_nm+">Code does not match anything>"+str(datetime.datetime.now())+">0>"+pas)))

        
             
except :
    if chinp(shot)==0:
                down(shot)
    ser.close()
    os.system("pkill python3")
    syslog.syslog(syslog.LOG_WARNING,"SCRIPT TERMINATED")
    client_end(client)
    ser.close()
    cleanup()   