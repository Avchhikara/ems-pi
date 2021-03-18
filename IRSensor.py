import RPi.GPIO as GPIO
import time


class IRSensor:
    sensorPin = None
    __instance = None
    subscribers = []

    @staticmethod
    def getInstance():
        if IRSensor.__instance is None:
            IRSensor()
        return IRSensor.__instance

    def __init__(self, sensorPin=16):
        if IRSensor.__instance is not None:
            raise Exception(
                "[IRSensor] - Instance already created, use getInstance to get the instance")
        else:
            IRSensor.__instance = self

        self.sensorPin = sensorPin
        self.subscribers = []
        # Setting up the pins

        GPIO.setup(self.sensorPin, GPIO.IN)

    def startLooking(self):
        i = 0
        freshFunctionCall = True
        while True:
            if not GPIO.input(self.sensorPin):
                print(
                    f"[IRSensor - {i}] - Object Detected, calling the function passed")
                if freshFunctionCall:
                    for subscriber in self.subscribers:
                        subscriber()
                    freshFunctionCall = False
                i += 1
                while not GPIO.input(self.sensorPin):
                    print(
                        "[IRSensor] - Going to sleep, will check after 2 seconds is the vehicle is gone or not")
                    time.sleep(2)
                    freshFunctionCall = True
                    if GPIO.input(self.sensorPin):
                        break

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
        print("[IRSensor] - Deleting the object")


if __name__ == "__main__":
    irSensor = IRSensor()
    irSensor.startLooking(lambda: print("hello from the function"))
    del irSensor
