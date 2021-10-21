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
        self.orb = cv.ORB_create(nlevels=5, firstLevel=1, edgeThreshold=1,
                                  nfeatures=50, fastThreshold=config.FAST_THRESHOLD)
        self.BFMatcher = cv.BFMatcher(cv.NORM_HAMMING, crossCheck=False)
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

        R = self.Rz(psi) * self.Ry(theta) * self.Rx(phi)
        # print(np.round(R, decimals=2))
        return R

    def translate(self, x0, y0, z0, x1, y1, z1):
        difx = x1 - x0
        dify = y1 - y0
        difz = z1 - z0
        return np.array([x0 + difx, y0 + dify, z0 + difz])

    def run(self):
        #Obtenemos los keypoints del frame actual y el anterior
        kps_act, desc_act, img_act = self.obtenerKeypointsYDescriptors(2)
        kps_ant, desc_ant, img_ant = self.obtenerKeypointsYDescriptors(1)

        #Dibujamos los keypoints detectados
        img1 = cv.drawKeypoints(img_act, kps_act, 0, color=(0,255,0), flags=cv.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
        img2 = cv.drawKeypoints(img_ant, kps_ant, 0, color=(0,255,0), flags=cv.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

        # Mostramos las imagenes
        plt.imshow(img1)
        plt.show()
        plt.imshow(img2)
        plt.show()

        #Obtenemos los matches y filtramos los keypoints que necesitamos del frame actual y el anterior
            # recordando: query = actual; train = previo
        matches, matches_no_filtro = self.matchFeatures(desc_ant, desc_act)

        kp_xy_ant = []
        kp_xy_act = []
        for match in matches:
            kp_xy_ant.append(np.asarray(kps_ant[match[0].trainIdx].pt))
            kp_xy_act.append(np.asarray(kps_act[match[0].queryIdx].pt))
        
        kp_xy_ant = np.asarray(kp_xy_ant).T
        kp_xy_act = np.asarray(kp_xy_act).T

        # print(np.asarray(kp_xy_ant).T, np.asarray(kp_xy_act).T)

        # kp_xy_act = np.array([np.array([kp[0][0] for kp in kps_act]),
        #                       np.array([kp[0][1] for kp in kps_act])])

        # kp_xy_ant = np.array([np.array([kp[0][0] for kp in kps_ant]),
        #                       np.array([kp[0][1] for kp in kps_ant])])
        
        plt.imshow(
            cv.drawMatchesKnn(
                img_ant,
                kps_ant,
                img_act,
                kps_act,
                matches,
                None
            )
        )
        plt.show()

        # Angulos del dron euler
        R1 = self.rotate(0, 0, 0)
        # posiciones GPS (x, y, z) del dron
        T1 = self.translate(0, 0, 0, 0, 0, 0)

        R2 = self.rotate(0, 0, 0)
        T2 = self.translate(0, 0, 0, 10, 0, 0)

        """
    R = [[ 1 2 3 1],
         [1 2 3 2],
          [1 2 3 3]]

    T = [ 
        1
        2
        3
     ]
        """
        # rt1 = np.concatenate((R1, np.array([T1]).T), axis=1)
        # rt2 = np.concatenate((R2, np.array([T2]).T), axis=1)

        projection_mtx1 = np.array(
            [[R1[0,0],R1[0,1],R1[0,2],T1[0]],
            [R1[1,0],R1[1,1],R1[1,2],T1[1]],
            [R1[2,0],R1[2,1],R1[2,2],T1[2]]]
        )
        projection_mtx2 = np.array(
            [[R2[0,0],R2[0,1],R2[0,2],T2[0]],
            [R2[1,0],R2[1,1],R2[1,2],T2[1]],
            [R2[2,0],R2[2,1],R2[2,2],T2[2]]]
        )

        # multiplicar por la intrinseca
        # self.K = np.array([[7.18856e+02, 0.0, 6.071928e+02],
        #                   [0.0, 7.18856e+02, 1.852157e+02],
        #                   [0.0, 0.0, 1.0]])
        # self.pp = np.array([self.K[0, 2], self.K[1, 2]])
        # self.focal = self.K[0, 0]

        points_in_4d = cv.triangulatePoints(
            projection_mtx1, projection_mtx2, kp_xy_ant, kp_xy_act)
        # Normalize points [x, y, z, 1]
        points_in_3d = points_in_4d / points_in_4d[3]

        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        # ax.scatter([p[0] for p in points_in_3d], [p[1] for p in points_in_3d], [p[2] for p in points_in_3d])
        ax.scatter(points_in_3d[0], points_in_3d[1], points_in_3d[2])
        # ax.scatter([item[0][0] for item in points_in_3d], [item[0][1]])

        print(points_in_3d)
        print("ornelaseschido")

    def Rx(self, theta):
        return np.matrix([[1, 0, 0],
                        [0, m.cos(theta), -m.sin(theta)],
                        [0, m.sin(theta), m.cos(theta)]])


    def Ry(self, theta):
        return np.matrix([[m.cos(theta), 0, m.sin(theta)],
                        [0, 1, 0],
                        [-m.sin(theta), 0, m.cos(theta)]])


    def Rz(self, theta):
        return np.matrix([[m.cos(theta), -m.sin(theta), 0],
                        [m.sin(theta), m.cos(theta), 0],
                        [0, 0, 1]])


    def obtenerKeypointsYDescriptors(self, numeroImagen):
        img = cv.imread(
            f"{config.PROJECT_PATH}/proyecto-modular/project/assets/photos/photo_mtrx{numeroImagen}.jpeg")
        img = image_module.resize_image(
            img, config.VIDEO_WITDH_RESIZE, config.VIDEO_HEIGHT_RESIZE)
        gray = image_module.process_image(img)

        # Find the chess board corners
        # _, kp = cv.findChessboardCorners(gray, (9, 6), None)
        kp, desc = self.orb.detectAndCompute(gray, None)
        return kp, desc, gray;

    def matchFeatures(self, des_prev, desc_act):
        if des_prev is None or len(des_prev) < 2:
            return -1
        if desc_act is None or len(desc_act) < 2:
            return -1
        matches = self.BFMatcher.knnMatch(des_prev, desc_act, k=2)
        # Apply ratio test
        goodMatches = []
        for m, n in matches:
            if m.distance < 0.70 * n.distance:
                goodMatches.append([m])
        return goodMatches, matches
