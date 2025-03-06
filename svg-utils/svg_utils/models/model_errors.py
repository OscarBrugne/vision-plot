from pydantic import ValidationError


def generate_validation_error_message(e: ValidationError) -> str:
    """
    Generate a human-readable error message from a Pydantic ValidationError.

    Args:
        e (ValidationError): The Pydantic ValidationError object.

    Returns:
        str: A human-readable error message.
    """
    errors = e.errors()
    error_msgs = []
    for error in errors:
        key = error["loc"][0]
        value = error["input"]
        msg = error["msg"]
        error_msgs.append(f"The parameter '{key}:{value}' is invalid: {msg}")
    error_message = "\n ".join(error_msgs)

    return error_message
