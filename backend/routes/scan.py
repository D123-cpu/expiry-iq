# backend/routes/scan.py

from fastapi import APIRouter, UploadFile, File, HTTPException
from services.image_processing import preprocess_image
from services.vision import detect_items
from services.expiry_intelligence import check_expiry_intelligence
from services.recipe import generate_recipes
from services.insights import generate_insights
from services.waste_calculator import calculate_waste
from services.prioritize import prioritize_items
from services.reminder import generate_reminders
from services.db import save_scan
from utils.image_utils import save_image
from models.schema import ScanResponse

router = APIRouter()


@router.post("/scan-fridge", response_model=ScanResponse)
async def scan_fridge(file: UploadFile = File(...)):

    # Validate file type
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Uploaded file must be an image.")

    try:
        # Step 1: Save uploaded image
        file_path = save_image(file)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save image: {str(e)}")

    try:
        # Step 2: Preprocess image
        processed_path = preprocess_image(file_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to preprocess image: {str(e)}")

    try:
        # Step 3: Detect items from processed image
        detection    = detect_items(processed_path)
        items        = detection["items"]
        output_image = detection["output_image_path"]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to detect items: {str(e)}")

    try:
        # Step 4a: Run expiry intelligence on detected items
        expiry_data = check_expiry_intelligence(items)
        expiry      = {item: data["expiry_days"] for item, data in expiry_data.items()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to check expiry: {str(e)}")

    try:
        # Step 4b: Prioritize items by expiry
        priority = prioritize_items(expiry)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to prioritize items: {str(e)}")

    try:
        # Step 4c: Generate reminders
        reminders = generate_reminders(expiry)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate reminders: {str(e)}")

    try:
        # Step 4d: Generate structured recipes and explanation
        recipe_data  = generate_recipes(items)
        recipes      = recipe_data["recipes"]
        explanation  = recipe_data["explanation"]
        recipe_names = [r["name"] if isinstance(r, dict) else r for r in recipes]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate recipes: {str(e)}")

    try:
        # Step 4e: Generate insights using recipe names
        insights = generate_insights(items, expiry, recipe_names)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate insights: {str(e)}")

    try:
        # Step 4f: Calculate waste
        waste_data  = calculate_waste(items, expiry)
        waste_saved = waste_data["saved_value_str"]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to calculate waste: {str(e)}")

    try:
        # Step 5: Save scan result to MongoDB
        scan_id = save_scan({
            "items":        items,
            "expiry":       expiry,
            "expiry_data":  expiry_data,
            "priority":     priority,
            "reminders":    reminders,
            "recipes":      recipes,
            "explanation":  explanation,
            "insights":     insights,
            "waste_saved":  waste_saved,
            "output_image": output_image,
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save scan: {str(e)}")

    # Step 6: Return validated Pydantic response
    return ScanResponse(
        scan_id=scan_id,
        items=items,
        expiry=expiry,
        priority=priority,
        reminders=reminders,
        recipes=recipes,
        explanation=explanation,
        insights=insights,
        waste_saved=waste_saved,
        output_image=output_image,
    )