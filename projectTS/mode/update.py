import sys
sys.path.append('/home/huy/Documents/py-project')
from projectTS.lib.getData import getData 
from dotenv import load_dotenv
import os
import socketio

load_dotenv()
getDataURL = os.getenv('GET_DATA_URL')
interID = os.getenv('INTERSECTION_ID')
token = os.getenv('ACCESS_TOKEN')

sio = socketio.Client()
intersection = getData(getDataURL, interID, token)

""" @sio.on('update-mode', namespace='/update-mode/'+interID)
def updateMode():
    mode = intersection.modeControl()
    print(mode) """
    
mode = intersection.modeControl()
print(mode)

def modeControlUpdate(mode):
    if (mode == 'automatic'):
        print('automatic')
    elif (mode == 'manual'):
        print('manual')
    elif (mode == 'emergency'):
        print('emergency')
    else:
        pass


