import cv2

import config


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
    frame = resize_image(frame, config.VIDEO_WITDH_RESIZE, config.VIDEO_HEIGHT_RESIZE)
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
