# **** manual control mode ****
# * Author: Nguyen Cong Huy
# *****************************

# - *- coding: utf- 8 - *-

import sys
sys.path.append('/home/huy/Documents/py-project')
import projectTS.vals as vals

def manual():
    for index in range(0, vals.nTrafficLights):
        if ((vals.lightStatus[index] == 'red') and (vals.changeLight)):
            vals.lightStatus[index] = 'green'
        elif ((vals.lightStatus[index] == 'yellow') and (vals.timeLight[index] == 0)):
            vals.lightStatus[index] = 'red'
        elif ((vals.lightStatus[index] == 'green') and (vals.changeFlat)):
            vals.lightStatus[index] = 'yellow'
            vals.timeLight[index] = vals.timeYellow[index]
        else:
            pass
    vals.changeLight = False
    vals.changeFlat = False