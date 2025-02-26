from typing import Tuple, List, Union


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
        self,
        command: str,
        *parameters: Union[float, Tuple[float, float]],
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
        self,
        position: Tuple[float, float],
        relative: bool = False,
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

    def _update_x(
        self,
        x: float,
        relative: bool = False,
    ) -> None:
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

    def _update_y(
        self,
        y: float,
        relative: bool = False,
    ) -> None:
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

    def move_to(
        self,
        point: Tuple[float, float],
        relative: bool = False,
    ) -> None:
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

    def line_to(
        self,
        point: Tuple[float, float],
        relative: bool = False,
    ) -> None:
        """
        Draw a straight line from the current position to a new position.

        Args:
            point (Tuple[float, float]): End position of the line (x, y).
            relative (bool): If True, the coordinates are relative to the current position. Defaults to False.
        """
        command = "l" if relative else "L"
        self._add_data_path_part(command, point)
        self._update_position(point, relative)

    def horizontal_line_to(
        self,
        x: float,
        relative: bool = False,
    ) -> None:
        """
        Draw a horizontal line from the current position to a new x position.

        Args:
            x (float): New x position.
            relative (bool): If True, the coordinate is relative to the current position. Defaults to False.
        """
        command = "h" if relative else "H"
        self._add_data_path_part(command, x)
        self._update_x(x, relative)

    def vertical_line_to(
        self,
        y: float,
        relative: bool = False,
    ) -> None:
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
        self,
        end: Tuple[float, float],
        relative: bool = False,
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
