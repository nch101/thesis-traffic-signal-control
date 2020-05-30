# ********* image socket *********
# * Author: Nguyen Cong Huy
# *****************************

# - *- coding: utf- 8 - *-
import os
os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;udp"
import logging
import configparser
import time
import cv2
import base64
from projectTS.socketIO.socket import transmitImages

logger = logging.getLogger('projectTS.imagesProcessing.processStreet1')

config = configparser.ConfigParser()
config.read('config.ini')

street1Conf = config['STREET-1']
cameraURL = street1Conf['camera']

def onImagesProcessStreet1():
    logger.info('onImagesProcessStreet1 is running...')
    cap = cv2.VideoCapture(cameraURL, cv2.CAP_FFMPEG)
    ret, frame = cap.read()
    while ret:
        frame = cv2.resize(frame, (711, 400))
        buffer = cv2.imencode('.jpg', frame)
        frameEncode = base64.b64encode(buffer[1])
        frameText = frameEncode.decode('utf-8')
        transmitImages(frameText)
        ret, frame = cap.read()
        time.sleep(0.04)