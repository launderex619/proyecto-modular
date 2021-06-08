import cv2 as cv
from numpy import *
from numpy import array

import input_frame
import tracking_module
import utils.canvas_manager as cvn_manager

import config
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
    video_path = '../common/video/chessboard.mp4'
    cap = cv.VideoCapture(video_path)  # initialize an object based on a video

    tracker = tracking_module.Tracker()
    # mappper = ...
    ret = True
    # obtener el primer frame
    while ret:
        ret, imagefirstframe = cap.read()
        tracker.set_image(input_frame.process_image(imagefirstframe))
        tracker.create_keypoints()
        ret = not ret

    while cap.isOpened():
        ret, image = cap.read()
        if ret:

            # obtenemos el frame actual en gris
            gray_image = input_frame.process_image(image)

            # sacamos kps y dps del frame gris
            kp, dp = tracker.detect_features_and_descriptors(gray_image)

            # sacamos matches chidos y los índices de los descriptores de cada frame
            # matches, idx1, idx2 = tracker.matchFeatures(kp, dp)

            # proj_points_1 = np.array([
            #     np.array([kpt.pt[0] for kpt in matches[:, 0]]),
            #     np.array([kpt.pt[1] for kpt in matches[:, 0]])
            # ])
            #
            # proj_points_2 = np.array([
            #     np.array([kpt.pt[0] for kpt in matches[:, 1]]),
            #     np.array([kpt.pt[1] for kpt in matches[:, 1]])
            # ])
            #
            # proc_img = cv.drawKeypoints(gray_image, kp, None, color=(255, 0, 0))

            cv.imshow("gray", gray_image)

            tracker.set_image(gray_image)
            tracker.replaceLastFrame(kp, dp)

            if cv.waitKey(25) & 0xFF == ord('q'):
                break
        else:
            break

    cap.release()
    cv.destroyAllWindows()
