# ********* socket IO *********
# * Author: Nguyen Cong Huy
# *****************************

# - *- coding: utf- 8 - *-
import logging
import configparser

import socketio
import projectTS.vals as vals
from projectTS.initial import initAutomatic
from projectTS.modeControl.updateMode import changeMode, changeLight

logger = logging.getLogger('projectTS.socketIO.socket')

config = configparser.ConfigParser()
config.read('config.ini')

defaultConf = config['DEFAULT']
interID = defaultConf['intersection_id']
stateLightNsp = defaultConf['stateLightNsp']
controlLightNsp = defaultConf['controlLightNsp']
cameraNsp = defaultConf['cameraNsp']

dorm = config['DORM']
serverAddress = dorm['server']
# smartphone = config['SMARTPHONE']
# serverAddress = smartphone['server']

headers = { 'intersectionId': interID }

sio = socketio.Client(ssl_verify=False)

@sio.event
def connect():
    logger.info('Connection socket established')

sio.connect(serverAddress, headers = headers, namespaces=[stateLightNsp, controlLightNsp, cameraNsp])

sio.emit('room', interID, controlLightNsp)
sio.on('[intersection]-change-mode', changeMode, controlLightNsp)
sio.on('[intersection]-change-light', changeLight, controlLightNsp)

@sio.event
def disconnect():
    logger.info('Disconnected socket')
    # print('Change mode when connect lost')
    # vals.mode = 'automatic'
    # initAutomatic()

def updateStateLight():
    try:
        sio.emit('room', interID, stateLightNsp)
        timeData = {
            'room': interID, 
            'data': vals.timeLight
        }

        lightData = {
            'room': interID, 
            'data': vals.lightStatus
        }

        # logging.info('timeData: %s, lightData: %s', (timeData.data, lightData.data))
        sio.emit('[intersection]-time-light', timeData, stateLightNsp)
        sio.emit('[intersection]-light-state', lightData, stateLightNsp)
    except:
        logger.warning('Connect socket lost')

def transmitImages(frames):
    try:
        sio.emit('[intersection]-camera', frames, cameraNsp)
    except:
        logger.warning('Cannot transmit frames to server')