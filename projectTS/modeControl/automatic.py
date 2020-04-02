# ** automatic control mode **
# * Author: Nguyen Cong Huy
# ****************************

# - *- coding: utf- 8 - *-

import sys
sys.path.append('/home/huy/Documents/py-project')
import projectTS.vals as vals

def initAutomatic(timeRed, delta):
    vals.lightStatus = []
    vals.timeLight = []
    for index in range(0, vals.nTrafficLights):
        vals.lightStatus.append('red')
        if (index % 2):
            vals.timeLight.append(timeRed[index])
        else:
            vals.timeLight.append(delta)

def automatic(timeRed, timeYellow, timeGreen):
    for index in range(0, vals.nTrafficLights):
        if ((vals.timeLight[index] == 0) and (vals.lightStatus[index] == 'yellow')):
            vals.timeLight[index] = timeRed[index]
            vals.lightStatus[index] = 'red'
        if ((vals.timeLight[index] == 0) and (vals.lightStatus[index] == 'red')):
            vals.timeLight[index] = timeGreen[index]
            vals.lightStatus[index] = 'green'
        if ((vals.timeLight[index] == 0) and (vals.lightStatus[index] == 'green')):
            vals.timeLight[index] = timeYellow[index]
            vals.lightStatus[index] = 'yellow'