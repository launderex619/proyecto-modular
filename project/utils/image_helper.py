import cv2 as cv


def resize_image(image, width, height):
    """
      Resize the frame to size specified in params.
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
    return cv.resize(image, (width, height))


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
    return cv.cvtColor(image, cv.COLOR_BGR2GRAY)
