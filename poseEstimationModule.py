import cv2
import mediapipe as mp
import time
import math
class poseDetector():
    def __init__(self,mode=False,modelC = 1,smooth = True,enableS = False,Ss = True,detectionCon= 0.5,trackCon = 0.5):
        self.mode = mode
        self.modelC = modelC
        self.enableS = enableS
        self.Ss = Ss
        self.smooth = smooth
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        self.mpPose = mp.solutions.pose
        self.pose = self.mpPose.Pose(self.mode,self.modelC,self.smooth,self.enableS,self.Ss,self.detectionCon,self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils

    def findPos(self,img,draw = True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.pose.process(imgRGB)
        if self.results.pose_landmarks:
            if draw:
                self.mpDraw.draw_landmarks(img, self.results.pose_landmarks, self.mpPose.POSE_CONNECTIONS)
        return img


    def findPosition(self, img, draw = True):
        self.lmList = []
        if self.results.pose_landmarks:
            for id, lm in enumerate(self.results.pose_landmarks.landmark):
                h, w, c = img.shape
                # print(id, lm)
                cx, cy = int(lm.x * w), int(lm.y * h)
                self.lmList.append([id,cx,cy])
                if draw:
                    cv2.circle(img, (cx, cy), 5, (255, 0, 0), cv2.FILLED)
        return self.lmList
    def findAngle(self,img,p1,p2,p3,draw = True):
        x1,y1 = self.lmList[p1][1:]
        x2, y2 = self.lmList[p2][1:]
        x3, y3 = self.lmList[p3][1:]

        angle = math.degrees(math.atan2(y3-y2,x3-x2)-math.atan2(y1-y2,x1-x2))

        if angle<0:
            angle+=360

        if draw:
            cv2.line(img, (x1, y1), (x2, y2), (255, 255, 255), 3)
            cv2.line(img, (x3, y3), (x2, y2), (255, 255, 255), 3)
            cv2.circle(img, (x1, y1), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x1, y1), 15, (0, 0, 255), 2)
            cv2.circle(img, (x2, y2), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), 15, (0, 0, 255), 2)
            cv2.circle(img, (x3, y3), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x3, y3), 15, (0, 0, 255), 2)
            cv2.putText(img,str(int(angle)),(x1-50,y1-50),cv2.FONT_ITALIC,1,(45,5,54),2)

        return angle


def main():
    cap = cv2.VideoCapture('PoseVideos/3.mp4')
    cTime = 0
    pTime = 0
    detector = poseDetector()
    while True:
        success, img = cap.read()
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        img = detector.findPos(img,True)
        lmList = detector.findPosition(img)
        cv2.putText(img, str(int(fps)), (70, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
        cv2.imshow("video", img)
        cv2.waitKey(10)




if __name__ == "__main__":
    main()