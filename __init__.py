#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Copyright (C) 2015 - 2017 Martin Kauss (yo@bishoph.org)

Licensed under the Apache License, Version 2.0 (the "License"); you may
not use this file except in compliance with the License. You may obtain
a copy of the License at

 http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
License for the specific language governing permissions and limitations
under the License.
"""

# Default plugin for output of analysis

# readable results is an array of recognized commands, so if one recognizable
# command is made one after another the first will go first, can make a priority
# with a key word on action commands

import RPi.GPIO as GPIO
import time
GPIO.setwarnings(False)
# need to see the setup on connections for this really to work arbitruary outputs rn
def run(readable_results, data, rawbuf):
    GPIO.setmode(GPIO.BOARD) # RPi numbering scheme! Not to be confused with BCM numbering scheme!
    GPIO.setup(7, GPIO.OUT) # forward's pin  #GPIO4
    GPIO.setup(11, GPIO.OUT) # reverse's pin  #GPIO17
    GPIO.setup(13, GPIO.OUT) # Left's pin  #GPIO27
    GPIO.setup(15, GPIO.OUT) # right's pin  #GPIO22
    GPIO.setup(16, GPIO.OUT) # not recognized input. #GPIO23
    GPIO.setup(18, GPIO.OUT)
    
    try:
        if('Go' in readable_results):
            GPIO.output(7, True)
            GPIO.output(11, False)
            GPIO.output(13, False)
            GPIO.output(15, False)
            GPIO.output(16, False)
        elif('reverse' in readable_results):
            GPIO.output(7, False)
            GPIO.output(11, True)
            GPIO.output(13, False)
            GPIO.output(15, False)
            GPIO.output(16, False)
        elif('left' in readable_results): 
            GPIO.output(7, False)
            GPIO.output(11, False)
            GPIO.output(13, True)
            GPIO.output(15, False)
            GPIO.output(16, False)
        elif('right' in readable_results): 
            GPIO.output(7, False)
            GPIO.output(11, False)
            GPIO.output(13, False)
            GPIO.output(15, True)
            GPIO.output(16, False)
        elif('Stop' in readable_results): 
            GPIO.output(7, False)
            GPIO.output(11, False)
            GPIO.output(13, False)
            GPIO.output(15, False)
            GPIO.output(16, True)
        else:
            print(readable_results)
        
    except KeyboardInterrupt: # If CTRL+C is pressed, exit cleanly:
        GPIO.output(7, False)
        GPIO.output(11, False)
        GPIO.output(13, False)
        GPIO.output(15, False)
        GPIO.output(16, False)
        GPIO.output(18,False)
        GPIO.cleanup() # cleanup all GPIO

