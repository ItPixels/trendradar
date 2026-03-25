"""Search API endpoints."""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.services.search_service import SearchService

router = APIRouter()


@router.get("")
async def search_trends(
    q: str = Query(..., min_length=2, description="Search query"),
    limit: int = Query(20, ge=1, le=50),
    db: AsyncSession = Depends(get_db),
):
    """Search trends by topic, description, tags."""
    service = SearchService(db)
    results = await service.search_trends(q, limit)
    return {"items": results, "query": q, "total": len(results)}
