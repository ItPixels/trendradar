"""Content briefs API endpoints."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from typing import Optional
from app.database import get_db
from app.services.brief_service import BriefService
from app.services.trend_service import TrendService

router = APIRouter()

DEMO_USER_ID = "00000000-0000-0000-0000-000000000001"


class BriefRequest(BaseModel):
    format: str = "article"
    target_audience: str = "content creators and marketers"


@router.post("/trend/{trend_id}")
async def generate_brief(
    trend_id: str,
    data: BriefRequest,
    db: AsyncSession = Depends(get_db),
):
    """Generate a content brief for a trend."""
    # Get trend data
    trend_service = TrendService(db)
    trend = await trend_service.get_trend_by_id(trend_id)
    if not trend:
        raise HTTPException(status_code=404, detail="Trend not found")

    brief_service = BriefService(db)
    brief = await brief_service.generate_brief(
        trend_id=trend_id,
        user_id=DEMO_USER_ID,
        trend_data={
            "topic": trend.topic,
            "trend_score": trend.trend_score,
            "active_sources": trend.active_sources or [],
            "status": trend.status,
        },
        format=data.format,
        target_audience=data.target_audience,
    )

    if not brief:
        raise HTTPException(status_code=500, detail="Failed to generate brief")

    return brief


@router.get("/trend/{trend_id}")
async def get_briefs_for_trend(
    trend_id: str,
    db: AsyncSession = Depends(get_db),
):
    """Get all briefs for a trend."""
    service = BriefService(db)
    briefs = await service.get_briefs_for_trend(trend_id, DEMO_USER_ID)
    return {"items": briefs}
