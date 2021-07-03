import cv2
import cv2.aruco as aruco
import numpy as np
import glob


def Cam_Calib():
    chessboardSize = (9, 5)  # Change this for different chess board
    frameSize = (960, 540)   # Change this for different camera
    # termination criteria
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
    # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
    objp = np.zeros((chessboardSize[0] * chessboardSize[1], 3), np.float32)
    objp[:, :2] = np.mgrid[0:chessboardSize[0], 0:chessboardSize[1]].T.reshape(-1, 2)

    # Arrays to store object points and image points from all the images.
    objpoints = []  # 3d point in real world space
    imgpoints = []  # 2d points in image plane.

    images = glob.glob('/home/praks/PycharmProjects/ArUcoDetection/*.jpg')

    for image in images:

        img = cv2.imread(image)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Find the chess board corners
        ret, corners = cv2.findChessboardCorners(gray, chessboardSize, None)

        # If found, add object points, image points (after refining them)
        if ret == True:
            objpoints.append(objp)
            corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
            imgpoints.append(corners)
            cv2.drawChessboardCorners(img, chessboardSize, corners2, ret)
            #cv2.imshow('img', img)
            #cv2.waitKey(100)

    #cv2.destroyAllWindows()

    ret, cameraMatrix, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, frameSize, None, None)

    mean_error=0

    for i in range(len(objpoints)):
        imgpoints2, _ = cv2.projectPoints(objpoints[i], rvecs[i], tvecs[i], cameraMatrix, dist)
        error = cv2.norm(imgpoints[i], imgpoints2, cv2.NORM_L2) / len(imgpoints2)
        mean_error += error
        err=(mean_error / len(objpoints))

    print(err)
    return cameraMatrix, dist

def findArucoMarkers(img, markerSize=6, totalMarkers=250, draw=True):
    imgGray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    key=getattr(aruco,f'DICT_{markerSize}X{markerSize}_{totalMarkers}')
    arucoDict=aruco.Dictionary_get(key)
    arucoParam=aruco.DetectorParameters_create()
    bboxs, ids, rejected=aruco.detectMarkers(imgGray, arucoDict, parameters=arucoParam)

    if draw:
        aruco.drawDetectedMarkers(img,bboxs)


    return [bboxs, ids]

def Track(bbox, id, img, cameraMatrix, dist, ArucoId, Rvector, Tvector):
    tl = bbox[0][0][0], bbox[0][0][1]
    #tr = bbox[0][1][0], bbox[0][1][1]
    #bl = bbox[0][2][0], bbox[0][2][1]
    #br = bbox[0][3][0], bbox[0][3][1]
    a=int(tl[0])
    b=int(tl[1])
    cv2.putText(img, str(id), (a,b), cv2.FONT_HERSHEY_PLAIN, 1, (240, 240, 0), 1)
    rvec, tvec, markerPoints = aruco.estimatePoseSingleMarkers(bbox, 0.02, cameraMatrix, dist)
    (rvec - tvec).any()  # get rid of that nasty numpy value array error
    aruco.drawAxis(img, cameraMatrix, dist, rvec, tvec, 0.01)  # Draw Axis
    iteration=0
    for i in ArucoId:
        if (i == id):
            iteration=iteration+1
            return img, Rvector, Tvector, ArucoId

    ArucoId = np.append(ArucoId, id)
    Rvector = np.append(Rvector, rvec, axis=0)
    Tvector = np.append(Tvector, tvec, axis=0)
    return img, Rvector, Tvector, ArucoId


def main():
    ArucoId = [-1]
    Rvector = [[[0,0,0]]]
    Tvector = [[[0,0,0]]]
    cameraMatrix, dist= Cam_Calib()

    cap=cv2.VideoCapture(0)

    while(True):
        sucess,img= cap.read()
        arucoFound=findArucoMarkers(img)

        if len(arucoFound[0])!=0:
            for bbox, id in zip(arucoFound[0], arucoFound[1]):
                img, Rvector, Tvector, ArucoId=Track(bbox, id, img, cameraMatrix, dist, ArucoId, Rvector, Tvector)



        cv2.imshow("Image",img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("ID")
            print(ArucoId)
            print("RVector")
            print(Rvector)
            print("Tvector")
            print(Tvector)
            break



if __name__=="__main__":

    main()

