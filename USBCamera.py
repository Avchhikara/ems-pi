import cv2 as cv
from os import mkdir, listdir


class USBCamera:
    camera = None
    pathToSaveImage = "./img/"

    def __init__(self, cameraIndex=0):
        self.makeImageDir()
        self.camera = cv.VideoCapture(cameraIndex)
        print("[USBCamera] - Camera Initialized")

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
            return True
        except Exception as err:
            print("[USBCamera] - Error: ", err)
            return False

    def __del__(self):
        print("[USBCamera] - Releaseing camera resource")
        self.camera.release()


if __name__ == "__main__":
    usbCamera = USBCamera(0)
    usbCamera.takePhoto(imageName="1st.png")
    usbCamera.takePhoto(imageName="2nd.jpg")
    del usbCamera
