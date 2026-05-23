# backend/services/reminder.py


# Action verbs per food category for natural-sounding messages
CATEGORY_ACTIONS = {
    "dairy":     "Use",
    "meat":      "Cook",
    "protein":   "Use",
    "fruit":     "Eat",
    "vegetable": "Cook",
    "beverage":  "Drink",
    "bakery":    "Eat",
    "prepared":  "Finish",
    "unknown":   "Use",
}

# Category mapping for common items
ITEM_CATEGORIES = {
    "milk":       "dairy",
    "cheese":     "dairy",
    "butter":     "dairy",
    "yogurt":     "dairy",
    "cream":      "dairy",
    "chicken":    "meat",
    "beef":       "meat",
    "fish":       "meat",
    "egg":        "protein",
    "eggs":       "protein",
    "apple":      "fruit",
    "banana":     "fruit",
    "orange":     "fruit",
    "grape":      "fruit",
    "strawberry": "fruit",
    "watermelon": "fruit",
    "tomato":     "vegetable",
    "lettuce":    "vegetable",
    "carrot":     "vegetable",
    "cucumber":   "vegetable",
    "spinach":    "vegetable",
    "onion":      "vegetable",
    "potato":     "vegetable",
    "pepper":     "vegetable",
    "broccoli":   "vegetable",
    "bottle":     "beverage",
    "juice":      "beverage",
    "bread":      "bakery",
    "cake":       "bakery",
    "sandwich":   "prepared",
    "hot dog":    "prepared",
    "pizza":      "prepared",
}


def get_action(item: str) -> str:
    """Returns appropriate action verb for an item."""
    category = ITEM_CATEGORIES.get(item.lower(), "unknown")
    return CATEGORY_ACTIONS.get(category, "Use")


def generate_reminder_message(item: str, days: int) -> str:
    """
    Generates a single reminder message for an item.

    Args:
        item: Food item name.
        days: Days until expiry.

    Returns:
        Human-readable reminder string.
    """

    action = get_action(item)
    name   = item.capitalize()

    if days == 0:
        return f"⚠️ {action} {name} immediately — expires today!"
    elif days == 1:
        return f"🔴 {action} {name} today — expires tomorrow."
    elif days <= 3:
        return f"🟡 {action} {name} soon — only {days} days left."
    elif days <= 5:
        return f"🟡 Cook or consume {name} within {days} days."
    else:
        return f"🟢 {name} is fresh — {days} days remaining."


def generate_reminders(expiry: dict) -> dict:
    """
    Generates reminder alerts for all detected items.

    Args:
        expiry: Dict mapping item names to days until expiry.

    Returns:
        Dict with:
            - urgent:   list of urgent reminder messages (<=2 days)
            - soon:     list of soon reminder messages (<=5 days)
            - fresh:    list of fresh item messages (>5 days)
            - all:      all reminders combined sorted by urgency
    """

    urgent = []
    soon   = []
    fresh  = []

    # Sort items by days ascending (most urgent first)
    sorted_items = sorted(expiry.items(), key=lambda x: x[1])

    for item, days in sorted_items:
        message = generate_reminder_message(item, days)

        if days <= 2:
            urgent.append({"item": item, "days": days, "message": message})
        elif days <= 5:
            soon.append({"item": item, "days": days, "message": message})
        else:
            fresh.append({"item": item, "days": days, "message": message})

    return {
        "urgent": urgent,
        "soon":   soon,
        "fresh":  fresh,
        "all":    urgent + soon + fresh,
    }