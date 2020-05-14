# **** update control mode ****
# * Author: Nguyen Cong Huy
# *****************************

# - *- coding: utf- 8 - *-

import sys
sys.path.append('/home/huy/Documents/py-project')
import projectTS.vals as vals
from projectTS.initial import initAutomatic, initConfig
from projectTS.modeControl.automatic import automatic 
from projectTS.modeControl.manual import manual
from projectTS.modeControl.emergency import emergency

def changeMode(data):
    if (data == 'automatic'):
        initConfig()
        initAutomatic()
    elif (data == 'manual'):
        vals.mode = 'manual'
    elif (data == 'emergency'):
        vals.mode = 'emergency'
    else:
        pass

def changeLight():
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