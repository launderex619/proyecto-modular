import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from controllers import tracking_controller
from modules import image_module
from core import config
import glob


class TestingController:
    def __init__(self):
        self.object_points = (0, 0, 0)
        # self._path = config.PROJECT_PATH + '/proyecto-modular/project/assets/video/calibracion.mp4'
        self.mtx = None
        self.dist = None

    def draw(self, img, corners, imgpts):
        corner = tuple(corners[0].ravel())
        img = cv.line(img, corner, tuple(imgpts[0].ravel()), (255, 0, 0), 5)
        img = cv.line(img, corner, tuple(imgpts[1].ravel()), (0, 255, 0), 5)
        img = cv.line(img, corner, tuple(imgpts[2].ravel()), (0, 0, 255), 5)
        return img

    def run(self):      
        kps_act = obtenerKeypoints(1)
        kps_ant = obtenerKeypoints(2)

        # Extrayendo X y Y de el keypoint
        kp_xy_act = np.array([np.array([kp[0][0][0] for kp in kps_act]), 
                            np.array([kp[0][0][1] for kp in kps_act])])

        kp_xy_ant = np.array([np.array([kp['pt'][0] for kp in kps_ant]),
                            np.array([kp['pt'][1] for kp in kps_ant])])      

        # obtenemos las matrices (la mate)
        matrizProyecion1 = None
        matrizProyecion2 = None

        points_in_4d = cv.triangulatePoints(matrizProyecion1, matrizProyecion2, kp_xy_ant, kp_xy_act)
        points_in_3d = cv.convertPointsFromHomogeneous(points_in_4d.transpose())

        # fig = plt.figure()
        # ax = fig.add_subplot(111, projection='3d')
        # ax.scatter([item[0][0] for item in points_in_3d], [item[0][1]])

def obtenerKeypoints(numeroImagen):
    img = cv.imread(f"{config.PROJECT_PATH}/proyecto-modular/project/assets/photos/photo_mtrx{numeroImagen}.jpeg")
    gray = image_module.process_image(img)
    img = image_module.resize_image(img, config.VIDEO_WITDH_RESIZE, config.VIDEO_HEIGHT_RESIZE)

    # Find the chess board corners
    _, kp = cv.findChessboardCorners(gray, (9, 6), None)
    return kp
        