import json
from typing import Any

from pydantic import BaseModel, field_validator


class JsonParsingBaseModel(BaseModel):
    """Base model with automatic JSON string parsing for all fields."""

    @field_validator("*", mode="before")
    @classmethod
    def parse_json_field(cls, value: str) -> Any:
        """Parse a JSON string into a Python object."""
        try:
            return json.loads(value)
        except json.JSONDecodeError as e:
            raise ValueError(
                f"Invalid JSON value: '{value}' is not a valid JSON format."
            ) from e
