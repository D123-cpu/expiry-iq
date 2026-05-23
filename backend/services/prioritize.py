# backend/services/prioritize.py


def prioritize_items(expiry_dict: dict) -> dict:
    """
    Sorts fridge items into priority groups based on expiry days.

    Args:
        expiry_dict: Dict mapping item names to days until expiry.
                     e.g. {"milk": 2, "eggs": 5, "cheese": 7}

    Returns:
        Structured dict with urgent, medium, and safe categories.
    """

    urgent = {}
    medium = {}
    safe   = {}

    for item, days in expiry_dict.items():
        if days <= 2:
            urgent[item] = days
        elif days <= 5:
            medium[item] = days
        else:
            safe[item] = days

    # Sort each group by days ascending (most urgent first)
    urgent = dict(sorted(urgent.items(), key=lambda x: x[1]))
    medium = dict(sorted(medium.items(), key=lambda x: x[1]))
    safe   = dict(sorted(safe.items(),   key=lambda x: x[1]))

    return {
        "urgent": {
            "label":       "🔴 Use Immediately",
            "items":       urgent,
            "count":       len(urgent),
        },
        "medium": {
            "label":       "🟡 Use Soon",
            "items":       medium,
            "count":       len(medium),
        },
        "safe": {
            "label":       "🟢 Still Fresh",
            "items":       safe,
            "count":       len(safe),
        },
    }