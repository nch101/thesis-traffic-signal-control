# ** traffic density analysis **
# * Author: Nguyen Cong Huy
# ******************************

# - *- coding: utf- 8 - *-
import os
os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;udp"

# import logging
# import configparser
import cv2
import numpy as np
import time

# config = configparser.ConfigParser()
# config.read('config.ini')

# street1Conf = config['STREET-1']
# cameraURL = street1Conf['camera']

# cameraURL = 'rtsp://admin:test12345@192.168.100.14:554/onvif1'

pixel = 20
yBegin = 260
yEnd = 570

xBegin = 690
xEnd = 1070

def main():
    # cap = cv2.VideoCapture(cameraURL, cv2.CAP_FFMPEG)
    # ret, frame = cap.read()
    camerasArray = ['images/demo1.png', 'images/demo5.png']
    start_time = time.time()
    img1 = blockImage(camerasArray[0], yBegin, yEnd, xBegin, xEnd)
    img2 = blockImage(camerasArray[1], yBegin, yEnd, xBegin, xEnd)
    nBlock, ndBlock = densityAnalysis(img1, img2)
    print(nBlock, ndBlock)
    print('Ti le ', ((ndBlock/nBlock)*100))
    print("--- %s seconds ---" % (time.time() - start_time))
    while True:
        if cv2.waitKey(20) == 27:
            break

def blockImage(url, yBegin, yEnd, xBegin, xEnd):
    image = cv2.imread(url, cv2.IMREAD_GRAYSCALE)
    cropImage = image[yBegin:yEnd, xBegin:xEnd]
    cv2.imshow(url,cropImage)
    width, height = cropImage.shape
    for i in range(0, width, pixel):
        for j in range(0, height, pixel):
            cropImage[i:i+pixel, j:j+pixel] = np.mean(cropImage[i:i+pixel, j:j+pixel])
    return cropImage

def densityAnalysis(image1, image2, lowGrayLevel=50, highGrayLevel=205):
    nBlock = 0
    ndBlock = 0
    width, height = image1.shape
    blackImage = np.zeros((width, height), np.uint8)
    for i in range(0, width, pixel):
        for j in range(0, height, pixel):
            nBlock += 1
            deltaGray = np.mean(image2[i:i+pixel, j:j+pixel] - image1[i:i+pixel, j:j+pixel])
            if (deltaGray >= lowGrayLevel and deltaGray <= highGrayLevel):
                ndBlock += 1
                blackImage[i:i+pixel, j:j+pixel] = 255
    cv2.imshow('result', blackImage)
    return nBlock, ndBlock

main()