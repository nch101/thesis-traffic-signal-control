# ******* main program *******
# * Author: Nguyen Cong Huy
# ****************************

# - *- coding: utf- 8 - *-

import sys, os
projectPath = os.path.expanduser('~/Documents/py-project')
sys.path.append(projectPath)

import logging
import logging.config
logging.config.fileConfig(projectPath + '/projectTS/logging.conf', defaults={'logfilename': projectPath + '/projectTS/logs/app.log'})

import time
# import RPi.GPIO as GPIO
import projectTS.vals as vals
# from projectTS.lib.showNumber import showNumber
# from projectTS.lib.showLight import showLight
from projectTS.socketIO.socket import *
from projectTS.initial import initConfig, initAutomatic, initManual
from projectTS.modeControl.updateMode import updateModeControl
from projectTS.socketIO.socket import updateStateLight

data_pin1 = 15
clock_pin1 = 13
latch_pin1 = 11
# numberLight1 = showNumber(data_pin1, clock_pin1, latch_pin1)

data_pin2 = 29
clock_pin2 = 31
latch_pin2 = 33
# numberLight2 = showNumber(data_pin2, clock_pin2, latch_pin2)

red_pin2 = 36
yellow_pin2 = 38
green_pin2 = 40
# trafficLight2 = showLight(red_pin2, yellow_pin2, green_pin2)

red_pin1 = 12
yellow_pin1 = 16
green_pin1 = 18
# trafficLight1 = showLight(red_pin1, yellow_pin1, green_pin1)

logger = logging.getLogger('projectTS.main')
logger.info('Running... ')

initConfig()
if (vals.mode == 'automatic'):
    initAutomatic()
elif (vals.mode == 'manual'):
    initManual()
else:
    pass

updateStateLight()

def countDown():
    for i in range(0, vals.nTrafficLights):
        if (vals.timeLight[i] > 0):
            vals.timeLight[i] -= 1

        if ((vals.timeLight[i] == 0) and (vals.lightStatus[i] == 'yellow') and (vals.mode == 'manual')):
            vals.changeLight = True

def showLight():
    numberLight1.showNumber(vals.timeLight[0])
    numberLight2.showNumber(vals.timeLight[1])
    trafficLight1.showLight(vals.lightStatus[0])
    trafficLight2.showLight(vals.lightStatus[1])

def main():
    while True:
        time.sleep(1)
        updateModeControl()
        countDown()
        # showLight()
        updateStateLight()

        print('********* DEBUG *********')
        print('Mode control: ', vals.mode)
        print('Light status: ', vals.lightStatus)
        print('Time light: ', vals.timeLight)
        print('*************************')

try:
    main()
except KeyboardInterrupt:
    print('Keyboard interrupt')
    logger.info('Keyboard interrupt')
    # GPIO.cleanup()
    quit()