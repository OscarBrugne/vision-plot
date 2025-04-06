import os

from bottle import Bottle, run
from controllers import (
    camera_controller,
    data_controller,
    projector_calibration_controller,
)

app: Bottle = Bottle()

app.mount("/camera", camera_controller.app)
app.mount("/projector-calibration", projector_calibration_controller.app)
app.mount("/", data_controller.app)

if __name__ == "__main__":
    host = os.getenv("HOST")
    port = os.getenv("PORT")
    if not host or not port:
        raise ValueError("Environment variables HOST and PORT must be set.")

    run(app, host=host, port=port)
