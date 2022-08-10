from enum import auto
from pickle import FALSE
from tkinter import LEFT, RIGHT
from turtle import down
import cv2
import numpy as py
import HandTrackingModule as hm
import time
import autopy as ap

from autopy.key import *
from autopy import *

wCam, hCam = 640, 480
frameR = 100 # Frame Reduction
smoothening = 9

pTime = 0
plocX, plocY = 0, 0
clocX, clocY = 0, 0


cap = cv2.VideoCapture(0)
cap.set(3, 640)#3 for width
cap.set(4, 480)#4 for height

detector = hm.handDetector(maxHands=1)
wScr, hScr = ap.screen.size()#screensize
# print(wScr,hScr)

while True:
    #1.Find the hand landmarks
    success, img = cap.read()
    img = detector.findHands(img)
    lmlist, bbox = detector.findPosition(img)
    #2.Get the tip index and middle fingers
    if len(lmlist)!=0:
        x1, y1 = lmlist[8][1:]
        x2, y2 = lmlist[12][1:]
        # print(x1,y1,x2,y2)
        #3.Check which finger is up
        fingers = detector.fingersUp()
        # print(fingers)
        # #4.Only Index Finger : movingmode
        cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR),
                        (255, 0, 255), 2)
        if fingers[1]==1 and fingers[2]==1:
            #5.Convert Coordinates
            x3 = py.interp(x1, (frameR, wCam - frameR), (0, wScr))
            y3 = py.interp(y1, (frameR, hCam - frameR), (0, hScr))
            
            #6.Smoothen Values
            clocX = plocX + (x3 - plocX) / smoothening
            clocY = plocY + (y3 - plocY) / smoothening

            #7.Move Mouse
            
            ap.mouse.move(wScr - clocX,clocY)
            cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
            plocX, plocY = clocX, clocY
            
        #8.Both index and mid are up:clickingmode
        # if fingers[1]==1 and fingers[2]==1:
            #9.Find distance between 
            
            #click leftmouse
            length, img, lineInfo = detector.findDistance(8, 12, img)
            if length < 40:
                cv2.circle(img, (lineInfo[4], lineInfo[5]),
                            15, (0, 255, 0), cv2.FILLED)
                #10.Click mouse if distance short
                ap.mouse.click(ap.mouse.Button.LEFT) 

#double click              
        if fingers[1]==0 and fingers[2]==1:
            #9.Find distance between Fingers
            # length, img, lineInfo = detector.findDistance(4, 8, img)
            # if length < 40:
            #     cv2.circle(img, (lineInfo[4], lineInfo[5]),
            #                 15, (0, 255, 0), cv2.FILLED)
            #     #10.Click mouse if distance short
            ap.mouse.click(ap.mouse.Button.LEFT, True)       
#click rightmoyse
        if fingers[1]==1 and fingers[2]==0:
            #9.Find distance between Fingers
            # length, img, lineInfo = detector.findDistance(4, 8, img)
            # if length < 40:
            #     cv2.circle(img, (lineInfo[4], lineInfo[5]),
            #                 15, (0, 255, 0), cv2.FILLED)
            #     #10.Click mouse if distance short
            ap.mouse.click(ap.mouse.Button.RIGHT)
#DRAG 
        if fingers[1]==0 and fingers[2]==0:
            ap.mouse.toggle(ap.mouse.Button.LEFT, True)

            x3 = py.interp(x1, (frameR, wCam - frameR), (0, wScr))
            y3 = py.interp(y1, (frameR, hCam - frameR), (0, hScr))
            
            #6.Smoothen Values
            clocX = plocX + (x3 - plocX) / smoothening
            clocY = plocY + (y3 - plocY) / smoothening

            #7.Move Mouse
            
            ap.mouse.move(wScr - clocX,clocY)
            cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
            plocX, plocY = clocX, clocY
            #drop
            if fingers[1]==1 and fingers[2]==1:
                ap.mouse.toggle(ap.mouse.Button.LEFT, False)

        

 
 #SCROLL DOWN
        # if fingers[1]==1 and fingers[4]==1:
        #     # 9.Find distance between Fingers
        #     ap.mouse.toggle(ap.mouse.Button.MIDDLE, False)
        #         #10.Click mouse if distance short
        #     x3 = py.interp(x1, (frameR, wCam - frameR), (0, wScr))
        #     y3 = py.interp(y1, (frameR, hCam - frameR), (0, hScr))
            
        #     #6.Smoothen Values
        #     clocX = plocX + (x3 - plocX) / smoothening
        #     clocY = plocY + (y3 - plocY) / smoothening

        #     #7.Move Mouse
            
        #     ap.mouse.move(wScr - clocX,clocY)
        #     cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
        #     plocX, plocY = clocX, clocY
        
    #11.Frame rate
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)),(20,50),cv2.FONT_HERSHEY_PLAIN,3, (255,0,0),3)
    #12.Display
    cv2.imshow("Image", img)
    cv2.waitKey(1)