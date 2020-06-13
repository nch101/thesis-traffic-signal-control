import configparser
import logging
import urllib3

import projectTS.vals as vals
from projectTS.lib.getData import getData

logger = logging.getLogger('projectTS.initial')

config = configparser.ConfigParser()
config.read('config.ini')

# dormConf = config['DORM']
# getDataURL = dormConf['getData']

testConf = config['TEST']
getDataURL = testConf['getData']

defaultConf = config['DEFAULT']
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

def initEmergency():
    vals.lightStatus = []
    vals.timeLight = []
    intersection.getData()
    vals.priorityStreet = intersection.priorityStreet
    for index in range(0, vals.nTrafficLights):
        if (vals.priorityStreet[index]):
            vals.lightStatus.append('green')
            vals.timeLight.append(0)
        else:
            vals.lightStatus.append('yellow')
            vals.timeLight.append(8)

    logger.info('Init emergency')
    logger.info('Light status: %s', vals.lightStatus)
    logger.info('Time light: %s', vals.timeLight)

def checkModeControl():
    intersection.getData()
    vals.mode = intersection.modeControl