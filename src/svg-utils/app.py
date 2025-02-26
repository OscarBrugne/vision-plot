from bottle import Bottle, run
from controllers.path_to_svg_controller import path_to_svg_controller

app: Bottle = Bottle()

app.mount("/svg", path_to_svg_controller)

if __name__ == "__main__":
    run(app, host="localhost", port=8080)
