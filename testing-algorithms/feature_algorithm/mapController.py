import numpy as np


class MapController:
    def __init__(self):
        self._cameraPosition = (0, 0)
        self._cameraMovement = [(0,0)]
        self._points = [(0, 0)]

    def getPoints(self):
        return self._points

    def addPoints(self, points):
        self._points.append(np.add(points, self._cameraPosition))

    def moveCamera(self, movementVector):
        self._cameraPosition = np.add(self._cameraPosition, movementVector)
        self._cameraMovement.append(self._cameraPosition)

    def getCameraMovement(self):
        return self._cameraMovement