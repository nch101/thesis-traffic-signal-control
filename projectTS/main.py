# ******* main program *******
# * Author: Nguyen Cong Huy
# ****************************

# - *- coding: utf- 8 - *-

import sys
sys.path.append('/home/huy/Documents/py-project')

import time
import projectTS.vals as vals
from projectTS.socketIO.socket import *
from projectTS.initial import initConfig, initAutomatic, initManual
from projectTS.modeControl.updateMode import updateModeControl
from projectTS.socketIO.socket import updateStateLight

initConfig()
if (vals.mode == 'automatic'):
    initAutomatic()
elif (vals.mode == 'manual'):
    initManual()
else:
    pass

print('Mode control:', vals.mode)
updateStateLight()

def countDown():
    for i in range(0, vals.nTrafficLights):
        if (vals.timeLight[i] > 0):
            vals.timeLight[i] -= 1

        if ((vals.timeLight[i] == 0) and (vals.lightStatus[i] == 'yellow') and (vals.mode == 'manual')):
            vals.changeLight = True

while True:
    time.sleep(1)
    updateModeControl()
    countDown()
    updateStateLight()
    print('******* DEBUG *******')
    print('Mode control: ', vals.mode)
    print('Light status: ', vals.lightStatus)
    print('Time light: ', vals.timeLight)
    print('********************')
