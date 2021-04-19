import cv2 as cv

import input_frame
import tracking_module


def init():
    """  """
    cap = cv.VideoCapture(0)  # initialize an object based on the webcam

    while cap.isOpened():
        ret, frame = cap.read()
        if ret:
            # Por cada frame, procesamos la imagen y retorna un objeto con la imagen procesada
            processed = input_frame.process_image(frame)
            tracker = tracking_module.Tracker(processed)

            # result = slam(proceessed)

            if cv.waitKey(25) & 0xFF == ord('q'):
                break

        else:
            break

    cap.release()
    cv.destroyAllWindows()
