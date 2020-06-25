# **** update control mode ****
# * Author: Nguyen Cong Huy
# *****************************

# - *- coding: utf- 8 - *-

import logging
import projectTS.vals as vals
from projectTS.initial import initConfig, initAutomatic, initAutomaticFlexible, initManual, initEmergency
from projectTS.modeControl.automaticFixedTime import automaticFixedTime
from projectTS.modeControl.automaticFlexibleTime import automaticFlexibleTime
from projectTS.modeControl.manual import manual
from projectTS.modeControl.emergency import emergency

logger = logging.getLogger('projectTS.modeControl.updateMode')

def changeMode(data):
    if (data == 'automatic-fixed-time'):
        initConfig()
        initAutomatic()
        vals.mode = 'automatic-fixed-time'
        logger.info('Updated mode control: %s', vals.mode)
    elif (data == 'automatic-flexible-time'):
        initConfig()
        initAutomaticFlexible()
        vals.updateTimeFlag = True
        vals.mode = 'automatic-flexible-time'
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
        vals.changeFlag = True

# def updateModeOnServer():


def updateModeControl():
    if (vals.mode == 'automatic-fixed-time'):
        automaticFixedTime()
    elif (vals.mode == 'automatic-flexible-time'):
        automaticFlexibleTime()
    elif (vals.mode == 'manual'):
        manual()
    elif (vals.mode == 'emergency'):
        emergency()
    else:
        pass