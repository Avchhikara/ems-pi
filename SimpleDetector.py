from multiprocessing import Process, Queue
import requests
from time import sleep
import RPi.GPIO as GPIO
# import logging

from utils.loggerConfig import getDefaultConfigLogger
from components.ServoMotor import ServoMotor
from components.IRSensor import IRSensor
from components.USBCamera import USBCamera
# from components.USBCameraAsync import USBCameraAsync

GPIO.setmode(GPIO.BOARD)


# servoMotor = ServoMotor()
# irSensor = IRSensor()
# usbCamera = USBCamera.getInstance()
# usbCamera = USBCameraAsync(0)


class SimpleDetector:
    usbCamera = None
    irSensor = None
    servoMotor = None
    logger = None
    counter = 0

    def __init__(self,
                 usbCamera=USBCamera.getInstance(),
                 #  usbCamera=USBCameraAsync(),
                 irSensor=IRSensor.getInstance(),
                 servoMotor=ServoMotor.getInstance()
                 ):
        self.logger = getDefaultConfigLogger(__file__)
        self.logger.debug("Inititalizing the Pi detector")
        self.usbCamera = usbCamera
        self.irSensor = irSensor
        self.servoMotor = servoMotor

    def onObjectDetection(self, args):
        objectDetected, objectMoved = args
        if objectDetected:
            image_name = "vehicleImage-" + str(self.counter) + ".png"
            self.logger.debug("Object is detected, taking photo")
            self.usbCamera.takePhoto(image_name)
            self.logger.debug("Sending photo to Centrifuge")
            self.logger.debug("Processing the input from centrifuge")
            self.servoMotor.setAngle(90)
            self.counter += 1
        elif objectMoved:
            self.logger.debug(
                "Object seems to have moved so, flank will come down after 2 seconds")
            sleep(2)
            self.servoMotor.setAngle(0)

    def run(self):
        self.irSensor.subscribe(self.onObjectDetection)
        p = Process(target=self.irSensor.startLooking, args=())
        p.start()
        p.join()


if __name__ == "__main__":
    sd = SimpleDetector()
    sd.run()
