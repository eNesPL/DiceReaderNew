import random
from time import sleep

import cv2
import numpy as np
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
readings = [0,0,0]
def allTheSame(items):
    if(items.__contains__(0)):
        return False
    return all(x == items[0] for x in items)

def addReadings(value):
    readings.pop()
    readings.insert(0,value)
    if(allTheSame(readings)):
        return readings[0]
    else:
        return 0

def readDice():
    print(config.Camera)
    if(config.Camera!="Remote_Camera"):
        return readDiceWithCam(config.Camera)
    else:
        print(config.RemoteCamera)
        return readDiceWithCam(config.RemoteCamera)

def readDiceWithCam2(cam):
    return 6
def readDiceWithCam(cam):
    params = cv2.SimpleBlobDetector_Params()
    params.filterByArea = True
    params.filterByCircularity = True
    params.filterByInertia = True
    params.minThreshold = 100
    params.maxThreshold = 200
    params.minArea = 100
    params.minCircularity = 0.5
    params.minInertiaRatio = 0.5
    cap = cv2.VideoCapture(cam)
    detector = cv2.SimpleBlobDetector_create(params)
    while True:
        ret, frame = cap.read()
        # --
        frame_blurred = cv2.medianBlur(frame, 9)
        imgray = cv2.cvtColor(frame_blurred, cv2.COLOR_BGR2GRAY)
        th, im_gray = cv2.threshold(imgray, 128, 192, cv2.THRESH_OTSU)
        # --
        blobs = detector.detect(im_gray)
        reading = len(blobs)
        answer = addReadings(reading)
        if(answer!=0 and answer<7):
            print("WIN: "+str(answer))
            return answer
        else:
            print(answer)

