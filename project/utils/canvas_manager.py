import cv2
import numpy as np

import project.config as config


def createBlankCanvas(width, height):
    blank_canvas = np.zeros((height, width, 3), np.uint8)
    blank_canvas.fill(255)
    return blank_canvas
