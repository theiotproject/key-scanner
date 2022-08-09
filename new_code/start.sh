#!/usr/bin/env python3
nohup python3 virtual.py &
sleep 2
nohup python3 core.py &
nohup  python3 write2.py &
nohup python3 czujnik.py &
nohup python3 write.py
