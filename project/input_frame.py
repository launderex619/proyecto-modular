import cv2

import config


def process_image(frame):
    # Redimencionar el fotograma a un tamaño mas manejable
    frame = resize_image(frame, config.VIDEO_WITDH_RESIZE, config.VIDEO_HEIGHT_RESIZE)
    gray = convert_image_to_gray_scale(frame)
    return gray


def resize_image(image, width, height):
    return cv2.resize(image, (width, height))


def convert_image_to_gray_scale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
