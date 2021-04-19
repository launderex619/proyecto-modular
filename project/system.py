import cv2 as cv

import input_frame
import tracking_module
import utils.canvas_manager as cvn_manager

import config


def init():
    """  """
    cap = cv.VideoCapture(0)  # initialize an object based on the webcam

    while cap.isOpened():
        ret, frame = cap.read()
        if ret:
            gray = input_frame.process_image(frame)
            tracker = tracking_module.Tracker(gray)
            keypoints, descriptors = tracker.detect_features_and_descriptors(gray)
            canvas = cvn_manager.createBlankCanvas(config.VIDEO_WITDH_RESIZE, config.VIDEO_HEIGHT_RESIZE)

            img_with_kp = tracker.createImageFromKeypoints(gray, keypoints)

            # creacion de los canvas para mostrar la imagen
            gray = Helper.createImageFromKeypoints(gray, keypoints)

            if cv.waitKey(25) & 0xFF == ord('q'):
                break

        else:
            break

    cap.release()
    cv.destroyAllWindows()
