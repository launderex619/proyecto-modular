import cv2 as cv


class MatcherController:
    """
    This class is used to match the query image to the training images.
    """

    def __init__(self):

        self.matcher = cv.BFMatcher(cv.NORM_HAMMING, crossCheck=False)

    def match(self, query_image, train_images):
        pass
