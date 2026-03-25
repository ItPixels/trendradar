"""Trends API endpoints."""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from app.database import get_db
from app.services.trend_service import TrendService
from app.schemas.trend import TrendResponse, TrendListResponse

router = APIRouter()


@router.get("", response_model=TrendListResponse)
async def list_trends(
    category: Optional[str] = Query(None, description="Category slug filter"),
    status: Optional[str] = Query(None, description="Trend status filter"),
    min_score: float = Query(0, ge=0, le=100, description="Minimum trend score"),
    sort_by: str = Query("score", description="Sort by: score, velocity, newest, sources"),
    time_range: str = Query("24h", description="Time range: 1h, 6h, 24h, 7d, 30d"),
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db),
):
    """Get trending topics with filters and sorting."""
    service = TrendService(db)
    trends, total = await service.get_trends(
        category_slug=category,
        status=status,
        min_score=min_score,
        sort_by=sort_by,
        time_range=time_range,
        limit=limit,
        offset=offset,
    )

    return TrendListResponse(
        items=[TrendResponse.model_validate(t, from_attributes=True) for t in trends],
        total=total,
        limit=limit,
        offset=offset,
    )


@router.get("/{trend_id}")
async def get_trend(
    trend_id: str,
    db: AsyncSession = Depends(get_db),
):
    """Get a single trend by ID."""
    service = TrendService(db)
    trend = await service.get_trend_by_id(trend_id)

    if not trend:
        raise HTTPException(status_code=404, detail="Trend not found")

    # Increment view count
    await service.increment_view_count(trend_id)

    return TrendResponse.model_validate(trend, from_attributes=True)


@router.get("/slug/{slug}")
async def get_trend_by_slug(
    slug: str,
    db: AsyncSession = Depends(get_db),
):
    """Get a trend by its topic slug."""
    service = TrendService(db)
    trend = await service.get_trend_by_slug(slug)

    if not trend:
        raise HTTPException(status_code=404, detail="Trend not found")

    return TrendResponse.model_validate(trend, from_attributes=True)


@router.get("/categories/trending")
async def get_trending_categories(
    limit: int = Query(10, ge=1, le=20),
    db: AsyncSession = Depends(get_db),
):
    """Get categories with most active trends."""
    service = TrendService(db)
    return await service.get_trending_categories(limit)
