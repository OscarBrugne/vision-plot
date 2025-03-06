import json
from typing import Any, Dict, List, Optional, Tuple

from bottle import Bottle, request, response
from pydantic import BaseModel, ValidationError, field_validator
from services import PathToSVGService


class SinglePathRequest(BaseModel):
    """Request schema for a single path request."""

    points: List[List[int]]
    size: List[int]
    viewbox: Optional[List[int]] = None
    is_closed_path: bool = False
    stroke: str = "black"
    stroke_width: int = 1

    @field_validator("*", mode="before")
    @classmethod
    def parse_json_field(cls, value: str) -> Any:
        try:
            return json.loads(value)
        except json.JSONDecodeError as e:
            raise ValueError(
                f"Invalid JSON value: '{value}' is not a valid JSON format."
            ) from e


class MultiplePathsRequest(BaseModel):
    """Request schema for a multiple paths request."""

    paths: List[List[List[int]]]
    size: List[int]
    viewbox: Optional[List[int]] = None
    is_closed_path: bool = False
    stroke: str = "black"
    stroke_width: int = 1

    @field_validator("*", mode="before")
    @classmethod
    def parse_json_field(cls, value: str) -> Any:
        try:
            return json.loads(value)
        except json.JSONDecodeError as e:
            raise ValueError(
                f"Invalid JSON value: '{value}' is not a valid JSON format."
            ) from e


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
        self._app.post("/generate-single-path", callback=self.generate_single_path)
        self._app.post(
            "/generate-multiple-paths", callback=self.generate_multiple_paths
        )

    def _generate_validation_error_message(self, e: ValidationError) -> str:
        errors = e.errors()
        error_msgs = []
        for error in errors:
            key = error["loc"][0]
            value = error["input"]
            msg = error["msg"]
            error_msgs.append(f"The parameter '{key}:{value}' is invalid: {msg}")
        error_message = "\n ".join(error_msgs)

        return error_message

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
                "message": self._generate_validation_error_message(e),
            }

        svg_string: str = self._svg_service.generate_line_path_svg(
            data.points,
            data.size,
            data.viewbox,
            data.is_closed_path,
            data.stroke,
            data.stroke_width,
        )

        response.content_type = "application/json"
        return {"svg": svg_string}

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
        if request.content_type != "application/x-www-form-urlencoded":
            response.status = 400
            return {
                "error": "Invalid Content-Type",
                "message": "Expected application/x-www-form-urlencoded",
            }

        try:
            data = MultiplePathsRequest.model_validate(request.forms)
            print(data.model_dump())
        except Exception as e:
            response.status = 400
            return {
                "error": "Invalid request data",
                "message": self._generate_validation_error_message(e),
            }

        svg_string: str = self._svg_service.generate_multiple_line_paths_svg(
            data.paths,
            data.size,
            data.viewbox,
            data.is_closed_path,
            data.stroke,
            data.stroke_width,
        )

        response.content_type = "application/json"
        return {"svg": svg_string}
