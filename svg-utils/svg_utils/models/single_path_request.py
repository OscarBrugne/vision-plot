from typing import List, Optional

from .string_parsing_base_model import StringParsingBaseModel


class SinglePathRequest(StringParsingBaseModel):
    """Request model for a single path request."""

    points: List[List[int]]
    size: List[int]
    viewbox: Optional[List[int]] = None
    is_closed_path: bool = False
    stroke: str = "black"
    stroke_width: int = 1
