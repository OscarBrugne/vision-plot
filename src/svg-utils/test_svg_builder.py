import unittest
from unittest import mock
from svg_builder import SVGBuilder, PathBuilder


class TestSVGBuilder(unittest.TestCase):
    """Test for the SVGBuilder class."""

    def setUp(self):
        """Set up test environment for each test."""
        self.svg = SVGBuilder(
            filename="test_output.svg",
            size=(400, 600),
            viewbox=(0, 0, 400, 600),
            profile="tiny",
        )

    def test_get_svg_string(self):
        """Test getting the SVG string."""
        svg_string = self.svg.get_svg_string().replace(",", " ")
        self.assertIn("<svg", svg_string)
        self.assertIn("</svg>", svg_string)

    def test_initialization(self):
        """Test initialization of SVGBuilder."""
        # Replace commas with spaces for handling formats with and without commas
        svg_string = self.svg.get_svg_string().replace(",", " ")

        self.assertIn('width="400"', svg_string)
        self.assertIn('height="600"', svg_string)
        self.assertIn('viewBox="0 0 400 600"', svg_string)
        self.assertIn('baseProfile="tiny"', svg_string)

    def test_set_size(self):
        """Test changing the size of the SVG."""
        self.svg.set_size((800, 1000))
        svg_string = self.svg.get_svg_string().replace(",", " ")
        self.assertIn('width="800"', svg_string)
        self.assertIn('height="1000"', svg_string)

    def test_set_viewbox(self):
        """Test setting the viewbox for the SVG."""
        self.svg.set_viewbox((0, 0, 800, 1000))
        svg_string = self.svg.get_svg_string().replace(",", " ")

        self.assertIn('viewBox="0 0 800 1000"', svg_string)

    def test_add_circle(self):
        """Test adding a circle to the SVG."""
        self.svg.add_circle((100, 200), 50)
        svg_string = self.svg.get_svg_string().replace(",", " ")
        self.assertIn("<circle", svg_string)
        self.assertIn('cx="100"', svg_string)
        self.assertIn('cy="200"', svg_string)
        self.assertIn('r="50"', svg_string)

    def test_add_ellipse(self):
        """Test adding an ellipse to the SVG."""
        self.svg.add_ellipse((100, 200), (25, 50))
        svg_string = self.svg.get_svg_string().replace(",", " ")
        self.assertIn("<ellipse", svg_string)
        self.assertIn('cx="100"', svg_string)
        self.assertIn('cy="200"', svg_string)
        self.assertIn('rx="25"', svg_string)
        self.assertIn('ry="50"', svg_string)

    def test_add_rectangle(self):
        """Test adding a rectangle to the SVG."""
        self.svg.add_rectangle((100, 200), (25, 50))
        svg_string = self.svg.get_svg_string().replace(",", " ")
        self.assertIn("<rect", svg_string)
        self.assertIn('x="100"', svg_string)
        self.assertIn('y="200"', svg_string)
        self.assertIn('width="25"', svg_string)
        self.assertIn('height="50"', svg_string)

    def test_add_line(self):
        """Test adding a line to the SVG."""
        self.svg.add_line((100, 200), (150, 250))
        svg_string = self.svg.get_svg_string().replace(",", " ")
        self.assertIn("<line", svg_string)
        self.assertIn('x1="100"', svg_string)
        self.assertIn('y1="200"', svg_string)
        self.assertIn('x2="150"', svg_string)
        self.assertIn('y2="250"', svg_string)

    def test_add_path(self):
        """Test adding a path to the SVG."""
        path_data = "M 50 100 L 150 200 L 250 300 L 350 400 Z"
        self.svg.add_path(path_data)
        svg_string = self.svg.get_svg_string().replace(",", " ")
        self.assertIn("<path", svg_string)
        self.assertIn(f'd="{path_data}"', svg_string)

    def test_add_text(self):
        """Test adding text to the SVG."""
        self.svg.add_text("Hello world!", (100, 200))
        svg_string = self.svg.get_svg_string().replace(",", " ")
        self.assertIn("<text", svg_string)
        self.assertIn('x="100"', svg_string)
        self.assertIn('y="200"', svg_string)
        self.assertIn(">Hello world!</text>", svg_string)

    def test_add_polygon(self):
        """Test adding a polygon to the SVG."""
        # Use a list of tuples for points with strictly distinct x and y values (no duplicates even between points and x or y values)
        points = [(100, 150), (200, 300), (400, 250), (375, 125), (225, 75)]
        self.svg.add_polygon(points)
        svg_string = self.svg.get_svg_string().replace(",", " ")
        self.assertIn("<polygon", svg_string)
        self.assertIn('points="100 150 200 300 400 250 375 125 225 75"', svg_string)

    def test_add_polyline(self):
        """Test adding a polyline to the SVG."""
        points = [(100, 150), (200, 300), (400, 250), (375, 125), (225, 75)]
        self.svg.add_polyline(points)
        svg_string = self.svg.get_svg_string().replace(",", " ")
        self.assertIn("<polyline", svg_string)
        self.assertIn('points="100 150 200 300 400 250 375 125 225 75"', svg_string)

    @mock.patch("io.open", new_callable=mock.mock_open)
    def test_save(self, mock_open):
        """Test saving the SVG to a file and verifying the filename.

        This test depends on the implemntation of the save method, which uses the io.open function to write to a file.
        The mock replaces the io.open call to avoid writing to the file system.
        """
        self.svg.save()
        mock_open.assert_called_once_with("test_output.svg", mode="w", encoding="utf-8")
        mock_open().write.assert_called()

        content = mock_open().write.call_args[0][0].replace(",", " ")
        self.assertIn("<svg", content)
        self.assertIn("</svg>", content)

    @mock.patch("io.open", new_callable=mock.mock_open)
    def test_set_filename(self, mock_open):
        """Test setting the filename of the SVG.

        This test depends on the implemntation of the save method, which uses the io.open function to write to a file.
        The mock replaces the io.open call to avoid writing to the file system.
        """
        self.svg.set_filename("test_set_filename.svg")
        self.svg.save()
        mock_open.assert_called_once_with(
            "test_set_filename.svg", mode="w", encoding="utf-8"
        )
        mock_open().write.assert_called()

    def test_clear(self):
        """Test clearing the SVG content."""
        self.svg.add_circle((100, 100), 50)
        self.svg.clear()
        svg_string = self.svg.get_svg_string().replace(",", " ")
        self.assertNotIn("<circle", svg_string)

    def test_basic_presentation_attributes(self):
        """Test basic presentation attributes: fill, stroke, stroke-width, opacity."""
        self.svg.add_circle(
            (100, 100), 50, fill="yellow", stroke="red", stroke_width=2, opacity=0.5
        )
        svg_string = self.svg.get_svg_string().replace(",", " ")
        self.assertIn('fill="yellow"', svg_string)
        self.assertIn('stroke="red"', svg_string)
        self.assertIn('stroke-width="2"', svg_string)
        self.assertIn('opacity="0.5"', svg_string)

    def test_stroke_presentation_attributes(self):
        """Test stroke-specific presentation attributes: stroke-dasharray, stroke-dashoffset, stroke-linecap, stroke-linejoin."""
        self.svg.add_rectangle(
            (50, 50),
            (200, 100),
            stroke="black",
            stroke_width=3,
            stroke_dasharray="5 5",
            stroke_dashoffset=2,
            stroke_linecap="round",
            stroke_linejoin="bevel",
        )
        svg_string = self.svg.get_svg_string().replace(",", " ")
        self.assertIn('stroke="black"', svg_string)
        self.assertIn('stroke-width="3"', svg_string)
        self.assertIn('stroke-dasharray="5 5"', svg_string)
        self.assertIn('stroke-dashoffset="2"', svg_string)
        self.assertIn('stroke-linecap="round"', svg_string)
        self.assertIn('stroke-linejoin="bevel"', svg_string)

    def test_text_presentation_attributes(self):
        """Test text-specific presentation attributes: font-size, font-family, text-anchor, letter-spacing."""
        self.svg.add_text(
            "Hello world!",
            (100, 100),
            font_size="20px",
            font_family="Arial",
            font_weight="bold",
            text_anchor="middle",
        )
        svg_string = self.svg.get_svg_string().replace(",", " ")
        self.assertIn('font-size="20px"', svg_string)
        self.assertIn('font-family="Arial"', svg_string)
        self.assertIn('font-weight="bold"', svg_string)
        self.assertIn('text-anchor="middle"', svg_string)


class TestPathBuilder(unittest.TestCase):
    """Test for the PathBuilder class."""

    def setUp(self):
        """Set up test environment for each test."""
        self.path_builder = PathBuilder()

    def test_initialization(self):
        """Test initialization of PathBuilder."""
        path_data = self.path_builder.get_data()
        self.assertEqual(path_data, "")

    def test_move_to(self):
        """Test moving to a new position."""
        self.path_builder.move_to((50, 100))
        path_data = self.path_builder.get_data()
        self.assertIn("M 50 100", path_data)

    def test_move_to_relative(self):
        """Test moving to a new position relative to the current position."""
        self.path_builder.move_to((50, 100), relative=True)
        path_data = self.path_builder.get_data()
        self.assertIn("m 50 100", path_data)

    def test_line_to(self):
        """Test drawing a line to a new position."""
        self.path_builder.line_to((50, 100))
        path_data = self.path_builder.get_data()
        self.assertIn("L 50 100", path_data)

    def test_line_to_relative(self):
        """Test drawing a line to a new position relative to the current position."""
        self.path_builder.line_to((50, 100), relative=True)
        path_data = self.path_builder.get_data()
        self.assertIn("l 50 100", path_data)

    def test_horizontal_line_to(self):
        """Test drawing a horizontal line to a new position."""
        self.path_builder.horizontal_line_to(100)
        path_data = self.path_builder.get_data()
        self.assertIn("H 100", path_data)

    def test_horizontal_line_to_relative(self):
        """Test drawing a horizontal line to a new position relative to the current position."""
        self.path_builder.horizontal_line_to(100, relative=True)
        path_data = self.path_builder.get_data()
        self.assertIn("h 100", path_data)

    def test_vertical_line_to(self):
        """Test drawing a vertical line to a new position."""
        self.path_builder.vertical_line_to(100)
        path_data = self.path_builder.get_data()
        self.assertIn("V 100", path_data)

    def test_vertical_line_to_relative(self):
        """Test drawing a vertical line to a new position relative to the current position."""
        self.path_builder.vertical_line_to(100, relative=True)
        path_data = self.path_builder.get_data()
        self.assertIn("v 100", path_data)

    def test_cubic_bezier_curve_to(self):
        """Test drawing a cubic Bezier curve to a new position."""
        self.path_builder.cubic_bezier_curve_to((100, 150), (50, 250), (300, 350))
        path_data = self.path_builder.get_data()
        self.assertIn("C 100 150 50 250 300 350", path_data)

    def test_cubic_bezier_curve_to_relative(self):
        """Test drawing a cubic Bezier curve to a new position relative to the current position."""
        self.path_builder.cubic_bezier_curve_to(
            (100, 150), (50, 250), (300, 350), relative=True
        )
        path_data = self.path_builder.get_data()
        self.assertIn("c 100 150 50 250 300 350", path_data)

    def test_extend_cubic_bezier_curve_to(self):
        """Test extending a cubic Bezier curve to a new position."""
        self.path_builder.extend_cubic_bezier_curve_to((50, 250), (300, 350))
        path_data = self.path_builder.get_data()
        self.assertIn("S 50 250 300 350", path_data)

    def test_extend_cubic_bezier_curve_to_relative(self):
        """Test extending a cubic Bezier curve to a new position relative to the current position."""
        self.path_builder.extend_cubic_bezier_curve_to(
            (50, 250), (300, 350), relative=True
        )
        path_data = self.path_builder.get_data()
        self.assertIn("s 50 250 300 350", path_data)

    def test_quadratic_bezier_curve_to(self):
        """Test drawing a quadratic Bezier curve to a new position."""
        self.path_builder.quadratic_bezier_curve_to((100, 150), (200, 250))
        path_data = self.path_builder.get_data()
        self.assertIn("Q 100 150 200 250", path_data)

    def test_quadratic_bezier_curve_to_relative(self):
        """Test drawing a quadratic Bezier curve to a new position relative to the current position."""
        self.path_builder.quadratic_bezier_curve_to(
            (100, 150), (200, 250), relative=True
        )
        path_data = self.path_builder.get_data()
        self.assertIn("q 100 150 200 250", path_data)

    def test_extend_quadratic_bezier_curve_to(self):
        """Test extending a quadratic Bezier curve to a new position."""
        self.path_builder.extend_quadratic_bezier_curve_to((200, 250))
        path_data = self.path_builder.get_data()
        self.assertIn("T 200 250", path_data)

    def test_extend_quadratic_bezier_curve_to_relative(self):
        """Test extending a quadratic Bezier curve to a new position relative to the current position."""
        self.path_builder.extend_quadratic_bezier_curve_to((200, 250), relative=True)
        path_data = self.path_builder.get_data()
        self.assertIn("t 200 250", path_data)

    def test_arc_to(self):
        """Test drawing an arc to a new position."""
        self.path_builder.arc_to((50, 25), 20, True, False, (100, 150))
        path_data = self.path_builder.get_data()
        self.assertIn("A 50 25 20 1 0 100 150", path_data)

    def test_arc_to_relative(self):
        """Test drawing an arc to a new position relative to the current position."""
        self.path_builder.arc_to((50, 25), 20, True, False, (100, 150), relative=True)
        path_data = self.path_builder.get_data()
        self.assertIn("a 50 25 20 1 0 100 150", path_data)

    def test_close_path(self):
        """Test closing the path."""
        self.path_builder.close_path()
        path_data = self.path_builder.get_data()
        self.assertIn("Z", path_data)

    def test_clear(self):
        """Test clearing the path data."""
        self.path_builder.move_to((100, 100))
        self.path_builder.line_to((200, 100))
        self.path_builder.clear()
        path_data = self.path_builder.get_data()
        self.assertEqual(path_data, "")

    def test_subpath_start_position(self):
        """Test retrieving the start position of the current sub-path."""
        self.path_builder.move_to((100, 150))
        self.assertEqual(self.path_builder.subpath_start_position, (100, 150))

    def test_subpath_start_position_after_move(self):
        """Test that the subpath start position updates correctly after moving."""
        self.path_builder.move_to((100, 150))
        self.path_builder.line_to((200, 250))
        self.assertEqual(self.path_builder.subpath_start_position, (100, 150))

    def test_subpath_start_position_after_new_subpath(self):
        """Test that the subpath start position updates correctly after creating a new sub-path."""
        self.path_builder.move_to((100, 150))
        self.path_builder.line_to((200, 250))
        self.path_builder.close_path()
        self.path_builder.move_to((125, 300))
        self.assertEqual(self.path_builder.subpath_start_position, (125, 300))

    def test_current_position(self):
        """Test retrieving the current position."""
        self.path_builder.move_to((100, 150))
        self.assertEqual(self.path_builder.current_position, (100, 150))

    def test_current_position_after_move(self):
        """Test that the current position updates correctly after moving."""
        self.path_builder.move_to((100, 150))
        self.path_builder.line_to((200, 250))
        self.assertEqual(self.path_builder.current_position, (200, 250))

    def test_current_position_after_close(self):
        """Test that the current position updates correctly after closing the path."""
        self.path_builder.move_to((100, 150))
        self.path_builder.line_to((200, 250))
        self.path_builder.close_path()
        self.assertEqual(self.path_builder.current_position, (100, 150))


if __name__ == "__main__":
    unittest.main()
