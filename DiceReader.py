import random
from time import sleep

import cv2
import numpy as np
from collections import deque
#import PiUi as ui
from sklearn import cluster

import Config
from Config import config


def returnCameraIndexes():
    # checks the first 10 indexes.
    index = 0
    arr = []
    i = 10
    while i > 0:
        cap = cv2.VideoCapture(index)
        if cap.read()[0]:
            arr.append(index)
            cap.release()
        index += 1
        i -= 1
    return arr

def readDice():
    print(config.Camera)
    if(config.Camera!="Remote_Camera"):
        return readDiceWithCam(config.Camera)
    else:
        print(config.RemoteCamera)
        return readDiceWithCam(config.RemoteCamera)

def readDiceWithCam(cam):
    return 6
def readDiceWithCam2(cam):
    # parametry detektora
    print(cam)
    params = cv2.SimpleBlobDetector_Params()  # declare filter parameters.
    params.filterByArea = True
    params.filterByCircularity = True
    params.filterByInertia = True
    params.minThreshold = 5
    params.maxThreshold = 200
    params.minArea = 20
    params.minCircularity = 0.3
    params.minInertiaRatio = 0.5
    cap = cv2.VideoCapture(cam)
    cap.set(15, -4)  # '15' references video's exposure. '-4' sets it.
    detector = cv2.SimpleBlobDetector_create(params)  # create a blob detector object.

    counter = 0  # script will use a counter to handle FPS.
    readings = deque([ 0, 0 ], maxlen=10)  # lists are used to track the number of pips.
    display = deque([ 0, 0 ], maxlen=10)
    while True:
        cleared=False
        ret, frame = cap.read()
        #--
        imgray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(imgray, 127, 255, 0)
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cv2.imshow("TE",imgray)
        imgg = cv2.drawContours(imgray, contours, -1, (0, 255, 0), 3)
        cv2.imshow("TE2", imgg)
        #--
        blobs = detector.detect(frame)
        reading = len(blobs)
        print(f"TEST:{reading}")
        if counter % 5 == 0:
            reading = len(blobs)
            readings.append(reading)
            if(reading != 0):
                cleared=True

            if(cleared):
                if readings[ -1 ] == readings[ -2 ] == readings[ -3 ]:
                    display.append(readings[ -1 ])
                if display[ -1 ] == display[ -2 ] and display[ -1 ] != 0:
                    msg = f"{display[ -1 ]}\n****"
                    print(msg)
                    return display[ -1 ]

        counter += 1

