import pytest
from unittest import mock
from svg_utils.utils.svg_builder import SVGBuilder


class TestSVGBuilder:
    """Test for the SVGBuilder class."""

    @pytest.fixture
    def svg_builder(self):
        """Fixture to create an SVGBuilder instance."""
        return SVGBuilder(
            filename="test_output.svg",
            size=(400, 600),
            viewbox=(0, 0, 400, 600),
            profile="tiny",
        )

    def test_get_svg_string(self, svg_builder):
        """Test getting the SVG string."""
        svg_string = svg_builder.get_svg_string().replace(",", " ")
        assert "<svg" in svg_string
        assert "</svg>" in svg_string

    def test_initialization(self, svg_builder):
        """Test initialization of SVGBuilder."""
        svg_string = svg_builder.get_svg_string().replace(",", " ")
        assert 'width="400"' in svg_string
        assert 'height="600"' in svg_string
        assert 'viewBox="0 0 400 600"' in svg_string
        assert 'baseProfile="tiny"' in svg_string

    def test_set_size(self, svg_builder):
        """Test changing the size of the SVG."""
        svg_builder.set_size((800, 1000))
        svg_string = svg_builder.get_svg_string().replace(",", " ")
        assert 'width="800"' in svg_string
        assert 'height="1000"' in svg_string

    def test_set_viewbox(self, svg_builder):
        """Test setting the viewbox for the SVG."""
        svg_builder.set_viewbox((0, 0, 800, 1000))
        svg_string = svg_builder.get_svg_string().replace(",", " ")
        assert 'viewBox="0 0 800 1000"' in svg_string

    def test_add_circle(self, svg_builder):
        """Test adding a circle to the SVG."""
        svg_builder.add_circle((100, 200), 50)
        svg_string = svg_builder.get_svg_string().replace(",", " ")
        assert "<circle" in svg_string
        assert 'cx="100"' in svg_string
        assert 'cy="200"' in svg_string
        assert 'r="50"' in svg_string

    def test_add_ellipse(self, svg_builder):
        """Test adding an ellipse to the SVG."""
        svg_builder.add_ellipse((100, 200), (25, 50))
        svg_string = svg_builder.get_svg_string().replace(",", " ")
        assert "<ellipse" in svg_string
        assert 'cx="100"' in svg_string
        assert 'cy="200"' in svg_string
        assert 'rx="25"' in svg_string
        assert 'ry="50"' in svg_string

    def test_add_rectangle(self, svg_builder):
        """Test adding a rectangle to the SVG."""
        svg_builder.add_rectangle((100, 200), (25, 50))
        svg_string = svg_builder.get_svg_string().replace(",", " ")
        assert "<rect" in svg_string
        assert 'x="100"' in svg_string
        assert 'y="200"' in svg_string
        assert 'width="25"' in svg_string
        assert 'height="50"' in svg_string

    def test_add_line(self, svg_builder):
        """Test adding a line to the SVG."""
        svg_builder.add_line((100, 200), (150, 250))
        svg_string = svg_builder.get_svg_string().replace(",", " ")
        assert "<line" in svg_string
        assert 'x1="100"' in svg_string
        assert 'y1="200"' in svg_string
        assert 'x2="150"' in svg_string
        assert 'y2="250"' in svg_string

    def test_add_path(self, svg_builder):
        """Test adding a path to the SVG."""
        path_data = "M 50 100 L 150 200 L 250 300 L 350 400 Z"
        svg_builder.add_path(path_data)
        svg_string = svg_builder.get_svg_string().replace(",", " ")
        assert "<path" in svg_string
        assert f'd="{path_data}"' in svg_string

    def test_add_text(self, svg_builder):
        """Test adding text to the SVG."""
        svg_builder.add_text("Hello world!", (100, 200))
        svg_string = svg_builder.get_svg_string().replace(",", " ")
        assert "<text" in svg_string
        assert 'x="100"' in svg_string
        assert 'y="200"' in svg_string
        assert ">Hello world!</text>" in svg_string

    def test_add_polygon(self, svg_builder):
        """Test adding a polygon to the SVG."""
        points = [(100, 150), (200, 300), (400, 250), (375, 125), (225, 75)]
        svg_builder.add_polygon(points)
        svg_string = svg_builder.get_svg_string().replace(",", " ")
        assert "<polygon" in svg_string
        assert 'points="100 150 200 300 400 250 375 125 225 75"' in svg_string

    def test_add_polyline(self, svg_builder):
        """Test adding a polyline to the SVG."""
        points = [(100, 150), (200, 300), (400, 250), (375, 125), (225, 75)]
        svg_builder.add_polyline(points)
        svg_string = svg_builder.get_svg_string().replace(",", " ")
        assert "<polyline" in svg_string
        assert 'points="100 150 200 300 400 250 375 125 225 75"' in svg_string

    @mock.patch("io.open", new_callable=mock.mock_open)
    def test_save(self, mock_open, svg_builder):
        """Test saving the SVG to a file and verifying the filename.

        This test depends on the implemntation of the save method, which uses the io.open function to write to a file.
        The mock replaces the io.open call to avoid writing to the file system.
        """
        svg_builder.save()
        mock_open.assert_called_once_with("test_output.svg", mode="w", encoding="utf-8")
        mock_open().write.assert_called()
        content = mock_open().write.call_args[0][0].replace(",", " ")
        assert "<svg" in content
        assert "</svg>" in content

    @mock.patch("io.open", new_callable=mock.mock_open)
    def test_set_filename(self, mock_open, svg_builder):
        """Test setting the filename of the SVG.

        This test depends on the implemntation of the save method, which uses the io.open function to write to a file.
        The mock replaces the io.open call to avoid writing to the file system.
        """
        svg_builder.set_filename("test_set_filename.svg")
        svg_builder.save()
        mock_open.assert_called_once_with(
            "test_set_filename.svg", mode="w", encoding="utf-8"
        )
        mock_open().write.assert_called()

    def test_clear(self, svg_builder):
        """Test clearing the SVG content."""
        svg_builder.add_circle((100, 100), 50)
        svg_builder.clear()
        svg_string = svg_builder.get_svg_string().replace(",", " ")
        assert "<circle" not in svg_string

    def test_basic_presentation_attributes(self, svg_builder):
        """Test basic presentation attributes: fill, stroke, stroke-width, opacity."""
        svg_builder.add_circle(
            (100, 100), 50, fill="yellow", stroke="red", stroke_width=2, opacity=0.5
        )
        svg_string = svg_builder.get_svg_string().replace(",", " ")
        assert 'fill="yellow"' in svg_string
        assert 'stroke="red"' in svg_string
        assert 'stroke-width="2"' in svg_string
        assert 'opacity="0.5"' in svg_string

    def test_stroke_presentation_attributes(self, svg_builder):
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

    def test_text_presentation_attributes(self, svg_builder):
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
