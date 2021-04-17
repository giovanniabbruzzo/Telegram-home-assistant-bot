#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 21 15:46:24 2020

@author: pi
"""
import RPi.GPIO as GPIO
import time

FAN = 26

GPIO.setmode(GPIO.BCM)
GPIO.setup(FAN, GPIO.OUT)

while 1:
    print("High\n")
    GPIO.output(FAN,GPIO.HIGH)
    time.sleep(5)
    print("Low\n")
    GPIO.output(FAN,GPIO.LOW)
    time.sleep(5)
