import RPi.GPIO as GPIO
import time


class IRSensor:
    sensorPin = None

    def __init__(self, sensorPin=16):
        self.sensorPin = sensorPin

    def startLooking(self, functionToCall):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.sensorPin, GPIO.IN)
        try:
            i = 0
            freshFunctionCall = True
            while True:
                if not GPIO.input(self.sensorPin):
                    print(
                        f"[IRSensor - {i}] - Object Detected, calling the function passed")
                    if freshFunctionCall:
                        functionToCall()
                        freshFunctionCall = False
                    i += 1
                    while not GPIO.input(self.sensorPin):
                        print(
                            "[IRSensor] - Going to sleep, will check after 2 seconds is the vehicle is gone or not")
                        time.sleep(2)
                        freshFunctionCall = True
                        if GPIO.input(self.sensorPin): break

        except Exception as err:
            GPIO.cleanup()
            print("[IRSensor] - Error: ", err)

    def __del__(self):
        print("[IRSensor] - Cleaning the GPIO board")
        GPIO.cleanup()


if __name__ == "__main__":
    irSensor = IRSensor()
    irSensor.startLooking(lambda: print("hello from the function"))
    del irSensor
