# **** manual control mode ****
# * Author: Nguyen Cong Huy
# *****************************

# - *- coding: utf- 8 - *-

def manual(quantity, lightStatus, timeLight, timeYellow):
    for index in range(0, quantity):
        if (lightStatus[index] == 'red'):
            lightStatus[index] = 'green'
        elif (lightStatus[index] == 'yellow'):
            lightStatus[index] = 'red'
        elif (lightStatus[index] == 'green'):
            lightStatus[index] = 'yellow'
            timeLight[index] = timeYellow[index]
        else:
            pass