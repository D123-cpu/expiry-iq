# backend/models/schema.py

from pydantic import BaseModel


class RecipeItem(BaseModel):
    name:             str
    difficulty:       str
    time_minutes:     int
    reason:           str
    ingredients_used: list[str]


class ReminderItem(BaseModel):
    item:    str
    days:    int
    message: str


class Reminders(BaseModel):
    urgent: list[ReminderItem]
    soon:   list[ReminderItem]
    fresh:  list[ReminderItem]
    all:    list[ReminderItem]


class ScanResponse(BaseModel):
    scan_id:      str
    items:        list[str]
    expiry:       dict[str, int]
    priority:     dict
    reminders:    Reminders
    recipes:      list[RecipeItem]
    explanation:  str
    insights:     list[str]
    waste_saved:  str
    output_image: str