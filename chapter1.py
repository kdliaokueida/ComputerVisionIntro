import cv2
import numpy as np
print("Package Imported")

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)
cap.set(10, 100)

while True:
    success, img = cap.read()
    if img is not None:
        cv2.imshow("Webcam", img)
    if cv2.waitKey(1) & 0xFF==ord('q'):
        break

