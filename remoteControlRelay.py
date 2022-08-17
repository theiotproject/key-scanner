from encodings.utf_8 import decode
import time
import serial
import os
import paho.mqtt.client as mqttClient
import time
import re
import syslog
import platform
import subprocess
import random



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

teamcode,magic,serial_nm=conff()

blacklist="/etc/KeyScannerconf/blacklist"
def append_new_line(file_name, text_to_append):
    """Append given text as a new line at the end of file"""
    # Open the file in append & read mode ('a+')
    with open(file_name, "a+") as file_object:
        # Move read cursor to the start of file.
        file_object.seek(0)
        # If file is not empty then append '\n'
        data = file_object.read(100)
        if len(data) > 0:
            file_object.write("\n")
        # Append text at the end of file
        file_object.write(text_to_append)
        file_object.close()
        


def on_message(client, userdata, message):
    ser.write(message.payload)
    syslog.syslog(syslog.LOG_INFO,"CODE FROM MQTT")

def on_message1(client, userdata, message):
    f=open(blacklist,"w")
    f.close()
    var=message.payload
    var=var.decode()
    try:
        list=var.split(";")
        for x in list:
            append_new_line(blacklist,x)
    except:
            append_new_line(blacklist,var)

    
def on_connect(client, userdata, flags, rc):
  
    if rc == 0:
  
        print("Connected to broker")
  
        global Connected                #Use global variable
        Connected = True                #Signal connection 
  
    else:
  
        print("Connection failed")
Connected = False   #global variable for the state of the connection
port = 1883                         #Broker port
user = "nikodem"                    #Connection username
password = "nikodem"     
broker_add="s39.mydevil.net"       #Connection password

client1 = mqttClient.Client(f'blacklist{serial_nm}')  
client1.username_pw_set(user, password=password)    
client1.on_connect=on_connect
client1.on_message=on_message1
client = mqttClient.Client(f'open{serial_nm}')               #create new instance
client.username_pw_set(user, password=password)    #set username and password
client.on_connect= on_connect                      #attach function to callback
client.on_message= on_message  
ser = serial.Serial(
        port='/dev/ttyS90', 
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

def myping(host):
    parameter = '-n' if platform.system().lower()=='windows' else '-c'

    command = ['ping', parameter, '1', host]
    response = subprocess.call(command)

    if response == 0:
        return True
    else:
        return False
controll=0
try:
    while 1:
        if myping("s39.mydevil.net") and controll==0:
            try:
                client.connect(broker_add, port=port)   
                client1.connect(broker_add, port=port)       #connect to broker
                client.loop_start()       
                client1.loop_start() #start the loop
                while Connected != True:    #Wait for connection
                    time.sleep(0.1)
                client.subscribe(f"iotlock/v1/{teamcode}/control/{serial_nm}")
                syslog.syslog(syslog.LOG_INFO,f"subscribed to iotlock/v1/{teamcode}/control/{serial_nm}")
                client1.subscribe(f"iotlock/v1/{teamcode}/blacklist")
                syslog.syslog(syslog.LOG_INFO,f"subscribed to iotlock/v1/{teamcode}/blacklist")
                controll=1
            except:
                syslog.syslog(syslog.LOG_INFO,"No connection")
        elif myping("s39.mydevil.net")==False:
            client1.disconnect()
            client1.loop_stop()
            client.disconnect()
            client.loop_stop()
            controll=0
        time.sleep(10)

except:
    print ("exiting")
   
    ser.close()
    client.disconnect()
    client.loop_stop()