"""Categories API endpoints."""
import logging
import traceback
from fastapi import APIRouter, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from sqlalchemy import select, func
from app.database import _create_engine
from app.models.category import Category
from app.models.trend import Trend

logger = logging.getLogger(__name__)
router = APIRouter()


def _category_to_dict(cat, trend_count: int = 0) -> dict:
    return {
        "id": str(cat.id),
        "name": cat.name,
        "slug": cat.slug,
        "description": cat.description,
        "icon": getattr(cat, "icon", None),
        "color": getattr(cat, "color", "#6366f1"),
        "sort_order": cat.sort_order,
        "trend_count": trend_count,
    }


@router.get("")
async def list_categories():
    """Get all active categories with trend counts."""
    engine = _create_engine()
    session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    try:
        async with session_maker() as db:
            # Get categories with trend counts
            result = await db.execute(
                select(Category, func.count(Trend.id).label("trend_count"))
                .outerjoin(Trend, (Trend.category_id == Category.id) & (Trend.deleted_at.is_(None)))
                .where(Category.is_active == True)
                .group_by(Category.id)
                .order_by(Category.sort_order)
            )
            rows = result.all()
            return {"items": [_category_to_dict(cat, count) for cat, count in rows]}
    except Exception as e:
        logger.error(f"Categories error: {e}\n{traceback.format_exc()}")
        return {"items": [], "error": str(e)}
    finally:
        await engine.dispose()


@router.get("/{slug}")
async def get_category(slug: str):
    """Get a category by slug."""
    engine = _create_engine()
    session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    try:
        async with session_maker() as db:
            result = await db.execute(
                select(Category, func.count(Trend.id).label("trend_count"))
                .outerjoin(Trend, (Trend.category_id == Category.id) & (Trend.deleted_at.is_(None)))
                .where(Category.slug == slug)
                .where(Category.is_active == True)
                .group_by(Category.id)
            )
            row = result.first()
            if not row:
                raise HTTPException(status_code=404, detail="Category not found")
            cat, count = row
            return _category_to_dict(cat, count)
    finally:
        await engine.dispose()
