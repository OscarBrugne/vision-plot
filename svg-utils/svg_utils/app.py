import os

from bottle import Bottle, run
from controllers import PathToSVGController

app: Bottle = Bottle()

path_to_svg_controller = PathToSVGController()
app.mount("/svg", path_to_svg_controller.app)

if __name__ == "__main__":
    host = os.getenv("HOST")
    port = os.getenv("PORT")
    if not host or not port:
        raise ValueError("Environment variables HOST and PORT must be set.")

    run(app, host=host, port=port)
