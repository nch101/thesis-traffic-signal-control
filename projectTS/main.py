# ******* main program *******
# * Author: Nguyen Cong Huy
# ****************************

# - *- coding: utf- 8 - *-

import sys
sys.path.append('/home/huy/Documents/py-project')

from projectTS.vals as vals
from projectTS.socketIO.socket import *
from projectTS.modeControl.updateMode import updateModeControl

# timeLight = list(map(lambda x: x-1, timeLight)) need to fix

vals.initVals()

while True:
    updateModeControl()
