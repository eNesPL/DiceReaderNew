import cv2
import numpy as np
from collections import deque


#parametry detektora
params = cv2.SimpleBlobDetector_Params()  # declare filter parameters.
params.filterByArea = True
params.filterByCircularity = True
params.filterByInertia = True
params.minThreshold = 10
params.maxThreshold = 200
params.minArea = 100
params.minCircularity = 0.3
params.minInertiaRatio = 0.5
cap = cv2.VideoCapture("http://192.168.0.150:8080/video")
cap.set(15, -4)  # '15' references video's exposure. '-4' sets it.
detector = cv2.SimpleBlobDetector_create(params)  # create a blob detector object.

counter = 0  # script will use a counter to handle FPS.
readings = deque([ 0, 0 ], maxlen=10)  # lists are used to track the number of pips.
display = deque([ 0, 0 ], maxlen=10)

while True:
    ret, frame = cap.read()
    frame = cv2.Canny(frame, 30, 255)
    blobs = detector.detect(frame)

    reading = len(blobs)
    print(f"TEST:{reading}")

    if counter % 10 == 0:
        reading = len(blobs)
        readings.append(reading)

        if readings[ -1 ] == readings[ -2 ] == readings[ -3 ]:
            display.append(readings[ -1 ])

        if display[ -1 ] != display[ -2 ] and display[ -1 ] != 0:
            msg = f"{display[ -1 ]}\n****"
            print(msg)

    counter += 1
