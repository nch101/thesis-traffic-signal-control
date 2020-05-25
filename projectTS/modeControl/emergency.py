# ** emergency control mode **
# * Author: Nguyen Cong Huy
# ****************************

# - *- coding: utf- 8 - *-

import sys
sys.path.append('/home/huy/Documents/py-project')
import logging
import projectTS.vals as vals

def emergency():
    for i in range(0, vals.nTrafficLights):
        if ((vals.lightStatus[i] == 'yellow') and (vals.timeLight[i] == 0)):
            vals.lightStatus[i] = 'red'