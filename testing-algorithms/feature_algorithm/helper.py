import cv2
import numpy as np


def showImage(imageName, image):
    cv2.imshow(imageName, image)


def resizeImage(image, width, height):
    return cv2.resize(image, (width, height))


def convertImageToGrayScale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


def createBlankCanvas(width, height):
    blankCanvas = np.zeros((height, width, 3), np.uint8)
    blankCanvas.fill(255)
    return blankCanvas


def createImageFromKeypoints(image, kp):
    return cv2.drawKeypoints(image, kp, None, color=(255, 0, 0))


def createImageOfMatches(lastFrameImage, keypontsLastFrame, actualFrameImage, keypointsActualFrame, matches):
    # cv.drawMatchesKnn expects list of lists as matches.
    return cv2.drawMatchesKnn(lastFrameImage,
                              keypontsLastFrame,
                              actualFrameImage,
                              keypointsActualFrame,
                              matches,
                              None,
                              flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
