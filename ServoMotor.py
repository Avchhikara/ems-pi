import RPi.GPIO as GPIO
from time import sleep


class ServoMotor:
    pwm = None

    def __init__(self):
        pass

    def setAngle(self, angleToSet=90):
        print("[ServoMotor] - Setting up the servo motor")
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(3, GPIO.OUT)
        self.pwm = GPIO.PWM(3, 50)
        self.pwm.start(0)
        print("[ServoMotor] - Starting rotation of servo motor to angle:", angleToSet)
        duty = angleToSet / 18 + 2
        GPIO.output(3, True)
        self.pwm.ChangeDutyCycle(duty)
        print("[ServoMotor] - Rotation complete")
        sleep(1)
        GPIO.output(3, False)
        self.pwm.ChangeDutyCycle(0)
        self.pwm.stop()
        GPIO.cleanup()

    def __del__(self):
        print("[ServoMotor] - cleaning the GPIO board")


if __name__ == "__main__":
    servoMotor = ServoMotor()
    servoMotor.setAngle(0)
    # servoMotor.setAngle(90)
    # servoMotor.setAngle(0)
    # servoMotor.setAngle(90)
    del servoMotor
