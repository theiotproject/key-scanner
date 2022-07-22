# Overview 
Key-scanner is python based pack of scripts, able to scan, interpret, and authorize QR codes in order to open electronic lock

We advise you to use the product with our website https://keymanager.theiotproject.com/, mobile app and to visit our blog https://theiotproject.com/
# Inputs 

Raspberry is programmed to 
- listen to MQTT signals on topic ```dev/test```
- waiting for QR scanner input from COM port ```/dev/ttyACM0```
- simulate COM ports: ```/dev/ttyS90```, ```/dev/ttyS91```

Sample input 
```
- yyyy-mm-dd HH:MM:SS/10 digit A-Z0-9 code ("2022-07-18 11:59:21/MSDECVKOPN")
```

  ![image](https://user-images.githubusercontent.com/108795150/179507239-9243d965-799c-47a6-9533-e53ef24ed8ad.png)
  
  
lock has tollerance of ```+-1 minute```, so the key will expire one minute after being generated

 # Additional features
 - Lock is able to open via MQTT after recieving ```secret``` signal
 - Lock is shipped with emergency opening. In order to open it scan QR code with the code matching ```magic.guid``` in /etc folder
 - Lock can push its logs to mosquitto MQTT broker, which then can forward them to MSQL database
  
  # Requirements
  -Raspberry Pi model B or higher
  
  -Honeywell QR scanner CM2D
  
  -Single channel 12v relay
  
  -Electronical lock
  
  Modules:
  
  -https://pypi.org/project/paho-mqtt/
  
  -https://pypi.org/project/RPi.GPIO2/
  
  -datetime
  
  -serial
  
  -mqtt client and mqtt broker
  # how to set everything up
  
  - flash the latest raspbian release, you can find it <a href="https://www.raspberrypi.com/software/operating-systems/">here</a>
  - connect rasperry with pc using COM->USB hub
  - connect you raspberry to internet
  - set static ip and enable ssh protocol
  - now you can enter your pi remotely using cli ssh client or <a href="https://www.putty.org/">PuTTY</a>
  - connect your scanner to raspberry pi
  - set it to send signal as COM port
  - connect single channel relay on GPIO 2
  - install given modules:
  ```sh
  pip3 install pyserial paho-mqtt mysql.connector syslog
  ```
  
  - select a desired folder to store this repo and clone it, excluding ```MQTTlogPush.py``` as it`s a server side script
  - set up external server and install your database and mosquitto broker, config documentation can be found <a href="https://mosquitto.org/man/mosquitto-conf-5.html">here<a>
  - enter valid credentials in core.py your database and correct hosts to all the brokers and other hosts
  - deploy MQTTlogPush.py on the same server
  - run command ```mosquitto <path_to_config_file>``` and ```python MQTTlogPush.py```
  - start all cloned scripts using command bash start in the containing folder
  
  
  
