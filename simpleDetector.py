from multiprocessing import Process, Queue
import requests
from time import sleep
import RPi.GPIO as GPIO

from ServoMotor import ServoMotor
from IRSensor import IRSensor
from USBCamera import USBCamera

GPIO.setmode(GPIO.BOARD)

print("[SimpleDetector] - Inititalizing the Pi detector")
servoMotor = ServoMotor()
irSensor = IRSensor()
usbCamera = USBCamera.getInstance()


def savePhotoOnDetection(angle=0):
    print(angle)
    sleep(5)
    photoPath = usbCamera.takePhoto(f"{angle}.png")
    # here, make the request to centrifuge and then do the needful
    print("photo taken so, now moving motor")
    servoMotor.setAngle(angle)
    # raise Exception("complete")


def throwException():
    raise Exception("complete")


try:
    irSensor.subscribe(lambda: savePhotoOnDetection(90))
    irSensor.subscribe(lambda: savePhotoOnDetection(0))
    print(irSensor.subscribers)
    irSensor.subscribe(lambda: throwException())
    p = Process(target=irSensor.startLooking, args=())
    p.start()
    p.join()
except Exception as e:
    del servoMotor
    del usbCamera
    del irSensor
    GPIO.cleanup()
