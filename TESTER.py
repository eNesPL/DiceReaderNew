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
        frame_blurred = cv2.medianBlur(frame, 9)
        imgray = cv2.cvtColor(frame_blurred, cv2.COLOR_BGR2GRAY)
        th, im_gray = cv2.threshold(imgray, 128, 192, cv2.THRESH_OTSU)
        # --
        blobs = detector.detect(im_gray)
        reading = len(blobs)
        print(f"TEST:{reading}")
        a = addReadings(reading)
        if(a!=0):
            print("WIN: "+str(a))
            return a
        else:
            print(a)

