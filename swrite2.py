from encodings.utf_8 import decode
import time
import serial
import os
import paho.mqtt.client as mqttClient
import time
import re
import syslog

ser = serial.Serial(
        port='/dev/ttyS90', 
        baudrate = 9600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=1
)


  
def on_connect(client, userdata, flags, rc):
  
    if rc == 0:
  
        print("Connected to broker")
  
        global Connected                #Use global variable
        Connected = True                #Signal connection 
  
    else:
  
        print("Connection failed")
  
def on_message(client, userdata, message):
    var=message.payload
    var=var.decode()
    print (var)
    ser.write(message.payload+ b'w')
    syslog.syslog(syslog.LOG_INFO,"CODE FROM MQTT")
  
Connected = False   #global variable for the state of the connection
  
broker_address= "192.168.8.164"  #Broker address
port = 1883                         #Broker port
user = "nikodem"                    #Connection username
password = "nikodem"            #Connection password
  
client = mqttClient.Client("Python")               #create new instance
client.username_pw_set(user, password=password)    #set username and password
client.on_connect= on_connect                      #attach function to callback
client.on_message= on_message                      #attach function to callback
  
client.connect(broker_address, port=port)          #connect to broker
  
client.loop_start()        #start the loop
  
while Connected != True:    #Wait for connection
    time.sleep(0.1)
  
client.subscribe("dev/test")
  
try:
    while True:
        time.sleep(1)
  
except KeyboardInterrupt:
    print ("exiting")
    ser.close()
    client.disconnect()
    client.loop_stop()