# ** traffic density analysis **
# * Author: Nguyen Cong Huy
# ******************************

# - *- coding: utf- 8 - *-
import os
os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;udp"

import logging
import configparser
import time

from projectTS.lib.timeDecision import timeDecision
import projectTS.vals as vals

import enum
class street(enum.Enum):
    street1 = 0
    street2 = 1
    street3 = 2
    street4 = 3

logger = logging.getLogger('projectTS.imagesProcessing.trafficDensityAnalysis')

config = configparser.ConfigParser()
config.read('config.ini')

street1Conf = config['STREET-1']
cameraURL = street1Conf['camera']
xBegin1 = int(street1Conf['xBegin'])
xEnd1 = int(street1Conf['xEnd'])
yBegin1 = int(street1Conf['yBegin'])
yEnd1 = int(street1Conf['yEnd'])
pixelBlock1 = int(street1Conf['pixelBlock'])

default = config['DEFAULT']
deltaGray = int(default['deltaGray'])
timeToCapture = int(default['timeToCapture'])

def trafficDensityAnalysis(stop_event):
    logger.info('traffic density analysis is running...')
    street1 = timeDecision(cameraURL, xBegin1, xEnd1, yBegin1, yEnd1, pixelBlock1, deltaGray, timeToCapture)
    isBegin = True
    while not stop_event.wait(0):
        if ((vals.lightStatus[street.street1.value] == 'yellow') and (vals.timeLight[street.street1.value] == 1)):
            logger.info('Traffic density analysis at %s is running', street.street1.name)
            vals.timeGreenFlexible = street1.timeGreen()
            logger.info('Time green FCL %s', vals.timeGreenFlexible)
        elif ((vals.lightStatus[street.street2.value] == 'yellow') and (vals.timeLight[street.street2.value] == 1)):
            logger.info('Traffic density analysis at %s is running', street.street2.name)
            vals.timeGreenFlexible = vals.timeGreen[street.street2.value]
            logger.info('Time green FCL %s', vals.timeGreenFlexible)
        elif (isBegin):
            isBegin = False
            vals.timeGreenFlexible = vals.timeGreen[street.street1.value]
            logger.info('Time green FCL %s', vals.timeGreenFlexible)
        else:
            pass
        time.sleep(0.5)