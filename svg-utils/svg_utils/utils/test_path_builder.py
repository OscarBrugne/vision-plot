import pytest
from utils import PathBuilder


class TestPathBuilder:
    """Test for the PathBuilder class."""

    @pytest.fixture
    def path_builder(self) -> PathBuilder:
        """Fixture to create a PathBuilder instance."""
        return PathBuilder()

    def test_init(self, path_builder: PathBuilder):
        """Test initialization of PathBuilder."""
        assert path_builder.get_data() == ""

    @pytest.mark.parametrize(
        "position, relative, expected",
        [
            ((50, 100), False, "M 50 100"),
            ((50, 100), True, "m 50 100"),
            ((-50, -100), False, "M -50 -100"),
            ((-50, -100), True, "m -50 -100"),
        ],
    )
    def test_move_to(
        self,
        path_builder: PathBuilder,
        position: tuple[int, int],
        relative: bool,
        expected: str,
    ):
        """Test moving to a new position (absolute and relative)."""
        path_builder.move_to(position, relative)
        path_data = path_builder.get_data()
        assert expected in path_data

    @pytest.mark.parametrize(
        "position, relative, expected",
        [
            ((50, 100), False, "L 50 100"),
            ((50, 100), True, "l 50 100"),
            ((-50, -100), False, "L -50 -100"),
            ((-50, -100), True, "l -50 -100"),
        ],
    )
    def test_line_to(
        self,
        path_builder: PathBuilder,
        position: tuple[int, int],
        relative: bool,
        expected: str,
    ):
        """Test drawing a line to a new position (absolute and relative)."""
        path_builder.line_to(position, relative)
        path_data = path_builder.get_data()
        assert expected in path_data

    @pytest.mark.parametrize(
        "position, relative, expected",
        [
            (100, False, "H 100"),
            (100, True, "h 100"),
            (-100, False, "H -100"),
            (-100, True, "h -100"),
        ],
    )
    def test_horizontal_line_to(
        self, path_builder: PathBuilder, position: int, relative: bool, expected: str
    ):
        """Test drawing a horizontal line to a new position (absolute and relative)."""
        path_builder.horizontal_line_to(position, relative)
        path_data = path_builder.get_data()
        assert expected in path_data

    @pytest.mark.parametrize(
        "position, relative, expected",
        [
            (100, False, "V 100"),
            (100, True, "v 100"),
            (-100, False, "V -100"),
            (-100, True, "v -100"),
        ],
    )
    def test_vertical_line_to(
        self, path_builder: PathBuilder, position: int, relative: bool, expected: str
    ):
        """Test drawing a vertical line to a new position (absolute and relative)."""
        path_builder.vertical_line_to(position, relative)
        path_data = path_builder.get_data()
        assert expected in path_data

    @pytest.mark.parametrize(
        "control1, control2, end, relative, expected",
        [
            ((100, 150), (50, 250), (300, 350), False, "C 100 150 50 250 300 350"),
            ((100, 150), (50, 250), (300, 350), True, "c 100 150 50 250 300 350"),
            ((-100, -150), (50, 250), (300, 350), False, "C -100 -150 50 250 300 350"),
            ((-100, -150), (50, 250), (300, 350), True, "c -100 -150 50 250 300 350"),
        ],
    )
    def test_cubic_bezier_curve_to(
        self,
        path_builder: PathBuilder,
        control1: tuple[int, int],
        control2: tuple[int, int],
        end: tuple[int, int],
        relative: bool,
        expected: str,
    ):
        """Test drawing a cubic Bezier curve to a new position (absolute and relative)."""
        path_builder.cubic_bezier_curve_to(control1, control2, end, relative)
        path_data = path_builder.get_data()
        assert expected in path_data

    @pytest.mark.parametrize(
        "control2, end, relative, expected",
        [
            ((50, 250), (300, 350), False, "S 50 250 300 350"),
            ((50, 250), (300, 350), True, "s 50 250 300 350"),
            ((-50, -250), (300, 350), False, "S -50 -250 300 350"),
            ((-50, -250), (300, 350), True, "s -50 -250 300 350"),
        ],
    )
    def test_extend_cubic_bezier_curve_to(
        self,
        path_builder: PathBuilder,
        control2: tuple[int, int],
        end: tuple[int, int],
        relative: bool,
        expected: str,
    ):
        """Test extending a cubic Bezier curve to a new position (absolute and relative)."""
        path_builder.extend_cubic_bezier_curve_to(control2, end, relative)
        path_data = path_builder.get_data()
        assert expected in path_data

    @pytest.mark.parametrize(
        "control, end, relative, expected",
        [
            ((100, 150), (200, 250), False, "Q 100 150 200 250"),
            ((100, 150), (200, 250), True, "q 100 150 200 250"),
            ((-100, -150), (200, 250), False, "Q -100 -150 200 250"),
            ((-100, -150), (200, 250), True, "q -100 -150 200 250"),
        ],
    )
    def test_quadratic_bezier_curve_to(
        self,
        path_builder: PathBuilder,
        control: tuple[int, int],
        end: tuple[int, int],
        relative: bool,
        expected: str,
    ):
        """Test drawing a quadratic Bezier curve to a new position (absolute and relative)."""
        path_builder.quadratic_bezier_curve_to(control, end, relative)
        path_data = path_builder.get_data()
        assert expected in path_data

    @pytest.mark.parametrize(
        "end, relative, expected",
        [
            ((200, 250), False, "T 200 250"),
            ((200, 250), True, "t 200 250"),
            ((-200, -250), False, "T -200 -250"),
            ((-200, -250), True, "t -200 -250"),
        ],
    )
    def test_extend_quadratic_bezier_curve_to(
        self,
        path_builder: PathBuilder,
        end: tuple[int, int],
        relative: bool,
        expected: str,
    ):
        """Test extending a quadratic Bezier curve to a new position (absolute and relative)."""
        path_builder.extend_quadratic_bezier_curve_to(end, relative)
        path_data = path_builder.get_data()
        assert expected in path_data

    @pytest.mark.parametrize(
        "radii, rotation, large_arc, sweep, end, relative, expected",
        [
            ((50, 25), 20, True, False, (100, 150), False, "A 50 25 20 1 0 100 150"),
            ((50, 25), 20, True, False, (100, 150), True, "a 50 25 20 1 0 100 150"),
            (
                (-50, -25),
                20,
                False,
                True,
                (-100, -150),
                False,
                "A -50 -25 20 0 1 -100 -150",
            ),
            (
                (-50, -25),
                20,
                False,
                True,
                (-100, -150),
                True,
                "a -50 -25 20 0 1 -100 -150",
            ),
        ],
    )
    def test_arc_to(
        self,
        path_builder: PathBuilder,
        radii: int,
        rotation: int,
        large_arc: bool,
        sweep: bool,
        end: tuple[int, int],
        relative: bool,
        expected: str,
    ):
        """Test drawing an arc to a new position (absolute and relative)."""
        path_builder.arc_to(radii, rotation, large_arc, sweep, end, relative)
        path_data = path_builder.get_data()
        assert expected in path_data

    def test_close_path(self, path_builder: PathBuilder):
        """Test closing the path."""
        path_builder.close_path()
        path_data = path_builder.get_data()
        assert "Z" in path_data

    def test_clear(self, path_builder: PathBuilder):
        """Test clearing the path data."""
        path_builder.move_to((100, 100))
        path_builder.line_to((200, 100))
        path_builder.clear()
        path_data = path_builder.get_data()
        assert path_data == ""

    @pytest.mark.parametrize(
        "initial_position, expected",
        [
            ((100, 150), (100, 150)),
            ((-100, -150), (-100, -150)),
        ],
    )
    def test_subpath_start_position(
        self,
        path_builder: PathBuilder,
        initial_position: tuple[int, int],
        expected: tuple[int, int],
    ):
        """Test retrieving the start position of the current sub-path."""
        path_builder.move_to(initial_position)
        assert path_builder.subpath_start_position == expected

    def test_subpath_start_position_after_move(
        self,
        path_builder: PathBuilder,
    ):
        """Test that the subpath start position updates correctly after moving."""
        path_builder.move_to((100, 150))
        path_builder.line_to((200, 250))
        assert path_builder.subpath_start_position == (100, 150)

    def test_subpath_start_position_after_new_subpath(self, path_builder: PathBuilder):
        """Test that the subpath start position updates correctly after creating a new sub-path."""
        path_builder.move_to((100, 150))
        path_builder.line_to((200, 250))
        path_builder.close_path()
        path_builder.move_to((125, 300))
        assert path_builder.subpath_start_position == (125, 300)

    @pytest.mark.parametrize(
        "initial_position, expected",
        [
            ((100, 150), (100, 150)),
            ((-100, -150), (-100, -150)),
        ],
    )
    def test_current_position(
        self,
        path_builder: PathBuilder,
        initial_position: tuple[int, int],
        expected: tuple[int, int],
    ):
        """Test retrieving the current position."""
        path_builder.move_to(initial_position)
        assert path_builder.current_position == expected

    def test_current_position_after_close(self, path_builder: PathBuilder):
        """Test that the current position updates correctly after closing the path."""
        path_builder.move_to((100, 150))
        path_builder.line_to((200, 250))
        path_builder.close_path()
        assert path_builder.current_position == (100, 150)
