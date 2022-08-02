import paho.mqtt.client as mqttClient
import time
def pub(topic,message):
    client.publish(topic,message)
    #print("dev")
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