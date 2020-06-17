# ******* main program *******
# * Author: Nguyen Cong Huy
# ****************************

# - *- coding: utf- 8 - *-

import sys, os
projectPath = os.path.expanduser('~/Documents/py-project')
sys.path.append(projectPath)

import logging
import logging.config
logging.config.fileConfig(projectPath + '/projectTS/logging.conf', 
                    defaults={'logfilename': projectPath + '/projectTS/logs/app.log', 
                            'logwarnname': projectPath + '/projectTS/logs/warn.log'})
import configparser
import time
import threading

# import RPi.GPIO as GPIO
import projectTS.vals as vals
# from projectTS.lib.showNumber import showNumber
# from projectTS.lib.showLight import showLight
from projectTS.socketIO.socket import *
from projectTS.initial import initConfig, initAutomatic, initManual
from projectTS.imagesProcessing.imagesProcessing1 import onImagesProcessing1
from projectTS.imagesProcessing.imagesProcessing2 import onImagesProcessing2
from projectTS.modeControl.updateMode import updateModeControl
from projectTS.socketIO.socket import updateStateLight

logger = logging.getLogger('projectTS.main')
config = configparser.ConfigParser()
config.read('config.ini')

stopThread = threading.Event()

# street1Conf = config['STREET-1']
# numberLight1 = showNumber(int(street1Conf['data_pin']), 
#                         int(street1Conf['clock_pin']), 
#                         int(street1Conf['latch_pin']))

# trafficLight1 = showLight(int(street1Conf['red_pin']),
#                         int(street1Conf['yellow_pin']),
#                         int(street1Conf['green_pin']))

# street2Conf = config['STREET-2']
# numberLight2 = showNumber(int(street2Conf['data_pin']), 
#                         int(street2Conf['clock_pin']), 
#                         int(street2Conf['latch_pin']))

# trafficLight2 = showLight(int(street2Conf['red_pin']),
#                         int(street2Conf['yellow_pin']),
#                         int(street2Conf['green_pin']))

def showLight():
    numberLight1.showNumber(vals.timeLight[0])
    numberLight2.showNumber(vals.timeLight[1])
    trafficLight1.showLight(vals.lightStatus[0])
    trafficLight2.showLight(vals.lightStatus[1])

def countDown():
    for i in range(0, vals.nTrafficLights):
        if (vals.timeLight[i] >= 0):
            vals.timeLight[i] -= 1

        if ((vals.timeLight[i] == 0) and (vals.lightStatus[i] == 'yellow') and (vals.mode == 'manual')):
            vals.changeLight = True

def onControlAndDisplay(stop_event):
    logger.info('onControlAndDisplay is running...')
    initConfig()
    if (vals.mode == 'automatic-fixed-time' or vals.mode == 'automatic-flexible-time'):
        initAutomatic()
    elif (vals.mode == 'manual'):
        initManual()
    else:
        pass

    while not stop_event.wait(0):
        updateModeControl()
        logger.debug('Mode control: %s', vals.mode)
        logger.debug('Light status: %s', vals.lightStatus)
        logger.debug('Time light: %s', vals.timeLight)
        updateStateLight()
        # showLight()
        time.sleep(1)
        countDown()

try:
    thread1 = threading.Thread(target=onControlAndDisplay, args=(stopThread, ))
    thread2 = threading.Thread(target=onImagesProcessing1, args=(stopThread, ))
    thread3 = threading.Thread(target=onImagesProcessing2, args=(stopThread, ))

    thread1.start()
    thread2.start()
    thread3.start()

    thread1.join()
    thread2.join()
    thread3.join()

except KeyboardInterrupt:
    logger.info('Keyboard interrupt')
    stopThread.set()
    # GPIO.cleanup()
    quit()
except Exception as e:
    logger.error('Something is wrong: %s', e)