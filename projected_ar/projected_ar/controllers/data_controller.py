import os
from pathlib import Path

from bottle import Bottle, FileUpload, request, response, static_file
from services import data_service

PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
ALLOWED_CONTENT_TYPES = {
    "image/jpeg",
    "image/png",
    "image/svg+xml",
    "text/plain, application/json",
}
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".svg", ".txt", ".json"}
MAX_FILE_SIZE_B = 1024 * 1024 * 10  # 10 MB
MAX_FILENAME_LENGTH = 255

app = Bottle()


@app.get("/data/<filepath:path>")
def serve_data(filepath):
    full_filepath: Path = DATA_DIR / filepath

    if not full_filepath.exists() or not full_filepath.is_file():
        response.status = 404
        response.content_type = "application/json"
        return {
            "error": "File not found",
            "message": f"The file '{filepath}' was not found.",
        }

    return static_file(filepath, root=DATA_DIR)


@app.post("/data/<dirpath:path>")
def upload_data(dirpath):
    response.content_type = "application/json"

    if not request.content_type.startswith("multipart/form-data"):
        response.status = 415
        return {
            "error": "Unsupported Media Type",
            "message": "The content type must be 'multipart/form-data'.",
        }

    file: FileUpload = request.files.get("file")
    if not file:
        response.status = 400
        return {
            "error": "Invalid request data",
            "message": "The parameter 'file' is required.",
        }

    full_dirpath: Path = DATA_DIR / dirpath
    if not full_dirpath.exists():
        full_dirpath.mkdir(parents=True, exist_ok=True)

    if not file.filename:
        response.status = 400
        return {
            "error": "Invalid request data",
            "message": "The filename is required.",
        }

    file_extension = Path(file.filename).suffix.lower()
    if file_extension not in ALLOWED_EXTENSIONS:
        response.status = 400
        return {
            "error": "Invalid file extension",
            "message": f"The file extension '{file_extension}' is not allowed.",
            "allowed_extensions": list(ALLOWED_EXTENSIONS),
        }

    if file.content_type not in ALLOWED_CONTENT_TYPES:
        response.status = 400
        return {
            "error": "Invalid content type",
            "message": f"The content type '{file.content_type}' is not allowed.",
            "allowed_content_types": list(ALLOWED_CONTENT_TYPES),
        }

    if file.content_length > MAX_FILE_SIZE_B:
        response.status = 400
        return {
            "error": "File too large",
            "message": f"The file is too large. The maximum size allowed is {MAX_FILE_SIZE_B / 1024 / 1024} MB.",
            "max_size": f"{MAX_FILE_SIZE_B} bytes",
        }

    secure_filename = data_service.secure_filename(file.filename, MAX_FILENAME_LENGTH)
    full_filepath: Path = full_dirpath / secure_filename

    try:
        file.save(str(full_filepath))
    except Exception as e:
        response.status = 500
        return {
            "error": "Internal Server Error",
            "message": f"Failed to save the file: {str(e)}",
        }

    response.status = 201
    return {
        "message": "File uploaded successfully.",
        "filepath": str(full_filepath),
        "url": f"/data/{dirpath}/{secure_filename}",
    }
