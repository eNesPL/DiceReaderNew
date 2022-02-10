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
        return readDiceWithCam(config.Camera,False)
    else:
        print(config.RemoteCamera)
        return readDiceWithCam(config.RemoteCamera,True)

def readDiceWithCam2(cam):
    return 6
def readDiceWithCam(cam,is_ip):
    params = cv2.SimpleBlobDetector_Params()
    params.filterByArea = True
    params.filterByCircularity = True
    params.filterByInertia = True
    params.minArea = 100
    params.minCircularity = 0.7
    params.minInertiaRatio = 0.7
    if(not is_ip):
        cap = cv2.VideoCapture(int(cam))
    else:
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
        blank = np.zeros((1, 1))
        found = cv2.drawKeypoints(frame, blobs, blank, (0, 0, 255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
        found = cv2.resize(found, (960, 540))
        cv2.imshow('blobs using default parameters', found)
        cv2.waitKey(5)
        reading = len(blobs)
        answer = addReadings(reading)
        if(answer!=0 and answer<7):
            print("WIN: "+str(answer))
            cv2.waitKey(100)
            cv2.destroyAllWindows()
            return answer

