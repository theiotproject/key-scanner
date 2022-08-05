import paho.mqtt.client as mqttClient
import time
import platform
import subprocess


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
    f=open("/etc/offlinelogs","r")
    rea=f.readline()
    print(rea)
    if x and rea=="":
        print("publishing")
        client.publish(topic,message)
        #client.publish(topic,message)
        f.close()
    elif x and rea!="":
        f.close()
        f=open("/etc/offlinelogs","r")
        print("updating")
        client.publish(topic,message)
        for index, line in enumerate(f):
                list=line.split(']')
                client.publish(list[0],list[1])
                
        f.close()
        ftd=open("/etc/offlinelogs","w")
        ftd.close()
        
    else:
        f.close()
        f=open("/etc/offlinelogs","a")
        print("dopisek")
        f.write(topic+"]"+message)
        f.close
        


    
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
def client_end(client):
    client.disconnect()
    client.loop_stop()