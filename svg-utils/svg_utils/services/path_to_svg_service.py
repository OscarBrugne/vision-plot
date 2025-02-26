from typing import List, Optional, Tuple

from utils import PathBuilder, SVGBuilder


class PathToSVGService:
    """Service class to generate SVG strings from paths defined by points."""

    def __init__(self) -> None:
        """Initialize a new SVGService object."""
        self._path_builder: PathBuilder = PathBuilder()
        self._svg_builder: SVGBuilder = SVGBuilder()

    def generate_line_path_svg(
        self,
        points: List[Tuple[int, int]],
        size: Tuple[int, int],
        viewbox: Optional[Tuple[int, int, int, int]] = None,
        is_closed_path: bool = False,
        stroke: str = "black",
        stroke_width: int = 1,
    ) -> str:
        """
        Generate SVG string with a single path defined by the given points using line segments to connect them.

        Args:
            points (List[Tuple[int, int]]): List of points to define the path.
            size (Tuple[int, int]): Size of the SVG image (width, height).
            viewbox (Optional[Tuple[int, int, int, int]]): Defines the viewbox for the SVG in the form of a tuple (x, y, width, height). Defaults to None.
            is_closed_path (bool): Whether the path should be closed. Defaults to False.
            stroke (str): Stroke color. Defaults to "black".
            stroke_width (int): Stroke width. Defaults to 1.

        Returns:
            str: SVG as a string
        """
        self._initialize_svg(size, viewbox)
        self._add_path_to_svg(points, is_closed_path, stroke, stroke_width)
        return self._svg_builder.get_svg_string()

    def generate_multiple_line_paths_svg(
        self,
        paths: List[List[Tuple[int, int]]],
        size: Tuple[int, int],
        viewbox: Optional[Tuple[int, int, int, int]] = None,
        is_closed_path: bool = False,
        stroke: str = "black",
        stroke_width: int = 1,
    ) -> str:
        """
        Generate SVG string with multiple paths defined by the given list of paths using line segments to connect the points.

        Args:
            paths (List[List[Tuple[int, int]]): List of paths, where each path is a list of points.
            size (Tuple[int, int]): Size of the SVG image (width, height).
            viewbox (Optional[Tuple[int, int, int, int]]): Defines the viewbox for the SVG in the form of a tuple (x, y, width, height). Defaults to None.
            is_closed_path (bool): Whether the paths should be closed. Defaults to False.
            stroke (str): Stroke color. Defaults to "black".
            stroke_width (int): Stroke width. Defaults to 1.

        Returns:
            str: SVG as a string
        """
        self._initialize_svg(size, viewbox)
        for path in paths:
            self._add_path_to_svg(path, is_closed_path, stroke, stroke_width)
        return self._svg_builder.get_svg_string()

    def _initialize_svg(
        self,
        size: Tuple[int, int],
        viewbox: Optional[Tuple[int, int, int, int]] = None,
    ) -> None:
        """
        Initialize the SVG with the given size and viewbox.

        Args:
            size (Tuple[int, int]): Size of the SVG image (width, height).
            viewbox (Optional[Tuple[int, int, int, int]]): Defines the viewbox for the SVG in the form of a tuple (x, y, width, height). Defaults to None.
        """
        self._svg_builder.clear()
        self._svg_builder.set_size(size)
        if viewbox:
            self._svg_builder.set_viewbox(viewbox)

    def _add_path_to_svg(
        self,
        points: List[Tuple[int, int]],
        is_closed_path: bool,
        stroke: str,
        stroke_width: int,
    ) -> None:
        """
        Add a path to the active SVG.

        Args:
            points (List[Tuple[int, int]]): List of points to define the path.
            is_closed_path (bool): Whether the path should be closed.
            stroke (str): Stroke color.
            stroke_width (int): Stroke width.
        """
        self._path_builder.clear()

        self._path_builder.move_to(points[0])
        for point in points[1:]:
            self._path_builder.line_to(point)
        if is_closed_path:
            self._path_builder.close_path()

        path_data = self._path_builder.get_data()

        self._svg_builder.add_path(
            path_data, fill="none", stroke=stroke, stroke_width=stroke_width
        )
