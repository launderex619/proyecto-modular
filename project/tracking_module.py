import cv2
import numpy as np

import config


class Tracker:
    def __init__(self, image):
        self.orb = cv2.ORB_create(fastThreshold=config.FAST_THRESHOLD)
        self.BFMatcher = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=False)
        kp, desc = self.detectFeaturesAndDescriptors(image)
        self.lastFrame = {
            'keypoints': kp,
            'descriptors': desc,
            'image': image
        }

    def detectFeaturesAndDescriptors(self, image):
        """Detects keipoints and computes the descriptors of given image
        Args:
            image (bgrImage): [description]

        Returns:
           Keypoints, Descriptors: [description]
        """
        return self.orb.detectAndCompute(image, None)

    def replaceLastFrame(self, keypoints, descriptors, image):
        self.lastFrame = {
            'keypoints': keypoints,
            'descriptors': descriptors,
            'image': image
        }

    def matchFeatures(self, descriptors):
        if descriptors is None or len(descriptors) < 2:
            return -1
        matches = self.BFMatcher.knnMatch(self.lastFrame.get('descriptors'), descriptors, k=2)
        # Apply ratio test
        goodMatches = []
        for m, n in matches:
            if m.distance < 0.75 * n.distance:
                goodMatches.append([m])
        return goodMatches

    def getLastFrame(self):
        return self.lastFrame

    def getLastFrameKeypoints(self):
        return self.lastFrame.get('keypoints')

    def getPairPointArray(self, matches, keypoints):
        points = []
        for match in matches:
            queryPoint = self.lastFrame.get('keypoints')[match[0].queryIdx].pt
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
        distance = np.sqrt((queryPoint[0] - trainPoint[0]) ** 2 + (queryPoint[1] - trainPoint[1]) ** 2)
        # distance = np.linalg.norm(point_np, ord=2, axis=1)
        return distance

    def filterOutliers(self, points):
        if len(points) < 1:
            return []
        distances = list(map((lambda element: element.get('distance')), points))
        percentiles = np.percentile(distances, [25, 50, 75])  # (Q1, median Q3)
        filtered = list(filter((lambda element: percentiles[0] <= element.get('distance') <= percentiles[2]), points))
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
        velocity = (-1 * velocity[0] / len(points), -1 * velocity[1] / len(points))
        return velocity
