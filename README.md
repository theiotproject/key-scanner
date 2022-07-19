# Overview 
Key-scanner is python based pack of scripts, able to scanm interpret, and authorize QR codes in order to open electronic lock

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
  
