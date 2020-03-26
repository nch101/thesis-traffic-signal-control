import paho.mqtt.client as mqtt
import time
from datetime import datetime
mqttc = mqtt.Client()

# Config MQTT
username = "demo"
password = "123456"
hostname = "tailor.cloudmqtt.com"
port = 13231
mqttc.username_pw_set(username, password)
mqttc.connect(hostname, port)
mqttc.loop_start()

mqttc.subscribe("set", 0)

currentTime = timeGreen = timeYellow = timeRed = 0
lightState = ""
systemState = ""
changeFlag = False

def setTime(mes):
    global timeRed, timeYellow, timeGreen
    if (mes.find('red') != -1):
        timeRed = int(mes.split(' ',1)[1])
        print("Time red: " + str(timeRed))
    elif (mes.find('yellow') != -1):
        timeYellow = int(mes.split(' ',1)[1])
        print("Time yellow: " + str(timeYellow))
    elif (mes.find('green') != -1):
        timeGreen = int(mes.split(' ',1)[1])
        print("Time green: " + str(timeGreen))
    else:
        pass

def setState(mes):
    global systemState, currentTime, timeGreen, timeRed, lightState
    if (mes.find('auto') != -1):
        systemState = 'auto'
        if (lightState == "green-red"):
            currentTime = timeGreen
        if (lightState == "red-green"):
            currentTime = timeRed
    elif (mes.find('manual') != -1):
        systemState = 'manual'
    elif (mes.find('emergency') != -1):
        systemState = 'emergency'
    else:
        pass
    mqttc.publish("current", "System-state: " + systemState)

def systemSet(client, obj, msg):
    global changeFlag
    print("Message arrived: " + str(msg.payload) + " in topic " + msg.topic)
    if      (str(msg.payload).find("Set-system-state") != -1):
        setState(str(msg.payload))
    elif    (str(msg.payload).find("Set-time") != -1):
        setTime(str(msg.payload))
    elif    (str(msg.payload).find("Change-light") != -1):
        changeFlag = True
    else:
        pass

def systemStateUpdate():
    global systemState
    if (systemState == 'auto'):
        lightStateUpdateAuto()
    elif (systemState == 'manual'):
        lightStateUpdateManual()
    elif (systemState == 'emergency'):
        lightStateUpdateEmergency()
    else:
        pass

def lightStateUpdateAuto():
    global lightState, currentTime, timeRed, timeGreen, timeYellow
    if (lightState == "red-green"):
        if (currentTime == timeYellow):
            lightState = "red-yellow"
            print(lightState)
            mqttc.publish("current", "Light-state: " + lightState)
    elif (lightState == "red-yellow"):
        if (currentTime == 0):
            lightState = "green-red"
            currentTime = timeGreen
            print(lightState)
            mqttc.publish("current", "Light-state: " + lightState)
    elif (lightState == "green-red"):
        if (currentTime == timeYellow):
            lightState = "yellow-red"
            print(lightState)
            mqttc.publish("current", "Light-state: " + lightState)
    elif (lightState == "yellow-red"):
        if (currentTime == 0):
            lightState = "red-green"
            currentTime = timeRed
            print(lightState)
            mqttc.publish("current", "Light-state: " + lightState)
    else:
        pass
    mqttc.publish("current", "Current-time: " + str(currentTime))
    print(currentTime)
    time.sleep(1)
    currentTime -= 1

def initSystem():
    global systemState, lightState, timeRed, timeYellow, timeGreen, currentTime
    timeRed = 10
    timeYellow = 3
    timeGreen = 10
    systemState = 'auto'
    lightState = "red-green"
    currentTime = timeRed
    mqttc.publish("current", "System-state: " + systemState)
    mqttc.publish("current", "Light-state: " + lightState)

initSystem()

def lightStateUpdateManual():
    global currentTime, lightState, changeFlag
    if (lightState == "red-green"):
        if (changeFlag == True):
            changeFlag = False
            currentTime = timeYellow
            lightState = "red-yellow"
            print(lightState)
            mqttc.publish("current", "Light-state: " + lightState)
    elif (lightState == "red-yellow"):
        if (currentTime == 0):
            lightState = "green-red"
            print(lightState)
            mqttc.publish("current", "Light-state: " + lightState)
    elif (lightState == "green-red"):
        if (changeFlag == True):
            changeFlag = False
            currentTime = timeYellow
            lightState = "yellow-red"
            print(lightState)
            mqttc.publish("current", "Light-state: " + lightState)
    elif (lightState == "yellow-red"):
        if (currentTime == 0):
            lightState = "red-green"
            print(lightState)
            mqttc.publish("current", "Light-state: " + lightState)
    else:
        pass
    time.sleep(1)
    if (currentTime >= 0):
        mqttc.publish("current", "Current-time: " + str(currentTime))
        print(currentTime)
        currentTime -= 1

while True:
    mqttc.on_message = systemSet
    systemStateUpdate()
