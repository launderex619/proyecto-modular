import numpy as np
import cv2 as cv
from project.modules import image_module
from project import config
import glob


class CalibrationController:
    def __init__(self):
        self.object_points = (0, 0, 0)
        self._video_path = '/Users/lumedina/Documents/Uni/proyecto-modular/project/assets/video/calibracion.mp4'

    def draw(self, img, corners, imgpts):
        corner = tuple(corners[0].ravel())
        img = cv.line(img, corner, tuple(imgpts[0].ravel()), (255, 0, 0), 5)
        img = cv.line(img, corner, tuple(imgpts[1].ravel()), (0, 255, 0), 5)
        img = cv.line(img, corner, tuple(imgpts[2].ravel()), (0, 0, 255), 5)
        return img

    def calibrate(self):
        # termination criteria
        criteria = (cv.TERM_CRITERIA_EPS +
                    cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)
        # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
        objp = np.zeros((6 * 9, 3), np.float32)
        objp[:, :2] = np.mgrid[0:9, 0:6].T.reshape(-1, 2)
        axis = np.float32([[3, 0, 0], [0, 3, 0], [0, 0, -3]]).reshape(-1, 3)
        # Arrays to store object points and image points from all the images.
        objpoints = []  # 3d point in real world space
        imgpoints = []  # 2d points in image plane.
        # initialize an object based on the webcam
        _cap = cv.VideoCapture(self._video_path)
        ret, image = _cap.read()

        with open(self._video_path) as f:
            print('se abrio el archivo')

        while _cap.isOpened():
            ret, img = _cap.read()
            if ret:
                # img = cv.imread(image)
                gray = image_module.process_image(img)
                img = image_module.resize_image(
                    img, config.VIDEO_WITDH_RESIZE, config.VIDEO_HEIGHT_RESIZE)
                # Find the chess board corners
                ref, corners = cv.findChessboardCorners(gray, (9, 6), None)
                if ref:
                    # If found, add object points, image points (after refining them)
                    objpoints = [objp]
                    corners2 = cv.cornerSubPix(
                        gray, corners, (11, 11), (-1, -1), criteria)
                    imgpoints = [corners]
                    # Draw and display the corners
                    cv.drawChessboardCorners(img, (9, 6), corners2, ref)
                    cv.imshow('img', img)
                    # cv.waitKey(500)

                    # TODO Hay que regresar la matriz de la camara para que se use en el System.py
                    # TODO return rvecs and tvecs or make them properties
                    ref, self.mtx, self.dist, rvecs, tvecs = cv.calibrateCamera(
                        objpoints, imgpoints, gray.shape[::-1], None, None)

                    if ref:
                        print("calibration succed")

                        # corners2 = cv.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
                        # # Find the rotation and translation vectors.
                        # ret, rvecs, tvecs = cv.solvePnP(objp, corners2, mtx, dist)
                        # # project 3D points to image plane
                        # imgpts, jac = cv.projectPoints(axis, rvecs, tvecs, mtx, dist)
                        # # img = self.draw(img, corners2, imgpts)
                        # # cv.imshow('img', img)

                        # points_in_3d = cv2.triangulatePoints(IRt, Rt, proj_points_1, proj_points_2)

                    break

            if cv.waitKey(25) & 0xFF == ord('q'):
                break

        cv.destroyAllWindows()
