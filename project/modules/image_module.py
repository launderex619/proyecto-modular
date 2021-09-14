import operator
from typing import List

import cv2

from core import config


def process_image(frame):
    """Resize the frame to a more manageable size specified in config.CONSTANTS and transform it to grayscale.

    Params
    ----------
    frame: Array[][]
        frame of cv2 video or stream

    Returns
    ----------
    Image: Array[][]
        Grayscale resized image.
    """
    frame = resize_image(frame, config.VIDEO_WITDH_RESIZE,
                         config.VIDEO_HEIGHT_RESIZE)
    gray = convert_image_to_gray_scale(frame)
    return gray


def resize_image(image, width, height):
    """Resize the frame to size specified in params.

    Params
    ----------
    image: Array[][]
        frame of cv2 video or stream
    width: int
        width in pixels
    height: int
        height in pixels

    Returns
    ----------
    Image: Array[][]
        Grayscale resized image.
    """
    return cv2.resize(image, (width, height))


def convert_image_to_gray_scale(image):
    """Transforms the image to grayscale.

    Params
    ----------
    image: Array[][]
        frame of cv2 video or stream

    Returns
    ----------
    Image: Array[][]
        Grayscale image.
    """
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


def filter_frame(image: List[object]) -> List[object]:
    '''
    Este metodo aplica un filtro gaussiano difuminado y un filtro gaussiano adaptativo
    :param image: image[int][int]
    :return: image[int][int]
    '''
    # image = cv2.GaussianBlur(image, (11, 11), 0)
    image = process_image(image)
    # image = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 5)
    return image


def draw_identifier_keypoint(tag, img, center_pixel, size):
    green_color = (255, 255, 0)
    black_color = (0, 0, 0)
    center_pixel = (int(center_pixel[0]), int(center_pixel[1]))
    size = (int(size[0]), int(size[1]))
    cv2.rectangle(
        img,
        tuple(map(operator.sub, center_pixel, size)),
        tuple(map(operator.add, center_pixel, size)),
        black_color,
        2)
    cv2.circle(img, center_pixel, 1, green_color, 1)
    cv2.putText(img, tag, tuple(map(operator.sub, center_pixel, size)),
                cv2.FONT_ITALIC, .5, black_color)


def create_image_of_matches(lastFrameImage, keypontsLastFrame, actualFrameImage, keypointsActualFrame, matches):
    # cv.drawMatchesKnn expects list of lists as matches.
    return cv2.drawMatchesKnn(lastFrameImage,
                              keypontsLastFrame,
                              actualFrameImage,
                              keypointsActualFrame,
                              matches,
                              None,
                              flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
