import cv2
import numpy as np


def load_image(image_path: str) -> np.ndarray:
    """
    Load an image from the specified path.

    Args:
        image_path (str): The path to the image file.

    Returns:
        np.ndarray: The loaded image.
    """
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"Could not load image from path: {image_path}")
    return image


def save_image(image: np.ndarray, output_path: str) -> None:
    """
    Save an image to the specified path.

    Args:
        image (np.ndarray): The image to save.
        output_path (str): The path where the image will be saved.
    """
    success = cv2.imwrite(output_path, image)
    if not success:
        raise ValueError(f"Could not save image to path: {output_path}")
