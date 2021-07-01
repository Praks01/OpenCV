import cv2
import numpy as np

img = cv2.imread("OpenTut.png")                         # file name
kernel = np.ones((5,5),np.uint8)

imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)          # BGR to Gray
imgCanny=cv2.Canny(img,100,100)                         # Draw edge
imgBlur=cv2.GaussianBlur(imgGray,(7,7),0)               # InduceBlur
imgDilation=cv2.dilate(imgCanny,kernel,iterations=1)    # Thicken canny
imgEroded=cv2.erode(imgCanny,kernel,iterations=1)       # Reduce Thickness

print(img.shape)
imgResize=cv2.resize(img,(300,200))                     # Resize
print(imgResize.shape)
imgCrop=img[0:200,200:500]                              # Crop

imghor=np.hstack((img,img))                             # HorizontalStack
imgver=np.vstack((imghor,imghor))                       # VerticalStack

cv2.imshow("image",img)
cv2.imshow("Gray",imgGray)
cv2.imshow("Blur",imgBlur)
cv2.imshow("Canny",imgCanny)
cv2.imshow("dilation",imgDilation)
cv2.imshow("erosion",imgEroded)
cv2.imshow("imageresize",imgResize)
cv2.imshow("imagecrop",imgCrop)
cv2.imshow('Stacked',imgver)


cv2.waitKey(0)
