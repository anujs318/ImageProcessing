import os

import cvzone
import cv2
from cvzone.PoseModule import PoseDetector

cap = cv2.VideoCapture("Resources/Videos/1.mp4")
detector = PoseDetector()

shirtFolderPath = "Resources/Shirts"
listShirts = os.listdir(shirtFolderPath)


fixedRatio = 234/ 180 
shirtRatioHeightWidth = 512 / 430
imageNumber = 0
imgButtonRight = cv2.imread("Resources/button.png", cv2.IMREAD_UNCHANGED)
imgButtonLeft = cv2.flip(imgButtonRight, 1)
counterRight = 0
counterLeft = 0
selectionSpeed = 10



while True:
    success, img = cap.read()
    img = detector.findPose(img)
    img = cv2.flip(img,1)
    lmList, bboxInfo = detector.findPosition(img, bboxWithHands=False, draw=False)
    if lmList:
        #center = bboxInfo["center"]
        lm12 = lmList[12][1:3]
        lm11 = lmList[11][1:3]
        imgShirt = cv2.imread(os.path.join(shirtFolderPath, listShirts[imageNumber]), cv2.IMREAD_UNCHANGED)
        widthOfShirt = int((lm11[1] - lm12[1]) * fixedRatio)
        # imgShirt=cv2.resize(imgShirt,(widthOfShirt,int(widthOfShirt+shirtRatioHeightWidth)))
        imgShirt=cv2.resize(imgShirt,(0,0),None,0.42,0.42)
        print(widthOfShirt)
       
        currentScale = (lm12[0] - lm11[0]) / 190
        offset = int(0), int(1)

        try:
            img = cvzone.overlayPNG(img, imgShirt,(lm12[0] - offset[1],lm12[0]-offset[0]))
        except:
            pass

        img = cvzone.overlayPNG(img, imgButtonRight, (345, 231))
        img = cvzone.overlayPNG(img, imgButtonLeft, (11, 226))

        if lmList[16][1] < 300:
            counterRight += 1
            cv2.ellipse(img, (139, 360), (66, 66), 0, 0,
                        counterRight * selectionSpeed, (0, 255, 0), 20)
            if counterRight * selectionSpeed > 360:
                counterRight = 0
                if imageNumber < len(listShirts) - 1:
                    imageNumber += 1
        elif lmList[15][1] > 900:
            counterLeft += 1
            cv2.ellipse(img, (1138, 360), (66, 66), 0, 0,
                        counterLeft * selectionSpeed, (0, 255, 0), 20)
            if counterLeft * selectionSpeed < 360:
                counterLeft = 0
                if imageNumber > 0:
                    imageNumber -= 1

        else:
            counterRight = 0
            counterLeft = 0

    cv2.imshow("Image", img)
    cv2.waitKey(1)


    
  
