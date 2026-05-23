# backend/services/waste_calculator.py

# Approximate prices of common items in INR
ITEM_PRICES = {
    # Dairy
    "milk":       50,
    "cheese":     80,
    "butter":     55,
    "yogurt":     40,
    "cream":      60,

    # Meat & Protein
    "chicken":    150,
    "beef":       200,
    "fish":       120,
    "egg":        6,
    "eggs":       30,

    # Fruits
    "apple":      30,
    "banana":     20,
    "orange":     25,
    "grape":      80,
    "strawberry": 60,
    "watermelon": 40,

    # Vegetables
    "tomato":     20,
    "lettuce":    25,
    "carrot":     15,
    "cucumber":   15,
    "spinach":    30,
    "onion":      10,
    "potato":     15,
    "pepper":     25,
    "broccoli":   40,

    # Beverages
    "bottle":     40,
    "juice":      60,

    # Bakery
    "bread":      35,
    "cake":       120,

    # Prepared
    "sandwich":   60,
    "hot dog":    80,
    "pizza":      150,
}

DEFAULT_PRICE     = 30   # fallback for unknown items in INR
WASTE_THRESHOLD   = 5    # days — items at risk of being wasted
SAVED_PERCENTAGE  = 0.85 # 85% of at-risk value is saved by using recipes


def get_item_price(item: str) -> int:
    """Returns price of an item in INR."""
    return ITEM_PRICES.get(item.lower().strip(), DEFAULT_PRICE)


def calculate_waste(items: list, expiry: dict) -> dict:
    """
    Calculates potential waste value and saved amount after recipe suggestion.

    Args:
        items:  List of detected food item names.
        expiry: Dict mapping item names to days until expiry.

    Returns:
        Dict with:
            - waste_risk:    total INR value of items at risk of being wasted
            - saved_value:   INR value saved by using recipes
            - at_risk_items: list of dicts with item, days, price
            - safe_items:    list of dicts with item, days, price
            - waste_risk_str:  human-readable waste risk string
            - saved_value_str: human-readable saved value string
    """

    at_risk_items = []
    safe_items    = []
    waste_risk    = 0

    for item in items:
        days  = expiry.get(item, 999)
        price = get_item_price(item)

        if days <= WASTE_THRESHOLD:
            waste_risk += price
            at_risk_items.append({
                "item":  item,
                "days":  days,
                "price": price,
            })
        else:
            safe_items.append({
                "item":  item,
                "days":  days,
                "price": price,
            })

    # Amount saved by using recipes on at-risk items
    saved_value = round(waste_risk * SAVED_PERCENTAGE)

    # Sort at-risk by most urgent first
    at_risk_items = sorted(at_risk_items, key=lambda x: x["days"])

    return {
        "waste_risk":      waste_risk,
        "saved_value":     saved_value,
        "at_risk_items":   at_risk_items,
        "safe_items":      safe_items,
        "waste_risk_str":  f"₹{waste_risk} worth of food at risk of being wasted",
        "saved_value_str": f"₹{saved_value} saved by using suggested recipes",
    }