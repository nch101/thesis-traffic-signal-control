# ** automatic control mode **
# * Author: Nguyen Cong Huy
# ****************************

# - *- coding: utf- 8 - *-

def initAutomatic(quantity, lightStatus, timeRed, delta):
    lightStatus = []
    timeLight = []
    for index in range(0, quantity):
        lightStatus.append('red')
        if (index % 2):
            timeLight.append(timeRed[index])
        else:
            timeLight.append(delta)

def automatic(timeRed, timeYellow, timeGreen, timeLight, lightStatus, quantity):
    for index in range(0, quantity):
        if ((timeLight[index] == 0) and (lightStatus[index] == 'yellow')):
            timeLight[index] = timeRed[index]
            lightStatus[index] = 'red'
        if ((timeLight[index] == 0) and (lightStatus[index] == 'red')):
            timeLight[index] = timeGreen[index]
            lightStatus[index] = 'green'
        if ((timeLight[index] == 0) and (lightStatus[index] == 'green')):
            timeLight[index] = timeYellow[index]
            lightStatus[index] = 'yellow'