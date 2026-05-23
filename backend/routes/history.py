# backend/routes/history.py

from fastapi import APIRouter, HTTPException
from services.db import scans_collection
from bson import ObjectId

router = APIRouter()


def serialize_scan(scan: dict) -> dict:
    """Convert MongoDB document to JSON-serializable dict."""
    scan["id"] = str(scan.pop("_id"))
    if "timestamp" in scan:
        scan["timestamp"] = scan["timestamp"].isoformat()
    return scan


@router.get("/history")
def get_history(limit: int = 20):
    """Returns the most recent scan history from MongoDB."""
    try:
        scans = list(
            scans_collection.find()
            .sort("timestamp", -1)
            .limit(limit)
        )
        return {"scans": [serialize_scan(s) for s in scans]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch history: {str(e)}")