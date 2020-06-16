import os
os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;udp"
import logging

import cv2
import numpy as np
import time

logger = logging.getLogger('projectTS.lib.timeDesition')

class timeDecision:
    """ Traffic density analysis use fuzzy control logic to decide time green
        ** Crop image **
        @param xBegin: Pixel x begins
        @param xEnd: Pixel x ends
        @param yBegin: Pixel y begins
        @param yEnd: Pixel y ends
        ****************

        @param pixelBlock: Size of block (pixelBlock x pixelBlock)
        @param deltaGrayLevel: Gray level difference of 2 images
        @param timeToCapture: Time interval between 2 consecutive shots
        @param isWriteImage; default False. Whether write image or not
        @param pathToStoreImg: default ''. Path to store image
    """
    def __init__(self, xBegin, xEnd, yBegin, yEnd, 
    pixelBlock, deltaGrayLevel, timeToCapture, 
    isWriteImage=False, pathToStoreImg=''):
        self.xBegin = xBegin
        self.xEnd = xEnd
        self.yBegin = yBegin
        self.yEnd = yEnd
        self.pixelBlock = pixelBlock
        self.deltaGrayLevel = deltaGrayLevel
        self.timeToCapture = timeToCapture
        self.isWriteImage = isWriteImage
        self.pathToStoreImg = pathToStoreImg
        self.frame = np.ones((1,1,1), dtype=np.uint8)

    def grayImageToBlockGrayImage(self):
        image = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
        cropImage = image[self.yBegin:self.yEnd, self.xBegin:self.xEnd]
        width, height = cropImage.shape
        for i in range(0, width, self.pixelBlock):
            for j in range(0, height, self.pixelBlock):
                cropImage[i:i+self.pixelBlock, j:j+self.pixelBlock] = np.mean(cropImage[i:i+self.pixelBlock, j:j+self.pixelBlock])
        return cropImage

    def onSubBlockGrayImage(self):
        nBlock = 0
        ndBlock = 0
        time.sleep(self.timeToCapture)
        image1 = self.grayImageToBlockGrayImage()
        time.sleep(self.timeToCapture)
        image2 = self.grayImageToBlockGrayImage()
        
        width, height = image1.shape
        blackImage = np.zeros((width, height), np.uint8)
        for i in range(0, width, self.pixelBlock):
            for j in range(0, height, self.pixelBlock):
                nBlock += 1
                deltaGray = np.mean(image2[i:i+self.pixelBlock, j:j+self.pixelBlock] - image1[i:i+self.pixelBlock, j:j+self.pixelBlock])
                if (deltaGray >= self.deltaGrayLevel and deltaGray <= (255-self.deltaGrayLevel)):
                    ndBlock += 1
                    blackImage[i:i+self.pixelBlock, j:j+self.pixelBlock] = 255
        if (self.isWriteImage):
            cv2.imwrite(self.pathToStoreImg + time.ctime(time.time()) + 'image1' + '.png', image1)
            cv2.imwrite(self.pathToStoreImg + time.ctime(time.time()) + 'image2' + '.png', image2)
            cv2.imwrite(self.pathToStoreImg + time.ctime(time.time()) + 'black-image' + '.png', blackImage)

        logger.info('ndBlock: %s, nBlock: %s, rate: %s', ndBlock, nBlock, ndBlock/nBlock*100)
        return nBlock, ndBlock

    def __trafficDensityAnalysis(self):
        nBlock, ndBlock = self.onSubBlockGrayImage()
        rate = ndBlock/nBlock

        if (rate >= 0 and rate < 0.2):
            u1 = -5*rate + 1
            trafficState1 = 'very-low'
        elif (rate >= 0.3 and rate < 0.5):
            u1 = 5*rate - 3/2
            trafficState1 = 'medium'
        elif (rate >= 0.5 and rate < 0.7):
            u1 = -5*rate + 7/2
            trafficState1 = 'medium'
        elif (rate >= 0.8 and rate <= 1):
            u1 = 5*rate -4
            trafficState1 = 'very-high'
        else:
            u1 = 0
            trafficState1 = None

        if (rate >= 0.1 and rate < 0.25):
            u2 = 20/3*rate - 2/3
            trafficState2 = 'low'
        elif (rate >= 0.25 and rate < 0.4):
            u2 = -20/3*rate + 8/3
            trafficState2 = 'low'
        elif (rate >= 0.6 and rate < 0.75):
            u2 = 20/3*rate - 4
            trafficState2 = 'high'
        elif (rate >= 0.75 and rate < 0.9):
            u2 = -20/3*rate + 6
            trafficState2 = 'high'
        else:
            u2 = 0
            trafficState2 = None

        return u1, u2, trafficState1, trafficState2

    def __deFuzzy(self, u, state):
        if (state == 'very-low'):
            y = u*20
        elif (state == 'low'):
            y = u*30
        elif (state == 'medium'):
            y = u*50
        elif (state == 'high'):
            y = u*70
        elif (state == 'very-high'):
            y = u*80
        else:
            y = 0
        return y

    def timeGreen(self):
        u1, u2, trafficState1, trafficState2 = self.__trafficDensityAnalysis()
        logger.info('u1: %s, u2: %s, trafficState1: %s, trafficState2: %s', u1, u2, trafficState1, trafficState2)
        if (trafficState1 == None):
            timeGreen = self.__deFuzzy(u2, trafficState2)/u2
        elif (trafficState2 == None):
            timeGreen = self.__deFuzzy(u1, trafficState1)/u1
        else:
            timeGreen = (self.__deFuzzy(u1, trafficState1) + self.__deFuzzy(u2, trafficState2))/(u1+u2)
        
        return int(timeGreen)

# # # Test timeDecision
# abc = timeDecision('rtsp://localhost:8554', 0, 720, 0, 1280, 10, 50, 5)
# print('TimeGreen', abc.timeGreen())