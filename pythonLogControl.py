import paho.mqtt.client as mqttClient
import time
import platform
import subprocess
import os


offline="/etc/KeyScannerconf/offlinelogs"
def myping(host):
    parameter = '-n' if platform.system().lower()=='windows' else '-c'

    command = ['ping', parameter, '1', host]
    response = subprocess.call(command)

    if response == 0:
        return True
    else:
        return False

def pub(topic,message):
    x=myping("s39.mydevil.net")
    f=open(offline,"r")
    rea=f.readline()
    print(rea)
    if x and rea=="":
        client.connect(broker_address, port=port) 
        client.loop_start()
        print("publishing")
        client.publish(topic,message)
        #client.publish(topic,message)
        f.close()
        client_end(client)
    elif x and rea!="":
        f.close()
        f=open(offline,"r")
        print("updating")
        client.connect(broker_address, port=port) 
        client.loop_start()        #start the loop

        while Connected != True:    #Wait for connection
            time.sleep(0.1)
        client.publish(topic,message)
        try:
            for index, line in enumerate(f):
                list=line.split(']')
                client.publish(list[0],list[1])
        except:
            print("problem")        
        f.close()
        ftd=open(offline,"w")
        ftd.close()
        client_end(client)
        
    else:
        f.close()
        #f=open("/etc/offlinelogs","a+")
        #f.write(topic+"]"+message)
        var=topic+"]"+message
        append_new_line(offline,var)
        print("dopisek")
        

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
    
def on_connect(client, userdata, flags, rc):

    if rc == 0:

        print("Connected to broker")

        global Connected                #Use global variable
        Connected = True                #Signal connection 

    else:

        print("Connection failed")
def client_end(client):
    client.disconnect()
    client.loop_stop()
try:
    Connected = False   #global variable for the state of the connection
    broker_address= "s39.mydevil.net"
    port = 1883
    user = "nikodem"
    password = "nikodem"


    client = mqttClient.Client("Publisher")               #create new instance
    client.username_pw_set(user, password=password)    #set username and password
    client.on_connect= on_connect                      #attach function to callback
             #connect to broker
except:
    print("nie działa")