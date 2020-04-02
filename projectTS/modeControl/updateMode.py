# **** update control mode ****
# * Author: Nguyen Cong Huy
# *****************************

# - *- coding: utf- 8 - *-

import sys
sys.path.append('/home/huy/Documents/py-project')
import projectTS.vals as vals
import os
from dotenv import load_dotenv
from projectTS.lib.getData import getData
from projectTS.modeControl.automatic import initAutomatic, 
from projectTS.modeControl.manual import manual
from projectTS.modeControl.emergency import emergency

load_dotenv()
getDataURL = os.getenv('GET_DATA_URL')
interID = os.getenv('INTERSECTION_ID')
token = os.getenv('ACCESS_TOKEN')

intersection = getData(getDataURL, interID, token)

def changeMode():
    intersection.getData()
    vals.mode = intersection.modeControl()
    vals.nTrafficLights = intersection.nTrafficLights()
    global timeRed = intersection.timeRed()
    global timeYellow = intersection.timeYellow()
    global timeGreen = intersection.timeGreen()
    global delta = intersection
    global priorityStreet = intersection

    if (vals.mode == 'automatic'):
        initAutomatic(timeRed, delta)
    print('Mode control:', vals.mode)

def updateModeControl():
    if (vals.mode == 'automatic'):
        automatic(timeRed, timeYellow, timeGreen)
    elif (vals.mode == 'manual'):
        manual(timeYellow)
    elif (vals.mode == 'emergency'):
        emergency(priorityStreet)
    else:
        pass