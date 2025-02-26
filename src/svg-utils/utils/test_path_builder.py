import unittest
from path_builder import PathBuilder


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
