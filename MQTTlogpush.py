from encodings.utf_8 import decode
import time
#import serial
import os
import paho.mqtt.client as mqttClient
import time
import re
#import syslog
import mysql.connector

mydb=mysql.connector.connect(
    host="",
    user="",
    password="",
    database=""
)
print(mydb)


cursor=mydb.cursor()
  
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
    #ser.write(message.payload+ b'w')
    list=var.split(';')
    time=list[0]
    GUID=list[1]
    status=list[2]
    qr=list[3]
    sql="INSERT INTO events (GUID, scan_time, status,qr_code) values (%s, %s, %s,%s)"
    val=(var)
    cursor.execute(sql,(GUID,time,status,qr,))
    mydb.commit()
    #syslog.syslog(syslog.LOG_INFO,"CODE FROM MQTT")
  
Connected = False   #global variable for the state of the connection
  
broker_address= ""  #Broker address
port = 1883                         #Broker port
user = ""                    #Connection username
password = ""            #Connection password
  
client = mqttClient.Client("DB")               #create new instance
client.username_pw_set(user, password=password)    #set username and password
client.on_connect= on_connect                      #attach function to callback
client.on_message= on_message                      #attach function to callback
  
client.connect(broker_address, port=port)          #connect to broker

client.loop_start()        #start the loop
  
while Connected != True:    #Wait for connection
    time.sleep(0.1)
  
client.subscribe("/iotlocks/v1/+/event")
  
try:
    while True:
        time.sleep(1)
  
except KeyboardInterrupt:
    print ("exiting")
    client.disconnect()
    client.loop_stop()
