import cv2 as cv
import numpy as np
from numpy import *

from project.controllers import tracking_controller
from project.controllers import landmark_controller
from project.controllers.calibration_controller import CalibrationController
from project.modules import image_module
from project.utils import canvas_manager


def init():
    """
    Entry point of the project. Here we initialize all modules and threads that we require in order to start working.
    """
    print(
        "░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░\n",
        "┌─┐┌─┐░░░░░░░░░░░┌┐░░░░░░░░░░░░░░░░░░░░░░░░░░░░░┌┐░░░┌┐░░░░░░░░░░░░\n",
        "││└┘││░░░░░░░░░░░││░░░░░░░░░░░░░░░░░░░░░░░░░░░░┌┘└┐░░││░░░░░░░░░░░░\n",
        "│┌┐┌┐├──┬─┐┌──┬──┤│┌──┬┐┌┐░░░┌──┬─┬──┬┐░┌┬──┬──┼┐┌┘░░│└─┬┐░┌┐░░░░░░\n",
        "││││││┌┐│┌┐┤┌┐│──┤││┌┐│└┘│░░░│┌┐│┌┤┌┐││░│││─┤┌─┘││░░░│┌┐││░││░░░░░░\n",
        "││││││└┘││││└┘├──│└┤┌┐││││░░░│└┘│││└┘│└─┘││─┤└─┐│└┐░░│└┘│└─┘│░░░░░░\n",
        "└┘└┘└┴──┴┘└┴──┴──┴─┴┘└┴┴┴┘░░░│┌─┴┘└──┴─┐┌┴──┴──┘└─┘░░└──┴─┐┌┘░░░░░░\n",
        "░░░░░░░░░░░░░░░░░░░░░░░░░░░░░││░░░░░░┌─┘│░░░░░░░░░░░░░░░┌─┘│░░░░░░░\n",
        "░░░░░░░░░░░░░░░░░░░░░░░░░░░░░└┘░░░░░░└──┘░░░░░░░░░░░░░░░└──┘░░░░░░░\n",
        "┌───┐░░░░┌┐░░░░░░░░░░░░┌───┐░░░░░░░┌┐░░░░░░░░░░░┌───┐░░░░░░┌┐░░░░░░\n",
        "│┌─┐│░░░░││░░░░░░░░░░░░│┌─┐│░░░░░░░││░░░░░░░░░░░│┌─┐│░░░░░░││░░░░░░\n",
        "││░│├─┐┌─┘├─┬──┬──┐░░░░││░│├─┬─┐┌──┤│┌──┬──┐░░░░││░│├┐░┌┬──┤│┌──┐░░\n",
        "│└─┘│┌┐┤┌┐│┌┤│─┤──┤░░░░││░││┌┤┌┐┤│─┤││┌┐│──┤░░░░│└─┘││░││┌┐│││┌┐│░░\n",
        "│┌─┐││││└┘││││─┼──│░░░░│└─┘│││││││─┤└┤┌┐├──│░░░░│┌─┐│└─┘│┌┐│└┤┌┐│░░\n",
        "└┘░└┴┘└┴──┴┘└──┴──┘░░░░└───┴┘└┘└┴──┴─┴┘└┴──┘░░░░└┘░└┴─┐┌┴┘└┴─┴┘└┘░░\n",
        "░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░┌─┘│░░░░░░░░░░░\n",
        "░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░└──┘░░░░░░░░░░░\n",
        "┌───┐░░░░┌┐░░░░░░░┌───┐░░░░░░░░░░░░░░░┌┐░┌┐░░┌┐░░░░░░░░░░░░░░░░░░░░\n",
        "│┌─┐│░░░░││░░░░░░░│┌─┐│░░░░░░░░░░░┌┐░░││░│└┐┌┘│░░░░░░░░░░░░░░░░░░░░\n",
        "││░└┼──┬─┤│┌──┬──┐││░└┼──┬─┬┐┌┬──┐└┼──┤│░└┐││┌┼──┬───┬──┬┐┌┬──┬───┐\n",
        "││░┌┤┌┐│┌┤││┌┐│──┤││░┌┤┌┐│┌┤└┘│┌┐│┌┤┌┐││░░│└┘││┌┐├──││┌┐│││││─┼──││\n",
        "│└─┘│┌┐│││└┤└┘├──││└─┘│┌┐││└┐┌┤┌┐│││┌┐│└┐░└┐┌┘│┌┐││──┤└┘│└┘││─┤│──┤\n",
        "└───┴┘└┴┘└─┴──┴──┘└───┴┘└┴┘░└┘└┘└┘│├┘└┴─┘░░└┘░└┘└┴───┴─┐├──┴──┴───┘\n",
        "░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░┌┘│░░░░░░░░░░░░░░░░░░░││░░░░░░░░░░\n",
        "░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░└─┘░░░░░░░░░░░░░░░░░░░└┘░░░░░░░░░░\n",
        "┌┐░░░░░░░░░░░┌──┐░░░░┌┐░░░░░┌─┐┌─┐░░░░┌┐░░░░░░░░┌───┐░░┌┐░░░░░░░░░░\n",
        "││░░░░░░░░░░░│┌┐│░░░┌┘└┐░░░░││└┘││░░░░││░░░░░░░░│┌─┐│░░││░░░░░░░░░░\n",
        "││░░┌┐┌┬┬──┐░│└┘└┬──┼┐┌┼──┐░│┌┐┌┐├──┬─┘├┬─┐┌──┐░││░└┼──┤│┌┐┌┬──┬─┐░\n",
        "││░┌┤││├┤──┤░│┌─┐││─┤│││┌┐│░│││││││─┤┌┐├┤┌┐┤┌┐│░││┌─┤┌┐│││└┘│┌┐│┌┐┐\n",
        "│└─┘│└┘│├──│░│└─┘││─┤│└┤└┘│░│││││││─┤└┘│││││┌┐│░│└┴─│┌┐│└┼┐┌┤┌┐││││\n",
        "└───┴──┴┴──┘░└───┴──┘└─┴──┘░└┘└┘└┴──┴──┴┴┘└┴┘└┘░└───┴┘└┴─┘└┘└┘└┴┘└┘\n",
        "░░Todos░los░derechos░reservados░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░\n",
    )
    # TODO: Cambiar esto por una webcam juas juas
    _video_path = '/Users/lumedina/Documents/Uni/proyecto-modular/project/assets/video/calibracion.mp4'

    # Controlador de calibracion
    calibrationController = CalibrationController()
    calibrationController.calibrate()
    # PATH = os.path.dirname(os.path.abspath(__file__))
    _cap = cv.VideoCapture(_video_path)  # initialize an object based on the webcam

    _tracker_controller = tracking_controller.Tracker()
    _landmark_controller = landmark_controller.LandmarkController()

    ret = True
    frame_counter = 1
    # obtener el primer frame
    while ret:
        ret, imagefirstframe = _cap.read()
        if ret:
            _tracker_controller.set_image(image_module.process_image(imagefirstframe))
            _tracker_controller.create_keypoints()
            ret = not ret

    while _cap.isOpened():
        ret, image = _cap.read()

        if ret:
            continue

        # Filtramos la imagen
        gray_image = image_module.filter_frame(image)

        # Obtenemos keypoints y descriptores
        kp_actual, dp = _tracker_controller.detect_features_and_descriptors(gray_image)
        # Obtenemos los matches en base a los descriptores
        matches = _tracker_controller.matchFeatures(dp)
        # Si no hay matches nos saltamos al siguiente frame
        if matches == -1:
            continue

        # Encontramos los landmarks, los etiquetamos y los guardamos a lo largo de los frames
        _landmark_controller.update_landmarks(frame_counter, matches, _tracker_controller.getLastFrameKeypoints(), kp_actual)

        # Creamos una copia de la imagen filtrada para imprimir los keypoints
        image_with_labeled_keypoints = array(_tracker_controller.image)

        # for i, keypoint in enumerate(_tracker_controller.getLastFrameKeypoints()):
        #     image_module.draw_identifier_keypoint(str(i), image_with_labeled_keypoints, keypoint.pt, (10.0, 10.0))
        # img = image_module.create_image_of_matches(image_with_labeled_keypoints,
        #                                            _tracker_controller.getLastFrameKeypoints(), gray_image, kp,
        #                                            matches)
        for point in _landmark_controller.get_points_by_frame(frame_counter):
            taggg = _landmark_controller.get_landmark_by_point(point)
            if taggg is not None:
                taggg = taggg.tag
            else:
                taggg = str(point.frame_number)
            image_module.draw_identifier_keypoint(
                taggg,
                image_with_labeled_keypoints,
                (point.x, point.y),
                (10.0, 10.0))

        # TODO: Necesitamos agrupar los keypoints que esten super cercanos unos de otros para tomarlos como el mismo elemento

        cv.imshow("matches", image_with_labeled_keypoints)
        # cv.imshow("imagen", filtered_image)
        # cv.imshow("blur", gray_image)

        # Show image with keypoints
        # cv.imshow('keypoints', _tracker_controller.last_frame.get('image'))
        # cv.imshow('keypoints', _tracker_controller.image)

        # mappper.map_with_new_keypoints()

        # creamos
        _tracker_controller.replaceLastFrame(kp_actual, dp)

        # ======= PNP, ProjectPoints & Triangulate ======= 
        #@ objp      => vector 3x, (x, y, z)  {son los matches pero con una tercera dimesion z (23.10, 90.73, z?)} antes z era 0
        #@ corners2  => kp, (ver si son (x,y))
        #@ mtx       => se obtiene en la calibracion, 
        #@ dist => se obtine en la calibracion

        objp_anterior = []
        for p in kp_actual:
            objp_actual.append([p.pt[0], p.pt[1], 0])

        objp_actual = []
        for p in _tracker_controller.getLastFrameKeypoints():
            objp_actual.append([p.pt[0], p.pt[1], 0])

        ret, rvecs_anterior, tvecs_anterior = cv.solvePnP(objp_anterior, _tracker_controller.getLastFrameKeypoints(), calibrationController.mtx, calibrationController.dist) 
        ret, rvecs_actual, tvecs_actual = cv.solvePnP(objp_actual, kp_actual, calibrationController.mtx, calibrationController.dist) 
      
        #@ objp => object points (3d coordinates) cada keypoint que haya tenido match con el fram anterior (recorrer lista de los matches y hacer su proyeccoiob)
        #@ rvecs => viene de pnp
        #@ tvecs => viene de pnp
        #@ mtx => viene de la calibracion
        #@ dist => viene de la calibracion 
        
        # imgpts, jac = cv.projectPoints(objp, rvecs, tvecs, calibrationController.mtx, calibrationController.dist)

        #? matrizProyecion1 => de donde se saca??
        #? matrizProyecion2 =>
        #@ proj_points_1 => los sacamode de cv.projectpoints (frame anterior)
        #@ proj_points_2 => los sacamode de cv.projectpoints

        matrizProyecion1 = np.array(3,4)
        matrizProyecion1[0][0] = rvecs_anterior[0]
        matrizProyecion1[1][1] = rvecs_anterior[1]
        matrizProyecion1[2][2] = rvecs_anterior[2]
        
        matrizProyecion1[0][3] = tvecs_anterior[0]
        matrizProyecion1[1][3] = tvecs_anterior[1]
        matrizProyecion1[2][3] = tvecs_anterior[2]

        matrizProyecion2 = np.array(3,4)
        matrizProyecion2[0][0] = rvecs_actual[0]
        matrizProyecion2[1][1] = rvecs_actual[1]
        matrizProyecion2[2][2] = rvecs_actual[2]
        
        matrizProyecion2[0][3] = tvecs_actual[0]
        matrizProyecion2[1][3] = tvecs_actual[1]
        matrizProyecion2[2][3] = tvecs_actual[2]
        
        points_in_3d = cv.triangulatePoints(matrizProyecion1, matrizProyecion2, kp_actual, _tracker_controller.getLastFrameKeypoints())

        frame_counter += 1
        if cv.waitKey(25) & 0xFF == ord('q'):
            break

    _cap.release()
    cv.destroyAllWindows()
