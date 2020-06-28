import configparser
import logging
import urllib3

import projectTS.vals as vals
from projectTS.lib.getData import getData

logger = logging.getLogger('projectTS.initial')

config = configparser.ConfigParser()
config.read('config.ini')

defaultConf = config['DEFAULT']
getDataURL = defaultConf['getData']
interID = defaultConf['intersection_id']
token = defaultConf['access_token']

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
intersection = getData(getDataURL, interID, token)

def initConfig():
    intersection.getData()
    vals.mode = intersection.modeControl
    vals.nTrafficLights = intersection.quantity
    vals.timeRed = intersection.timeRed
    vals.timeYellow = intersection.timeYellow
    vals.timeGreen = intersection.timeGreen
    vals.delta = intersection.deltaTime

    logger.info('Initial config')
    logger.info('Mode: %s', vals.mode)
    logger.info('Number of traffic lights: %s', vals.nTrafficLights)
    logger.info('Time red: %s', vals.timeRed)
    logger.info('Time yellow: %s', vals.timeYellow)
    logger.info('Time green: %s', vals.timeGreen)
    logger.info('Time delta: %s', vals.delta)

def initAutomatic():
    vals.lightStatus = []
    vals.timeLight = []
    for index in range(0, vals.nTrafficLights):
        vals.lightStatus.append('red')
        if (index % 2):
            vals.timeLight.append(vals.timeRed[index])
        else:
            vals.timeLight.append(vals.delta)

    logger.info('Init automatic')
    logger.info('Light status: %s', vals.lightStatus)
    logger.info('Time light: %s', vals.timeLight)

def initAutomaticFlexible():
    vals.lightStatus = []
    vals.timeLight = []
    for index in range(0, vals.nTrafficLights):
        vals.lightStatus.append('red')
        if (index % 2):
            vals.timeLight.append(vals.timeGreenFlexibleWS + vals.timeYellow[index] + 2*vals.delta + 3)
        else:
            vals.timeLight.append(vals.delta)

    logger.info('Init automatic')
    logger.info('Light status: %s', vals.lightStatus)
    logger.info('Time light: %s', vals.timeLight)

def initManual():
    vals.lightStatus = []
    vals.timeLight = []
    for index in range(0, vals.nTrafficLights):
        vals.timeLight.append(0)
        if (index % 2):
            vals.lightStatus.append('red')
        else:
            vals.lightStatus.append('green')

    logger.info('Init manual')
    logger.info('Light status: %s', vals.lightStatus)
    logger.info('Time light: %s', vals.timeLight)

def initEmergency(priorityStreet):
    for index in range(0, vals.nTrafficLights):
        if (priorityStreet == index):
            if (vals.lightStatus[index] == 'green'):
                vals.timeLight[index] = 0
            elif (vals.lightStatus[index] == 'yellow'):
                vals.timeLight[index] = 0
                vals.lightStatus[index] = 'green'
            else:
                vals.timeLight[index] = 8
        else:
            if (vals.lightStatus[index] == 'green'):
                vals.lightStatus[index] = 'yellow'
                vals.timeLight[index] = 8
            elif (vals.lightStatus[index] == 'yellow'):
                vals.lightStatus[index] = 'red'
                vals.timeLight[index] = 0
            else:
                vals.timeLight[index] = 0

    logger.info('Init emergency')
    logger.info('Light status: %s', vals.lightStatus)
    logger.info('Time light: %s', vals.timeLight)

def checkModeControl():
    intersection.getData()
    vals.mode = intersection.modeControl