from fastapi import UploadFile
import shutil
import uuid
import os

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


def save_image(file: UploadFile) -> str:
    """
    Saves an uploaded image to the uploads folder with a unique filename.

    Args:
        file: FastAPI UploadFile object from the request.

    Returns:
        File path string where the image was saved.
    """

    extension = os.path.splitext(file.filename)[-1].lower()
    unique_filename = f"{uuid.uuid4().hex}{extension}"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return file_path