# backend/services/recipe.py

from groq import Groq
from config import GROQ_API_KEY
import json

client = Groq(api_key=GROQ_API_KEY)


def generate_recipes(items: list) -> dict:
    """
    Generates structured recipes using Groq with difficulty,
    time required, and reason for suggestion.

    Args:
        items: List of detected food item names.

    Returns:
        Dict with:
            - recipes: list of structured recipe dicts
            - explanation: overall explanation string
    """

    ingredients = ", ".join(items) if items else "basic ingredients"

    prompt = (
        f"Given these fridge ingredients: {ingredients}.\n"
        "Suggest 3 simple recipes. For each recipe return a JSON array.\n"
        "Each recipe must have these exact fields:\n"
        "- name: recipe name\n"
        "- difficulty: Easy / Medium / Hard\n"
        "- time_minutes: estimated cooking time as integer\n"
        "- reason: one sentence why this recipe is suggested\n"
        "- ingredients_used: list of ingredients from the given list used in this recipe\n\n"
        "Reply with ONLY a valid JSON array, no extra text, no markdown, no backticks.\n"
        "Example format:\n"
        "[\n"
        "  {\n"
        '    "name": "Banana Smoothie",\n'
        '    "difficulty": "Easy",\n'
        '    "time_minutes": 5,\n'
        '    "reason": "Quick way to use bananas before they overripen.",\n'
        '    "ingredients_used": ["banana", "milk"]\n'
        "  }\n"
        "]"
    )

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You are a helpful kitchen assistant. Always reply with valid JSON only."},
            {"role": "user",   "content": prompt},
        ],
        max_tokens=500,
        temperature=0.7,
    )

    raw = response.choices[0].message.content.strip()

    # Parse JSON response
    try:
        # Strip markdown code blocks if model adds them
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
        recipes_list = json.loads(raw)
    except json.JSONDecodeError:
        # Fallback if parsing fails
        recipes_list = [
            {
                "name":              "Simple Stir Fry",
                "difficulty":        "Easy",
                "time_minutes":      15,
                "reason":            "Quick meal using available ingredients.",
                "ingredients_used":  items[:3] if items else [],
            }
        ]

    return {
        "recipes":     recipes_list,
        "explanation": f"These recipes are suggested based on your available ingredients: {ingredients}.",
    }