"""Alerts API endpoints — manages user alert rules."""
import logging
import traceback
import uuid
from datetime import datetime, timezone
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from sqlalchemy import select, desc
from app.database import _create_engine

logger = logging.getLogger(__name__)
router = APIRouter()

# TODO: Replace with actual auth
DEMO_USER_ID = "00000000-0000-0000-0000-000000000001"


class AlertCreate(BaseModel):
    name: str
    categories: list[str] = []
    keywords: list[str] = []
    excluded_keywords: list[str] = []
    min_score: float = 50
    min_velocity: float = 0
    min_sources: int = 2
    channels: list[str] = ["email"]
    cooldown_minutes: int = 60


class AlertUpdate(BaseModel):
    name: Optional[str] = None
    categories: Optional[list[str]] = None
    keywords: Optional[list[str]] = None
    min_score: Optional[float] = None
    min_sources: Optional[int] = None
    channels: Optional[list[str]] = None


@router.get("")
async def list_alerts():
    """Get all alerts for the current user."""
    engine = _create_engine()
    session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    try:
        async with session_maker() as db:
            from app.models.alert import Alert
            result = await db.execute(
                select(Alert)
                .where(Alert.user_id == DEMO_USER_ID)
                .where(Alert.deleted_at.is_(None))
                .order_by(desc(Alert.created_at))
            )
            alerts = result.scalars().all()
            return {"items": [_alert_to_dict(a) for a in alerts]}
    except Exception as e:
        logger.error(f"Alerts list error: {e}\n{traceback.format_exc()}")
        return {"items": [], "error": str(e)}
    finally:
        await engine.dispose()


@router.post("")
async def create_alert(data: AlertCreate):
    """Create a new alert."""
    engine = _create_engine()
    session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    try:
        async with session_maker() as db:
            from app.models.alert import Alert
            alert = Alert(
                user_id=DEMO_USER_ID,
                name=data.name,
                categories=data.categories,
                keywords=data.keywords,
                excluded_keywords=data.excluded_keywords,
                min_score=data.min_score,
                min_velocity=data.min_velocity,
                min_sources=data.min_sources,
                channels=data.channels,
                cooldown_minutes=data.cooldown_minutes,
                is_active=True,
            )
            db.add(alert)
            await db.commit()
            await db.refresh(alert)
            return _alert_to_dict(alert)
    except Exception as e:
        logger.error(f"Create alert error: {e}\n{traceback.format_exc()}")
        return {"error": str(e)}
    finally:
        await engine.dispose()


@router.delete("/{alert_id}")
async def delete_alert(alert_id: str):
    """Delete an alert (soft delete)."""
    engine = _create_engine()
    session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    try:
        async with session_maker() as db:
            from app.models.alert import Alert
            result = await db.execute(
                select(Alert)
                .where(Alert.id == alert_id)
                .where(Alert.user_id == DEMO_USER_ID)
                .where(Alert.deleted_at.is_(None))
            )
            alert = result.scalar_one_or_none()
            if not alert:
                raise HTTPException(status_code=404, detail="Alert not found")
            alert.deleted_at = datetime.now(timezone.utc)
            await db.commit()
            return {"status": "deleted"}
    finally:
        await engine.dispose()


@router.post("/{alert_id}/toggle")
async def toggle_alert(alert_id: str):
    """Toggle alert active/inactive."""
    engine = _create_engine()
    session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    try:
        async with session_maker() as db:
            from app.models.alert import Alert
            result = await db.execute(
                select(Alert)
                .where(Alert.id == alert_id)
                .where(Alert.user_id == DEMO_USER_ID)
                .where(Alert.deleted_at.is_(None))
            )
            alert = result.scalar_one_or_none()
            if not alert:
                raise HTTPException(status_code=404, detail="Alert not found")
            alert.is_active = not alert.is_active
            await db.commit()
            return _alert_to_dict(alert)
    finally:
        await engine.dispose()


def _alert_to_dict(alert) -> dict:
    return {
        "id": str(alert.id),
        "name": alert.name,
        "categories": alert.categories or [],
        "keywords": alert.keywords or [],
        "excluded_keywords": getattr(alert, "excluded_keywords", []) or [],
        "min_score": alert.min_score,
        "min_sources": alert.min_sources,
        "channels": alert.channels or [],
        "is_active": alert.is_active,
        "trigger_count": getattr(alert, "trigger_count", 0) or 0,
        "last_triggered_at": alert.last_triggered_at.isoformat() if getattr(alert, "last_triggered_at", None) else None,
        "created_at": alert.created_at.isoformat() if alert.created_at else None,
    }
