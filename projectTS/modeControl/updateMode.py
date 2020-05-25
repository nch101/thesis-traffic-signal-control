# **** update control mode ****
# * Author: Nguyen Cong Huy
# *****************************

# - *- coding: utf- 8 - *-

import sys
sys.path.append('/home/huy/Documents/py-project')
import logging
import projectTS.vals as vals
from projectTS.initial import initConfig, initAutomatic, initManual, initEmergency
from projectTS.modeControl.automatic import automatic 
from projectTS.modeControl.manual import manual
from projectTS.modeControl.emergency import emergency

logger = logging.getLogger('projectTS.modeControl.updateMode')

def changeMode(data):
    if (data == 'automatic'):
        initConfig()
        initAutomatic()
        vals.mode = 'automatic'
        logger.info('Updated mode control: %s', vals.mode)
    elif (data == 'manual'):
        vals.mode = 'manual'
        logger.info('Updated mode control: %s', vals.mode)
    elif (data == 'emergency'):
        initEmergency()
        vals.mode = 'emergency'
        logger.info('Updated mode control: %s', vals.mode)
    else:
        pass

def changeLight(data):
    logger.info('Change light')
    if (data == 'change-light'):
        vals.changeFlat = True

# def updateModeOnServer():


def updateModeControl():
    if (vals.mode == 'automatic'):
        automatic()
    elif (vals.mode == 'manual'):
        manual()
    elif (vals.mode == 'emergency'):
        emergency()
    else:
        pass