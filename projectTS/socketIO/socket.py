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
from projectTS.modeControl.updateMode import changeMode

load_dotenv()
serverAddress = os.getenv('SERVER_ADDRESS')
interID = os.getenv('INTERSECTION_ID')
headers = { 'intersectionId': interID }
namespace = '/intersection/' + interID

sio = socketio.Client()

@sio.event
def connect():
    print('connection established')

sio.on('change-light', changeLight, namespace)
sio.on('change-mode', changeMode, namespace)
sio.emit('current-time', vals.timeLight, namespace)
sio.emit('light-status', vals.lightStatus, namespace)

@sio.event
def disconnect():
    print('disconnected from server')

sio.connect(serverAddress, headers = headers )
sio.wait()
