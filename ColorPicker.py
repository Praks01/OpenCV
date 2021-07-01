import cv2
import numpy as np

def empty(a):
    pass

cv2.namedWindow('TrackBar')                                 # TrackBar to set Values
cv2.resizeWindow('Trackbar',640,240)
cv2.createTrackbar('Hue Min','TrackBar',0,179,empty)
cv2.createTrackbar('Hue Max','TrackBar',179,179,empty)
cv2.createTrackbar('Sat Min','TrackBar',0,255,empty)
cv2.createTrackbar('Sat Max','TrackBar',255,255,empty)
cv2.createTrackbar('Val Min','TrackBar',0,255,empty)
cv2.createTrackbar('Val Max','TrackBar',255,255,empty)

cap=cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)
while True:
    success, img=cap.read()
    cv2.imshow("Video",img)
    imgHSV=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    h_min=cv2.getTrackbarPos('Hue Min','TrackBar')
    h_max = cv2.getTrackbarPos('Hue Max', 'TrackBar')
    s_min = cv2.getTrackbarPos('Sat Min', 'TrackBar')
    s_max = cv2.getTrackbarPos('Sat Max', 'TrackBar')
    v_min = cv2.getTrackbarPos('Val Min', 'TrackBar')
    v_max = cv2.getTrackbarPos('Val Max', 'TrackBar')
    lower=np.array([h_min,s_min,v_min])
    upper=np.array([h_max,s_max,v_max])
    mask=cv2.inRange(imgHSV,lower,upper)                            # Setting values
    imgResult=cv2.bitwise_and(img,img,mask=mask)                    # Masking
    cv2.imshow('Result',imgResult)
    if cv2.waitKey(1) & 0xFF ==ord('q'):
        break
