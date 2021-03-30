from .componentLogger import getDefaultConfigLogger
import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BOARD)
GPIO.setup(3, GPIO.OUT)


# Making it singleton so to have only one access to the resource.


class ServoMotor:
    pwm = GPIO.PWM(3, 50)
    __instance = None
    logger = None

    @staticmethod
    def getInstance():
        if ServoMotor.__instance is None:
            ServoMotor()
        return ServoMotor.__instance

    def __init__(self):
        self.logger = getDefaultConfigLogger(__file__)
        if ServoMotor.__instance is not None:
            raise Exception(
                "Instance already created, use getInstance to get the instance")
        else:
            ServoMotor.__instance = self

    def setAngle(self, angleToSet=90):
        self.logger.debug("Setting up the servo motor")

        self.pwm.start(0)
        self.logger.debug(
            "Starting rotation of servo motor to angle: " + str(angleToSet))
        duty = angleToSet / 18 + 2
        GPIO.output(3, True)
        self.pwm.ChangeDutyCycle(duty)
        self.logger.debug("Rotation complete")
        sleep(1)
        GPIO.output(3, False)
        self.pwm.ChangeDutyCycle(0)
        # self.pwm.stop()

    def __del__(self):
        self.pwm.stop()
        self.logger.debug("deleting the object")


if __name__ == "__main__":
    servoMotor = ServoMotor()
    servoMotor.setAngle(0)
    servoMotor.setAngle(90)
    servoMotor.setAngle(0)
    servoMotor.setAngle(90)
    del servoMotor
