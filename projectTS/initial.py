import sys
sys.path.append('/home/huy/Documents/py-project')
import os
from dotenv import load_dotenv
import projectTS.vals as vals
from projectTS.lib.getData import getData

load_dotenv()
getDataURL = os.getenv('GET_DATA_URL')
interID = os.getenv('INTERSECTION_ID')
token = os.getenv('ACCESS_TOKEN')

intersection = getData(getDataURL, interID, token)

def initConfig():
    intersection.getData()
    vals.mode = intersection.modeControl()
    vals.nTrafficLights = intersection.nTrafficLights()
    vals.timeRed = intersection.timeRed()
    vals.timeYellow = intersection.timeYellow()
    vals.timeGreen = intersection.timeGreen()
    vals.delta = intersection.deltaTime()
    #global priorityStreet = intersection
    print('**** Init config ****')
    print(vals.mode)
    print(vals.nTrafficLights)
    print(vals.timeRed)
    print(vals.timeYellow)
    print(vals.timeGreen)
    print(vals.delta)
    print('**********************')

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
    print('Light status ')
    print(vals.lightStatus)
    print('Time light ')
    print(vals.timeLight)
    print('**************************')