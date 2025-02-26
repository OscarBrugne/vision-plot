from bottle import Bottle, run
from controllers import PathToSVGController

app: Bottle = Bottle()

path_to_svg_controller = PathToSVGController()
app.mount("/svg", path_to_svg_controller.app)

if __name__ == "__main__":
    run(app, host="localhost", port=8080)
