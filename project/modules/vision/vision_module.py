import numpy as np
import cv2 as cv
import math as m

from project.controllers.vision import orb_controller as oc
from project.controllers.vision import matcher_controller as mc
from project.core import config
from project.utils import image_helper


class Display:
    # TODO: Mover esta clase a donde corresponda
    def __init__(self):
        self.W = 960
        self.H = 540

    def display_points2d(self, img, kpts, matches):
        if kpts != 0:
            for kpt in kpts:
                cv.circle(img, (int(kpt.pt[0]), int(kpt.pt[1])), radius=2, color=(
                    0, 255, 0), thickness=-1)

        if matches != 0:
            for match in matches:
                (u1, v1) = np.int32(match[0].pt)
                (u2, v2) = np.int32(match[1].pt)
                cv.line(img, (u1, v1), (u2, v2),
                        color=(0, 0, 255), thickness=1)
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
    # TODO: Mover esta clase a donde corresponda
    def __init__(self):
        self.array = [0, 0, 0]

    def collect_points(self, tripoints):
        if len(tripoints) > 0:
            array_to_project = np.array([0, 0, 0])

            x_points = [pt for pt in tripoints[0]]
            y_points = [-pt for pt in tripoints[1]]
            z_points = [-pt for pt in tripoints[2]]

            for i in range(tripoints.shape[1]):
                curr_array = np.array([x_points[i], y_points[i], z_points[i]])
                array_to_project = np.vstack((array_to_project, curr_array))

            array_to_project = array_to_project[1:, :]

            return array_to_project


class VisionModule:
    """
    This class is responsible for processing the frames
    """

    def __init__(self):
        """
        TODO: Use data received in input_drone_data
        """
        self.orb_controller = oc.ORBController()
        self.matcher_controller = mc.MatcherController()
        # self.image_controller = ic.ImageController() TODO: implement image controller
        # self.video = not implemented

    def rotate(self, phi, theta, psi):
        # TODO: Mover este metodo a donde corresponda
        phi = m.pi/2
        theta = m.pi/4
        psi = m.pi/2

        R = self.Rz(psi) * self.Ry(theta) * self.Rx(phi)
        return R

    def translate(self, x0, y0, z0, x1, y1, z1):
        # TODO: Mover este metodo a donde corresponda
        difx = x1 - x0
        dify = y1 - y0
        difz = z1 - z0
        return np.array([x0 + difx, y0 + dify, z0 + difz])

    def process(self, frame_act, frame_prev):
        """
        This method process the frame doing all the necessary steps to monoslam
        we could say this is the most important method of the module
        """
        new_frame_act = image_helper.resize_image(
            frame_act, config.VIDEO_WITDH_RESIZE, config.VIDEO_HEIGHT_RESIZE)
        new_frame_prev = image_helper.resize_image(
            frame_prev, config.VIDEO_WITDH_RESIZE, config.VIDEO_HEIGHT_RESIZE)
        frame_act_gray = image_helper.convert_image_to_gray_scale(
            new_frame_act)
        frame_prev_gray = image_helper.convert_image_to_gray_scale(
            new_frame_prev)

        # Obtenemos los keypoints del frame actual y el anterior
        kps_act, desc_act,  = self.get_keypoints_and_descriptors(
            frame_act_gray)
        kps_prev, desc_prev = self.get_keypoints_and_descriptors(
            frame_prev_gray)

        # Dibujamos los keypoints detectados
        """
        TODO: Implement the method to draw the keypoints in the image_controller
                img_act = cv.drawKeypoints(new_frame_act, kps_act, 0, color=(0,255,0), flags=cv.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
                img_prev = cv.drawKeypoints(new_frame_prev, kps_prev, 0, color=(0,255,0), flags=cv.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
        """

        # Mostramos las imagenes
        """
        TODO: Implement the method to show the images in the image_controller
        plt.imshow(img1)
        plt.show()
        plt.imshow(img2)
        plt.show()
        """

        # Obtenemos los matches y filtramos los keypoints que necesitamos del frame actual y el anterior
        # recordando: query = actual; train = previo
        matches, _ = self.matchFeatures(desc_prev, desc_act)

        kp_xy_ant = []
        kp_xy_act = []
        for match in matches:
            kp_xy_ant.append(np.asarray(kps_prev[match[0].trainIdx].pt))
            kp_xy_act.append(np.asarray(kps_act[match[0].queryIdx].pt))

        kp_xy_ant = np.asarray(kp_xy_ant).T
        kp_xy_act = np.asarray(kp_xy_act).T

        #  TODO: Meter las 2 lineas de abajo en el controlador ImageController
        # plt.imshow(cv.drawMatchesKnn(img_ant,kps_ant,img_act,kps_act,matches,None))
        # plt.show()

        # Angulos del dron euler
        R1 = self.rotate(0, 0, 0)
        # posiciones GPS (x, y, z) del dron
        T1 = self.translate(0, 0, 0, 0, 0, 0)

        R2 = self.rotate(0, 0, 0)
        T2 = self.translate(0, 0, 0, 10, 0, 0)

        projection_mtx1 = np.array(
            [[R1[0, 0], R1[0, 1], R1[0, 2], T1[0]],
             [R1[1, 0], R1[1, 1], R1[1, 2], T1[1]],
             [R1[2, 0], R1[2, 1], R1[2, 2], T1[2]]]
        )
        projection_mtx2 = np.array(
            [[R2[0, 0], R2[0, 1], R2[0, 2], T2[0]],
             [R2[1, 0], R2[1, 1], R2[1, 2], T2[1]],
             [R2[2, 0], R2[2, 1], R2[2, 2], T2[2]]]
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

        pmap = PointMap()
        display = Display()

        """
        TODO:
        pcd = o3d.geometry.PointCloud()
        visualizer = o3d.visualization.Visualizer()
        visualizer.create_window(window_name="3D plot", width=960, height=540)

        xyz = pmap.collect_points(points_in_3d)

        display.display_points3d(xyz, pcd, visualizer)
        """

    def start_analysis(self):
        """
        TODO: Using input data received from input_drone_data, do a while loop
        to process the frames calling self.process()
        """
        pass

    def get_keypoints_and_descriptors(self, frame):
        """
        This method returns the keypoints and descriptors of the frame
        """
        return self.orb_controller.get_keypoints_and_descriptors(frame)
