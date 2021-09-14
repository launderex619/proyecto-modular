import cv2
import numpy as np

from core import config


class Tracker:
    def __init__(self):
        self.image = None
        self.last_frame = None

        # TODO esto chance va en mapper
        self.orb = cv2.ORB_create(nlevels=8, firstLevel=1, edgeThreshold=1,
                                  nfeatures=20, fastThreshold=config.FAST_THRESHOLD)
        self.BFMatcher = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=False)

    def set_image(self, image):
        """
        Setter to add an image

        Parameters
        ----------
        image: Array[3]
            Image represented by 3 layers (R,G,B) created by openCV
        """
        self.image = image

    def replaceLastFrame(self, keypoints, descriptors):
        """
        Setter to replace a given frame into the object

        Parameters
        ----------
        keypoints: Array
            ORB given keypoints
        descriptors: Array
            ORB given descriptors
        """
        # TODO Frame puede ser un objeto
        self.last_frame = {
            'keypoints': keypoints,
            'descriptors': descriptors,
            'image': self.image
        }

    def getLastFrame(self):
        """
        Getter to retrieve the last frame

        returns
        ----------
        last_frame: Dictionary
            ORB given keypoints, descriptors and cv2 image
        """
        return self.last_frame

    def getLastFrameKeypoints(self):
        """
        Getter to retrieve the last frame keypoints

        returns
        ----------
        keypoints: Array
            ORB given keypoints
        """
        return self.last_frame.get('keypoints')

    def getLastFrameDescriptors(self):
        return self.last_frame.get('descriptors')

    def detect_features_and_descriptors(self, image):
        """Detects keypoints and computes the descriptors of self.image

        Returns
        ----------
        Keypoints, Descriptors: Array
            ORB given keypoints,
            ORB given descriptors
        """
        return self.orb.detectAndCompute(image, None)

    def create_keypoints_self_image(self):
        """Detects keypoints and computes the descriptors of self.image and replaces last_frame to given information.

        returns
        ----------
        last_frame: Dictionary
            ORB given keypoints, descriptors and cv2 image
        """
        kp, desc = self.detect_features_and_descriptors(self.image)
        self.replaceLastFrame(kp, desc)

    def add_keypoints_into_image(self):
        """Update the image information to add the keypoints inside the image.
        """
        self.image = cv2.drawKeypoints(
            self.image, self.last_frame['keypoints'], None, color=(255, 0, 0))

    # ===========

    def matchFeatures(self, descriptors):
        if descriptors is None or len(descriptors) < 2:
            return -1
        matches = self.BFMatcher.knnMatch(
            self.last_frame.get('descriptors'), descriptors, k=2)
        # Apply ratio test
        goodMatches = []
        for m, n in matches:
            if m.distance < 0.70 * n.distance:
                goodMatches.append([m])
        return goodMatches

    def getPairPointArray(self, matches, keypoints):
        points = []
        for match in matches:
            queryPoint = self.last_frame.get('keypoints')[match[0].queryIdx].pt
            trainPoint = keypoints[match[0].trainIdx].pt
            distance = self.getEuclideanDistance(queryPoint, trainPoint)
            pair = {
                'queryPoint': queryPoint,
                'trainPoint': trainPoint,
                'distance': distance
            }
            points.append(pair)
        return points

    def getEuclideanDistance(self, queryPoint, trainPoint):
        distance = np.sqrt(
            (queryPoint[0] - trainPoint[0]) ** 2 + (queryPoint[1] - trainPoint[1]) ** 2)
        # distance = np.linalg.norm(point_np, ord=2, axis=1)
        return distance

    def filterOutliers(self, points):
        if len(points) < 1:
            return []
        distances = list(
            map((lambda element: element.get('distance')), points))
        percentiles = np.percentile(distances, [25, 50, 75])  # (Q1, median Q3)
        filtered = list(filter((lambda element: percentiles[0] <= element.get(
            'distance') <= percentiles[2]), points))
        return filtered

    def getVelocityVector(self, points):
        if len(points) == 0:
            return 0, 0
        velocity = (0, 0)
        for point in points:
            x1, y1 = point.get('queryPoint')
            x2, y2 = point.get('trainPoint')
            x, y = (x1 - x2, y2 - y1)
            velocity = np.add(velocity, (x, y))
        velocity = (-1 * velocity[0] / len(points), -
                    1 * velocity[1] / len(points))
        return velocity
