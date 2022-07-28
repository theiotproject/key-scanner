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

#from pythonlog import pub

#GUID;serial_number;message;time;qr;status
ser = serial.Serial(
    port='/dev/ttyS91',
    baudrate = 9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=2
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
ser_nm="923842098394"
topic="/iotlocks/v1/{}/event".format(ser_nm)
shot=2
fel()

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
        #client.publish(topic,(str(datetime.datetime.now())+": SCANNED CODE MATCHING MAGIC FILE"))
        #pub(topic,(str(datetime.datetime.now())+": SCANNED CODE MATCHING MAGIC FILE"))
        pub(topic,(str(pas+"/"+ser_nm+"/"+"Opened using magic code"+"/"+str(datetime.datetime.now())+"/"+"1"+"/"+pas)))
        opening(pas,pas)
    else:
        print("nie zgadza sie")
        syslog.syslog(syslog.LOG_WARNING,"SCANNED CODE DOES NOT MATCH MAGIC FILE")
        #client.publish(topic,(str(datetime.datetime.now())+"/"+None+">"+"0"+">"+pas))
        #pub(topic,(str(datetime.datetime.now())+">"+None+">"+"0"+">"+pas))
        #client.publish("dev>pub",(str(datetime.datetime.now())+": SCANNED CODE DOES NOT MATCH MAGIC FILE"))
def opening(GUID,code):
    up(shot)
    print("lock opened")
    syslog.syslog(syslog.LOG_INFO,"LOCK OPENED")
    #client.publish(topic,(str(datetime.datetime.now())+"\"+GUID+"\"+"1"+"\"+code))
    #pub(topic,(str(datetime.datetime.now())+"\"+GUID+"\"+"1"+"\"+code))
    #print((str(datetime.datetime.now())+"\"+GUID+"\"+"1"+code))
    time.sleep(10)
    down(shot)
    syslog.syslog(syslog.LOG_INFO,"LOCK CLOSED")
    #client.publish("dev\pub",(str(datetime.datetime.now())+": LOCK CLOSED"))
    print("Lock closed")

#OPEN:ID:a716ea50-09b9-11ed-9743-07e33a4825a1;CA:2022-07-22 14:27:29;G:923842098394,309485394865;


print (list)
def time_in_range(start, end, current):
     if start <= end:
        return start <= current <= end
     else:
        return start <= current or current <= end

def check_num(list):
    for x in list:
        if x==ser_nm:
            return True
        else:
            return False

def validate_time(datestr,current,list):
   
    temp=list[2]

    list1=temp[2:].split(',')
    print(list1)
        
    #print(dateobj)
    print(datestr)
    print(int(datestr[11]+datestr[12]),int(datestr[14]+datestr[15]),0)
    ctime=datetime.time(int(datestr[11]+datestr[12]),int(datestr[14]+datestr[15]),0)
    if(current.minute==00):
        print("00")
        start = datetime.time(current.hour-1, 59, 0)
        end = datetime.time(current.hour, current.minute+1, 59)
        if (time_in_range(start, end, ctime)):
            if check_num(list1):
                return True
        else:
            return False
           
    elif(current.minute==59):
        start = datetime.time(current.hour, current.minute-1, 0)
        end = datetime.time(current.hour+1, 00, 59)
        if (time_in_range(start, end, ctime)):
            if check_num(list1):
                return True
        else:
            return False
            
    else:
        start = datetime.time(current.hour, current.minute-1, 0)
        end = datetime.time(current.hour, current.minute+1, 59)
        print(start, end)
        if (time_in_range(start, end, ctime)):
            if check_num(list1):
                return True
        else:
            return False
def start(code):
    if code[:4]=="OPEN":
        list=code[:-1].split(';')
        current = datetime.datetime.now().time()
        today=date.today()
        #list=code.split(';')
        sublist=list[0].split(':')
        print(sublist)
        datestr=list[1]
        datestr=datestr[3:]
        yr=datestr[:10]
        GUID=sublist[2]
        print(GUID)
        if isValidGUID(GUID):
            if yr==str(today):
                if validate_time(datestr,current,list):
                        guidl=list[0].split(':')
                        print(guidl)
                        pub(topic,(str(GUID+">"+ser_nm+">"+"Correct code"+">"+str(datetime.datetime.now())+">"+"1"+">"+code)))
                        opening(GUID,code)
                        return True
                else:
                    #client.publish(topic,(str(datetime.datetime.now()))+">"+ GUID +">"+"0"+">"+code)
                    #pub(topic,(str(datetime.datetime.now()))+">"+ GUID +">"+"0"+">"+code)
                    pub(topic,(str(GUID+">"+ser_nm+">"+"Code expired"+">"+str(datetime.datetime.now())+">"+"0"+">"+code)))
                    return False
            else:
                #client.publish(topic,(str(datetime.datetime.now()))+">"+ GUID +">"+"0"+">"+code)
                pub(topic,(str(GUID+">"+ser_nm+">"+"Code expired"+">"+str(datetime.datetime.now())+">"+"0"+">"+code)))
                return False
        else:
            #client.publish(topic,(str(datetime.datetime.now()))+">"+ GUID +">"+"0"+">"+code)
            pub(topic,(str(GUID+">"+ser_nm+">"+"Kod nie zawiera poprawnego GUID"+">"+str(datetime.datetime.now())+">"+"0"+">"+code)))
            return False
    else:
        print("nie ma open")
        return False
    
    





def opening_key():
    up()
    print("lock opened")
    syslog.syslog(syslog.LOG_INFO,"LOCK OPENED")
    #client.publish("dev>pub",(str(datetime.datetime.now())+": LOCK.OPENED"))
    time.sleep(15)
    down()
    syslog.syslog(syslog.LOG_INFO,"LOCK CLOSED")
    #client.publish("dev>pub",(str(datetime.datetime.now())+": LOCK CLOSED"))
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
            if isValidGUID(pas)==True:
                comparing(pas)  
            elif start(pas):
                #client.publish("dev>pub",(str(datetime.datetime.now())+": SCANNED CODE IS A VALID VIRTUAL KEY"))
                #pub(topic,(str(datetime.datetime.now())+": SCANNED CODE IS A VALID VIRTUAL KEY"))
                syslog.syslog(syslog.LOG_INFO,"SCANNED CODE IS A VALID VIRTUAL KEY")
            elif pas[:4]!="OPEN":
                syslog.syslog(syslog.LOG_INFO,"SCANNED CODE DOES NOT MATCH ANYTHNG")
                #client.publish(topic,(str(datetime.datetime.now()))+">"+" "+">"+"0"+">"+pas)
                #pub(topic,">"+(str(datetime.datetime.now()))+">"+" "+">"+"0"+">"+pas)
                pub(topic,(str(" "+">"+ser_nm+">"+"Code does not match anything"+">"+str(datetime.datetime.now())+">"+"0"+">"+pas)))
                #client.publish("dev>pub",(str(datetime.datetime.now())+": SCANNED CODE DOES NOT MATCH ANYTHING"))
                print("nie pasuje")
             
except :
    if chinp(shot)==0:
                down
    ser.close()
    syslog.syslog(syslog.LOG_WARNING,"SCRIPT TERMINATED")
    client_end(client)
    ser.close()
cleanup()   
    
    
	
        
	
	
	
	


