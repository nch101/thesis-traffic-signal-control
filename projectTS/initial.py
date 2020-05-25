import sys
sys.path.append('/home/huy/Documents/py-project')
import os
import logging
import urllib3
from dotenv import load_dotenv
import projectTS.vals as vals
from projectTS.lib.getData import getData

logger = logging.getLogger('projectTS.initial')

load_dotenv()
getDataURL = os.getenv('GET_DATA_URL')
interID = os.getenv('INTERSECTION_ID')
token = os.getenv('ACCESS_TOKEN')

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

    print('******* Init config *******')
    print('Mode: ', vals.mode)
    print('Number of traffic lights: ', vals.nTrafficLights)
    print('Time red: ', vals.timeRed)
    print('Time yellow: ', vals.timeYellow)
    print('Time green: ', vals.timeGreen)
    print('Time delta: ', vals.delta)
    print('***************************')

    logger.info('Initial config')

def initAutomatic():
    vals.lightStatus = []
    vals.timeLight = []
    for index in range(0, vals.nTrafficLights):
        vals.lightStatus.append('red')
        if (index % 2):
            vals.timeLight.append(vals.timeRed[index])
        else:
            vals.timeLight.append(vals.delta)
    #debug vals
    print('***** Init automatic *****')
    print('Light status ', vals.lightStatus)
    print('Time light ', vals.timeLight)
    print('**************************')

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
    #debug vals
    print('***** Init manual *****')
    print('Light status ', vals.lightStatus)
    print('Time light ', vals.timeLight)
    print('**************************')

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

    print('***** Init emergency *****')
    print('Light status ', vals.lightStatus)
    print('Time light ', vals.timeLight)
    print('**************************')

    logger.info('Init emergency')
    logger.info('Light status: %s', vals.lightStatus)
    logger.info('Time light: %s', vals.timeLight)