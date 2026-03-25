"""Search API endpoints."""
import logging
import traceback
from fastapi import APIRouter, Query
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from sqlalchemy import select, or_, desc
from app.database import _create_engine
from app.models.trend import Trend

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("")
async def search_trends(
    q: str = Query(..., min_length=2, description="Search query"),
    limit: int = Query(20, ge=1, le=50),
):
    """Search trends by topic, description, tags."""
    engine = _create_engine()
    session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    try:
        async with session_maker() as db:
            pattern = f"%{q}%"
            result = await db.execute(
                select(Trend)
                .where(Trend.deleted_at.is_(None))
                .where(
                    or_(
                        Trend.topic.ilike(pattern),
                        Trend.description.ilike(pattern),
                        Trend.topic_slug.ilike(pattern),
                    )
                )
                .order_by(desc(Trend.trend_score))
                .limit(limit)
            )
            trends = result.scalars().all()

            items = []
            for t in trends:
                items.append({
                    "id": str(t.id),
                    "topic": t.topic,
                    "topic_slug": t.topic_slug,
                    "description": t.description,
                    "trend_score": t.trend_score,
                    "velocity_24h": t.velocity_24h,
                    "source_count": t.source_count,
                    "active_sources": t.active_sources or [],
                    "signal_count_24h": t.signal_count_24h,
                    "status": t.status,
                    "is_viral": t.is_viral,
                    "is_breaking": t.is_breaking,
                    "category_id": str(t.category_id) if t.category_id else None,
                    "first_seen_at": t.first_seen_at.isoformat() if t.first_seen_at else None,
                    "created_at": t.created_at.isoformat() if t.created_at else None,
                    "updated_at": t.updated_at.isoformat() if t.updated_at else None,
                    "view_count": t.view_count or 0,
                    "tags": t.tags or [],
                    "acceleration": t.acceleration or 0,
                })

            return {"items": items, "query": q, "total": len(items)}
    except Exception as e:
        logger.error(f"Search error: {e}\n{traceback.format_exc()}")
        return {"items": [], "query": q, "total": 0, "error": str(e)}
    finally:
        await engine.dispose()
