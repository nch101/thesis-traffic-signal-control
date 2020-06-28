# ** emergency control mode **
# * Author: Nguyen Cong Huy
# ****************************

# - *- coding: utf- 8 - *-

import logging
import projectTS.vals as vals

def emergency():
    for i in range(0, vals.nTrafficLights):
        if ((vals.lightStatus[i] == 'yellow') and \
            (vals.timeLight[i] == 0)):
            vals.lightStatus[i] = 'red'
            vals.timeLight[i] = 0
        elif ((vals.lightStatus[i] == 'red') and \
            (vals.timeLight[i] == 0) and \
            (vals.priorityStreet == i)):
            vals.lightStatus[i] = 'green'
            vals.timeLight[i] = 0