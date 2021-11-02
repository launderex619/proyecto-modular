import cv2

class VideoModel:
    def __init__(self, videoPath):
        self.videoPath = videoPath
        self.videoCapture = cv2.VideoCapture(self.videoPath)
        self.numberFrames = self.videoCapture.get(cv2.CAP_PROP_FRAME_COUNT)
        self.width, self.height = self.getResolution()
        self.frameRate = self.videoCapture.get(cv2.CAP_PROP_FPS)

    def getResolution(self):
        return self.videoCapture.get(cv2.CAP_PROP_FRAME_WIDTH), self.videoCapture.get(cv2.CAP_PROP_FRAME_HEIGHT)

    def getNextFrame(self):
        return self.videoCapture.read()

    def closeVideo(self):
        self.videoCapture.release()

    def getNumberFrames(self):
        return int(self.numberFrames)

    def getFrameRate(self):
        return self.frameRate