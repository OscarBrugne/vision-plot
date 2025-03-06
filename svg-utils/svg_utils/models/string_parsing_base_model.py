import json
from types import UnionType
from typing import Any, Union, get_args, get_origin

from pydantic import BaseModel, ValidationInfo, field_validator


class StringParsingBaseModel(BaseModel):
    """Base model with automatic parsing of string inputs."""

    @field_validator("*", mode="before")
    @classmethod
    def parse_string_field(cls, value: str, info: ValidationInfo) -> Any:
        """Parse a string field into the correct type.

        Args:
            value (str): The string value to be parsed.
            info (ValidationInfo): The validation information which includes the field name.

        Raises:
            ValueError: If the string value cannot be parsed.

        Returns:
            Any: The parsed value.
        """

        field_type = cls.model_fields[info.field_name].annotation
        is_string = cls._is_string_like(field_type)
        if is_string:
            return cls._remove_quotes(value)

        try:
            return json.loads(value)
        except json.JSONDecodeError as e:
            raise ValueError(
                f"Invalid JSON value: '{value}' is not a valid JSON format."
            ) from e

    @staticmethod
    def _is_string_like(field_type: Any) -> bool:
        """Check if the given field type is a string, a subtype of string, or a Union with a string type.
        The type can come from built-in types, types module, or typing module.

        Args:
            field_type (Any): The type to check.

        Returns:
            bool: True if the type is a string-like type, False otherwise.
        """
        # Check if the field type is a string or a subtype of string
        if isinstance(field_type, type) and issubclass(field_type, str):
            return True

        # Check if the field type is a Union with a string type
        origin = get_origin(field_type)
        if origin in (Union, UnionType):
            for arg in get_args(field_type):
                if isinstance(arg, type) and issubclass(arg, str):
                    return True

        return False

    @staticmethod
    def _remove_quotes(value: str) -> str:
        """Remove quotes from a string value.
        A quote is either a single quote (`'`) or a double quote (`"`).

        Args:
            value (str): The string value to remove quotes from.

        Returns:
            str: The string value without quotes.
        """
        if (value.startswith('"') and value.endswith('"')) or (
            value.startswith("'") and value.endswith("'")
        ):
            return value[1:-1]
        return value
