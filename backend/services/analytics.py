# backend/services/analytics.py

from datetime import datetime, timezone, timedelta
from collections import Counter
from services.db import scans_collection


def get_scans_last_7_days() -> list:
    """
    Fetches all scans from the last 7 days from MongoDB.

    Returns:
        List of scan documents.
    """
    seven_days_ago = datetime.now(timezone.utc) - timedelta(days=7)
    scans = list(scans_collection.find({"timestamp": {"$gte": seven_days_ago}}))
    return scans


def track_items_over_time(scans: list) -> dict:
    """
    Tracks how many items were scanned per day over the last 7 days.

    Args:
        scans: List of scan documents.

    Returns:
        Dict mapping date string to item count.
    """
    daily_counts = {}

    for scan in scans:
        date_str = scan["timestamp"].strftime("%Y-%m-%d")
        items    = scan.get("items", [])
        daily_counts[date_str] = daily_counts.get(date_str, 0) + len(items)

    return dict(sorted(daily_counts.items()))


def track_wasted_items(scans: list, waste_threshold: int = 2) -> dict:
    """
    Tracks items that were likely wasted (expiry <= threshold days).

    Args:
        scans:           List of scan documents.
        waste_threshold: Days threshold to consider an item at risk.

    Returns:
        Dict with wasted item counts and total waste value.
    """
    wasted_counter = Counter()
    total_waste    = 0

    for scan in scans:
        expiry = scan.get("expiry", {})
        for item, days in expiry.items():
            if days <= waste_threshold:
                wasted_counter[item] += 1

        # Accumulate waste value if stored
        waste_data = scan.get("waste_saved", "")
        if isinstance(waste_data, str) and "₹" in waste_data:
            try:
                value = int("".join(filter(str.isdigit, waste_data.split("₹")[1].split()[0])))
                total_waste += value
            except (ValueError, IndexError):
                pass

    return {
        "wasted_items":     dict(wasted_counter.most_common()),
        "most_wasted_item": wasted_counter.most_common(1)[0][0] if wasted_counter else None,
        "total_waste_risk": total_waste,
    }


def calculate_savings_trend(scans: list) -> dict:
    """
    Calculates savings trend over the last 7 days.

    Args:
        scans: List of scan documents.

    Returns:
        Dict mapping date to savings amount.
    """
    daily_savings = {}

    for scan in scans:
        date_str   = scan["timestamp"].strftime("%Y-%m-%d")
        waste_data = scan.get("waste_saved", "")

        savings = 0
        if isinstance(waste_data, str) and "₹" in waste_data:
            try:
                savings = int("".join(filter(str.isdigit, waste_data.split("₹")[1].split()[0])))
            except (ValueError, IndexError):
                savings = 0

        daily_savings[date_str] = daily_savings.get(date_str, 0) + savings

    return dict(sorted(daily_savings.items()))


def generate_weekly_report() -> dict:
    """
    Generates a full weekly analytics report.

    Returns:
        Dict with:
            - period:             report date range
            - total_scans:        number of scans in last 7 days
            - total_items_scanned: total items detected
            - items_over_time:    daily item scan counts
            - wasted_items:       items most at risk of waste
            - most_wasted_item:   single most wasted item
            - total_waste_risk:   total INR value at risk
            - savings_trend:      daily savings amounts
            - total_savings:      total INR saved this week
            - summary:            human-readable summary string
    """

    scans = get_scans_last_7_days()

    if not scans:
        return {
            "period":              _get_period_string(),
            "total_scans":         0,
            "total_items_scanned": 0,
            "items_over_time":     {},
            "wasted_items":        {},
            "most_wasted_item":    None,
            "total_waste_risk":    0,
            "savings_trend":       {},
            "total_savings":       0,
            "summary":             "No scans recorded in the last 7 days.",
        }

    items_over_time = track_items_over_time(scans)
    waste_data      = track_wasted_items(scans)
    savings_trend   = calculate_savings_trend(scans)

    total_items_scanned = sum(items_over_time.values())
    total_savings       = sum(savings_trend.values())

    summary = (
        f"This week you scanned {total_items_scanned} items across {len(scans)} scans. "
        f"{'Most at-risk item: ' + waste_data['most_wasted_item'] + '.' if waste_data['most_wasted_item'] else 'No items wasted.'} "
        f"Total savings: ₹{total_savings}."
    )

    return {
        "period":              _get_period_string(),
        "total_scans":         len(scans),
        "total_items_scanned": total_items_scanned,
        "items_over_time":     items_over_time,
        "wasted_items":        waste_data["wasted_items"],
        "most_wasted_item":    waste_data["most_wasted_item"],
        "total_waste_risk":    waste_data["total_waste_risk"],
        "savings_trend":       savings_trend,
        "total_savings":       total_savings,
        "summary":             summary,
    }


def _get_period_string() -> str:
    """Returns a human-readable date range string for the last 7 days."""
    end   = datetime.now(timezone.utc)
    start = end - timedelta(days=7)
    return f"{start.strftime('%b %d')} – {end.strftime('%b %d, %Y')}"