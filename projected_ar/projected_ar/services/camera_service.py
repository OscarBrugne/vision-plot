import cv2


class CameraOpenException(Exception):
    """Exception raised when the camera fails to open."""

    def __init__(self, message: str = "Failed to open camera."):
        super().__init__(message)


class CameraCaptureException(Exception):
    """Exception raised when the camera fails to capture an image."""

    def __init__(self, message: str = "Failed to capture image."):
        super().__init__(message)


def open_camera(camera_source: int | str = 0) -> cv2.VideoCapture:
    """
    Opens a camera with the given source (ID or URL).

    Args:
        camera_source (int | str, optional): The source of the camera to use. Defaults to 0.

    Raises:
        CameraOpenException: If the camera fails to open.

    Returns:
        cv2.VideoCapture: The camera object.
    """
    camera = cv2.VideoCapture(camera_source)
    if not camera.isOpened():
        raise CameraOpenException()
    return camera


def capture_image(
    camera: cv2.VideoCapture,
) -> cv2.typing.MatLike:
    """
    Captures an image from the camera.

    Args:
        camera (cv2.VideoCapture): The camera object.

    Raises:
        CameraCaptureException: If the camera fails to capture an image.

    Returns:
        cv2.typing.MatLike: The captured image.
    """
    ret, frame = camera.read()
    if not ret:
        raise CameraCaptureException()
    return frame


def close_camera(camera: cv2.VideoCapture):
    """
    Closes the camera.

    Args:
        camera (cv2.VideoCapture): The camera object.
    """
    camera.release()
