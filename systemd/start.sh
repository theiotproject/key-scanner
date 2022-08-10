#!/usr/bin/env python3
nohup python3 /samba/shares/new_code/virtual.py &
sleep 2
nohup python3 /samba/shares/new_code/core.py &
nohup python3 /samba/shares/new_code/write2.py &
nohup python3 /samba/shares/new_code/czujnik.py &
nohup python3 /samba/shares/new_code/write.py
