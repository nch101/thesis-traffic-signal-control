# **** update control mode ****
# * Author: Nguyen Cong Huy
# *****************************

# - *- coding: utf- 8 - *-

import sys
sys.path.append('/home/huy/Documents/py-project')
from projectTS.lib.getData import getData
from projectTS.modeControl.automatic import initAutomatic, 
from projectTS.modeControl.manual import manual
from projectTS.modeControl.emergency import emergency
from dotenv import load_dotenv
import os

load_dotenv()
getDataURL = os.getenv('GET_DATA_URL')
interID = os.getenv('INTERSECTION_ID')
token = os.getenv('ACCESS_TOKEN')

intersection = getData(getDataURL, interID, token)

def changeMode():
    intersection.getData()
    mode = intersection.modeControl()
    timeRed = intersection.timeRed()
    timeYellow = intersection.timeYellow()
    timeGreen = intersection.timeGreen()
    nTrafficLight = intersection.nTrafficLights()
    
    if (mode == 'automatic'):
        initAutomatic()
    elif (mode == 'manual'):
        pass
    elif (mode == 'emergency'):
        pass
    else:
        pass
    print('Mode control:', mode)

def updateModeControl(mode):
    if (mode == 'automatic'):
        automatic()
    elif (mode == 'manual'):
        manual()
    elif (mode == 'emergency'):
        emergency()
    else:
        pass