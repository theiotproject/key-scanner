from encodings.utf_8 import decode
import time
import os
import paho.mqtt.client as mqttClient
import time
import re
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
  
        global Connected                
        Connected = True                
  
    else:
  
        print("Connection failed")
  
def on_message(client, userdata, message):
    var=message.payload
    var=var.decode()
    print (var)
    list=var.split('>')
    GUID=list[0]
    serial=list[1]
    message=list[2]
    time=list[3]
    qr=list[5]
    status=list[4]
    sql="INSERT INTO events (GUID, serial_number,message,scan_time,qr_code,status) values (%s, %s, %s,%s,%s,%s)"
    val=(var)
    cursor.execute(sql,(GUID,serial,message,time,qr,status,))
    mydb.commit()
  
Connected = False   
  
broker_address= "mysql39.mydevil.net"  
port = 1883                         
user = "nikodem"                    
password = "nikodem"            
  
client = mqttClient.Client("DB")               
client.username_pw_set(user, password=password)    
client.on_connect= on_connect                      
client.on_message= on_message                      
  
client.connect(broker_address, port=port)         

client.loop_start()        
  
while Connected != True:    
    time.sleep(0.1)
  
client.subscribe("/iotlocks/v1/+/event")
  
try:
    while True:
        time.sleep(1)
  
except KeyboardInterrupt:
    print ("exiting")
    client.disconnect()
    client.loop_stop()
    os.system("python MQTTlogPUSH.py")
