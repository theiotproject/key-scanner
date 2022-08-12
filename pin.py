#!/usr/bin/env python3
try:
    import RPi.GPIO as GPIO
except:
    syslog.syslog(syslog.LOG_INFO,"Enviroment without GPIO support")

import syslog
def up(shot):
    GPIO.output(shot, False)
    syslog.syslog(syslog.LOG_WARNING,"CLOSE")
def down(shot):
    GPIO.output(shot,True)
    syslog.syslog(syslog.LOG_WARNING,"OPEN")
def sett(shot):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(shot,GPIO.OUT)
    #syslog.syslog(syslog.LOG_WARNING,"SCANNED MATCHING MAGIC CODE")
    #syslog.syslog(syslog.LOG_INFO,"info")
def chinp(shot):
    return GPIO.input(shot)
def fel():
    GPIO.setwarnings(False)
    print("")
def cleanup():
    GPIO.cleanup() 
    print("clean")