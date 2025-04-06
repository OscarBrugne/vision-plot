import json
from pathlib import Path
from typing import Any

from bottle import Bottle, FormsDict, request, response
import numpy as np
from services import aruco_dict_service, image_service, projector_calibration_service

PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"

app = Bottle()


@app.post("/detect-markers")
def detect_markers() -> dict[str, Any]:
    """
    Handle a POST request to detect ArUco markers in an image.

    Expects a form-urlencoded payload with the following fields:
    - capture_filepath: Path to the image file.
    - aruco_dict_type: Type of ArUco dictionary to use for detection.

    Returns:
        dict[str, Any]: A JSON response with the detected markers or an error message.
    """
    response.content_type = "application/json"

    if request.content_type != "application/x-www-form-urlencoded":
        response.status = 415
        return {
            "error": "Unsupported Media Type",
            "message": "The content type must be 'application/x-www-form-urlencoded'.",
        }

    form: FormsDict = request.forms
    capture_filepath = form.get("capture_filepath")
    aruco_dict_type = form.get("aruco_dict_type")

    # Check if the required fields are present
    if not capture_filepath:
        response.status = 400
        return {
            "error": "Bad Request",
            "message": "The 'capture_filepath' field is required.",
        }
    if not aruco_dict_type:
        response.status = 400
        return {
            "error": "Bad Request",
            "message": "The 'aruco_dict_type' field is required.",
        }

    # Check if the file exists
    capture_filepath = Path(capture_filepath)
    if not capture_filepath.is_file():
        response.status = 404
        return {
            "error": "Not Found",
            "message": f"The file '{capture_filepath}' does not exist.",
        }

    # Check if the file is a valid image
    try:
        image = image_service.load_image(str(capture_filepath))
    except ValueError:
        response.status = 415
        return {
            "error": "Unsupported Media Type",
            "message": f"The file '{capture_filepath}' is not a valid image.",
        }

    # Check if the aruco_dict_type is valid
    try:
        aruco_dict = aruco_dict_service.get_aruco_dict(aruco_dict_type)
    except ValueError as e:
        response.status = 400
        return {
            "error": "Bad Request",
            "message": f"The 'aruco_dict_type' is invalid: {aruco_dict_type}.",
            "valid_types": list(aruco_dict_service.ARUCO_DICTS.keys()),
        }

    # Process the image and detect markers
    try:
        detected_markers = projector_calibration_service.detect_markers(
            image, aruco_dict
        )
    except Exception as e:
        response.status = 500
        return {
            "error": "Internal Server Error",
            "message": str(e),
        }

    response.status = 200
    return {
        "detected_markers": detected_markers,
    }


@app.post("/calculate-homography-correction")
def calculate_homography_correction() -> dict[str, Any]:
    """
    Handle a POST request to calculate the homography correction for the projector.

    Expects a form-urlencoded payload with the following fields:
    - detected_markers: A JSON string containing the detected markers from the camera.
    - real_markers: A JSON string containing the real markers.
    - projected_markers: A JSON string containing the expected projected markers.
    Expects the JSON strings to be in the format:
    {
        "marker_id": [
            [x1, y1],
            [x2, y2],
            [x3, y3],
            [x4, y4]
        ]
    }

    Returns:
        dict[str, Any]: A JSON response with the calculated homography matrix or an error message.
    """
    response.content_type = "application/json"

    if request.content_type != "application/x-www-form-urlencoded":
        response.status = 415
        return {
            "error": "Unsupported Media Type",
            "message": "The content type must be 'application/x-www-form-urlencoded'.",
        }

    form: FormsDict = request.forms
    detected_markers_string = form.get("detected_markers")
    real_markers_string = form.get("real_markers")
    expected_projected_markers_string = form.get("projected_markers")

    # Check if the required fields are present
    if not detected_markers_string:
        response.status = 400
        return {
            "error": "Bad Request",
            "message": "The 'detected_markers' field is required.",
        }
    if not real_markers_string:
        response.status = 400
        return {
            "error": "Bad Request",
            "message": "The 'real_markers' field is required.",
        }
    if not expected_projected_markers_string:
        response.status = 400
        return {
            "error": "Bad Request",
            "message": "The 'projected_markers' field is required.",
        }

    # Convert the JSON strings to dictionaries
    try:
        detected_markers_list = json.loads(detected_markers_string)
        real_markers_list = json.loads(real_markers_string)
        expected_projected_markers_list = json.loads(expected_projected_markers_string)
    except json.JSONDecodeError:
        response.status = 400
        return {
            "error": "Bad Request",
            "message": "Invalid JSON format in the input fields.",
        }

    # Convert the lists to numpy arrays
    try:
        detected_markers = {
            int(marker_id): np.array(corners, dtype=np.float64)
            for marker_id, corners in detected_markers_list.items()
        }
        real_markers = {
            int(marker_id): np.array(corners, dtype=np.float64)
            for marker_id, corners in real_markers_list.items()
        }
        expected_projected_markers = {
            int(marker_id): np.array(corners, dtype=np.float64)
            for marker_id, corners in expected_projected_markers_list.items()
        }
    except ValueError:
        response.status = 400
        return {
            "error": "Bad Request",
            "message": "Invalid data format in the input fields.",
        }

    # Calculate the homography correction
    try:
        homography_correction: np.ndarray[tuple[3, 3], np.float64] = (
            projector_calibration_service.calculate_homography(
                detected_markers,
                real_markers,
                expected_projected_markers,
            )
        )
    except Exception as e:
        response.status = 500
        return {
            "error": "Internal Server Error",
            "message": str(e),
        }

    # Convert the homography matrix to a list for JSON serialization
    homography_correction_list = homography_correction.tolist()
    response.status = 200
    return {
        "homography_correction": homography_correction_list,
    }


@app.post("/apply-homography")
def apply_homography() -> dict[str, Any]:
    """
    Handle a POST request to apply a homography  to an image.

    Expects a form-urlencoded payload with the following fields:
    - image_filepath: Path to the image file.
    - homography: A JSON string containing the homography matrix.
    Expects the JSON string to be in the format:
    [
        [h11, h12, h13],
        [h21, h22, h23],
        [h31, h32, h33]
    ]

    Returns:
        dict[str, Any]: A JSON response with the corrected image or an error message.
    """
    response.content_type = "application/json"

    if request.content_type != "application/x-www-form-urlencoded":
        response.status = 415
        return {
            "error": "Unsupported Media Type",
            "message": "The content type must be 'application/x-www-form-urlencoded'.",
        }

    form: FormsDict = request.forms
    image_filepath_string = form.get("image_filepath")
    homography_string = form.get("homography")

    # Check if the required fields are present
    if not image_filepath:
        response.status = 400
        return {
            "error": "Bad Request",
            "message": "The 'image_filepath' field is required.",
        }
    if not homography_string:
        response.status = 400
        return {
            "error": "Bad Request",
            "message": "The 'homography' field is required.",
        }

    # Check if the file exists
    image_filepath = Path(image_filepath_string)
    if not image_filepath.is_file():
        response.status = 404
        return {
            "error": "Not Found",
            "message": f"The file '{image_filepath}' does not exist.",
        }

    # Check if the file is a valid image
    try:
        image = image_service.load_image(str(image_filepath))
    except ValueError:
        response.status = 415
        return {
            "error": "Unsupported Media Type",
            "message": f"The file '{image_filepath}' is not a valid image.",
        }

    # Convert the JSON string to a list
    try:
        homography = json.loads(homography_string)
        homography = np.array(homography, dtype=np.float64)
    except json.JSONDecodeError:
        response.status = 400
        return {
            "error": "Bad Request",
            "message": "Invalid JSON format in the 'homography' field.",
        }

    # Check if the homography matrix is valid
    if homography.shape != (3, 3):
        response.status = 400
        return {
            "error": "Bad Request",
            "message": "The 'homography' matrix must be a 3x3 matrix.",
        }

    # Apply the homography to the image
    try:
        corrected_image = projector_calibration_service.apply_homography(
            image, homography
        )
    except Exception as e:
        response.status = 500
        return {
            "error": "Internal Server Error",
            "message": str(e),
        }

    # Save the corrected image to a temporary file
    output_filepath = image_filepath.with_name(
        f"{image_filepath.stem}_corrected{image_filepath.suffix}"
    )
    try:
        image_service.save_image(corrected_image, str(output_filepath))
    except ValueError:
        response.status = 500
        return {
            "error": "Internal Server Error",
            "message": f"Failed to save the corrected image to '{output_filepath}'.",
        }

    response.status = 201
    return {
        "message": "Homography applied successfully.",
        "corrected_image_filepath": str(output_filepath),
        "corrected_image_url": str(output_filepath.relative_to(PROJECT_ROOT)),
    }
