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

idVehicles = []
indexOfStreet = []

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

def prepareEmergencyMode(data):
    if (data['state']):
        if (data['vehicleType'] == 'firetruck'):
            idVehicles.insert(0, data['vehicleId'])
            indexOfStreet.insert(0, data['indexOfStreet'])
            
            initEmergency(indexOfStreet[0])
            vals.priorityStreet = indexOfStreet[0]
            vals.preMode = vals.mode
            vals.mode = 'emergency'
            logger.info('Updated mode control: %s', vals.mode)
        elif (data['vehicleType'] == 'police'):
            idVehicles.insert(0, data['vehicleId'])
            indexOfStreet.insert(0, data['indexOfStreet'])

            initEmergency(indexOfStreet[0])
            vals.priorityStreet = indexOfStreet[0]
            vals.preMode = vals.mode
            vals.mode = 'emergency'
            logger.info('Updated mode control: %s', vals.mode)
        else:
            if data['vehicleId'] not in idVehicles:
                idVehicles.append(data['vehicleId'])
                indexOfStreet.append(data['indexOfStreet'])
                logger.info('Vehicle queue: %s', idVehicles)
                logger.info('Index of street queue: %s', indexOfStreet)
        
        if (vals.mode != 'emergency'):
            initEmergency(indexOfStreet[0])
            vals.priorityStreet = indexOfStreet[0]

            vals.preMode = vals.mode
            vals.mode = 'emergency'
            logger.info('Updated mode control: %s', vals.mode)
    else:
        del idVehicles[0]
        del indexOfStreet[0]
        if len(idVehicles) > 0:
            initEmergency(indexOfStreet[0])
            vals.priorityStreet = indexOfStreet[0]

        else:
            vals.mode = vals.preMode
            if (vals.mode == 'automatic-fixed-time'):
                initAutomatic()
            elif (vals.mode == 'automatic-flexible-time'):
                initAutomaticFlexible()
            elif (vals.mode == 'manual'):
                initManual()
            else:
                pass

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