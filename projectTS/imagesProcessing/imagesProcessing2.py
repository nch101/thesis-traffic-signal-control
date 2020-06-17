# ********* images processing *********
# * Author: Nguyen Cong Huy
# *****************************

# - *- coding: utf- 8 - *-
import os
os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;udp"
import logging
import configparser
import time
import enum
import threading
import cv2
import base64
import projectTS.vals as vals
from projectTS.socketIO.socket import transmitImagesAtWestStreet
from projectTS.lib.timeDecision import timeDecision

logger = logging.getLogger('projectTS.imagesProcessing.imagesProcessing2')

config = configparser.ConfigParser()
config.read('config.ini')

streetConf = config['STREET-2']
cameraURL = streetConf['camera']
xBegin = int(streetConf['xBegin'])
xEnd = int(streetConf['xEnd'])
yBegin = int(streetConf['yBegin'])
yEnd = int(streetConf['yEnd'])
pixelBlock = int(streetConf['pixelBlock'])

default = config['DEFAULT']
deltaGray = int(default['deltaGray'])
timeToCapture = int(default['timeToCapture'])
isWriteImage = default['isWriteImage'].lower() in ['true', '1']
pathToStoreImg = default['pathToStoreImage']

class streetEnum(enum.Enum):
    street1 = 0
    street2 = 1
    street3 = 2
    street4 = 3

def onImagesProcessing2(stop_event):
    logger.info('on Images Processing')

    street2 = timeDecision(xBegin, xEnd, yBegin, yEnd, 
    pixelBlock, deltaGray, timeToCapture, 
    isWriteImage=isWriteImage, pathToStoreImg=pathToStoreImg)
    thread = threading.Thread(target=trafficDensityAnalysis, args=(street2, stop_event, ))
    thread.start()
    cap = cv2.VideoCapture(cameraURL, cv2.CAP_FFMPEG)
    while not stop_event.wait(0):
        ret, frame = cap.read()
        onStreamStreet(frame)
        street2.frame = frame

def onStreamStreet(frame):
    frame = cv2.resize(frame, (711, 400))
    buffer = cv2.imencode('.jpg', frame)
    frameEncode = base64.b64encode(buffer[1])
    frameText = frameEncode.decode('utf-8')
    # transmitImagesAtWestStreet(frameText)

def trafficDensityAnalysis(street, stop_event):
    logger.info('Traffic density analysis at street 2 is running ')

    isBegin = True
    while not stop_event.wait(0):
        if (isBegin):
            isBegin = False
            # vals.timeGreenFlexible = 20
            # logger.info('Init time green %s', vals.timeGreenFlexible)
        else:
            if ((vals.lightStatus[streetEnum.street2.value] == 'yellow') and \
                (vals.timeLight[streetEnum.street2.value] == 0)):
                logger.info('Traffic density analysis at %s is running', streetEnum.street2.name)
                vals.timeGreenFlexible = street.timeGreen()
                logger.info('Time green at %s : %s', streetEnum.street2.name, vals.timeGreenFlexible)
            else:
                pass
        time.sleep(1)