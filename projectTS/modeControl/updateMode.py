# **** update control mode ****
# * Author: Nguyen Cong Huy
# *****************************

# - *- coding: utf- 8 - *-

import sys
sys.path.append('/home/huy/Documents/py-project')
import projectTS.vals as vals
from projectTS.initial import initAutomatic, initConfig, initManual
from projectTS.modeControl.automatic import automatic 
from projectTS.modeControl.manual import manual
from projectTS.modeControl.emergency import emergency

def changeMode(data):
    if (data == 'automatic'):
        initConfig()
        initAutomatic()
        vals.mode = 'automatic'
    elif (data == 'manual'):
        # initManual()
        vals.mode = 'manual'
    elif (data == 'emergency'):
        vals.mode = 'emergency'
    else:
        pass

def changeLight(data):
    print('Data received: ' + data)
    if (data == 'change-light'):
        vals.changeFlat = True

def updateModeControl():
    if (vals.mode == 'automatic'):
        automatic()
    elif (vals.mode == 'manual'):
        manual()
    elif (vals.mode == 'emergency'):
        emergency()
    else:
        pass