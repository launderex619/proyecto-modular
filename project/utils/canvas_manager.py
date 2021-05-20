import operator

import cv2
import numpy as np


def createBlankCanvas(width, height):
    blank_canvas = np.zeros((height, width, 3), np.uint8)
    blank_canvas.fill(255)
    return blank_canvas
