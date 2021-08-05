import cv2 as cv
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
    _video_path = 'assets/video/calibracion.mp4'

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

            # Filtramos la imagen
            gray_image = image_module.filter_frame(image)
            # Obtenemos keypoints y descriptores
            kp, dp = _tracker_controller.detect_features_and_descriptors(gray_image)
            # Obtenemos los matches en base a los descriptores
            matches = _tracker_controller.matchFeatures(dp)
            # Si no hay matches nos saltamos al siguiente frame
            if matches == -1:
                continue

            # Encontramos los landmarks, los etiquetamos y los guardamos a lo largo de los frames
            _landmark_controller.update_landmarks(frame_counter, matches, _tracker_controller.getLastFrameKeypoints(), kp)

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
            _tracker_controller.set_image(gray_image)
            _tracker_controller.replaceLastFrame(kp, dp)

            frame_counter += 1
            if cv.waitKey(25) & 0xFF == ord('q'):
                break
        else:
            break

    _cap.release()
    cv.destroyAllWindows()
