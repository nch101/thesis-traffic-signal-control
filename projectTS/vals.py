# ***** global variables *****
# * Author: Nguyen Cong Huy
# ****************************

# - *- coding: utf- 8 - *-

global mode, timeRed, timeYellow, timeGreen, delta, nTrafficLights, \
lightStatus, priorityStreet, timeLight, timeGreenFlexibleNS, timeGreenFlexibleWS, \
rateNS, rateWS, stateNS, stateWS, changeFlag, changeLight

mode = ''
timeRed = 0
timeYellow = 0
timeGreen = 0
delta = 0
nTrafficLights = 0
lightStatus = []
priorityStreet = []
timeLight = []
timeGreenFlexibleNS = 0
timeGreenFlexibleWS = 0
rateNS = 0
rateWS = 0
stateNS = ''
stateWS = ''
changeFlag = False
changeLight = False