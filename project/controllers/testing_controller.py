import numpy as np
import math as m
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

    def rotate(self, phi, theta, psi):
        phi = m.pi/2
        theta = m.pi/4
        psi = m.pi/2
        # print("phi =", phi)
        # print("theta  =", theta)
        # print("psi =", psi)
        
        R = Rz(psi) * Ry(theta) * Rx(phi)
        # print(np.round(R, decimals=2))
        return R

    def translate(self, x0, y0, z0, x1, y1, z1):
        difx = x1 - x0  
        dify = y1 - y0  
        difz = z1 - z0  
        return np.array([x0 + difx, y0 + dify, z0 + difz])

    def run(self):      
        kps_act = obtenerKeypoints(1)
        kps_ant = obtenerKeypoints(2)

        # Extrayendo X y Y de el keypoint
        kp_xy_act = np.array([np.array([kp[0][0] for kp in kps_act]), 
                            np.array([kp[0][1] for kp in kps_act])])

        kp_xy_ant = np.array([np.array([kp[0][0] for kp in kps_ant]), 
                            np.array([kp[0][1] for kp in kps_ant])])    

        # obtenemos las matrices (la mate)
        matrizProyecion1 = None
        matrizProyecion2 = None

        # Angulos del dron euler
        R = self.rotate(0, 0, 0)
        # posiciones GPS (x, y, z) del dron
        T = self.translate(0, 0, 0, 10, 0, 0)

        proj_points_1 = np.array([np.array([kp[0] for kp in kp_xy_ant]),
                                  np.array([kp[1] for kp in kp_xy_ant])])

        proj_points_2 = np.array([np.array([kp[0] for kp in kp_xy_act]),
                                  np.array([kp[1] for kp in kp_xy_act])])


        points_in_4d = cv.triangulatePoints(matrizProyecion1, matrizProyecion2, kp_xy_ant, kp_xy_act)
        points_in_3d = cv.convertPointsFromHomogeneous(points_in_4d.transpose())

        # fig = plt.figure()
        # ax = fig.add_subplot(111, projection='3d')
        # ax.scatter([item[0][0] for item in points_in_3d], [item[0][1]])

def Rx(theta):
  return np.matrix([[ 1, 0           , 0           ],
                   [ 0, m.cos(theta),-m.sin(theta)],
                   [ 0, m.sin(theta), m.cos(theta)]])
  
def Ry(theta):
  return np.matrix([[ m.cos(theta), 0, m.sin(theta)],
                   [ 0           , 1, 0           ],
                   [-m.sin(theta), 0, m.cos(theta)]])
  
def Rz(theta):
  return np.matrix([[ m.cos(theta), -m.sin(theta), 0 ],
                   [ m.sin(theta), m.cos(theta) , 0 ],
                   [ 0           , 0            , 1 ]])

def obtenerKeypoints(numeroImagen):
    img = cv.imread(f"{config.PROJECT_PATH}/proyecto-modular/project/assets/photos/photo_mtrx{numeroImagen}.jpeg")
    gray = image_module.process_image(img)
    img = image_module.resize_image(img, config.VIDEO_WITDH_RESIZE, config.VIDEO_HEIGHT_RESIZE)

    # Find the chess board corners
    _, kp = cv.findChessboardCorners(gray, (9, 6), None)
    return kp
        