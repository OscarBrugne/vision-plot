from dataclasses import dataclass
from pathlib import Path

import cv2
from bottle import Bottle, FormsDict, request, response
from services import camera_service

PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"


@dataclass
class Camera:
    id: int
    source: int
    video_capture: cv2.VideoCapture
    id_capture: int = 0


app = Bottle()

id_counter: int = 0
cameras: dict[int, Camera] = {}


@app.post("/camera")
def open_camera():
    global id_counter

    response.content_type = "application/json"

    if request.content_type != "application/x-www-form-urlencoded":
        response.status = 415
        return {
            "error": "Unsupported Media Type",
            "message": "The content type must be 'application/x-www-form-urlencoded'.",
        }

    form: FormsDict = request.forms
    camera_source = form.get("source", 0)

    try:
        camera = camera_service.open_camera(camera_source)
    except camera_service.CameraOpenException:
        response.status = 500
        return {
            "error": "Camera Error",
            "message": "Failed to open the camera.",
        }

    id_counter += 1
    while id_counter in cameras:
        id_counter += 1

    cameras[id_counter] = Camera(
        id=id_counter, source=camera_source, video_capture=camera
    )

    response.status = 201
    return {
        "message": "Camera opened successfully.",
        "camera_id": id_counter,
        "camera_source": camera_source,
    }


@app.get("/camera/<camera_id>")
def get_camera(camera_id: str):
    response.content_type = "application/json"

    try:
        camera_id = int(camera_id)
    except ValueError:
        response.status = 400
        return {
            "error": "Invalid request data",
            "message": "The camera ID must be an integer.",
        }

    camera = cameras.get(camera_id)
    if not camera:
        response.status = 404
        return {
            "error": "Camera not found",
            "message": f"The camera with ID '{camera_id}' was not found.",
        }

    response.status = 200
    return {
        "camera_id": camera.id,
        "camera_source": camera.source,
    }


@app.delete("/camera/<camera_id>")
def close_camera(camera_id: str):
    response.content_type = "application/json"

    try:
        camera_id = int(camera_id)
    except ValueError:
        response.status = 400
        return {
            "error": "Invalid request data",
            "message": "The camera ID must be an integer.",
        }

    camera = cameras.get(camera_id)
    if not camera:
        response.status = 404
        return {
            "error": "Camera not found",
            "message": f"The camera with ID '{camera_id}' was not found.",
        }

    camera_service.close_camera(camera.video_capture)
    del cameras[camera_id]

    response.status = 200
    return {"message": f"Camera with ID '{camera_id}' closed successfully."}


@app.post("/camera/<camera_id>/capture")
def capture_image(camera_id: str):
    response.content_type = "application/json"

    try:
        camera_id = int(camera_id)
    except ValueError:
        response.status = 400
        return {
            "error": "Invalid request data",
            "message": "The camera ID must be an integer.",
        }

    camera = cameras.get(camera_id)
    if not camera:
        response.status = 404
        return {
            "error": "Camera not found",
            "message": f"The camera with ID '{camera_id}' was not found.",
        }

    try:
        image = camera_service.capture_image(camera.video_capture)
    except camera_service.CameraCaptureException:
        response.status = 500
        return {
            "error": "Camera Error",
            "message": f"Failed to capture an image from the camera with ID '{camera_id}'.",
            "camera_id": camera_id,
        }

    camera.id_capture += 1
    capture_filename = f"capture_{camera_id}_{camera.id_capture}.jpg"
    capture_filepath = (
        DATA_DIR / "camera" / str(camera_id) / "captures" / capture_filename
    )
    capture_filepath.parent.mkdir(parents=True, exist_ok=True)

    try:
        cv2.imwrite(str(capture_filepath), image)
    except cv2.error:
        response.status = 500
        return {
            "error": "Image Error",
            "message": "Failed to save the captured image.",
            "camera_id": camera_id,
        }

    response.status = 201
    return {
        "message": "Image captured successfully.",
        "camera_id": camera_id,
        "capture_id": camera.id_capture,
        "capture_filename": capture_filename,
        "capture_filepath": str(capture_filepath),
        "capture_url": f"/data/camera/{camera_id}/captures/{capture_filename}",
    }
