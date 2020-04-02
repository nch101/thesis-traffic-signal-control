# ** emergency control mode **
# * Author: Nguyen Cong Huy
# ****************************

# - *- coding: utf- 8 - *-

import sys
sys.path.append('/home/huy/Documents/py-project')
import projectTS.vals as vals

def emergency(priorityStreet):
    for index in range(0, vals.nTrafficLights):
        vals.timeTraffic[index] = 0
        vals.lightStatus[index] = priorityStreet[index]