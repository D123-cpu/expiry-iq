# backend/services/vision.py

from ultralytics import YOLO
import cv2
import os

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Items to ignore — non-food objects YOLO commonly detects
IGNORE_ITEMS = {
    "refrigerator", "oven", "microwave", "sink", "bowl",
    "cup", "knife", "fork", "spoon", "scissors", "vase",
    "clock", "chair", "table", "person", "cell phone",
}

# Load pretrained model once at module level
model = YOLO("yolov8n.pt")


def detect_items(image_path: str) -> dict:
    """
    Detects food objects in a fridge image using YOLOv8.
    Filters out non-food items and saves annotated image.

    Args:
        image_path: Path to the preprocessed image file.

    Returns:
        Dict with:
            - items: list of unique detected food item names
            - output_image_path: path to the annotated image
    """

    results = model(image_path)

    # Extract detected class names
    detected_items = []
    for result in results:
        for cls_id in result.boxes.cls:
            class_name = model.names[int(cls_id)]
            detected_items.append(class_name)

    # Remove duplicates and filter out non-food items
    unique_items = [
        item for item in list(dict.fromkeys(detected_items))
        if item.lower() not in IGNORE_ITEMS
    ]

    # Save annotated image with bounding boxes
    filename        = os.path.basename(image_path)
    output_filename = f"annotated_{filename}"
    output_path     = os.path.join(UPLOAD_DIR, output_filename)

    for result in results:
        annotated_frame = result.plot()
        cv2.imwrite(output_path, annotated_frame)
        break

    return {
        "items":             unique_items,
        "output_image_path": output_path,
    }