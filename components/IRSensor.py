import RPi.GPIO as GPIO
from time import sleep

from .componentLogger import getDefaultConfigLogger

GPIO.setmode(GPIO.BOARD)


class IRSensor:
    sensorPin = None
    __instance = None
    subscribers = []
    logger = None

    @staticmethod
    def getInstance():
        if IRSensor.__instance is None:
            IRSensor()
        return IRSensor.__instance

    def __init__(self, sensorPin=16):
        self.logger = getDefaultConfigLogger(__file__)
        if IRSensor.__instance is not None:
            raise Exception(
                "Instance already created, use getInstance to get the instance")
        else:
            IRSensor.__instance = self

        self.sensorPin = sensorPin
        self.subscribers = []

        GPIO.setup(self.sensorPin, GPIO.IN)

    def startLooking(self, subscribers=[]):
        for sbs in subscribers:
            self.subscribers.append(sbs)
            
        while True:
            sleep(0.5)
            # Waiting for object detection
            while GPIO.input(self.sensorPin):
                sleep(0.5)
            # Notifying subscribers that object is detected
            self.logger.debug("Object detected, notifying the subscribers")
            self.objectDetected()

            # Waiting for the object to be moved
            while not GPIO.input(self.sensorPin):
                sleep(0.5)
            # Notifying subscribers that object is moved
            self.logger.debug("Object moved, notifying the subscribers")
            self.objectPassed()

    def objectDetected(self):
        for sbscriber in self.subscribers:
            sbscriber((True, False))

    def objectPassed(self):
        for sbscriber in self.subscribers:
            sbscriber((False, True))

    def subscribe(self, fx):
        self.subscribers.append(fx)
        return True

    def unsubscribe(self, fx):
        newSubscribers = []
        for subscriber in self.subscribers:
            if id(fx) != id(subscriber):
                newSubscribers.append(subscriber)
        self.subscribers = newSubscribers
        return True

    def __del__(self):
        self.logger.debug("Deleting the object")


if __name__ == "__main__":
    irSensor = IRSensor()
    # irSensor.subscribe(lambda x: print(
    #     "Object detected: ", x[0], " , Object moved: ", x[1]))
    def simplePrint(*args):
        print(args)
    irSensor.startLooking([simplePrint])
    del irSensor
