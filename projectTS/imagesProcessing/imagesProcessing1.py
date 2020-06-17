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
from projectTS.socketIO.socket import transmitImagesAtNorthStreet
from projectTS.lib.timeDecision import timeDecision

logger = logging.getLogger('projectTS.imagesProcessing.imagesProcessing1')

config = configparser.ConfigParser()
config.read('config.ini')

street1Conf = config['STREET-1']
cameraURL = street1Conf['camera']
xBegin = int(street1Conf['xBegin'])
xEnd = int(street1Conf['xEnd'])
yBegin = int(street1Conf['yBegin'])
yEnd = int(street1Conf['yEnd'])
pixelBlock = int(street1Conf['pixelBlock'])

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

def onImagesProcessing1(stop_event):
    logger.info('on Images Processing')

    street1 = timeDecision(xBegin, xEnd, yBegin, yEnd, 
    pixelBlock, deltaGray, timeToCapture, 
    isWriteImage=isWriteImage, pathToStoreImg=pathToStoreImg)
    thread3 = threading.Thread(target=trafficDensityAnalysis, args=(street1, stop_event, ))
    thread3.start()
    cap = cv2.VideoCapture(cameraURL, cv2.CAP_FFMPEG)
    while not stop_event.wait(0):
        ret, frame = cap.read()
        onStreamStreet(frame)
        street1.frame = frame

def onStreamStreet(frame):
    frame = cv2.resize(frame, (711, 400))
    buffer = cv2.imencode('.jpg', frame)
    frameEncode = base64.b64encode(buffer[1])
    frameText = frameEncode.decode('utf-8')
    # transmitImagesAtNorthStreet(frameText)

def trafficDensityAnalysis(street, stop_event):
    logger.info('Traffic density analysis at street 1 is running ')

    isBegin = True
    while not stop_event.wait(0):
        if (isBegin):
            isBegin = False
            vals.timeGreenFlexible = 20
            logger.info('Init time green %s', vals.timeGreenFlexible)
        else:
            if ((vals.lightStatus[streetEnum.street1.value] == 'yellow') and \
                (vals.timeLight[streetEnum.street1.value] == 0)):
                logger.info('Traffic density analysis at %s is running', streetEnum.street1.name)
                vals.timeGreenFlexible = street.timeGreen()
                logger.info('Time green at %s : %s', streetEnum.street1.name, vals.timeGreenFlexible)
            else:
                pass
        time.sleep(1)