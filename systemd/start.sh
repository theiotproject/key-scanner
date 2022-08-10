#!/usr/bin/env python3
socat -d -d  pty,b9600,raw,echo=0,link=/dev/ttyS90    pty,b9600,raw,echo=0,link=/dev/ttyS91 &
sleep 2
nohup python3 /samba/shares/new_code/core.py &
nohup python3 /samba/shares/new_code/write2.py &
nohup python3 /samba/shares/new_code/czujnik.py &
nohup python3 /samba/shares/new_code/write.py
