"""Trend service — business logic for trend operations."""
import logging
from datetime import datetime, timezone, timedelta
from typing import Optional
from sqlalchemy import select, func, desc, and_, or_
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.trend import Trend
from app.models.signal_event import SignalEvent
from app.models.category import Category

logger = logging.getLogger(__name__)


class TrendService:
    """Business logic for trend operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_trends(
        self,
        category_slug: Optional[str] = None,
        status: Optional[str] = None,
        min_score: float = 0,
        sources: Optional[list[str]] = None,
        sort_by: str = "score",
        time_range: str = "24h",
        limit: int = 50,
        offset: int = 0,
    ) -> tuple[list[Trend], int]:
        """Get trending topics with filters."""
        query = select(Trend).where(Trend.deleted_at.is_(None))
        count_query = select(func.count(Trend.id)).where(Trend.deleted_at.is_(None))

        # Apply filters
        if category_slug:
            cat_subq = select(Category.id).where(Category.slug == category_slug)
            query = query.where(Trend.category_id.in_(cat_subq))
            count_query = count_query.where(Trend.category_id.in_(cat_subq))

        if status:
            query = query.where(Trend.status == status)
            count_query = count_query.where(Trend.status == status)

        if min_score > 0:
            query = query.where(Trend.trend_score >= min_score)
            count_query = count_query.where(Trend.trend_score >= min_score)

        # Time range filter
        time_map = {"1h": 1, "6h": 6, "24h": 24, "7d": 168, "30d": 720}
        hours = time_map.get(time_range, 24)
        cutoff = datetime.now(timezone.utc) - timedelta(hours=hours)
        query = query.where(Trend.first_seen_at >= cutoff)
        count_query = count_query.where(Trend.first_seen_at >= cutoff)

        # Sort
        sort_map = {
            "score": Trend.trend_score.desc(),
            "velocity": Trend.velocity_24h.desc(),
            "newest": Trend.first_seen_at.desc(),
            "sources": Trend.source_count.desc(),
        }
        query = query.order_by(sort_map.get(sort_by, Trend.trend_score.desc()))

        # Get total count
        total_result = await self.db.execute(count_query)
        total = total_result.scalar() or 0

        # Paginate
        query = query.limit(limit).offset(offset)
        result = await self.db.execute(query)
        trends = list(result.scalars().all())

        return trends, total

    async def get_trend_by_id(self, trend_id: str) -> Optional[Trend]:
        """Get a single trend by ID."""
        result = await self.db.execute(
            select(Trend).where(
                and_(Trend.id == trend_id, Trend.deleted_at.is_(None))
            )
        )
        return result.scalar_one_or_none()

    async def get_trend_by_slug(self, slug: str) -> Optional[Trend]:
        """Get a trend by its topic slug."""
        result = await self.db.execute(
            select(Trend).where(
                and_(Trend.topic_slug == slug, Trend.deleted_at.is_(None))
            )
        )
        return result.scalar_one_or_none()

    async def create_or_update_trend(
        self,
        topic: str,
        topic_slug: str,
        category_id: Optional[str] = None,
        **kwargs,
    ) -> Trend:
        """Create a new trend or update existing one."""
        existing = await self.get_trend_by_slug(topic_slug)

        if existing:
            # Update existing trend
            for key, value in kwargs.items():
                if hasattr(existing, key) and value is not None:
                    setattr(existing, key, value)
            await self.db.flush()
            return existing

        # Create new trend
        trend = Trend(
            topic=topic,
            topic_slug=topic_slug,
            category_id=category_id,
            **kwargs,
        )
        self.db.add(trend)
        await self.db.flush()
        return trend

    async def increment_view_count(self, trend_id: str):
        """Increment view count for a trend."""
        result = await self.db.execute(
            select(Trend).where(Trend.id == trend_id)
        )
        trend = result.scalar_one_or_none()
        if trend:
            trend.view_count = (trend.view_count or 0) + 1
            await self.db.flush()

    async def get_trending_categories(self, limit: int = 10) -> list[dict]:
        """Get categories with most active trends."""
        result = await self.db.execute(
            select(
                Category.slug,
                Category.name,
                Category.icon,
                Category.color,
                func.count(Trend.id).label("trend_count"),
            )
            .join(Trend, Trend.category_id == Category.id, isouter=True)
            .where(Trend.deleted_at.is_(None))
            .group_by(Category.id)
            .order_by(desc("trend_count"))
            .limit(limit)
        )

        return [
            {
                "slug": row.slug,
                "name": row.name,
                "icon": row.icon,
                "color": row.color,
                "trend_count": row.trend_count,
            }
            for row in result.all()
        ]
