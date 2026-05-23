# backend/routes/analytics.py

from fastapi import APIRouter, HTTPException
from services.analytics import generate_weekly_report

router = APIRouter()


@router.get("/weekly-report")
def weekly_report():
    """
    Returns weekly analytics report with waste tracking and savings trend.
    """
    try:
        report = generate_weekly_report()
        return report
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate report: {str(e)}")