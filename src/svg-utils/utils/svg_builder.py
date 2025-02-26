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
            profile (Literal["tiny", "full"]) : SVG profile to use ("tiny", "basic", or "full"). Defaults to "tiny".
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
            text (str) : Text to display.
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
        self,
        points: List[Tuple[float, float]],
        **presentation_attributes: Dict,
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
