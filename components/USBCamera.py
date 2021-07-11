import cv2 as cv
from os import mkdir, listdir
from time import sleep

# Making this class a singleton since there is only one resource and it should be accessed once.

from .componentLogger import getDefaultConfigLogger


class USBCamera:
    camera = None
    pathToSaveImage = "./static/img/"
    __instance = None
    logger = None
    cameraIndex = 0

    @staticmethod
    def getInstance():
        """Static method access"""
        if USBCamera.__instance is None:
            USBCamera()
        return USBCamera.__instance

    def __init__(self, cameraIndex=0):
        self.logger = getDefaultConfigLogger(__file__)
        if USBCamera.__instance is not None:
            raise Exception(
                "This class is already initialized - use getInstance method to get the instance")
        else:
            USBCamera.__instance = self

        self.cameraIndex = cameraIndex

    def _initializeCamera(self):
        self.camera = cv.VideoCapture(self.cameraIndex)
        while not self.camera.isOpened():
            self.logger.debug(
                "Faced error in camera initializing so, trying again after 1 sec")
            sleep(1)
            self.camera = cv.VideoCapture(self.cameraIndex)
        if self.camera.isOpened():
            self.logger.debug("Camera Initialized")
        else:
            self.logger.debug("Camera is still not open!")

    def _releaseCamera(self):
        self.logger.debug("Releasing camera resource")
        self.camera.release()

    def makeImageDir(self):
        self.logger.debug("Create img directory if not exist")
        if "img" not in listdir("./../static"):
            mkdir(self.pathToSaveImage)

    def takePhoto(self, imageName="vehicleImage.png"):
        self.logger.debug("Reading the camera input and capturing a frame")
        try:
            self._initializeCamera()
            ret, photoFrame = self.camera.read()
            msg = "Saving the frame as'" + imageName + "' in '" + self.pathToSaveImage + "' folder"
            self.logger.debug(msg)
            imageSavedSuccessfully = False
            if imageName.split(".")[-1] == "png":
                imageSavedSuccessfully = cv.imwrite(
                    self.pathToSaveImage + imageName, photoFrame)
            else:
                imageSavedSuccessfully = cv.imwrite(self.pathToSaveImage +
                                                    imageName + ".png", photoFrame)
            if imageSavedSuccessfully:
                self.logger.debug("Photo is taken and is saved!")
            else:
                self.logger.error("Unable to save image")
            self._releaseCamera()
            return True, self.pathToSaveImage + imageName
        except Exception as err:
            self.logger.error("Error: ", err)
            return False, ""

    def getVideoFeed(self):
        while True:
            success, frame = self.camera.read()
            if not success:
                break
            else:
                ret, buffer = cv.imencode(".jpg", frame)
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n'
                       )

    def __del__(self):
        pass


if __name__ == "__main__":
    usbCamera = USBCamera(0)
    usbCamera.takePhoto(imageName="1st.png")
    usbCamera.takePhoto(imageName="2nd.jpg")
    del usbCamera
