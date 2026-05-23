# backend/services/expiry_intelligence.py

import random

# Base expiry data: (min_days, max_days, category)
ITEM_EXPIRY_DATA = {
    # Dairy
    "milk":         (1,  4,  "dairy"),
    "cheese":       (5,  14, "dairy"),
    "butter":       (7,  21, "dairy"),
    "yogurt":       (3,  7,  "dairy"),
    "cream":        (2,  5,  "dairy"),

    # Meat & Protein
    "chicken":      (1,  3,  "meat"),
    "beef":         (2,  4,  "meat"),
    "fish":         (1,  2,  "meat"),
    "egg":          (7,  21, "protein"),
    "eggs":         (7,  21, "protein"),

    # Fruits
    "apple":        (7,  21, "fruit"),
    "banana":       (2,  5,  "fruit"),
    "orange":       (7,  14, "fruit"),
    "grape":        (3,  7,  "fruit"),
    "strawberry":   (2,  4,  "fruit"),
    "watermelon":   (3,  7,  "fruit"),

    # Vegetables
    "tomato":       (2,  5,  "vegetable"),
    "lettuce":      (3,  7,  "vegetable"),
    "carrot":       (7,  21, "vegetable"),
    "cucumber":     (3,  7,  "vegetable"),
    "spinach":      (2,  5,  "vegetable"),
    "onion":        (14, 30, "vegetable"),
    "potato":       (14, 30, "vegetable"),
    "pepper":       (5,  10, "vegetable"),
    "broccoli":     (3,  7,  "vegetable"),

    # Beverages
    "bottle":       (3,  7,  "beverage"),
    "juice":        (3,  7,  "beverage"),

    # Bakery
    "bread":        (2,  5,  "bakery"),
    "cake":         (2,  4,  "bakery"),

    # Other
    "sandwich":     (1,  2,  "prepared"),
    "hot dog":      (3,  7,  "prepared"),
    "pizza":        (1,  3,  "prepared"),
}

CATEGORY_CONFIDENCE = {
    "dairy":     0.90,
    "meat":      0.92,
    "protein":   0.85,
    "fruit":     0.80,
    "vegetable": 0.78,
    "beverage":  0.70,
    "bakery":    0.82,
    "prepared":  0.88,
    "unknown":   0.50,
}

DEFAULT_EXPIRY = (3, 7)


def calculate_urgency_score(days: int) -> int:
    """
    Returns urgency score from 1 (safe) to 10 (expires today).

    Args:
        days: Days until expiry.

    Returns:
        Integer urgency score between 1 and 10.
    """
    if days <= 0:  return 10
    if days == 1:  return 9
    if days == 2:  return 8
    if days == 3:  return 7
    if days <= 5:  return 5
    if days <= 7:  return 4
    if days <= 14: return 2
    return 1


def get_expiry_info(item: str) -> dict:
    """
    Returns dynamic expiry info for a single item.

    Args:
        item: Food item name.

    Returns:
        Dict with expiry_days, confidence, urgency_score, category.
    """

    key      = item.lower().strip()
    data     = ITEM_EXPIRY_DATA.get(key, None)

    if data:
        min_days, max_days, category = data
        # Simulate real-world variance within range
        expiry_days = random.randint(min_days, max_days)
        confidence  = round(CATEGORY_CONFIDENCE.get(category, 0.50), 2)
    else:
        expiry_days = random.randint(*DEFAULT_EXPIRY)
        category    = "unknown"
        confidence  = 0.50

    urgency_score = calculate_urgency_score(expiry_days)

    return {
        "expiry_days":    expiry_days,
        "confidence":     confidence,
        "urgency_score":  urgency_score,
        "category":       category,
    }


def check_expiry_intelligence(items: list) -> dict:
    """
    Runs expiry intelligence on all detected items.

    Args:
        items: List of detected food item names.

    Returns:
        Dict mapping each item to its expiry intelligence data.
    """

    result = {}
    for item in items:
        result[item] = get_expiry_info(item)

    return result