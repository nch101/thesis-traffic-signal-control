# ** automatic control mode **
# * Author: Nguyen Cong Huy  *
# ****************************

# - *- coding: utf- 8 - *-

import projectTS.vals as vals

def automatic():
    for index in range(0, vals.nTrafficLights):
        if ((vals.timeLight[index] == 0) and (vals.lightStatus[index] == 'yellow')):
            vals.timeLight[index] = vals.timeRed[index]
            vals.lightStatus[index] = 'red'
        if ((vals.timeLight[index] == 0) and (vals.lightStatus[index] == 'red')):
            vals.timeLight[index] = vals.timeGreen[index]
            vals.lightStatus[index] = 'green'
        if ((vals.timeLight[index] == 0) and (vals.lightStatus[index] == 'green')):
            vals.timeLight[index] = vals.timeYellow[index]
            vals.lightStatus[index] = 'yellow'