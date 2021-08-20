import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from project.controllers import tracking_controller
from project.modules import image_module
from project import config
import glob


class TestingController:
    def __init__(self):
        self.object_points = (0, 0, 0)
        self._path = 'C:/Users/carlo/Documents/universidad/Modular/proyecto-modular/project/assets/video/calibracion.mp4'
        self.mtx = None
        self.dist = None

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
        objpoints = [[],[]]  # 3d point in real world space
        imgpoints = [[],[]]  # 2d points in image plane.
        # initialize an object based on the webcam

        for i in range(1,3):
            img = cv.imread(f"C:/Users/carlo/Documents/universidad/Modular/proyecto-modular/project/assets/photos/photo{i}.jpg")
            gray = image_module.process_image(img)

            img = image_module.resize_image(img, config.VIDEO_WITDH_RESIZE, config.VIDEO_HEIGHT_RESIZE)

            # Find the chess board corners
            ref, corners = cv.findChessboardCorners(gray, (9, 6), None)

            if ref:
                # If found, add object points, image points (after refining them)
                objpoints[i-1] = [objp]
                corners2 = cv.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
                imgpoints[i-1] = [corners]

                # Draw and display the corners
                cv.drawChessboardCorners(img, (9, 6), corners2, ref)
                cv.imshow(f'img{i}', img)
                cv.waitKey(25)

                # TODO Hay que regresar la matriz de la camara para que se use en el System.py
                # TODO return rvecs and tvecs or make them properties
                ref, self.mtx, self.dist, rvecs, tvecs = cv.calibrateCamera(objpoints[i-1], imgpoints[i-1], gray.shape[::-1], None, None)

        print(objpoints)
        print(imgpoints)

        _tracker_controller = tracking_controller.Tracker()
        kp_actual = [[],[]]

        for i in range(1,3):
            img = cv.imread(f"C:/Users/carlo/Documents/universidad/Modular/proyecto-modular/project/assets/photos/photo{i}.jpg")
            gray_image = image_module.process_image(img)

            _tracker_controller.set_image(gray_image)

            kp_actual[i-1], dp = _tracker_controller.detect_features_and_descriptors(gray_image)

        objp_anterior = []
        objp_actual = []

        for p in kp_actual[1]:
            objp_actual = np.append([objp_actual], [p.pt[0], p.pt[1], 0]).reshape(-1, 3)

        for p in kp_actual[0]:
            objp_anterior = np.append([objp_anterior], [[p.pt[0], p.pt[1], 0]]).reshape(-1, 3)

        keypoints_frame_anterior = np.array([[kp.pt[0], kp.pt[1]] for kp in kp_actual[0]])
        keypoints_frame_actual = np.array([[kp.pt[0], kp.pt[1]] for kp in kp_actual[1]])

        if len(objp_anterior) > 0 and len(objp_actual) > 0:
            ret, rvecs_anterior, tvecs_anterior = cv.solvePnP(objp_anterior, keypoints_frame_anterior,self.mtx, self.dist)
            ret, rvecs_actual, tvecs_actual = cv.solvePnP(objp_actual, keypoints_frame_actual, self.mtx, self.dist)

            # @ objp => object points (3d coordinates) cada keypoint que haya tenido match con el fram anterior (recorrer lista de los matches y hacer su proyeccoiob)
            # @ rvecs => viene de pnp
            # @ tvecs => viene de pnp
            # @ mtx => viene de la calibracion
            # @ dist => viene de la calibracion

            # imgpts, jac = cv.projectPoints(objp, rvecs, tvecs, calibrationController.mtx, calibrationController.dist)

            # ? matrizProyecion1 => de donde se saca??
            # ? matrizProyecion2 =>
            # @ proj_points_1 => los sacamode de cv.projectpoints (frame anterior)
            # @ proj_points_2 => los sacamode de cv.projectpoints

            matrizProyecion1 = np.zeros(12).reshape(-1, 4)
            matrizProyecion1[0][0] = rvecs_anterior[0]
            matrizProyecion1[1][1] = rvecs_anterior[1]
            matrizProyecion1[2][2] = rvecs_anterior[2]

            matrizProyecion1[0][3] = tvecs_anterior[0]
            matrizProyecion1[1][3] = tvecs_anterior[1]
            matrizProyecion1[2][3] = tvecs_anterior[2]

            matrizProyecion2 = np.zeros(12).reshape(-1, 4)
            matrizProyecion2[0][0] = rvecs_actual[0]
            matrizProyecion2[1][1] = rvecs_actual[1]
            matrizProyecion2[2][2] = rvecs_actual[2]

            matrizProyecion2[0][3] = tvecs_actual[0]
            matrizProyecion2[1][3] = tvecs_actual[1]
            matrizProyecion2[2][3] = tvecs_actual[2]

            act_ = np.array([np.array([kp.pt[0] for kp in kp_actual[1]]),
                             np.array([kp.pt[1] for kp in kp_actual[1]])])

            ant_ = np.array([np.array([kp.pt[0] for kp in kp_actual[0]]),
                             np.array([kp.pt[1] for kp in kp_actual[0]])])

            points_in_3d = cv.triangulatePoints(matrizProyecion1, matrizProyecion2, ant_, act_)

            fig = plt.figure()
            ax = fig.add_subplot(111, projection='3d')
            ax.scatter(points_in_3d[0], points_in_3d[1], points_in_3d[2])
            plt.xlim([0, 1])
            plt.ylim([0, 1])
            plt.show()
