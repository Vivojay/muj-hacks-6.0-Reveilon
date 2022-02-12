import cv2
import time
import numpy as np
import HandTrackingModule as htm
import math
import os
import subprocess as sp

# cd to Working Directory
cur_dir = os.path.dirname(os.path.realpath(__file__))
os.chdir(cur_dir)

################################
wCam, hCam = 640, 480
################################

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0

detector = htm.handDetector(detectionCon=0.7)

last_letter = None


lengths_reference = {
    'a': {
        "nodes": ((8,5), (20,0), (16,0), (12,0)),
        "dists": (90, 90, 90, 85),
        "checks": (0, 0, 0, 1),
    },

    'b': {
        "nodes": ((8,4), (12,8), (16,12)),
        "dists": (30, 30, 30),
        "checks": (0, 0, 0),
    },
    'c': {
        "nodes": ((8,5),(12,9),(4,1),(16,0),(20,0)),
        "dists": (75, 75, 75, 100, 100),
        "checks": (0, 0, 0, 1),
    },
    'd': {
        "nodes": ((8,5), (12,9), (16,13), (20,17), (5,4)),
        "dists": (90, 90, 90, 85),
        "checks": (0, 0, 0, 1),
    },
}


def write_letter(letter):
    with open("letter", 'w', encoding='utf-8') as file:
        file.write(letter)

def letter_event(letter):
    global last_letter
    if last_letter != letter:
        print(letter)
        last_letter = letter
        write_letter(letter)

while True:
    _, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)
    if len(lmList) != 0:

        def lengthfunc(i, j):
            x101, y101 = lmList[i][1], lmList[i][2]
            x505, y505 = lmList[j][1], lmList[j][2]
            # cx8, cy8 = (x101 + x505) // 2, (y101 + y505) // 2
            length100 = math.hypot(x101 - x505, y101 - y505)
            direction = math.tan(x101 - x505)
            return length100, direction

        # # LETTER H
        # lengthh1, _ = lengthfunc(8,5)
        # lengthh2, _ = lengthfunc(12,0)
        # # lengthh3, _ = lengthfunc(4,1)
        # lengthh4, _ = lengthfunc(16,0)
        # lengthh5, _ = lengthfunc(20,0)
        # lengthh6, _ = lengthfunc(12,8)

        # if (lengthh1>75 and lengthh2>100 and lengthh4 < 100 and lengthh5 < 100 and lengthh6 < 25):
        #     letter_event('H')

        # LETTER L
        lengthl1, _ = lengthfunc(8,5)
        lengthl2, _ = lengthfunc(20,0)
        lengthl3, _ = lengthfunc(16,0)
        lengthl4, _ = lengthfunc(12,0)

        if (lengthl4 < 90 and lengthl3 < 90 and lengthl2 < 90 and lengthl1 > 85):
            letter_event('L')

        # LETTER O
        lengtho1, _ = lengthfunc(8,4)
        lengtho2, _ = lengthfunc(12,8)
        lengtho3, _ = lengthfunc(16,12)
        # lengtho4, _ = lengthfunc(20,4)

        if (lengtho1<15 and lengtho2<30 and lengtho3<30):
            letter_event('O')

        # LETTER V
        lengthv1, _ = lengthfunc(8,5)
        lengthv2, _ = lengthfunc(12,0)
        lengthv3, _ = lengthfunc(4,1)
        lengthv4, _ = lengthfunc(16,0)
        lengthv5, _ = lengthfunc(20,0)

        if (lengthv1>75 and lengthv2>100 and lengthv3>75 and lengthv4 < 100 and lengthv5 < 100):
            letter_event('V')

        # LETTER E
        lengthe1, _ = lengthfunc(8,5)
        lengthe2, _ = lengthfunc(12,9)
        lengthe3, _ = lengthfunc(16,13)
        lengthe4, _ = lengthfunc(20,17)
        # lengthe5, _ = lengthfunc(5,4)
        lengthe6, _ = lengthfunc(8,4)

        if (lengthe1<20 and lengthe2<20 and lengthe3<20 and lengthe4<20 and lengthe6>15):
            letter_event('E')

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img,
                f'FPS: {int(fps)}',
                (40, 50),
                cv2.FONT_HERSHEY_COMPLEX,
                1,
                (255, 0, 0),
                3)
    # cv2.imshow("Img", img)
    # if KeyboardInterrupt:
    #     break
