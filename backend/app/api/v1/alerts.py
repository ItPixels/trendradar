"""Alerts API endpoints."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from typing import Optional
from app.database import get_db
from app.services.alert_service import AlertService

router = APIRouter()


class AlertCreate(BaseModel):
    name: str
    categories: list[str] = []
    keywords: list[str] = []
    excluded_keywords: list[str] = []
    min_score: float = 50
    min_velocity: float = 0
    min_sources: int = 2
    channels: list[str] = ["email"]
    webhook_url: Optional[str] = None
    cooldown_minutes: int = 60


class AlertUpdate(BaseModel):
    name: Optional[str] = None
    categories: Optional[list[str]] = None
    keywords: Optional[list[str]] = None
    excluded_keywords: Optional[list[str]] = None
    min_score: Optional[float] = None
    min_velocity: Optional[float] = None
    min_sources: Optional[int] = None
    channels: Optional[list[str]] = None
    webhook_url: Optional[str] = None
    cooldown_minutes: Optional[int] = None


# TODO: Replace with actual auth — for now use a hardcoded user_id
DEMO_USER_ID = "00000000-0000-0000-0000-000000000001"


@router.get("")
async def list_alerts(db: AsyncSession = Depends(get_db)):
    """Get all alerts for the current user."""
    service = AlertService(db)
    alerts = await service.get_user_alerts(DEMO_USER_ID)
    return {"items": alerts}


@router.post("")
async def create_alert(data: AlertCreate, db: AsyncSession = Depends(get_db)):
    """Create a new alert."""
    service = AlertService(db)
    alert = await service.create_alert(
        user_id=DEMO_USER_ID,
        **data.model_dump(),
    )
    return alert


@router.get("/{alert_id}")
async def get_alert(alert_id: str, db: AsyncSession = Depends(get_db)):
    """Get a single alert."""
    service = AlertService(db)
    alert = await service.get_alert(alert_id, DEMO_USER_ID)
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    return alert


@router.put("/{alert_id}")
async def update_alert(alert_id: str, data: AlertUpdate, db: AsyncSession = Depends(get_db)):
    """Update an alert."""
    service = AlertService(db)
    alert = await service.update_alert(
        alert_id, DEMO_USER_ID,
        **data.model_dump(exclude_unset=True),
    )
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    return alert


@router.delete("/{alert_id}")
async def delete_alert(alert_id: str, db: AsyncSession = Depends(get_db)):
    """Delete an alert."""
    service = AlertService(db)
    deleted = await service.delete_alert(alert_id, DEMO_USER_ID)
    if not deleted:
        raise HTTPException(status_code=404, detail="Alert not found")
    return {"status": "deleted"}


@router.post("/{alert_id}/toggle")
async def toggle_alert(alert_id: str, db: AsyncSession = Depends(get_db)):
    """Toggle alert active/inactive."""
    service = AlertService(db)
    alert = await service.toggle_alert(alert_id, DEMO_USER_ID)
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    return alert
