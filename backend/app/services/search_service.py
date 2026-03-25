"""Search service — full text search across trends."""
from sqlalchemy import select, or_, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.trend import Trend


class SearchService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def search_trends(self, query: str, limit: int = 20) -> list[Trend]:
        """Search trends by topic, tags, description."""
        search_term = f"%{query}%"
        result = await self.db.execute(
            select(Trend)
            .where(
                Trend.deleted_at.is_(None),
                or_(
                    Trend.topic.ilike(search_term),
                    Trend.description.ilike(search_term),
                    Trend.summary.ilike(search_term),
                )
            )
            .order_by(Trend.trend_score.desc())
            .limit(limit)
        )
        return list(result.scalars().all())
