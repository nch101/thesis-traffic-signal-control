import cv2
import numpy as np
import time

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

    def grayImageToBlockGrayImage(self, frame):
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cropImage = image[self.yBegin:self.yEnd, self.xBegin:self.xEnd]
        width, height = cropImage.shape
        # if (self.isWriteImage):
        #     cv2.imwrite(self.pathToStoreImg + time.ctime(time.time()) + '- raw-image' + '.png', image)
        #     cv2.imwrite(self.pathToStoreImg + time.ctime(time.time()) + '- crop-image' + '.png', cropImage)

        for i in range(0, width, self.pixelBlock):
            for j in range(0, height, self.pixelBlock):
                cropImage[i:i+self.pixelBlock, j:j+self.pixelBlock] = np.mean(cropImage[i:i+self.pixelBlock, j:j+self.pixelBlock])
        return cropImage

    def onSubBlockGrayImage(self, inputImg1, inputImg2):
        nBlock = 0
        ndBlock = 0
        time.sleep(self.timeToCapture)
        image1 = self.grayImageToBlockGrayImage(inputImg1)
        time.sleep(self.timeToCapture)
        image2 = self.grayImageToBlockGrayImage(inputImg2)
        
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
            cv2.imwrite(self.pathToStoreImg + time.ctime(time.time()) + '- block-image1' + '.png', image1)
            cv2.imwrite(self.pathToStoreImg + time.ctime(time.time()) + '- block-image2' + '.png', image2)
            cv2.imwrite(self.pathToStoreImg + time.ctime(time.time()) + '- black-image' + '.png', blackImage)

        print('ndBlock: ', ndBlock, 'nBlock: ', nBlock, 'rate: ', ndBlock/nBlock*100)
        return nBlock, ndBlock

    def trafficDensityAnalysis(self, image1, image2):
        nBlock, ndBlock = self.onSubBlockGrayImage(image1, image2)
        rate = (ndBlock/nBlock)*100

        if (rate >= 0 and rate < 7):
            timeGreen = 25
            state = 'very-low'
        elif (rate >= 7 and rate < 15):
            timeGreen = 5/3*rate + 40/3
            state = 'low'
        elif (rate >= 15 and rate < 25):
            timeGreen = 5/3*rate + 40/3
            state = 'medium'
        elif (rate >= 25 and rate < 30):
            timeGreen = 5/3*rate + 40/3
            state = 'high'
        elif (rate >= 30 and rate <= 100):
            timeGreen = 80
            state = 'very-high'

        return int(timeGreen), int(rate), state

northStreet = timeDecision(648, 1093, 297, 683, 10, 50, 0.5, True)
print('Running..')

for i in range (0, 6):
    for j in range (i+1, 7):
        print(i, j)
        raw1 = cv2.imread('raw-image' + str(i) + '.png')
        raw2 = cv2.imread('raw-image' + str(j) + '.png')
        print(northStreet.trafficDensityAnalysis(raw1, raw2))