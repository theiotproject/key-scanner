import time
import re
import serial
import RPi.GPIO as GPIO
import syslog
from datetime import datetime
import datetime
import paho.mqtt.client as mqttClient

 
def on_connect(client, userdata, flags, rc):
 
    if rc == 0:
 
        print("Connected to broker")
 
        global Connected                #Use global variable
        Connected = True                #Signal connection 
 
    else:
 
        print("Connection failed")
 
Connected = False   #global variable for the state of the connection
 
broker_address= "s39.mydevil.net"
port = 1883
user = "nikodem"
password = "nikodem"
 
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
    return start <= current <= end
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
        client.publish("dev/pub",(str(datetime.datetime.now())+": SCANNED CODE MATCHING MAGIC FILE"))
        opening()
    else:
        print("nie zgadza sie")
        syslog.syslog(syslog.LOG_WARNING,"SCANNED CODE DOES NOT MATCH MAGIC FILE")
        client.publish("dev/pub",(str(datetime.datetime.now())+": SCANNED CODE DOES NOT MATCH MAGIC FILE"))
def opening():
    GPIO.output(shot, False)
    print("lock opened")
    syslog.syslog(syslog.LOG_INFO,"LOCK OPENED")
    client.publish("dev/pub",(str(datetime.datetime.now())+": LOCK OPENED"))
    time.sleep(10)
    GPIO.output(shot,True)
    syslog.syslog(syslog.LOG_INFO,"LOCK CLOSED")
    client.publish("dev/pub",(str(datetime.datetime.now())+": LOCK CLOSED"))
    print("Lock closed")

def validate(code):
    if len(code)==30:
        if regg(code[-10:]):
            current = datetime.datetime.now().time()
            ctime=datetime.time(int(code[11]+code[12]),int(code[14]+code[15]),0)
            if(current.minute==00):
                print("00")
                start = datetime.time(current.hour-1, 59, 0)
                end = datetime.time(current.hour, current.minute+1, 59)
                if (time_in_range(start, end, ctime)):
                    print("00")
                    opening_key()
            elif(current.minute==59):
                start = datetime.time(current.hour, current.minute-1, 0)
                end = datetime.time(current.hour+1, 00, 59)
                if (time_in_range(start, end, ctime)):
                    print("59")
                    opening_key()
            else:
                start = datetime.time(current.hour, current.minute-1, 0)
                end = datetime.time(current.hour, current.minute+1, 59)
                print(start, end)
                if (time_in_range(start, end, ctime)):
                    print(current)
                    opening_key()
        else:
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
            client.publish("dev/pub",(str(datetime.datetime.now())+": SCANNED CODE: "+str(pas)))
            if isValidGUID(pas)==True:
                comparing(pas)
            elif validate(pas):
                client.publish("dev/pub",(str(datetime.datetime.now())+": SCANNED CODE IS A VALID VIRTUAL KEY"))
                syslog.syslog(syslog.LOG_INFO,"SCANNED CODE IS A VALID VIRTUAL KEY")
            else:
                syslog.syslog(syslog.LOG_INFO,"SCANNED CODE DOES NOT MATCH ANYTHNG")
                client.publish("dev/pub",(str(datetime.datetime.now())+": SCANNED CODE DOES NOT MATCH ANYTHING"))
             
except :
    if(GPIO.input(shot)==0):
                GPIO.output(shot,True)
                
    syslog.syslog(syslog.LOG_WARNING,"SCRIPT TERMINATED")
    client.disconnect()
    client.loop_stop()
GPIO.cleanup()    
    
    
	
        
	
	
	
	


