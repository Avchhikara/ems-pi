from flask import Flask, render_template, Response
import concurrent.futures

from USBCamera import USBCamera

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/video_feed")
def video_feed():
    usbCamera = USBCamera.getInstance()
    result = ""
    with concurrent.futures.ThreadPoolExecutor() as executer:
        future = executer.submit(usbCamera.getVideoFeed)
        result = future.result()
    return Response(result, mimetype="multipart/x-mixed-replace; boundary=frame")


@app.route("/take-photo")
def take_photo():
    usbCam = USBCamera.getInstance()
    return {"photoLocation": usbCam.takePhoto()[1]}


if __name__ == "__main__":
    app.run(debug=True, port=9000, threaded=True)
    # also starting the simpleDetector as a seperate subprocess which will detect the vehicles
