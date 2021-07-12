import RPi.GPIO as GPIO
from time import sleep
from components.componentLogger import getDefaultConfigLogger


class LED:
    def __init__(self, outputPin=12) -> None:
        # Setting up the pins
        self.outputPin = outputPin
        self.logger = getDefaultConfigLogger(__file__)
        GPIO.setup(outputPin, GPIO.OUT)

    def turnOn(self, turnOffAutomatically=True, turnOffAfterInSeconds=2):
        self.logger.debug(f"Turning ON the LED")
        GPIO.output(self.outputPin, True)
        if turnOffAutomatically:
            sleep(turnOffAfterInSeconds)
            self.turnOff()

    def turnOff(self):
        self.logger.debug("Turning OFF the LED")
        GPIO.output(self.outputPin, False)


if __name__ == "__main__":
    led = LED()
    led.turnOn()
    GPIO.cleanup()
