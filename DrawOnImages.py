import cv2
import numpy as np

img=np.zeros((512,512,3),np.uint8)
#print(img.shape)
#img[0:250,200:400]=255,0,0
cv2.line(img,(0,0),(300,300),(0,250,0),3)
cv2.rectangle(img,(0,0),(250,350),(0,0,255),1)
cv2.putText(img,"openCV",(300,200),cv2.FONT_HERSHEY_PLAIN,2,(0,240,0),2)
cv2.imshow("Image",img)
cv2.waitKey(0)