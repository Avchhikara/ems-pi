import cv2 as cv
from os import mkdir, listdir
from time import sleep
from multiprocessing import Process

# Making this class a singleton since there is only one resource and it should be accessed once.

# from .componentLogger import getDefaultConfigLogger


class USBCameraAsync:
    camera = None
    pathToSaveImage = "./static/img/"
    __instance = None
    # logger = None
    latestFrame = None
    cameraIndex = 0

    def __init__(self, cameraIndex=0):
        self.cameraIndex = cameraIndex

    def takePhoto(self, imageName):
        self.camera = cv.VideoCapture(self.cameraIndex)
        ret, frame = self.camera.read()
        res = cv.imwrite(
            self.pathToSaveImage + imageName, frame
        )
        print(f"Photo saved: {res}")
        self.camera.release()

    def __del__(self):
        pass


if __name__ == "__main__":
    pass
