import cv2
import numpy as np
print("Package Imported")

frameWidth = 640
frameHeight = 480
cap = cv2.VideoCapture(0)
cap.set(3, frameWidth)
cap.set(4, frameWidth)
cap.set(10, 150)

myColors = [[64, 106, 67, 97, 184, 219],
            [87, 99, 70, 105, 255, 189],
            [138, 114, 84, 179, 196, 207],
            [2, 185, 86, 4, 225, 231]]

myColorValues = [[0, 255, 0],           # BGR
                 [255, 153, 0],
                 [206, 26, 250],
                 [51, 51, 255]]

myPoints = []    ## x, y, colorId


def findColor(img, myColors, myColorValues):
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    cnt = 0
    newPoints = []
    for color in myColors:
        lower = np.array(color[0:3])
        upper = np.array(color[3:])
        mask = cv2.inRange(imgHSV, lower, upper)
        cv2.imshow(str(color[0]), mask)
        x, y = getContours(mask)
        cv2.circle(imgResult, (x, y), 10, myColorValues[cnt], cv2.FILLED)
        if x != 0 and y != 0:
            newPoints.append([x, y, cnt])
        cnt += 1

    return newPoints


def getContours(img):
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    x, y, w, h = 0, 0, 0, 0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 100:
            print(area)
            cv2.drawContours(imgResult, cnt, -1, (255, 0, 0), 3)
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, .02*peri, True)
            x, y, w, h = cv2.boundingRect(approx)
    return x+w//2, y


def drawOnCanvas(myPoints, myColorValues):
    for point in myPoints:
        cv2.circle(imgResult, (point[0], point[1]), 10, myColorValues[point[2]], cv2.FILLED)


while True:
    success, img = cap.read()
    if img is not None:
        imgResult = img.copy()
        newPoints = findColor(img, myColors, myColorValues)
        if len(newPoints) != 0:
            for newP in newPoints:
                myPoints.append(newP)
        if len(myPoints) != 0:
            drawOnCanvas(myPoints, myColorValues)

        cv2.imshow("Webcam", imgResult)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break



