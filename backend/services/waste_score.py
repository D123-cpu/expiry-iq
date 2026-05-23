# backend/services/waste_score.py

# Approximate price of common items in INR
ITEM_PRICES = {
    "milk":     50,
    "eggs":     30,
    "tomato":   20,
    "cheese":   80,
    "butter":   55,
    "yogurt":   40,
    "chicken":  150,
    "fish":     120,
    "beef":     200,
    "juice":    60,
    "lettuce":  25,
    "carrot":   15,
    "apple":    30,
    "banana":   20,
    "bread":    35,
    "cucumber": 15,
    "onion":    10,
    "potato":   15,
    "pepper":   25,
    "spinach":  30,
}

EXPIRY_THRESHOLD  = 5   # days — items expiring within this are "at risk"
DEFAULT_ITEM_PRICE = 30  # fallback price for unknown items


def calculate_waste_score(items: list, expiry: dict) -> dict:
    """
    Calculates potential waste saved by using items expiring soon.

    Args:
        items:  List of detected food item names.
        expiry: Dict mapping item names to days until expiry.

    Returns:
        Dict with:
            - waste_saved: human-readable savings string (e.g. "₹70 saved by using items")
            - expiring_items: list of items that are at risk
            - total_value: total INR value of at-risk items
    """

    expiring_items = []
    total_value    = 0

    for item in items:
        days = expiry.get(item, None)
        if days is not None and days <= EXPIRY_THRESHOLD:
            price = ITEM_PRICES.get(item.lower(), DEFAULT_ITEM_PRICE)
            total_value += price
            expiring_items.append(item)

    if total_value > 0:
        waste_saved = f"₹{total_value} saved by using items"
    else:
        waste_saved = "No items expiring soon — great job!"

    return {
        "waste_saved":    waste_saved,
        "expiring_items": expiring_items,
        "total_value":    total_value,
    }