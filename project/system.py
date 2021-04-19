import cv2 as cv

import input_frame
import tracking_module
import utils.canvas_manager as cvn_manager

import config


def init():
    """  """
    cap = cv.VideoCapture(0)  # initialize an object based on the webcam

    tracker = tracking_module.Tracker()
    # mappper = ...

    while cap.isOpened():
        ret, image = cap.read()
        if ret:
            gray_image = input_frame.process_image(image)

            tracker.set_image(gray_image)
            tracker.create_keypoints()
            tracker.update_image_from_keypoints()

            # creacion de los canvas para mostrar la imagen
            gray = Helper.createImageFromKeypoints(gray, keypoints)

            if cv.waitKey(25) & 0xFF == ord('q'):
                break

        else:
            break

    cap.release()
    cv.destroyAllWindows()
