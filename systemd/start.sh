#!/usr/bin/env python3
socat -d -d  pty,b9600,raw,echo=0,link=/dev/ttyS90    pty,b9600,raw,echo=0,link=/dev/ttyS91 &
sleep 2
nohup python3 /usr/bin/key-scanner/core.py &
nohup python3 /usr/bin/key-scanner/remoteControlRelay.py &
nohup python3 /usr/bin/key-scanner/motionSensor.py &
nohup python3 /usr/bin/key-scanner/ttyForwarder.py
