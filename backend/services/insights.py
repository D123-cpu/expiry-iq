# backend/services/insights.py


def generate_insights(items: list, expiry: dict, recipes: list) -> list:
    """
    Generates human-readable insight messages based on scan results.

    Args:
        items:   List of detected food items.
        expiry:  Dict mapping item names to days until expiry.
        recipes: List of suggested recipe names.

    Returns:
        List of insight message strings.
    """

    insights = []

    # Expiry-based insights
    for item, days in expiry.items():
        if days == 0:
            insights.append(f"⚠️ Use {item} today — it's expiring!")
        elif days == 1:
            insights.append(f"🔴 {item.capitalize()} expires tomorrow.")
        elif days <= 3:
            insights.append(f"🟡 {item.capitalize()} is expiring soon ({days} days left).")
        else:
            insights.append(f"✅ {item.capitalize()} is fresh ({days} days left).")

    # Recipe insights
    if len(recipes) == 0:
        insights.append("😔 No recipes found for the detected items.")
    elif len(recipes) == 1:
        insights.append(f"🍽️ You have ingredients for 1 recipe: {recipes[0]}.")
    else:
        insights.append(f"🍽️ You have ingredients for {len(recipes)} recipes.")

    # Item count insight
    if len(items) == 0:
        insights.append("📷 No items detected. Try a clearer image.")
    elif len(items) >= 5:
        insights.append(f"🛒 Great stock! {len(items)} items detected in your fridge.")

    return insights