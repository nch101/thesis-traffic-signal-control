# ** traffic density analysis **
# * Author: Nguyen Cong Huy
# ******************************

# - *- coding: utf- 8 - *-
import os
os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;udp"

import logging
import configparser

from projectTS.lib.timeDecision import timeDecision
import projectTS.vals as vals

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
    while not stop_event.wait(0):
        if (vals.lightStatus[0] == 'red'):
            street1.timeGreen()