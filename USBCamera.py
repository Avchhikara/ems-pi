import cv2 as cv
from os import mkdir, listdir
from time import sleep

# Making this class a singleton since there is only one resource and it should be accessed once.


class USBCamera:
    camera = None
    pathToSaveImage = "./static/img/"
    __instance = None

    @staticmethod
    def getInstance():
        """Static method access"""
        if USBCamera.__instance is None:
            USBCamera()
        return USBCamera.__instance

    def __init__(self, cameraIndex=0):
        if USBCamera.__instance is not None:
            raise Exception(
                "This class is already initialized - use getInstance method to get the instance")
        else:
            USBCamera.__instance = self

        self.makeImageDir()
        self.camera = cv.VideoCapture(cameraIndex)
        while not self.camera.isOpened():
            print(
                "[USBCamera] - Faced error in camera initializing so, trying again after 1 sec")
            sleep(1)
            self.camera = cv.VideoCapture(cameraIndex)
        if self.camera.isOpened():
            print("[USBCamera] - Camera Initialized")
        else:
            print("[USBCamera] - Camera is still not open!")

    def makeImageDir(self):
        print("[USBCamera] - Create img directory if not exist")
        if "img" not in listdir("./"):
            mkdir(self.pathToSaveImage)

    def takePhoto(self, imageName="vehicleImage.png"):
        print("[USBCamera] - Reading the camera input and capturing a frame")
        try:
            ret, photoFrame = self.camera.read()
            print(
                f"[USBCamera] - Saving the frame as '{imageName}' in '{self.pathToSaveImage}' folder")
            if imageName.split(".")[-1] == "png":
                cv.imwrite(self.pathToSaveImage + imageName, photoFrame)
            else:
                cv.imwrite(self.pathToSaveImage +
                           imageName + ".png", photoFrame)
            print("[USBCamera] - Photo is taken and is saved!")
            return True, self.pathToSaveImage + imageName
        except Exception as err:
            print("[USBCamera] - Error: ", err)
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
        print("[USBCamera] - Releasing camera resource")
        self.camera.release()


if __name__ == "__main__":
    usbCamera = USBCamera(0)
    usbCamera.takePhoto(imageName="1st.png")
    usbCamera.takePhoto(imageName="2nd.jpg")
    del usbCamera
