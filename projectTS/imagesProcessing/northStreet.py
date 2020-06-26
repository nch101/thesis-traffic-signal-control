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
from projectTS.lib.estimatedTimeGreen import timeDecision

logger = logging.getLogger('projectTS.imagesProcessing.northStreet')

config = configparser.ConfigParser()
config.read('config.ini')

streetConf = config['NORTH-STREET']
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
    northStreet = 3
    westStreet = 2
    southStreet = 1
    eastStreet = 0

def northStreet(stop_event):
    logger.info('on Images Processing')

    northStreet = timeDecision(xBegin, xEnd, yBegin, yEnd, 
    pixelBlock, deltaGray, timeToCapture, 
    isWriteImage=isWriteImage, pathToStoreImg=pathToStoreImg)
    thread = threading.Thread(target=trafficDensityAnalysis, args=(northStreet, stop_event, ))
    thread.start()
    cap = cv2.VideoCapture(cameraURL, cv2.CAP_FFMPEG)
    # cap = cv2.VideoCapture(0)
    while not stop_event.wait(0):
        ret, frame = cap.read()
        onStreamStreet(frame)
        northStreet.frame = frame

def onStreamStreet(frame):
    if vals.isTransmitWestStreetOff:
        vals.isTransmitNorthStreetOff = False
        frame = cv2.resize(frame, (711, 400))
        buffer = cv2.imencode('.jpg', frame)
        frameEncode = base64.b64encode(buffer[1])
        frameText = frameEncode.decode('utf-8')
        # transmitImagesAtNorthStreet(frameText)
        vals.isTransmitNorthStreetOff = True

def trafficDensityAnalysis(street, stop_event):
    try:
        logger.info('Traffic density analysis at street 1 is running ')

        isBegin = True
        while not stop_event.wait(0):
            if (isBegin):
                isBegin = False
                vals.timeGreenFlexibleNS = 20
                logger.info('Init time green %s', vals.timeGreenFlexibleNS)
            else:
                if ((vals.lightStatus[streetEnum.northStreet.value] == 'yellow') and \
                    (vals.timeLight[streetEnum.northStreet.value] == 0)):
                    logger.info('Traffic density analysis at %s is running', streetEnum.northStreet.name)
                    vals.timeGreenFlexibleNS, vals.rateNS, vals.stateNS = street.trafficDensityAnalysis()
                    logger.info('State %s, rate %s', vals.stateNS, vals.rateNS)
                    logger.info('Time green at %s : %s', streetEnum.northStreet.name, vals.timeGreenFlexibleNS)
                else:
                    pass
            time.sleep(1)
    except Exception as e:
        logger.error('Something is wrong: %s', e)