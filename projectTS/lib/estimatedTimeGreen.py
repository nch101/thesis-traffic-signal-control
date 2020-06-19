import os
os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;udp"
import logging

import cv2
import numpy as np
import time

logger = logging.getLogger('projectTS.lib.estimatedTimeGreen')

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
            cv2.imwrite(self.pathToStoreImg + time.ctime(time.time()) + '- image1' + '.png', image1)
            cv2.imwrite(self.pathToStoreImg + time.ctime(time.time()) + '- image2' + '.png', image2)
            cv2.imwrite(self.pathToStoreImg + time.ctime(time.time()) + '- black-image' + '.png', blackImage)

        logger.info('ndBlock: %s, nBlock: %s, rate: %s', ndBlock, nBlock, ndBlock/nBlock*100)
        return nBlock, ndBlock

    def trafficDensityAnalysis(self):
        nBlock, ndBlock = self.onSubBlockGrayImage()
        rate = (ndBlock/nBlock)*100

        if (rate >= 0 and rate < 30):
            timeGreen = 25
            state = 'very-low'
        elif (rate >= 30 and rate < 45):
            timeGreen = 11/12*rate - 5/2
            state = 'low'
        elif (rate >= 45 and rate < 75):
            timeGreen = 11/12*rate - 5/2
            state = 'medium'
        elif (rate >= 75 and rate < 90):
            timeGreen = 11/12*rate - 5/2
            state = 'high'
        elif (rate >= 90 and rate <= 100):
            timeGreen = 80
            state = 'very-high'

        return int(timeGreen), int(rate), state