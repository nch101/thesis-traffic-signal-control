# ***** global variables *****
# * Author: Nguyen Cong Huy
# ****************************

# - *- coding: utf- 8 - *-

global mode, timeRed, timeYellow, timeGreen, delta, nTrafficLights
global lightStatus, priorityStreet, timeLight, timeGreenFlexible
global changeFlag, changeLight

mode = ''
timeRed = 0
timeYellow = 0
timeGreen = 0
delta = 0
nTrafficLights = 0
lightStatus = []
priorityStreet = []
timeLight = []
timeGreenFlexible = 0
changeFlag = False
changeLight = False