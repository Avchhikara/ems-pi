from components.ServoMotor import ServoMotor
from components.IRSensor import IRSensor
from flask import Flask, render_template, Response
from multiprocessing import Process

from components.USBCamera import USBCamera
# from SimpleDetector import SimpleDetector

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/video_feed")
def video_feed():
    usbCamera = USBCamera.getInstance()
    return Response(usbCamera.getVideoFeed(), mimetype="multipart/x-mixed-replace; boundary=frame")


@app.route("/take-photo")
def take_photo():
    usbCam = USBCamera.getInstance()
    return {"photoLocation": usbCam.takePhoto()[1]}


if __name__ == "__main__":
    # also starting the simpleDetector as a seperate subprocess which will detect the vehicles
    # simpleDetector = SimpleDetector(usbCamera=USBCamera.getInstance(
    # ), irSensor=IRSensor.getInstance(), servoMotor=ServoMotor.getInstance())

    # p1 = Process(target=simpleDetector.run)
    # p2 = Process(target=app.run, kwargs={
    #              "debug": True, "port": 9000, "threaded": True})
    # # p1.start()
    # p2.start()
    # # p1.join()
    # p2.join()
    app.run(debug=True, port=9000, threaded=True)
    # print("After app")
