# ** automatic control mode **
# * Author: Nguyen Cong Huy  *
# ****************************

# - *- coding: utf- 8 - *-

import projectTS.vals as vals

def automaticFlexibleTime():
    for index in range(0, vals.nTrafficLights):
        if index%2:
            setTimeLight(vals.timeGreenFlexibleNS, vals.timeGreenFlexibleWS, index)
        else:
            setTimeLight(vals.timeGreenFlexibleWS, vals.timeGreenFlexibleNS, index)

def setTimeLight(timeGreen, timeGreenForTimeRed, index):
    if ((vals.timeLight[index] == -1) and \
    (vals.lightStatus[index] == 'red')):
        vals.timeLight[index] = timeGreen
        vals.lightStatus[index] = 'green'
    elif ((vals.timeLight[index] == -1) and \
        (vals.lightStatus[index] == 'yellow')):
        vals.timeLight[index] = timeGreenForTimeRed + vals.timeYellow[index] + 2*vals.delta + 3
        vals.lightStatus[index] = 'red'
    elif ((vals.timeLight[index] == -1) and \
        (vals.lightStatus[index] == 'green')):
        vals.timeLight[index] = vals.timeYellow[index]
        vals.lightStatus[index] = 'yellow'
    else:
        pass