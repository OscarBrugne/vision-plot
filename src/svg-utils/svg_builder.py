from typing import Dict, Literal, Tuple, Optional, List, Union
import svgwrite


class SVGBuilder:
    """Class to generate SVG files with various geometric shapes and SVG elements."""

    def __init__(
        self,
        filename: str = "output.svg",
        size: Tuple[Union[float, str], Union[float, str]] = ("100%", "100%"),
        viewbox: Optional[Tuple[int, int, int, int]] = None,
        profile: Literal["tiny", "basic", "full"] = "tiny",
    ) -> None:
        """
        Initializes a new SVGBuilder object.

        Args:
            filename (str) : Name of the output SVG file Defaults to "output.svg".
            size (Tuple[Union[float, str], Union[float, str]]) : Size of the SVG image (width, height). Defaults to ("100%", "100%").
            viewbox (Optional[Tuple[int, int, int, int]]) : Defines the viewbox for the SVG in the form of a tuple (x, y, width, height). Defaults to None.
            profile (Literal["tiny", "full"]) : The SVG profile to use ("tiny", "basic", or "full"). Defaults to "tiny".
        """
        self._drawing: svgwrite.Drawing = svgwrite.Drawing(
            filename, size=size, profile=profile
        )
        if viewbox is not None:
            self._drawing.viewbox(*viewbox)

    def set_filename(self, filename: str) -> None:
        """
        Sets the filename for the SVG to be saved.

        Args:
            filename (str) : New filename for the SVG file.
        """
        self._drawing.filename = filename

    def set_size(self, size: Tuple[float, float]) -> None:
        """
        Modifies the size of the SVG.

        Args:
            size (Tuple[float, float]) : New size of the image (width, height).
        """
        self._drawing["width"] = size[0]
        self._drawing["height"] = size[1]

    def set_viewbox(self, viewbox: Tuple[int, int, int, int]) -> None:
        """
        Sets the viewbox for the SVG.

        Args:
            viewbox (Tuple[int, int, int, int]) : New viewbox (x, y, width, height) for the SVG.
        """
        self._drawing.viewbox(*viewbox)

    def add_circle(
        self,
        center: Tuple[float, float],
        radius: float,
        **presentation_attributes: Dict[str, Union[str, float]],
    ) -> None:
        """
        Adds a circle to the SVG

        Args:
            center (Tuple[float, float]) : Position of the center of the circle (x, y).
            radius (float) : Radius of the circle.
            **presentation_attributes (Dict[str, str]) : Additional SVG attributes such as:
                - 'fill': Fill color of the circle (default is 'none').
                - 'stroke': Stroke color of the circle (default is 'black').
                - 'stroke_width': Width of the stroke (default is 1).
                - ...

        For a full list of possible attributes, see the SVGwrite documentation:
        https://svgwrite.readthedocs.io/en/latest/attributes/presentation.html
        """
        circle = self._drawing.circle(
            center=center, r=radius, **presentation_attributes
        )
        self._drawing.add(circle)

    def add_ellipse(
        self,
        center: Tuple[float, float],
        radii: Tuple[float, float],
        **presentation_attributes: Dict[str, Union[str, float]],
    ) -> None:
        """
        Adds an ellipse to the SVG.

        Args:
            center (Tuple[float, float]) : Position of the center of the ellipse (x, y).
            radii (Tuple[float, float]) : Radii of the ellipse (rx, ry).
            **presentation_attributes (Dict[str, str]) : Additional SVG attributes such as:
                - 'fill': Fill color of the ellipse (default is 'none').
                - 'stroke': Stroke color of the ellipse (default is 'black').
                - 'stroke_width': Width of the stroke (default is 1).
                - ...

        For a full list of possible attributes, see the SVGwrite documentation:
        https://svgwrite.readthedocs.io/en/latest/attributes/presentation.html
        """
        ellipse = self._drawing.ellipse(
            center=center, r=radii, **presentation_attributes
        )
        self._drawing.add(ellipse)

    def add_rectangle(
        self,
        top_left: Tuple[float, float],
        size: Tuple[float, float],
        rx: Optional[float] = None,
        ry: Optional[float] = None,
        **presentation_attributes: Dict[str, Union[str, float]],
    ) -> None:
        """
        Adds a rectangle to the SVG.

        Args:
            top_left (Tuple[float, float]) : Position of the top-left corner of the rectangle (x, y).
            size (Tuple[float, float]) : Size of the rectangle (width, height).
            rx (Optional[float]) : Horizontal radius of the corners of the rectangle. Defaults to None (no rounding).
            ry (Optional[float]) : Vertical radius of the corners of the rectangle. Defaults to None (no rounding).
            **presentation_attributes (Dict[str, str]) : Additional SVG attributes such as:
                - 'fill': Fill color of the rectangle (default is 'none').
                - 'stroke': Stroke color of the rectangle (default is 'black').
                - 'stroke_width': Width of the stroke (default is 1).
                - ...

        For a full list of possible attributes, see the SVGwrite documentation:
        https://svgwrite.readthedocs.io/en/latest/attributes/presentation.html
        """
        rect = self._drawing.rect(
            insert=top_left, size=size, rx=rx, ry=ry, **presentation_attributes
        )
        self._drawing.add(rect)

    def add_line(
        self,
        start: Tuple[float, float],
        end: Tuple[float, float],
        **presentation_attributes: Dict[str, Union[str, float]],
    ) -> None:
        """
        Adds a line to the SVG.

        Args:
            start (Tuple[float, float]) : Starting point of the line (x, y).
            end (Tuple[float, float]) : Ending point of the line (x, y).
            **presentation_attributes (Dict[str, str]) : Additional SVG attributes such as:
                - 'stroke': Stroke color of the line.
                - 'stroke_width': Width of the stroke.
                - ...

        For a full list of possible attributes, see the SVGwrite documentation:
        https://svgwrite.readthedocs.io/en/latest/attributes/presentation.html
        """
        line = self._drawing.line(start=start, end=end, **presentation_attributes)
        self._drawing.add(line)

    def add_path(
        self,
        path_data: str,
        **presentation_attributes: Dict[str, Union[str, float]],
    ) -> None:
        """
        Adds a path to the SVG.

        Args:
            d (str) : Path data string for the path, following the SVG path data syntax (https://developer.mozilla.org/en-US/docs/Web/SVG/Tutorial/Paths).
            **presentation_attributes (Dict[str, str]) : Additional SVG attributes such as:
                - 'fill': Fill color of the path.
                - 'stroke': Stroke color of the path.
                - 'stroke_width': Width of the stroke.
                - ...

        For a full list of possible attributes, see the SVGwrite documentation:
        https://svgwrite.readthedocs.io/en/latest/attributes/presentation.html
        """
        path = self._drawing.path(d=path_data, **presentation_attributes)
        self._drawing.add(path)

    def add_text(
        self,
        text: str,
        position: Tuple[float, float],
        **presentation_attributes: Dict[str, Union[str, float]],
    ) -> None:
        """
        Adds text to the SVG.

        Args:
            text (str) : The text to display.
            position (Tuple[float, float]) : Position of the text (x, y).
            **presentation_attributes (Dict[str, str]) : Additional SVG attributes such as:
                - 'font_size': Font size of the text.
                - 'fill': Fill color of the text.
                - 'font_family': Font family for the text.
                - ...

        For a full list of possible attributes, see the SVGwrite documentation:
        https://svgwrite.readthedocs.io/en/latest/attributes/presentation.html
        """
        text_elem = self._drawing.text(text, insert=position, **presentation_attributes)
        self._drawing.add(text_elem)

    def add_polygon(
        self, points: List[Tuple[float, float]], **presentation_attributes: Dict
    ) -> None:
        """
        Adds a polygon to the SVG.

        Args:
            points (List[Tuple[float, float]]) : List of points defining the polygon.
            **presentation_attributes (Dict[str, str]) : Additional SVG attributes such as:
                - 'fill': Fill color of the polygon.
                - 'stroke': Stroke color of the polygon.
                - 'stroke_width': Width of the stroke.

        For a full list of possible attributes, see the SVGwrite documentation:
        https://svgwrite.readthedocs.io/en/latest/attributes/presentation.html
        """
        polygon = self._drawing.polygon(points=points, **presentation_attributes)
        self._drawing.add(polygon)

    def add_polyline(
        self,
        points: List[Tuple[float, float]],
        **presentation_attributes: Dict[str, Union[str, float]],
    ) -> None:
        """
        Adds a polyline to the SVG.

        Args:
            points (List[Tuple[float, float]]) : List of points defining the polyline.
            **presentation_attributes (Dict[str, str]) : Additional SVG attributes such as:
                - 'fill': Fill color of the polyline.
                - 'stroke': Stroke color of the polyline.
                - 'stroke_width': Width of the stroke.

        For a full list of possible attributes, see the SVGwrite documentation:
        https://svgwrite.readthedocs.io/en/latest/attributes/presentation.html
        """
        polyline = self._drawing.polyline(points=points, **presentation_attributes)
        self._drawing.add(polyline)

    def save(self, filename: Optional[str] = None) -> None:
        """
        Saves the SVG image to a file.

        Args:
            filename (Optional[str]) : Name of the output file. If None, the filename set in the constructor is used.
        """
        if filename is not None:
            self.set_filename(filename)
        self._drawing.save()

    def get_svg_string(self) -> str:
        """
        Returns the SVG as a string.

        Returns:
            str: SVG as a string.
        """
        return self._drawing.tostring()

    def clear(self) -> None:
        """Clears the SVG image."""
        self._drawing.elements.clear()


class PathBuilder:
    """Class to generate SVG paths with lines, quadratic Bézier curves, cubic Bézier curves and arcs."""

    def __init__(self) -> None:
        """Initializes a new PathBuilder object."""
        self._data_path_parts: List[str] = []
        self._subpath_start_position: Tuple[float, float] = (0, 0)
        self._current_position: Tuple[float, float] = (0, 0)

    @property
    def subpath_start_position(self) -> Tuple[float, float]:
        """
        Returns the start position of the current sub-path.

        Returns:
            Tuple[float, float]: Start position (x, y).
        """
        return self._subpath_start_position

    @property
    def current_position(self) -> Tuple[float, float]:
        """
        Returns the current position.

        Returns:
            Tuple[float, float]: Current position (x, y).
        """
        return self._current_position

    def _add_data_path_part(
        self, command: str, *parameters: Union[float, Tuple[float, float]]
    ) -> None:
        """
        Adds a path data part to the path data string.

        Args:
            command (str): Command for the path data part.
            *parameters (Union[float, Tuple[float, float]]): Parameters for the path data part (x, y or (x, y), 0 or 1).
        """
        flat_parameters = [
            str(p) if isinstance(p, (int, float)) else f"{p[0]} {p[1]}"
            for p in parameters
        ]

        if flat_parameters:
            self._data_path_parts.append(f"{command} {' '.join(flat_parameters)}")
        else:
            # Avoids adding a trailing space if there are no parameters
            self._data_path_parts.append(command)

    def _update_position(
        self, position: Tuple[float, float], relative: bool = False
    ) -> None:
        """
        Updates the current position.

        Args:
            position (Tuple[float, float]): New position (x, y).
            relative (bool): If True, the coordinates are relative to the current position. Defaults to False.
        """
        if relative:
            self._current_position = (
                self._current_position[0] + position[0],
                self._current_position[1] + position[1],
            )
        else:
            self._current_position = position

    def _update_x(self, x: float, relative: bool = False) -> None:
        """
        Updates the current x position.

        Args:
            x (float): New x position.
            relative (bool): If True, the coordinate is relative to the current position. Defaults to False.
        """
        if relative:
            self._current_position = (
                self._current_position[0] + x,
                self._current_position[1],
            )
        else:
            self._current_position = (x, self._current_position[1])

    def _update_y(self, y: float, relative: bool = False) -> None:
        """
        Updates the current y position.

        Args:
            y (float): New y position.
            relative (bool): If True, the coordinate is relative to the current position. Defaults to False.
        """
        if relative:
            self._current_position = (
                self._current_position[0],
                self._current_position[1] + y,
            )
        else:
            self._current_position = (self._current_position[0], y)

    def move_to(self, point: Tuple[float, float], relative: bool = False) -> None:
        """
        Move from the current position to a new position and start a new sub-path.

        Args:
            point (Tuple[float, float]): New position (x, y).
            relative (bool): If True, the coordinates are relative to the current position. Defaults to False.
        """
        command = "m" if relative else "M"
        self._add_data_path_part(command, point)
        self._update_position(point, relative)
        self._subpath_start_position = self._current_position

    def line_to(self, point: Tuple[float, float], relative: bool = False) -> None:
        """
        Draw a straight line from the current position to a new position.

        Args:
            point (Tuple[float, float]): End position of the line (x, y).
            relative (bool): If True, the coordinates are relative to the current position. Defaults to False.
        """
        command = "l" if relative else "L"
        self._add_data_path_part(command, point)
        self._update_position(point, relative)

    def horizontal_line_to(self, x: float, relative: bool = False) -> None:
        """
        Draw a horizontal line from the current position to a new x position.

        Args:
            x (float): New x position.
            relative (bool): If True, the coordinate is relative to the current position. Defaults to False.
        """
        command = "h" if relative else "H"
        self._add_data_path_part(command, x)
        self._update_x(x, relative)

    def vertical_line_to(self, y: float, relative: bool = False) -> None:
        """
        Draw a vertical line from the current position to a new y position.

        Args:
            y (float): New y position.
            relative (bool): If True, the coordinate is relative to the current position. Defaults to False.
        """
        command = "v" if relative else "V"
        self._add_data_path_part(command, y)
        self._update_y(y, relative)

    def cubic_bezier_curve_to(
        self,
        control1: Tuple[float, float],
        control2: Tuple[float, float],
        end: Tuple[float, float],
        relative: bool = False,
    ) -> None:
        """
        Draw a cubic Bézier curve from the current position to a new position.

        Args:
            control1 (Tuple[float, float]): First control point of the curve.
            control2 (Tuple[float, float]): Second control point of the curve.
            end (Tuple[float, float]): End point of the curve.
            relative (bool): If True, the coordinates are relative to the current position. Defaults to False.
        """
        command = "c" if relative else "C"
        self._add_data_path_part(command, control1, control2, end)
        self._update_position(end, relative)

    def extend_cubic_bezier_curve_to(
        self,
        control2: Tuple[float, float],
        end: Tuple[float, float],
        relative: bool = False,
    ) -> None:
        """
        Extend the current cubic Bézier curve to a new position.
        The first control point is calculated as the reflection of the second control point of the previous curve.

        Args:
            control2 (Tuple[float, float]): Second control point of the curve.
            end (Tuple[float, float]): End point of the curve.
            relative (bool): If True, the coordinates are relative to the current position. Defaults to False.
        """
        command = "s" if relative else "S"
        self._add_data_path_part(command, control2, end)
        self._update_position(end, relative)

    def quadratic_bezier_curve_to(
        self,
        control: Tuple[float, float],
        end: Tuple[float, float],
        relative: bool = False,
    ) -> None:
        """
        Draw a quadratic Bézier curve from the current position to a new position.

        Args:
            control (Tuple[float, float]): Control point of the curve.
            end (Tuple[float, float]): End point of the curve.
            relative (bool): If True, the coordinates are relative to the current position. Defaults to False.
        """
        command = "q" if relative else "Q"
        self._add_data_path_part(command, control, end)
        self._update_position(end, relative)

    def extend_quadratic_bezier_curve_to(
        self, end: Tuple[float, float], relative: bool = False
    ) -> None:
        """
        Extend the current quadratic Bézier curve to a new position.
        The control point is calculated as the reflection of the control point of the previous curve.

        Args:
            end (Tuple[float, float]): End point of the curve.
            relative (bool): If True, the coordinates are relative to the current position. Defaults to False.
        """
        command = "t" if relative else "T"
        self._add_data_path_part(command, end)
        self._update_position(end, relative)

    def arc_to(
        self,
        radius: Tuple[float, float],
        rotation: float,
        large_arc: bool,
        sweep: bool,
        end: Tuple[float, float],
        relative: bool = False,
    ) -> None:
        """
        Draw an elliptical arc from the current position to a new position.

        Args:
            radius (Tuple[float, float]): Radii of the ellipse (rx, ry).
            rotation (float): Rotation of the ellipse.
            large_arc (bool): Flag to choose the large arc (True) or the small arc (False).
            sweep (bool): Flag to choose the clockwise arc (True) or the counterclockwise arc (False).
            end (Tuple[float, float]): End point of the arc.
            relative (bool): If True, the coordinates are relative to the current position. Defaults to False.
        """
        command = "a" if relative else "A"
        self._add_data_path_part(
            command, radius, rotation, int(large_arc), int(sweep), end
        )
        self._update_position(end, relative)

    def close_path(self) -> None:
        """Close the current path."""
        self._add_data_path_part("Z")
        self._current_position = self._subpath_start_position

    def get_data(self) -> str:
        """
        Returns the path data string.

        Returns:
            str: Path data string.
        """
        return " ".join(self._data_path_parts)

    def clear(self) -> None:
        """Clears the path data."""
        self._data_path_parts = []
        self._subpath_start_position = (0, 0)
        self._current_position = (0, 0)
