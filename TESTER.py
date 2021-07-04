import cv2
import numpy as np
from sklearn import cluster

from Config import config

params = cv2.SimpleBlobDetector_Params()

detector = cv2.SimpleBlobDetector_create(params)
class v:
    Value = 240

def get_dice_from_blobs(blobs):
    X = []
    for b in blobs:
        pos = b.pt
        if pos != None:
            X.append(pos)

    X = np.asarray(X)

    if len(X) > 0:

        clustering = cluster.DBSCAN(eps=90, min_samples=0).fit(X)
        num_dice = max(clustering.labels_) + 1
        dice = []
        for i in range(num_dice):
            X_dice = X[clustering.labels_ == i]
            centroid_dice = np.mean(X_dice, axis=0)
            dice.append([len(X_dice), *centroid_dice])

        return dice

    else:
        return []


def overlay_info(frame, dice, blobs):

    for b in blobs:
        pos = b.pt
        r = b.size / 2

        cv2.circle(frame, (int(pos[0]), int(pos[1])),
                   int(r), (255, 0, 0), 2)


    for d in dice:

        textsize = cv2.getTextSize(
            str(d[0]), cv2.FONT_HERSHEY_PLAIN, 3, 2)[0]

        cv2.putText(frame, str(d[0]),
                    (int(d[1] - textsize[0] / 2),
                     int(d[2] + textsize[1] / 2)),
                    cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 2)

def threshold(img_in, value):
    img_out = img_in.copy()
    map, img_out = cv2.threshold(img_out, value, 255, cv2.THRESH_BINARY)
    return img_out

def onChange(value):
    v.Value = value


def most_frequent(List):
    return max(set(List), key = List.count)

def readDice():
    cap = cv2.VideoCapture(config.RemoteCamera)
    list_dice_roll = [ ]
    print("Start")
    diceR=0
    for i in range(0,10):
        ret, frame = cap.read()
        sum = 0
        frame_blurred = cv2.GaussianBlur(frame, (5, 5), 0)
        frame_gray = cv2.cvtColor(frame_blurred, cv2.COLOR_BGR2GRAY)
        frame_t = threshold(frame_gray, 187)
        blobs = detector.detect(frame_t)
        dice = get_dice_from_blobs(blobs)


        for num in dice:
            sum=sum+num[0]

        list_dice_roll.append(sum)
        avr = 0
        for i in list_dice_roll:
            avr = avr + i
    diceavr =int(avr/len(list_dice_roll))
    dicepop = most_frequent(list_dice_roll)
    print(dicepop)
    print(diceavr)
    print("Stop")
    cap.release()
    return diceR
