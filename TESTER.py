import cv2
import numpy as np
from collections import deque
import json
from sklearn import cluster
readings = [0,0,0]
def allTheSame(items):

    if(items.__contains__(0)):
        return False
    return all(x == items[0] for x in items)
def addReadings(value):
    readings.pop()
    readings.insert(0,value)
    print(readings)
    if(allTheSame(readings)):
        return readings[0]
    else:
        return 0
def readDice():
    params = cv2.SimpleBlobDetector_Params()
    params.filterByArea = True
    params.filterByCircularity = True
    params.filterByInertia = True
    params.minThreshold = 100
    params.maxThreshold = 200
    params.minArea = 100
    params.minCircularity = 0.5
    params.minInertiaRatio = 0.5
    cap = cv2.VideoCapture("http://192.168.0.209:8080/video")
    detector = cv2.SimpleBlobDetector_create(params)
    while True:
        ret, frame = cap.read()
        # --
        imS = cv2.resize(frame, (960, 540))
        cv2.imshow("test", imS)
        frame_blurred = cv2.medianBlur(frame, 9)
        imS = cv2.resize(frame_blurred, (960, 540))
        cv2.imshow("test2", imS)

        imgray = cv2.cvtColor(frame_blurred, cv2.COLOR_BGR2GRAY)
        imS = cv2.resize(imgray, (960, 540))
        cv2.imshow("test3", imS)
        th, thresh = cv2.threshold(imgray, 70, 255, cv2.THRESH_BINARY)
        imS = cv2.resize(thresh, (960, 540))
        cv2.imshow("test4", imS)
        frame_blurred = cv2.medianBlur(thresh, 9)
        imS = cv2.resize(frame_blurred, (960, 540))
        cv2.imshow("test5", imS)
        # --
        cv2.waitKey(1)
        blobs = detector.detect(thresh)
        reading = len(blobs)
        print(f"TEST:{reading}")
        a = addReadings(reading)
        if(a!=0):
            print("WIN: "+str(a))
            #return a
        else:
            print(a)


readDice()