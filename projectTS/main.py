# ******* main program *******
# * Author: Nguyen Cong Huy
# ****************************

# - *- coding: utf- 8 - *-

import sys
sys.path.append('/home/huy/Documents/projectTS')

from projectTS.socketIO.socket import *
from projectTS.modeControl.update import updateModeControl

mode = ''
timeLight = []
lightStatus = []
# timeLight = list(map(lambda x: x-1, timeLight)) need to fix