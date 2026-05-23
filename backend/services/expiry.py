DEFAULT_EXPIRY_DAYS = {
    "milk": 2,
    "eggs": 5,
    "tomato": 3,
    "cheese": 7,
    "butter": 10,
    "yogurt": 4,
    "chicken": 2,
    "fish": 1,
    "beef": 3,
    "juice": 7,
    "lettuce": 4,
    "carrot": 10,
    "apple": 14,
    "banana": 3,
}

FALLBACK_EXPIRY_DAYS = 5


def check_expiry(items: list) -> dict:
    """
    Returns estimated days until expiry for each detected item.

    Args:
        items: List of food item names (e.g. from detect_items()).

    Returns:
        Dict mapping each item to its estimated days until expiry.

    TODO: Replace static dictionary with a database lookup or
          AI-powered expiry estimation per item condition/brand.
    """

    # --- Dictionary lookup logic (replace with DB/AI call if needed) ---
    return {
        item: DEFAULT_EXPIRY_DAYS.get(item.lower(), FALLBACK_EXPIRY_DAYS)
        for item in items
    }
    # -------------------------------------------------------------------