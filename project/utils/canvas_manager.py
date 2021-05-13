import operator

import cv2
import numpy as np

import project.config as config


def createBlankCanvas(width, height):
    blank_canvas = np.zeros((height, width, 3), np.uint8)
    blank_canvas.fill(255)
    return blank_canvas


def draw_identifier_keypoint(tag, img, center_pixel, size):
    green_color = (255, 255, 0)
    black_color = (0, 0, 0)
    center_pixel = (int(center_pixel[0]), int(center_pixel[1]))
    size = (int(size[0]), int(size[1]))
    cv2.rectangle(img, tuple(map(operator.sub, center_pixel, size)), tuple(map(operator.add, center_pixel, size)), black_color, 2)
    cv2.circle(img, center_pixel, 1, green_color, 1)
    cv2.putText(img, tag, tuple(map(operator.sub, center_pixel, size)), cv2.FONT_ITALIC, .5, black_color)

def create_image_of_matches(lastFrameImage, keypontsLastFrame, actualFrameImage, keypointsActualFrame, matches):
    # cv.drawMatchesKnn expects list of lists as matches.
    return cv2.drawMatchesKnn(lastFrameImage,
                              keypontsLastFrame,
                              actualFrameImage,
                              keypointsActualFrame,
                              matches,
                              None,
                              flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)