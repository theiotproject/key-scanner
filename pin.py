#!/usr/bin/env python3
try:
    import RPi.GPIO as GPIO
except:
    syslog.syslog(syslog.LOG_INFO,"Enviroment without GPIO support")

import syslog
try:
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
except:
    pom=1
    def up(shot):
        pom=0
        syslog.syslog(syslog.LOG_WARNING,"CLOSE")
    def down(shot):
        pom=1
        syslog.syslog(syslog.LOG_WARNING,"OPEN")
    def sett(shot):
        x=1
        x+=x
    def chinp(shot):
        return pom
    def fel():
        print("")
    def cleanup():
        print("clean")