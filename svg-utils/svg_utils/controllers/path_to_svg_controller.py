from typing import Any, Dict, List, Optional, Tuple

from bottle import Bottle, request, response
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
        """
        Register routes for the controller.
        """
        self._app.post("/generate-single-path", callback=self.generate_single_path)
        self._app.post(
            "/generate-multiple-paths", callback=self.generate_multiple_paths
        )

    def generate_single_path(self) -> Dict[str, str]:
        """
        Handle a POST request to generate an SVG with a single path defined by a set of points.

        Expects a JSON payload with the following structure:
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
        data: Dict[str, Any] = request.json

        if "points" not in data:
            response.status = 400
            return {"error": "Missing required field: 'points'."}
        if "size" not in data:
            response.status = 400
            return {"error": "Missing required field: 'size'."}

        points: List[Tuple[int, int]] = data["points"]
        size: Tuple[int, int] = tuple(data["size"])

        viewbox: Optional[Tuple[int, int, int, int]] = data.get("viewbox", None)
        is_closed_path: bool = data.get("is_closed_path", False)
        stroke: str = data.get("stroke", "black")
        stroke_width: int = data.get("stroke_width", 1)

        svg_string: str = self._svg_service.generate_line_path_svg(
            points, size, viewbox, is_closed_path, stroke, stroke_width
        )

        response.content_type = "application/json"
        return {"svg": svg_string}

    def generate_multiple_paths(self) -> Dict[str, str]:
        """
        Handle a POST request to generate an SVG with multiple paths defined by sets of points.

        Expects a JSON payload with the following structure:
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
        data: Dict[str, Any] = request.json

        if "paths" not in data:
            response.status = 400
            return {"error": "Missing required field: 'paths'."}
        if "size" not in data:
            response.status = 400
            return {"error": "Missing required field: 'size'."}

        paths: List[List[Tuple[int, int]]] = data["paths"]
        size: Tuple[int, int] = tuple(data["size"])

        viewbox: Optional[Tuple[int, int, int, int]] = data.get("viewbox", None)
        is_closed_path: bool = data.get("is_closed_path", False)
        stroke: str = data.get("stroke", "black")
        stroke_width: int = data.get("stroke_width", 1)

        svg_string: str = self._svg_service.generate_multiple_line_paths_svg(
            paths, size, viewbox, is_closed_path, stroke, stroke_width
        )

        response.content_type = "application/json"
        return {"svg": svg_string}
