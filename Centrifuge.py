"""
This will act as middleware for communication (request, response) with the centrifuge system
"""
import requests
from os import path

from components.componentLogger import getDefaultConfigLogger


class Centrifuge:
    imageDir = ""
    CENTRIFUGE_URL = "https://ems-centrifuge.herokuapp.com/upload"

    def __init__(self, imageDir="./static/img/") -> None:
        self.imageDir = imageDir
        self.logger = getDefaultConfigLogger(__file__)

    def upload(self, imageName) -> bool:
        image_path = path.join(self.imageDir, imageName)
        with open(image_path, "rb") as file:
            self.logger.debug(f"Reading the image: {image_path}")
            req = requests.post(self.CENTRIFUGE_URL, files={
                                "vehicleImage": file.read()})
            response = req.json()
            authorised = response["authorised"]
            message = "vehicle is not authorised to enter!"
            if authorised:
                message = "vehicle is authorised to enter!"

            self.logger.debug(message)

            return authorised


if __name__ == "__main__":
    cf = Centrifuge()
    cf.upload("vehicleImage-0.png")
