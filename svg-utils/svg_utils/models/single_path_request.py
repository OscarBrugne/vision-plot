from .string_parsing_base_model import StringParsingBaseModel


class SinglePathRequest(StringParsingBaseModel):
    """Request model for a single path request."""

    points: list[list[int]]
    size: list[int]
    viewbox: list[int] | None = None
    is_closed_path: bool = False
    stroke: str = "black"
    stroke_width: int = 1
