from typing import List, Tuple
from unittest import mock

import pytest
from svg_utils.utils.svg_builder import SVGBuilder


class TestSVGBuilder:
    """Test for the SVGBuilder class."""

    DEFAULT_FILENAME = "test_output.svg"
    DEFAULT_SIZE = (400, 600)
    DEFAULT_VIEWBOX = (0, 0, 400, 600)
    DEFAULT_PROFILE = "tiny"

    @pytest.fixture
    def svg_builder(self) -> SVGBuilder:
        """Fixture to create an SVGBuilder instance."""
        return SVGBuilder(
            filename=self.DEFAULT_FILENAME,
            size=self.DEFAULT_SIZE,
            viewbox=self.DEFAULT_VIEWBOX,
            profile=self.DEFAULT_PROFILE,
        )

    def test_get_svg_string(self, svg_builder: SVGBuilder) -> None:
        """Test getting the SVG string."""
        svg_string = svg_builder.get_svg_string().replace(",", " ")
        assert "<svg" in svg_string
        assert "</svg>" in svg_string

    def test_initialization(self, svg_builder: SVGBuilder) -> None:
        """Test initialization of SVGBuilder."""
        svg_string = svg_builder.get_svg_string().replace(",", " ")
        assert f'width="{self.DEFAULT_SIZE[0]}"' in svg_string
        assert f'height="{self.DEFAULT_SIZE[1]}"' in svg_string
        assert f'viewBox="{" ".join(map(str, self.DEFAULT_VIEWBOX))}"' in svg_string
        assert f'baseProfile="{self.DEFAULT_PROFILE}"' in svg_string

    @pytest.mark.parametrize(
        "size, expected_width, expected_height",
        [
            ((800, 1000), "800", "1000"),
        ],
    )
    def test_set_size(
        self,
        svg_builder: SVGBuilder,
        size: Tuple[int, int],
        expected_width: str,
        expected_height: str,
    ) -> None:
        """Test setting the size of the SVG."""
        svg_builder.set_size(size)
        svg_string = svg_builder.get_svg_string().replace(",", " ")
        assert f'width="{expected_width}"' in svg_string
        assert f'height="{expected_height}"' in svg_string

    @pytest.mark.parametrize(
        "viewbox, expected",
        [
            ((0, 0, 800, 1000), "0 0 800 1000"),
        ],
    )
    def test_set_viewbox(
        self, svg_builder: SVGBuilder, viewbox: Tuple[int, int, int, int], expected: str
    ) -> None:
        """Test setting the viewbox for the SVG."""
        svg_builder.set_viewbox((0, 0, 800, 1000))
        svg_string = svg_builder.get_svg_string().replace(",", " ")
        assert 'viewBox="0 0 800 1000"' in svg_string

    @pytest.mark.parametrize(
        "center, radius, expected_cx, expected_cy, expected_r",
        [
            ((100, 200), 50, "100", "200", "50"),
        ],
    )
    def test_add_circle(
        self,
        svg_builder: SVGBuilder,
        center: Tuple[int, int],
        radius: int,
        expected_cx: str,
        expected_cy: str,
        expected_r: str,
    ) -> None:
        """Test adding a circle to the SVG."""
        svg_builder.add_circle(center, radius)
        svg_string = svg_builder.get_svg_string().replace(",", " ")
        assert "<circle" in svg_string
        assert f'cx="{expected_cx}"' in svg_string
        assert f'cy="{expected_cy}"' in svg_string
        assert f'r="{expected_r}"' in svg_string

    @pytest.mark.parametrize(
        "center, radii, expected_cx, expected_cy, expected_rx, expected_ry",
        [
            ((100, 200), (25, 50), "100", "200", "25", "50"),
        ],
    )
    def test_add_ellipse(
        self,
        svg_builder: SVGBuilder,
        center: Tuple[int, int],
        radii: Tuple[int, int],
        expected_cx: str,
        expected_cy: str,
        expected_rx: str,
        expected_ry: str,
    ) -> None:
        """Test adding an ellipse to the SVG."""
        svg_builder.add_ellipse(center, radii)
        svg_string = svg_builder.get_svg_string().replace(",", " ")
        assert "<ellipse" in svg_string
        assert f'cx="{expected_cx}"' in svg_string
        assert f'cy="{expected_cy}"' in svg_string
        assert f'rx="{expected_rx}"' in svg_string
        assert f'ry="{expected_ry}"' in svg_string

    @pytest.mark.parametrize(
        "position, size, expected_x, expected_y, expected_width, expected_height",
        [
            ((100, 200), (25, 50), "100", "200", "25", "50"),
        ],
    )
    def test_add_rectangle(
        self,
        svg_builder: SVGBuilder,
        position: Tuple[int, int],
        size: Tuple[int, int],
        expected_x: str,
        expected_y: str,
        expected_width: str,
        expected_height: str,
    ) -> None:
        """Test adding a rectangle to the SVG."""
        svg_builder.add_rectangle(position, size)
        svg_string = svg_builder.get_svg_string().replace(",", " ")
        assert "<rect" in svg_string
        assert f'x="{expected_x}"' in svg_string
        assert f'y="{expected_y}"' in svg_string
        assert f'width="{expected_width}"' in svg_string
        assert f'height="{expected_height}"' in svg_string

    @pytest.mark.parametrize(
        "start, end, expected_x1, expected_y1, expected_x2, expected_y2",
        [
            ((100, 200), (150, 250), "100", "200", "150", "250"),
        ],
    )
    def test_add_line(
        self,
        svg_builder: SVGBuilder,
        start: Tuple[int, int],
        end: Tuple[int, int],
        expected_x1: str,
        expected_y1: str,
        expected_x2: str,
        expected_y2: str,
    ) -> None:
        """Test adding a line to the SVG."""
        svg_builder.add_line(start, end)
        svg_string = svg_builder.get_svg_string().replace(",", " ")
        assert "<line" in svg_string
        assert f'x1="{expected_x1}"' in svg_string
        assert f'y1="{expected_y1}"' in svg_string
        assert f'x2="{expected_x2}"' in svg_string
        assert f'y2="{expected_y2}"' in svg_string

    @pytest.mark.parametrize(
        "path_data, expected",
        [
            (
                "M 50 100 L 150 200 L 250 300 L 350 400 Z",
                "M 50 100 L 150 200 L 250 300 L 350 400 Z",
            ),
        ],
    )
    def test_add_path(
        self,
        svg_builder: SVGBuilder,
        path_data: str,
        expected: str,
    ) -> None:
        """Test adding a path to the SVG."""
        svg_builder.add_path(path_data)
        svg_string = svg_builder.get_svg_string().replace(",", " ")
        assert "<path" in svg_string
        assert f'd="{expected}"' in svg_string

    @pytest.mark.parametrize(
        "text, position, expected_x, expected_y, expected_text",
        [
            ("Hello world!", (100, 200), "100", "200", "Hello world!"),
        ],
    )
    def test_add_text(
        self,
        svg_builder: SVGBuilder,
        text: str,
        position: Tuple[int, int],
        expected_x: str,
        expected_y: str,
        expected_text: str,
    ) -> None:
        """Test adding text to the SVG."""
        svg_builder.add_text(text, position)
        svg_string = svg_builder.get_svg_string().replace(",", " ")
        assert "<text" in svg_string
        assert f'x="{expected_x}"' in svg_string
        assert f'y="{expected_y}"' in svg_string
        assert f">{expected_text}</text>" in svg_string

    @pytest.mark.parametrize(
        "points, expected_points",
        [
            (
                [(100, 150), (200, 300), (400, 250), (375, 125), (225, 75)],
                "100 150 200 300 400 250 375 125 225 75",
            ),
        ],
    )
    def test_add_polygon(
        self,
        svg_builder: SVGBuilder,
        points: List[Tuple[int, int]],
        expected_points: str,
    ) -> None:
        """Test adding a polygon to the SVG."""
        svg_builder.add_polygon(points)
        svg_string = svg_builder.get_svg_string().replace(",", " ")
        assert "<polygon" in svg_string
        assert f'points="{expected_points}"' in svg_string

    @pytest.mark.parametrize(
        "points, expected_points",
        [
            (
                [(100, 150), (200, 300), (400, 250), (375, 125), (225, 75)],
                "100 150 200 300 400 250 375 125 225 75",
            ),
        ],
    )
    def test_add_polyline(
        self,
        svg_builder: SVGBuilder,
        points: List[Tuple[int, int]],
        expected_points: str,
    ) -> None:
        """Test adding a polyline to the SVG."""
        svg_builder.add_polyline(points)
        svg_string = svg_builder.get_svg_string().replace(",", " ")
        assert "<polyline" in svg_string
        assert f'points="{expected_points}"' in svg_string

    @mock.patch("io.open", new_callable=mock.mock_open)
    def test_save(self, mock_open: mock.Mock, svg_builder: SVGBuilder) -> None:
        """Test saving the SVG to a file and verifying the filename.

        This test depends on the implementation of the save method, which uses the io.open function to write to a file.
        The mock replaces the io.open call to avoid writing to the file system.
        """
        svg_builder.save()
        mock_open.assert_called_once_with("test_output.svg", mode="w", encoding="utf-8")
        mock_open().write.assert_called()
        content = mock_open().write.call_args[0][0].replace(",", " ")
        assert "<svg" in content
        assert "</svg>" in content

    @pytest.mark.parametrize(
        "filename, expected",
        [
            ("test_save.svg", "test_save.svg"),
        ],
    )
    @mock.patch("io.open", new_callable=mock.mock_open)
    def test_set_filename(
        self,
        mock_open: mock.Mock,
        svg_builder: SVGBuilder,
        filename: str,
        expected: str,
    ) -> None:
        """Test setting the filename of the SVG.

        This test depends on the implementation of the save method, which uses the io.open function to write to a file.
        The mock replaces the io.open call to avoid writing to the file system.
        """
        svg_builder.set_filename(filename)
        svg_builder.save()
        mock_open.assert_called_once_with(expected, mode="w", encoding="utf-8")
        mock_open().write.assert_called()

    def test_clear(self, svg_builder: SVGBuilder) -> None:
        """Test clearing the SVG content."""
        svg_builder.add_circle((100, 100), 50)
        svg_builder.clear()
        svg_string = svg_builder.get_svg_string().replace(",", " ")
        assert "<circle" not in svg_string

    def test_basic_presentation_attributes(self, svg_builder: SVGBuilder) -> None:
        """Test basic presentation attributes: fill, stroke, stroke-width, opacity."""
        svg_builder.add_circle(
            (100, 100), 50, fill="yellow", stroke="red", stroke_width=2, opacity=0.5
        )
        svg_string = svg_builder.get_svg_string().replace(",", " ")
        assert 'fill="yellow"' in svg_string
        assert 'stroke="red"' in svg_string
        assert 'stroke-width="2"' in svg_string
        assert 'opacity="0.5"' in svg_string

    def test_stroke_presentation_attributes(self, svg_builder: SVGBuilder) -> None:
        """Test stroke-specific presentation attributes: stroke-dasharray, stroke-dashoffset, stroke-linecap, stroke-linejoin."""
        svg_builder.add_rectangle(
            (50, 50),
            (200, 100),
            stroke="black",
            stroke_width=3,
            stroke_dasharray="5 5",
            stroke_dashoffset=2,
            stroke_linecap="round",
            stroke_linejoin="bevel",
        )
        svg_string = svg_builder.get_svg_string().replace(",", " ")
        assert 'stroke="black"' in svg_string
        assert 'stroke-width="3"' in svg_string
        assert 'stroke-dasharray="5 5"' in svg_string
        assert 'stroke-dashoffset="2"' in svg_string
        assert 'stroke-linecap="round"' in svg_string
        assert 'stroke-linejoin="bevel"' in svg_string

    def test_text_presentation_attributes(self, svg_builder: SVGBuilder) -> None:
        """Test text-specific presentation attributes: font-size, font-family, text-anchor, letter-spacing."""
        svg_builder.add_text(
            "Hello world!",
            (100, 100),
            font_size="20px",
            font_family="Arial",
            font_weight="bold",
            text_anchor="middle",
        )
        svg_string = svg_builder.get_svg_string().replace(",", " ")
        assert 'font-size="20px"' in svg_string
        assert 'font-family="Arial"' in svg_string
        assert 'font-weight="bold"' in svg_string
        assert 'text-anchor="middle"' in svg_string
