import cv2
import numpy as np


def detect_markers(
    frame: cv2.typing.MatLike,
    dict_type: int,
) -> dict[int, np.ndarray[tuple[4, 2], np.float64]]:
    """
    Detect ArUco markers in the given frame.

    Args:
        frame (cv2.typing.MatLike): The input frame.
        dict_type (int): The type of ArUco dictionary to use.

    Returns:
        dict[int, np.ndarray]: A dictionary mapping marker IDs to their corners.
    """
    aruco_dict = cv2.aruco.getPredefinedDictionary(dict_type)
    parameters = cv2.aruco.DetectorParameters()

    corners, ids, rejected = cv2.aruco.detectMarkers(
        frame,
        aruco_dict,
        parameters=parameters,
    )

    return {marker_id: corner for marker_id, corner in zip(ids.flatten(), corners)}


def apply_homography(
    frame: cv2.typing.MatLike,
    homography: np.ndarray[tuple[3, 3], np.float64],
) -> cv2.typing.MatLike:
    """
    Apply a homography transformation to the given frame.

    Args:
        frame (cv2.typing.MatLike): The input frame.
        homography (np.ndarray): The homography matrix.

    Returns:
        cv2.typing.MatLike: The transformed frame.
    """
    height, width = frame.shape[:2]
    transformed_frame = cv2.warpPerspective(frame, homography, (width, height))
    return transformed_frame


def calculate_homography(
    src_markers: dict[int, np.ndarray[tuple[4, 2], np.float64]],
    dst_markers: dict[int, np.ndarray[tuple[4, 2], np.float64]],
):
    src_points = []
    dst_points = []

    for marker_id, src_corners in src_markers.items():
        if marker_id not in dst_markers:
            continue

        dst_corners = dst_markers[marker_id]
        src_points.extend(src_corners)
        dst_points.extend(dst_corners)

    src_points = np.array(src_points, dtype=np.float32)
    dst_points = np.array(dst_points, dtype=np.float32)

    homography_src_to_dst, mask = cv2.findHomography(src_points, dst_points)
    return homography_src_to_dst


def calculate_homography_correction(
    detected_markers: dict[int, np.ndarray[tuple[4, 2], np.float64]],
    real_markers: dict[int, np.ndarray[tuple[4, 2], np.float64]],
    expected_projected_markers: dict[int, np.ndarray[tuple[4, 2], np.float64]],
) -> np.ndarray[tuple[3, 3], np.float64]:
    """
    Calculate the homography correction between detected markers and real/projected markers.

    Args:
        detected_markers (dict[int, np.ndarray]): Detected markers.
        real_markers (dict[int, np.ndarray]): Real markers.
        expected_projected_markers (dict[int, np.ndarray]): Expected projected markers (in the same coordinate system as real markers).

    Returns:
        np.ndarray: The homography correction matrix for the projector.
    """
    # Calculate homography matrices
    homography_real_to_camera = calculate_homography(real_markers, detected_markers)
    homography_projector_detected_to_camera = calculate_homography(
        expected_projected_markers, detected_markers
    )
    # The expected projected markers are already in the same coordinate system as the real markers
    homography_projector_corrected_to_real = np.eye(3, dtype=np.float64)

    if homography_real_to_camera is None:
        raise ValueError("Error: Could not compute the homography from real to camera.")
    if homography_projector_detected_to_camera is None:
        raise ValueError(
            "Error: Could not compute the homography from projector detected to camera."
        )
    if homography_projector_corrected_to_real is None:
        raise ValueError(
            "Error: Could not compute the homography from projector corrected to real."
        )

    # Calculate the homography correction matrix
    homography_camera_to_projector_detected = np.linalg.inv(
        homography_projector_detected_to_camera
    )
    homography_projector_corrected_to_camera = (
        homography_real_to_camera @ homography_projector_corrected_to_real
    )
    homography_projector_detected_to_projector_corrected = (
        homography_camera_to_projector_detected
        @ homography_projector_corrected_to_camera
    )

    homography_correction = homography_projector_detected_to_projector_corrected
    return homography_correction
