def secure_filename(filename: str, max_length: int = 255) -> str:
    """
    Make a filename safe for saving and ensure it does not exceed a certain length.

    Args:
        filename (str): The filename to make safe.
        max_length (int): The maximum length of the filename.

    Returns:
        str: The safe filename.
    """

    def is_allowed(c: str) -> bool:
        return c.isalnum() or c in "-_."

    safe_name = "".join(c if is_allowed(c) else "_" for c in filename).strip("_")
    return safe_name[:max_length]
