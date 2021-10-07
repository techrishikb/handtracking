import cv2
import mediapipe as mp
import time


class handDetector():
    def __init__(self,mode=False,maxhands = 2, detectioncon = 0.5, track_con = 0.5 ):
        self.mode = mode
        self.maxhands = maxhands
        self.detectioncon = detectioncon
        self.track_con = track_con


        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode,self.maxhands,self.detectioncon,self.track_con)
        self.mpDraw = mp.solutions.drawing_utils

    def findhands(self,img, draw = True):
        imgrgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgrgb)
        #print(results.multi_hand_landmarks)
        if self.results.multi_hand_landmarks:
            for hl in self.results.multi_hand_landmarks:
                self.mpDraw.draw_landmarks(img,hl, self.mpHands.HAND_CONNECTIONS)
        return img

    def findpositions(self,img,handNo=0, draw = True):
        lmlist = []
        if self.results.multi_hand_landmarks:
            myhand = self.results.multi_hand_landmarks[handNo]
            for id,hm in enumerate(myhand.landmark):
                #print(id,hm)
                h,w,c = img.shape
                cx,cy = int(hm.x*w),int(hm.y*h)
                #print(id,cx,cy)
                lmlist.append([id,cx,cy])
                #if id ==4:
                if draw:
                    cv2.circle(img,(cx,cy),15,(255,0,255),cv2.FILLED)
        return lmlist

def main():
    ctime = 0
    ptime = 0
    cap = cv2.VideoCapture(0)
    detector = handDetector()
    while True:
        success, img = cap.read()
        img = detector.findhands(img)
        lmlist = detector.findpositions(img)
        if len(lmlist)!= 0:
            print(lmlist[4])
        ctime = time.time()
        fps = 1 / (ctime - ptime)
        ptime = ctime

        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

        cv2.imshow("Image", img)
        cv2.waitKey(1)

if __name__=="__main__":
    main()