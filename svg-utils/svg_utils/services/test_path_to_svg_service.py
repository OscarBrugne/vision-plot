from typing import List, Optional, Tuple

import pytest
from svg_utils.services.path_to_svg_service import PathToSVGService


class TestPathToSVGService:
    """Test for the PathToSVGService class."""

    @pytest.fixture
    def path_to_svg_service(self) -> PathToSVGService:
        """Fixture to create a PathToSVGService instance."""
        return PathToSVGService()

    @pytest.mark.parametrize(
        "points, size, viewbox, is_closed_path, stroke, stroke_width, expected_d",
        [
            (
                [(300, 200), (231, 295), (119, 259), (119, 141), (231, 105)],
                (400, 400),
                (0, 0, 400, 400),
                True,
                "red",
                2,
                "M 300 200 L 231 295 L 119 259 L 119 141 L 231 105 Z",
            ),
        ],
    )
    def test_generate_line_path_svg(
        self,
        path_to_svg_service: PathToSVGService,
        points: List[Tuple[int, int]],
        size: Tuple[int, int],
        viewbox: Optional[Tuple[int, int, int, int]],
        is_closed_path: bool,
        stroke: str,
        stroke_width: int,
        expected_d: str,
    ) -> None:
        """Test the generate_line_path_svg method."""
        svg = path_to_svg_service.generate_line_path_svg(
            points, size, viewbox, is_closed_path, stroke, stroke_width
        ).replace(",", " ")

        assert "<svg" in svg
        assert "</svg>" in svg
        assert f'd="{expected_d}"' in svg
        assert f'width="{size[0]}"' in svg
        assert f'height="{size[1]}"' in svg
        assert f'viewBox="{" ".join(map(str, viewbox))}"' in svg
        assert 'fill="none"' in svg
        assert f'stroke="{stroke}"' in svg
        assert f'stroke-width="{stroke_width}"' in svg

    @pytest.mark.parametrize(
        "paths, size, viewbox, is_closed_path, stroke, stroke_width, expected_d_list",
        [
            (
                [
                    [(200, 150), (100, 325), (300, 325)],
                    [(50, 50), (50, 350), (350, 350), (350, 50)],
                    [(300, 200), (231, 295), (119, 259), (119, 141), (231, 105)],
                ],
                (400, 400),
                (0, 0, 400, 400),
                True,
                "red",
                2,
                (
                    "M 200 150 L 100 325 L 300 325 Z",
                    "M 50 50 L 50 350 L 350 350 L 350 50 Z",
                    "M 300 200 L 231 295 L 119 259 L 119 141 L 231 105 Z",
                ),
            ),
        ],
    )
    def test_generate_multiple_line_paths_svg(
        self,
        path_to_svg_service: PathToSVGService,
        paths: List[List[Tuple[int, int]]],
        size: Tuple[int, int],
        viewbox: Optional[Tuple[int, int, int, int]],
        is_closed_path: bool,
        stroke: str,
        stroke_width: int,
        expected_d_list: Tuple[str, ...],
    ) -> None:
        """Test the generate_paths_svg method."""
        svg = path_to_svg_service.generate_multiple_line_paths_svg(
            paths, size, viewbox, is_closed_path, stroke, stroke_width
        ).replace(",", " ")

        assert "<svg" in svg
        assert "</svg>" in svg
        for expected_d in expected_d_list:
            assert f'd="{expected_d}"' in svg
        assert f'width="{size[0]}"' in svg
        assert f'height="{size[1]}"' in svg
        assert f'viewBox="{" ".join(map(str, viewbox))}"' in svg
        assert 'fill="none"' in svg
        assert f'stroke="{stroke}"' in svg
        assert f'stroke-width="{stroke_width}"' in svg
