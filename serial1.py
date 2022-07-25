import time
import re
import serial
import RPi.GPIO as GPIO
import syslog
from datetime import datetime
import datetime
import paho.mqtt.client as mqttClient
import json
from datetime import date
 
ser_nm="923842098394"
topic="/iotlocks/v1/{}/event".format(ser_nm)

def on_connect(client, userdata, flags, rc):
 
    if rc == 0:
 
        print("Connected to broker")
 
        global Connected                #Use global variable
        Connected = True                #Signal connection 
 
    else:
 
        print("Connection failed")
 
Connected = False   #global variable for the state of the connection

broker_address= ""
port = 1883
user = ""
password = ""
 
client = mqttClient.Client("Publisher")               #create new instance
client.username_pw_set(user, password=password)    #set username and password
client.on_connect= on_connect                      #attach function to callback
client.connect(broker_address, port=port)          #connect to broker
 
client.loop_start()        #start the loop
 
while Connected != True:    #Wait for connection
    time.sleep(0.1)

shot=2
GPIO.setwarnings(False)
ser = serial.Serial(
    port='/dev/ttyS91',
    baudrate = 9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)
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
        opening(pas,pas)
    else:
        print("nie zgadza sie")
        syslog.syslog(syslog.LOG_WARNING,"SCANNED CODE DOES NOT MATCH MAGIC FILE")
        client.publish(topic,(str(datetime.datetime.now())+";"+None+";"+"0"+";"+pas))
        #client.publish("dev/pub",(str(datetime.datetime.now())+": SCANNED CODE DOES NOT MATCH MAGIC FILE"))
def opening(GUID,code):
    GPIO.output(shot, False)
    print("lock opened")
    syslog.syslog(syslog.LOG_INFO,"LOCK OPENED")
    client.publish(topic,(str(datetime.datetime.now())+";"+GUID+";"+"1"+";"+code))
    print((str(datetime.datetime.now())+";"+GUID+";"+"1"+code))
    time.sleep(10)
    GPIO.output(shot,True)
    syslog.syslog(syslog.LOG_INFO,"LOCK CLOSED")
    #client.publish("dev/pub",(str(datetime.datetime.now())+": LOCK CLOSED"))
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
    if code[:3]=="OPEN":
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
                        opening(GUID,code)
                        return True
                else:
                    client.publish(topic,(str(datetime.datetime.now()))+";"+ GUID +";"+"0"+";"+code)
                    return False
            else:
                client.publish(topic,(str(datetime.datetime.now()))+";"+ GUID +";"+"0"+";"+code)
                return False
        else:
            client.publish(topic,(str(datetime.datetime.now()))+";"+ GUID +";"+"0"+";"+code)
            return False
    else:
        return False
    





def opening_key():
    GPIO.output(shot, False)
    print("lock opened")
    syslog.syslog(syslog.LOG_INFO,"LOCK OPENED")
    client.publish("dev/pub",(str(datetime.datetime.now())+": LOCK.OPENED"))
    time.sleep(15)
    GPIO.output(shot,True)
    syslog.syslog(syslog.LOG_INFO,"LOCK CLOSED")
    client.publish("dev/pub",(str(datetime.datetime.now())+": LOCK CLOSED"))
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
            #client.publish("dev/pub",(str(datetime.datetime.now())+": SCANNED CODE: "+str(pas)))
            if isValidGUID(pas)==True:
                comparing(pas)  
            elif start(pas):
                #client.publish("dev/pub",(str(datetime.datetime.now())+": SCANNED CODE IS A VALID VIRTUAL KEY"))
                syslog.syslog(syslog.LOG_INFO,"SCANNED CODE IS A VALID VIRTUAL KEY")
            else:
                syslog.syslog(syslog.LOG_INFO,"SCANNED CODE DOES NOT MATCH ANYTHNG")
                client.publish(topic,(str(datetime.datetime.now()))+";"+" "+";"+"0"+";"+pas)
                #client.publish("dev/pub",(str(datetime.datetime.now())+": SCANNED CODE DOES NOT MATCH ANYTHING"))
             
except :
    if(GPIO.input(shot)==0):
                GPIO.output(shot,True)
    ser.close()
    syslog.syslog(syslog.LOG_WARNING,"SCRIPT TERMINATED")
    client.disconnect()
    client.loop_stop()
    ser.close()
GPIO.cleanup()    
    
    
	
        
	
	
	
	


