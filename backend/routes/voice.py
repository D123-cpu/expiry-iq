# backend/routes/voice.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.recipe import generate_recipes

router = APIRouter()


class VoiceInput(BaseModel):
    text: str


def extract_items_from_text(text: str) -> list:
    """
    Extracts food item names from a voice transcript.

    Example:
        "I have eggs, tomato and cheese" -> ["eggs", "tomato", "cheese"]
    """

    # Common filler words to remove
    fillers = {
        "i", "have", "got", "some", "a", "an", "the", "and", "or",
        "also", "there", "is", "are", "my", "fridge", "ingredients",
        "with", "plus", "few", "lot", "of", "in"
    }

    # Clean and split text
    text  = text.lower().strip()
    words = text.replace(",", " ").replace(".", " ").split()
    items = [word for word in words if word not in fillers and len(word) > 2]

    return list(dict.fromkeys(items))  # remove duplicates


@router.post("/voice-recipes")
def voice_recipes(payload: VoiceInput):
    """
    Accepts voice transcript, extracts ingredients,
    and returns structured recipe suggestions.
    """

    if not payload.text or not payload.text.strip():
        raise HTTPException(status_code=400, detail="Voice input text is empty.")

    try:
        items       = extract_items_from_text(payload.text)
        recipe_data = generate_recipes(items)
        return {
            "transcript": payload.text,
            "items":      items,
            "recipes":    recipe_data["recipes"],
            "explanation": recipe_data["explanation"],
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate recipes: {str(e)}")