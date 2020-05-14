# ******* main program *******
# * Author: Nguyen Cong Huy
# ****************************

# - *- coding: utf- 8 - *-

import sys
sys.path.append('/home/huy/Documents/py-project')

import time
import projectTS.vals as vals
from projectTS.socketIO.socket import *
from projectTS.initial import initConfig, initAutomatic
from projectTS.modeControl.updateMode import updateModeControl
from projectTS.socketIO.socket import updateStateLight

initConfig()
if (vals.mode == 'automatic'):
    initAutomatic()
print('Mode control:', vals.mode)

def countDown():
    for i in range(0, vals.nTrafficLights):
        if (vals.timeLight[i] >= 0):
            vals.timeLight[i] -= 1

while True:
    updateStateLight()
    updateModeControl()
    countDown()
    time.sleep(1)
    print('******* DEBUG *******')
    print('Mode control')
    print(vals.mode)
    print('Light status')
    print(vals.lightStatus)
    print('Time light')
    print(vals.timeLight)
    print('********************')
