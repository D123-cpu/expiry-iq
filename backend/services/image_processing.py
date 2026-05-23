# backend/services/image_processing.py

import cv2
import os

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


def resize_image(image, size=(640, 640)):
    """Resize image to given size."""
    return cv2.resize(image, size)


def improve_brightness_contrast(image, alpha=1.2, beta=20):
    """
    Improve brightness and contrast.
    alpha: contrast control (1.0 = no change, >1 increases contrast)
    beta:  brightness control (0 = no change, >0 increases brightness)
    """
    return cv2.convertScaleAbs(image, alpha=alpha, beta=beta)


def apply_gaussian_blur(image, kernel_size=(3, 3)):
    """Apply Gaussian blur to reduce noise."""
    return cv2.GaussianBlur(image, kernel_size, 0)


def preprocess_image(image_path: str) -> str:
    """
    Preprocesses a fridge image for AI analysis.

    Steps:
        1. Read image from disk
        2. Resize to 640x640
        3. Improve brightness and contrast
        4. Apply Gaussian blur
        5. Save processed image as processed_<filename>

    Args:
        image_path: Path to the original uploaded image.

    Returns:
        Path to the processed image.
    """

    # Step 1: Read image
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"Could not read image at path: {image_path}")

    # Step 2: Resize
    image = resize_image(image)

    # Step 3: Improve brightness and contrast
    image = improve_brightness_contrast(image)

    # Step 4: Apply Gaussian blur
    image = apply_gaussian_blur(image)

    # Step 5: Save processed image
    filename = os.path.basename(image_path)
    processed_filename = f"processed_{filename}"
    processed_path = os.path.join(UPLOAD_DIR, processed_filename)
    cv2.imwrite(processed_path, image)

    return processed_path