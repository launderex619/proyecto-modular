import cv2 as cv
import numpy as np

def init(): 
    """  """
    cap = cv.VideoCapture(0) # initialize an object based on the webcam

    while ( cap.isOpened() ):
        ret, frame = cap.read()
        if ret == True:

            # TODO
            # por cada frame, procesamos la imagen y retorna un objeto con la imagen procesada
            # processed = processImage( frame ) 
            # result = slam( proceessed )

            if cv.waitKey(25) & 0xFF == ord('q'):
                break
    
        else:
            break

    cap.release()
    cv.destroyAllWindows()

