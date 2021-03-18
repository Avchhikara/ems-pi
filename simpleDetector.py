from multiprocessing import Process, Queue
import requests

from ServoMotor import ServoMotor
from IRSensor import IRSensor
from USBCamera import USBCamera

print("[SimpleDetector] - Inititalizing the Pi detector")
servoMotor = ServoMotor()
irSensor = IRSensor()
usbCamera = USBCamera.getInstance()


def savePhotoOnDetection():
    photoPath = usbCamera.takePhoto()
    # here, make the request to centrifuge and then do the needful
    print("photo taken so, now moving motor")
    servoMotor.setAngle(0)
    raise Exception("complete")


try:
    p = Process(target=irSensor.startLooking, args=(savePhotoOnDetection,))
    p.start()
    p.join()
except Exception as e:
    del servoMotor
    del usbCamera
    del irSensor
