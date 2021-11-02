import numpy as np
import math as m
import cv2 as cv
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from controllers import tracking_controller
from modules import image_module
from core import config
import glob
import time
import open3d as o3d

class Display:
    def __init__(self):
        self.W = 960
        self.H = 540

    def display_points2d(self, img, kpts, matches):
        if kpts != 0:
            for kpt in kpts:
                cv.circle(img, (int(kpt.pt[0]), int(kpt.pt[1])), radius=2, color=(0,255,0), thickness=-1)
        
        if matches != 0:
            for match in matches:
                (u1, v1) = np.int32(match[0].pt)
                (u2, v2) = np.int32(match[1].pt)
                cv.line(img, (u1, v1), (u2, v2), color=(0,0,255), thickness=1)
        return img


    def display_points3d(self, tripoints3d, pcd, visualizer):
        # open3d
        if tripoints3d is not None:
            pcd.clear()
            pcd.points = o3d.utility.Vector3dVector(tripoints3d)
            visualizer.remove_geometry(pcd)
            visualizer.add_geometry(pcd)
            visualizer.poll_events()
            visualizer.update_renderer()
            time.sleep(.2)

    def display_vid(self, img):
        cv.imshow("main", img)

class PointMap(object):
	def __init__(self):
		self.array = [0,0,0]

	def collect_points(self, tripoints):
		if len(tripoints) > 0:
			array_to_project = np.array([0,0,0])

			x_points = [pt for pt in tripoints[0]]
			y_points = [-pt for pt in tripoints[1]]
			z_points = [-pt for pt in tripoints[2]]

			for i in range(tripoints.shape[1]):
				curr_array = np.array([x_points[i], y_points[i], z_points[i]])
				array_to_project = np.vstack((array_to_project, curr_array))

			array_to_project = array_to_project[1:, :]

			return array_to_project

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

        R = self.Rz(psi) * self.Ry(theta) * self.Rx(phi)
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

        # Obtenemos los matches y filtramos los keypoints que necesitamos del frame actual y el anterior
        # recordando: query = actual; train = previo
        matches, matches_no_filtro = self.matchFeatures(desc_ant, desc_act)

        kp_xy_ant = []
        kp_xy_act = []
        for match in matches:
            kp_xy_ant.append(np.asarray(kps_ant[match[0].trainIdx].pt))
            kp_xy_act.append(np.asarray(kps_act[match[0].queryIdx].pt))
        
        kp_xy_ant = np.asarray(kp_xy_ant).T
        kp_xy_act = np.asarray(kp_xy_act).T
        
        plt.imshow(cv.drawMatchesKnn(img_ant,kps_ant,img_act,kps_act,matches,None))
        plt.show()

        # Angulos del dron euler
        R1 = self.rotate(0, 0, 0)
        # posiciones GPS (x, y, z) del dron
        T1 = self.translate(0, 0, 0, 0, 0, 0)

        R2 = self.rotate(0, 0, 0)
        T2 = self.translate(0, 0, 0, 10, 0, 0)

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

        # fig = plt.figure()
        # ax = fig.add_subplot(111, projection='3d')
        # # ax.scatter([p[0] for p in points_in_3d], [p[1] for p in points_in_3d], [p[2] for p in points_in_3d])
        # ax.scatter(points_in_3d[0], points_in_3d[1], points_in_3d[2])
        # # ax.scatter([item[0][0] for item in points_in_3d], [item[0][1]])
        
        print(points_in_3d)

        pmap = PointMap()
        display = Display()

        pcd = o3d.geometry.PointCloud()
        visualizer = o3d.visualization.Visualizer()
        visualizer.create_window(window_name="3D plot", width=960, height=540)

        xyz = pmap.collect_points(points_in_3d)

        display.display_points3d(xyz, pcd, visualizer)

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
        return kp, desc, gray

    def matchFeatures(self, des_prev, desc_act):
        if des_prev is None or len(des_prev) < 2:
            return -1
        if desc_act is None or len(desc_act) < 2:
            return -1
        matches = self.BFMatcher.knnMatch(des_prev, desc_act, k=2)
        
        good_matches = []
        idx_of_des_from_f1, idx_of_des_from_f2 = [], []
        idx_set1, idx_set2 = set(), set()

        # for m, n in matches:
        #     if m.distance < 0.75 * n.distance:
        #         p1 = f1.kpus[m.queryIdx]
        #         p2 = f2.kpus[m.trainIdx]

        #         # ensure distance is within 32
        #         if m.distance < 32:
        #             if m.queryIdx not in idx_set1 and m.trainIdx not in idx_set2:
        #                 idx_of_des_from_f1.append(m.queryIdx)
        #                 idx_of_des_from_f2.append(m.trainIdx)
        #                 idx_set1.add(m.queryIdx)
        #                 idx_set2.add(m.trainIdx)

        #                 good_matches.append((p1, p2))

        # Apply ratio test
        goodMatches = []
        for m, n in matches:
            if m.distance < 0.70 * n.distance:
                goodMatches.append([m])
        return goodMatches, matches
