import cv2                  #CV2 Package

cap=cv2.VideoCapture(0)     # 0 means default cam
cap.set(3,640)              # 3 refers to FrameWidth
cap.set(4,480)              # 4 refers to FrameHeight
size=(640,480)
result = cv2.VideoWriter('Video.avi',cv2.VideoWriter_fourcc(*'MJPG'),10, size) #filename, fourcc, fps, frameSize

while True:

    success, img=cap.read()
    cv2.imshow("Video",img)
    result.write(img)

    if cv2.waitKey(1) & 0xFF ==ord('q'):    # Press q to exit
        break