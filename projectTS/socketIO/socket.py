# ********* socket IO *********
# * Author: Nguyen Cong Huy
# *****************************

# - *- coding: utf- 8 - *-

from dotenv import load_dotenv
import os
import socketio
import sys
sys.path.append('/home/huy/Documents/py-project')
import projectTS.vals as vals
from projectTS.modeControl.updateMode import changeMode, changeLight

load_dotenv()
serverAddress = os.getenv('SERVER_ADDRESS')
interID = os.getenv('INTERSECTION_ID')
headers = { 'intersectionId': interID }
stateLightNsp = '/socket/state-light'
controlLightNsp = '/socket/control-light'

sio = socketio.Client()

@sio.event
def connect():
    print('connection established')

sio.connect(serverAddress, headers = headers, namespaces=[stateLightNsp, controlLightNsp])
sio.on('[intersection]-change-mode', changeMode, controlLightNsp)
sio.on('[intersection]-change-light', changeLight, controlLightNsp)

def updateStateLight():
    try:
        sio.emit('[intersection]-time-light', vals.timeLight, stateLightNsp)
        sio.emit('[intersection]-light-state', vals.lightStatus, stateLightNsp)
    except:
        print('xxx updateStateLight() was not executed xxx')

@sio.event
def disconnect():
    print('disconnected from server')
    print('Change mode when connect lost')
    vals.mode = 'automatic'

