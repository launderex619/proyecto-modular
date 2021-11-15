import cv2 as cv

from project.core import config
from project.utils import image_helper


class ORBController:
    """
    This class is used to detect and track features in an image.
    """

    def __init__(self):
        self.orb = cv.ORB_create(nlevels=5, firstLevel=1, edgeThreshold=1,
                                 nfeatures=50, fastThreshold=config.FAST_THRESHOLD)

    def process_image(self, image):
        pass

    def get_keypoints_and_descriptors(self, image):
        """
        This function returns the keypoints and descriptors of an image.
        :param image: The image to process.
        :return: The keypoints and descriptors of the image.
        """
        return self.orb.detectAndCompute(image, None)
