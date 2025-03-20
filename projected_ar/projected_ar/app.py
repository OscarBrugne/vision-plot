import os

from bottle import Bottle, run
from controllers import data_controller

app: Bottle = Bottle()

app.mount("/", data_controller.app)

if __name__ == "__main__":
    host = os.getenv("HOST")
    port = os.getenv("PORT")
    if not host or not port:
        raise ValueError("Environment variables HOST and PORT must be set.")

    run(app, host=host, port=port)

    # $env:HOST="localhost"; $env:PORT="8080"; python .\projected_ar\app.py
