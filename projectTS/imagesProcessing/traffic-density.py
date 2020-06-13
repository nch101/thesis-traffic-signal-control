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
    street1 = ['images/demo1.png', 'images/demo5.png']
    # street2 = ['images/demo1.png', 'images/demo3.png']
    start_time = time.time()
    img1 = blockImage(street1[0], yBegin, yEnd, xBegin, xEnd)
    img2 = blockImage(street1[1], yBegin, yEnd, xBegin, xEnd)
    nBlock1, ndBlock1 = densityAnalysis(img1, img2)

    # img3 = blockImage(street2[0], yBegin, yEnd, xBegin, xEnd)(
    # img4 = blockImage(street2[1], yBegin, yEnd, xBegin, xEnd)
    # nBlock2, ndBlock2 = densityAnalysis(img3, img4)
    print(nBlock1, ndBlock1)
    rate = ndBlock1/nBlock1
    print('Ti le', (rate*100))
    # print('Ti le 2', (ndBlock2/nBlock1*100))

    print('Time green', int(trafficDensityAnalysis(rate)))
    
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

def densityAnalysis(image1, image2, deltaGrayLevel=40):
    nBlock = 0
    ndBlock = 0
    width, height = image1.shape
    blackImage = np.zeros((width, height), np.uint8)
    for i in range(0, width, pixel):
        for j in range(0, height, pixel):
            nBlock += 1
            deltaGray = np.mean(image2[i:i+pixel, j:j+pixel] - image1[i:i+pixel, j:j+pixel])
            if (deltaGray >= deltaGrayLevel and deltaGray <= (255-deltaGrayLevel)):
                ndBlock += 1
                blackImage[i:i+pixel, j:j+pixel] = 255
    cv2.imshow('result', blackImage)
    return nBlock, ndBlock

def trafficDensityAnalysis(rate):
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

    return timeDecision(u1, u2, trafficState1, trafficState2)

def deFuzzy(u, state):
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

def timeDecision(u1, u2, trafficState1, trafficState2):
    if (trafficState1 == None):
        timeGreen = deFuzzy(u2, trafficState2)/u2
    elif (trafficState2 == None):
        timeGreen = deFuzzy(u1, trafficState1)/u1
    else:
        timeGreen = (deFuzzy(u1, trafficState1) + deFuzzy(u2, trafficState2))/(u1+u2)
    return timeGreen

main()