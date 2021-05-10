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
    video_path = '../common/video/cards.mp4'
    cap = cv.VideoCapture(video_path)  # initialize an object based on the webcam

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
            gray_image = input_frame.process_image(image)

            kp, dp = tracker.detect_features_and_descriptors(gray_image)
            matches = tracker.matchFeatures(dp)
            if (matches == -1):
                continue

            image_copy = array(tracker.image)
            for i, keypoint in enumerate(tracker.getLastFrameKeypoints()):
                canvas_manager.draw_identifier_keypoint(str(i), image_copy, keypoint.pt, (10.0, 10.0))
            img = canvas_manager.create_image_of_matches(image_copy, tracker.getLastFrameKeypoints(), gray_image, kp, matches)

            # TODO: Necesitamos agrupar los keypoints que esten super cercanos unos de otros para tomarlos como el mismo elemento

            cv.imshow("matches", img)


            # Show image with keypoints
            # cv.imshow('keypoints', tracker.last_frame.get('image'))
            # cv.imshow('keypoints', tracker.image)

            # mappper.map_with_new_keypoints()

            # creamos
            tracker.set_image(gray_image)
            tracker.replaceLastFrame(kp, dp)

            if cv.waitKey(25) & 0xFF == ord('q'):
                break
        else:
            break

    cap.release()
    cv.destroyAllWindows()
