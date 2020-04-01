# ** automatic control mode **
# * Author: Nguyen Cong Huy
# ****************************

# - *- coding: utf- 8 - *-

def init():
    lightStatus = []
    timeLight = []
    for index in range(0, quantity):
        lightStatus.append('red')
        if (index % 2):
            timeLight.append(timeRed[index])
        else:
            timeLight.append(delta)

def timeAndLightStatusUpdate():
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

def automatic(timeRed, timeYellow, timeGreen, lightMode):
    if (first):
        init()
        first = False
    timeAndLightStatusUpdate()
    # showTime()
    # showLight()
    timeLight = list(map(lambda x: x-1, timeLight))

        

