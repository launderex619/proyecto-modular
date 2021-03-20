import time
import cv2
import sys
import helper as Helper
import numpy as np
import matplotlib.pyplot as plt

from mapController import MapController
from videoModel import VideoModel
from analysisController import AnalysisController

# constants
VIDEO_PATH = 'C:\\Users\\andre\\Documents\\Git\\proyecto-modular\\testing-algorithms\\feature_algorithm\\videos\\video2.mp4'
VIDEO_WITDH_RESIZE = 960
VIDEO_HEIGHT_RESIZE = 540
KEY_ENTER = 13
ZERO_DESCRIPTORS_ERROR = -1
FAST_THRESHOLD = 70


def startSystem(videoModel, analysisController, mapController):
    counter = 0
    for i in range(1, videoModel.getNumberFrames()):
        # usaremos esto para fijar el framerate
        now = time.time()
        # obtencion del frame actual
        _, frame = videoModel.getNextFrame()
        # redimencionar el fotograma a un tamaño mas manejable
        frame = Helper.resizeImage(frame, VIDEO_WITDH_RESIZE, VIDEO_HEIGHT_RESIZE)
        gray = Helper.convertImageToGrayScale(frame)
        # obtencion de los keypoints y descriptors
        keypoints, descriptors = analysisController.detectFeaturesAndDescriptors(gray)
        # creacion de los canvas para mostrar la imagen
        blankCanvas = Helper.createBlankCanvas(VIDEO_WITDH_RESIZE, VIDEO_HEIGHT_RESIZE)
        blankCanvas = Helper.createImageFromKeypoints(blankCanvas, keypoints)
        gray = Helper.createImageFromKeypoints(gray, keypoints)
        # mostramos los keypoints
        #-- Helper.showImage('Gris', gray)
        Helper.showImage('Keypoints', blankCanvas)
        # creamos los matches entre los puntos
        lastFrame = analysisController.getLastFrame()
        # if(lastFrame.get('keypoints'))
        matches = analysisController.matchFeatures(descriptors)
        if matches is ZERO_DESCRIPTORS_ERROR:
            continue
        # mostramos los matches
        matchesImg = Helper.createImageOfMatches(
            lastFrame.get('image'),
            lastFrame.get('keypoints'),
            gray,
            keypoints,
            matches
        )
        Helper.showImage('matches', matchesImg)

        ## obtener la distancia de los keypoints
        pairPoints = analysisController.getPairPointArray(matches, keypoints)
        pairPoints = analysisController.filterOutliers(pairPoints)
        velocityVector = analysisController.getVelocityVector(pairPoints)
        if len(pairPoints) > 0:
            mapController.moveCamera(velocityVector)
            for pairPoint in pairPoints:
                mapController.addPoints(pairPoint.get('trainPoint'))
        # Mostramos el recorrido de la camara
        pointX, pointY = zip(*mapController.getPoints())
        cameraX, cameraY = zip(*mapController.getCameraMovement())
        plt.scatter(pointX, pointY, c="black")
        plt.plot(cameraX, cameraY, c="red", marker='.', linestyle=':')
        if counter % 50 == 0:
            plt.show()
        # reemplazamos el frame anterior para nuevas comparaciones
        analysisController.replaceLastFrame(keypoints, descriptors, gray)
        counter += 1
        # Esto mantiene el tiempo constante (pone cada frame cada x tiempo constantemente)
        timeDiff = time.time() - now
        # if timeDiff < 1.0 / (videoModel.getFrameRate()):
        #     time.sleep(1.0 / (videoModel.getFrameRate()) - timeDiff)
        key = cv2.waitKey(1)
        if key == KEY_ENTER:
            break


if __name__ == "__main__":
    # 1- get video
    print(VIDEO_PATH)
    videoModel = VideoModel(VIDEO_PATH)
    # 2- start image processing
    # we need the first frame to initializate all the system so:
    hasFrames, frame = videoModel.getNextFrame()
    if (not hasFrames):
        print("Error, no image or video detected")
        sys.exit()
    gray = Helper.convertImageToGrayScale(frame)
    analysisController = AnalysisController(gray, FAST_THRESHOLD)
    mapController = MapController()
    startSystem(videoModel, analysisController, mapController)
    exit(0)
