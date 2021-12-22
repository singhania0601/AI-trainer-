import cv2
import numpy as np
import mediapipe as mp
import time
import poseEstimationModule as pm
cap = cv2.VideoCapture('PoseVideos/5.mp4')
cTime =0
pTime = 0
count = 0
dir = 0
detector = pm.poseDetector()
while True:
    success, img=cap.read()
    img = detector.findPos(img,False)
    LmList = detector.findPosition(img,False)
    detector.findAngle(img,12,14,16)
    angle = detector.findAngle(img, 11, 13, 15)
    per = np.interp(angle,(200,320),(0,100))
    bar = np.interp(angle, (200, 320), (650, 100))
    # print(angle,per)
    color = (255, 0, 255)
    if per == 100:
        color = (0, 255, 0)
        if dir == 0:
            count += 0.5
            dir = 1
    if per == 0:
        color = (0, 255, 0)
        if dir == 1:
            count += 0.5
            dir = 0
    print(count)
    cv2.rectangle(img, (550, 100), (590, 650), color, 3)
    cv2.rectangle(img, (550, int(bar)), (590, 650), color, cv2.FILLED)
    cv2.putText(img, f'{int(per)} ', (540, 75), cv2.FONT_HERSHEY_PLAIN, 4,
                color, 4)

    # Draw Curl Count
    cv2.rectangle(img, (0, 250), (200, 450), (200, 162, 200), cv2.FILLED)
    cv2.putText(img, str(int(count)), (45, 400), cv2.FONT_ITALIC, 5,
                (255, 25, 179), 25)


    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (50, 100), cv2.FONT_HERSHEY_PLAIN, 5,
                (255, 0, 0), 5)

    cv2.imshow("video", img)
    cv2.waitKey(1)