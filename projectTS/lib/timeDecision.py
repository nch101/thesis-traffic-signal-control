import cv2
import numpy as np
import time

class timeDecision:
    def __init__(self, cameraIp, xBegin, xEnd, yBegin, yEnd, pixelBlock, deltaGrayLevel, timeToCapture):
        self.cameraIp = cameraIp
        self.xBegin = xBegin
        self.xEnd = xEnd
        self.yBegin = yBegin
        self.yEnd = yEnd
        self.pixelBlock = pixelBlock
        self.deltaGrayLevel = deltaGrayLevel
        self.timeToCapture = timeToCapture

        # self.__cap = cv2.VideoCapture(cameraIp)

    def captureVideo(self):
        cap = cv2.VideoCapture(self.cameraIp)
        ret, frame = cap.read()
        cap.release()
        cv2.destroyAllWindows()
        return frame

    def grayImageToBlockGrayImage(self):
        image = cv2.cvtColor(self.captureVideo(), cv2.COLOR_BGR2GRAY)
        cropImage = image[self.yBegin:self.yEnd, self.xBegin:self.xEnd]
        width, height = cropImage.shape
        for i in range(0, width, self.pixelBlock):
            for j in range(0, height, self.pixelBlock):
                cropImage[i:i+self.pixelBlock, j:j+self.pixelBlock] = np.mean(cropImage[i:i+self.pixelBlock, j:j+self.pixelBlock])
        return cropImage

    def onSubBlockGrayImage(self):
        nBlock = 0
        ndBlock = 0
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
        
        cv2.imwrite('image-temp/image1.png', image1)
        cv2.imwrite('image-temp/image2.png', image2)
        cv2.imwrite('image-temp/black-image.png', blackImage)
        return nBlock, ndBlock, blackImage

    def __trafficDensityAnalysis(self):
        nBlock, ndBlock, blackImage = self.onSubBlockGrayImage()
        print(nBlock, ndBlock)
        rate = ndBlock/nBlock

        if (rate >= 0 and rate < 0.2):
            u1 = -5*rate + 1
            trafficState1 = 'rv'
        elif (rate >= 0.3 and rate < 0.5):
            u1 = 5*rate - 3/2
            trafficState1 = 'tb'
        elif (rate >= 0.5 and rate < 0.7):
            u1 = -5*rate + 7/2
            trafficState1 = 'tb'
        elif (rate >= 0.8 and rate <= 1):
            u1 = 5*rate -4
            trafficState1 = 'rd'
        else:
            u1 = 0
            trafficState1 = None

        if (rate >= 0.1 and rate < 0.25):
            u2 = 20/3*rate - 2/3
            trafficState2 = 'v'
        elif (rate >= 0.25 and rate < 0.4):
            u2 = -20/3*rate + 8/3
            trafficState2 = 'v'
        elif (rate >= 0.6 and rate < 0.75):
            u2 = 20/3*rate - 4
            trafficState2 = 'd'
        elif (rate >= 0.75 and rate < 0.9):
            u2 = -20/3*rate + 6
            trafficState2 = 'd'
        else:
            u2 = 0
            trafficState2 = None

        return u1, u2, trafficState1, trafficState2

    def __deFuzzy(self, u, state):
        if (state == 'rv'):
            y = u*20
        elif (state == 'v'):
            y = u*30
        elif (state == 'tb'):
            y = u*50
        elif (state == 'd'):
            y = u*70
        elif (state == 'rd'):
            y = u*80
        else:
            y = 0
        return y

    def timeGreen(self):
        u1, u2, trafficState1, trafficState2 = self.__trafficDensityAnalysis()
        print(u1, u2, trafficState1, trafficState2)
        if (trafficState1 == None):
            timeGreen = self.__deFuzzy(u2, trafficState2)/u2
        elif (trafficState2 == None):
            timeGreen = self.__deFuzzy(u1, trafficState1)/u1
        else:
            timeGreen = (self.__deFuzzy(u1, trafficState1) + self.__deFuzzy(u2, trafficState2))/(u1+u2)
        
        return int(timeGreen)

# # Test timeDecision
# abc = timeDecision(0, 0, 480, 0, 640, 50, 50, 5)
# print('TimeGreen', abc.timeGreen())