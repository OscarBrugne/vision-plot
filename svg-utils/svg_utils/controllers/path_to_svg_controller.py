from typing import Dict

from bottle import Bottle, request, response
from models import (
    MultiplePathsRequest,
    SinglePathRequest,
    generate_validation_error_message,
)
from pydantic import ValidationError
from services import PathToSVGService


class PathToSVGController:
    """Controller class to handle requests for generating SVGs from paths."""

    def __init__(self):
        """Initialize a new PathToSVGController object."""
        self._app: Bottle = Bottle()
        self._svg_service: PathToSVGService = PathToSVGService()

        self._register_routes()

    @property
    def app(self) -> Bottle:
        """
        Returns the Bottle app for this controller.

        Returns:
            Bottle: The Bottle app.
        """
        return self._app

    def _register_routes(self) -> None:
        """Register routes for the controller."""
        # /generate-single-path endpoint
        self._app.route(
            "/generate-single-path",
            method="OPTIONS",
            callback=self._options_generate_single_path,
        )
        self._app.post("/generate-single-path", callback=self.generate_single_path)

        # /generate-multiple-paths endpoint
        self._app.route(
            "/generate-multiple-paths",
            method="OPTIONS",
            callback=self._options_generate_multiple_paths,
        )
        self._app.post(
            "/generate-multiple-paths", callback=self.generate_multiple_paths
        )

    def _options_generate_single_path(self) -> None:
        """Handle an OPTIONS request for the /generate-single-path endpoint."""
        response.status = 204
        response.headers["Access-Control-Allow-Methods"] = "OPTIONS, POST"

    def generate_single_path(self) -> Dict[str, str]:
        """
        Handle a POST request to generate an SVG with a single path defined by a set of points.

        Expects a form-urlencoded payload with the following fields:
            {
                "points": [[x1, y1], [x2, y2], ...],
                "size": [width, height],
                "viewbox": [x, y, width, height] (optional),
                "is_closed_path": bool (optional),
                "stroke": "color" (optional, default "black"),
                "stroke_width": int (optional, default 1)
            }

        Returns:
            Dict[str, str]: A JSON response with the SVG string mapped to the key "svg".
        """
        response.headers["Accept"] = "application/x-www-form-urlencoded"
        response.content_type = "application/json"

        if request.content_type != "application/x-www-form-urlencoded":
            response.status = 400
            return {
                "error": "Invalid Content-Type",
                "message": "Expected application/x-www-form-urlencoded",
            }

        try:
            data = SinglePathRequest.model_validate(request.forms)
        except ValidationError as e:
            response.status = 400
            return {
                "error": "Invalid request data",
                "message": generate_validation_error_message(e),
            }

        try:
            svg_string: str = self._svg_service.generate_line_path_svg(
                data.points,
                data.size,
                data.viewbox,
                data.is_closed_path,
                data.stroke,
                data.stroke_width,
            )
        except Exception as e:
            response.status = 500
            return {
                "error": "Internal Server Error",
                "message": f"An error occurred while generating the SVG: {str(e)}",
            }

        return {"svg": svg_string}

    def _options_generate_multiple_paths(self) -> None:
        """Handle an OPTIONS request for the /generate-multiple-paths endpoint."""
        response.status = 204
        response.headers["Access-Control-Allow-Methods"] = "OPTIONS, POST"

    def generate_multiple_paths(self) -> Dict[str, str]:
        """
        Handle a POST request to generate an SVG with multiple paths defined by sets of points.

        Expects a form-urlencoded payload with the following fields:
            {
                "paths": [[[x1, y1], [x2, y2], ...], [[x1, y1], [x2, y2], ...], ...],
                "size": [width, height],
                "viewbox": [x, y, width, height] (optional),
                "is_closed_path": bool (optional),
                "stroke": "color" (optional, default "black"),
                "stroke_width": int (optional, default 1)
            }

        Returns:
            Dict[str, str]: A JSON response with the SVG string mapped to the key "svg".
        """
        response.headers["Accept"] = "application/x-www-form-urlencoded"
        response.content_type = "application/json"

        if request.content_type != "application/x-www-form-urlencoded":
            response.status = 400
            return {
                "error": "Invalid Content-Type",
                "message": "Expected application/x-www-form-urlencoded",
            }

        try:
            data = MultiplePathsRequest.model_validate(request.forms)
        except ValidationError as e:
            response.status = 400
            return {
                "error": "Invalid request data",
                "message": generate_validation_error_message(e),
            }

        try:
            svg_string: str = self._svg_service.generate_multiple_line_paths_svg(
                data.paths,
                data.size,
                data.viewbox,
                data.is_closed_path,
                data.stroke,
                data.stroke_width,
            )
        except Exception as e:
            response.status = 500
            return {
                "error": "Internal Server Error",
                "message": f"An error occurred while generating the SVG: {str(e)}",
            }

        return {"svg": svg_string}
