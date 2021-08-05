import numpy as np
import cv2 as cv
from project.modules import image_module
from project import config
import glob


class CalibrationController:
    def __init__(self):
        self.object_points = (0, 0, 0)
        self._video_path = 'C:/Users/carlo/Documents/universidad/Modular/proyecto-modular/project/assets/video/calibracion.mp4'

    def calibrate(self):
        # termination criteria
        criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)
        # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
        objp = np.zeros((6 * 7, 3), np.float32)
        objp[:, :2] = np.mgrid[0:7, 0:6].T.reshape(-1, 2)
        # Arrays to store object points and image points from all the images.
        objpoints = []  # 3d point in real world space
        imgpoints = []  # 2d points in image plane.
        _cap = cv.VideoCapture(self._video_path)  # initialize an object based on the webcam
        ret, image = _cap.read()

        with open(self._video_path) as f:
            print('se abrio el archivo')

        while _cap.isOpened():
            ret, img = _cap.read()
            if ret:
                # img = cv.imread(image)
                gray = image_module.process_image(img)
                img = image_module.resize_image(img, config.VIDEO_WITDH_RESIZE, config.VIDEO_HEIGHT_RESIZE)
                # Find the chess board corners
                ref, corners = cv.findChessboardCorners(gray, (9, 6), None)
                if ref:
                    # If found, add object points, image points (after refining them)
                    # objpoints.append(objp)
                    corners2 = cv.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
                    # imgpoints.append(corners)
                    # Draw and display the corners
                    cv.drawChessboardCorners(img, (9, 6), corners2, ref)
                    cv.imshow('img', img)
                    # cv.waitKey(500)

            if cv.waitKey(25) & 0xFF == ord('q'):
                break
        cv.destroyAllWindows()
