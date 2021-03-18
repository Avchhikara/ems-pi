from multiprocessing import Process, Queue
import requests
from time import sleep
import RPi.GPIO as GPIO

from ServoMotor import ServoMotor
from IRSensor import IRSensor
from USBCamera import USBCamera

GPIO.setmode(GPIO.BOARD)


servoMotor = ServoMotor()
irSensor = IRSensor()
usbCamera = USBCamera.getInstance()


class SimpleDetector:
    usbCamera = None
    irSensor = None
    servoMotor = None

    def __init__(self,
                 usbCamera=USBCamera.getInstance(),
                 irSensor=IRSensor.getInstance(),
                 servoMotor=ServoMotor.getInstance()
                 ):
        print("[SimpleDetector] - Inititalizing the Pi detector")
        self.usbCamera = usbCamera
        self.irSensor = irSensor
        self.servoMotor = servoMotor

    def onObjectDetection(self):
        print("[SimpleDetector] - Object is detected, taking photo")
        self.usbCamera.takePhoto()
        print("[SimpleDetector] - Dummy sending photo to centrifuge")
        print("[SimpleDetector] - Dummy yes so, lifting the flank")
        servoMotor.setAngle(90)
        sleep(5)
        servoMotor.setAngle(0)

    def run(self):
        irSensor.subscribe(self.onObjectDetection)
        p = Process(target=irSensor.startLooking, args=())
        p.start()
        p.join()


if __name__ == "__main__":
    sd = SimpleDetector()
    sd.run()
