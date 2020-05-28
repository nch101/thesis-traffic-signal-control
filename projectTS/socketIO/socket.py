# ********* socket IO *********
# * Author: Nguyen Cong Huy
# *****************************

# - *- coding: utf- 8 - *-

from dotenv import load_dotenv
import os
import socketio
import logging
import projectTS.vals as vals
from projectTS.initial import initAutomatic
from projectTS.modeControl.updateMode import changeMode, changeLight

logger = logging.getLogger('projectTS.socketIO.socket')

load_dotenv()
serverAddress = os.getenv('SERVER_ADDRESS')
interID = os.getenv('INTERSECTION_ID')
headers = { 'intersectionId': interID }
stateLightNsp = '/socket/state-light'
controlLightNsp = '/socket/control-light'

sio = socketio.Client(ssl_verify=False)

@sio.event
def connect():
    logger.info('Connection socket established')

sio.connect(serverAddress, headers = headers, namespaces=[stateLightNsp, controlLightNsp])


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