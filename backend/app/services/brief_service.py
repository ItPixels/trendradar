"""Content brief service."""
import logging
from typing import Optional
from sqlalchemy import select, desc, and_
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.content_brief import ContentBrief
from app.core.brief_generator.engine import BriefGenerator

logger = logging.getLogger(__name__)


class BriefService:
    """Business logic for content brief operations."""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.generator = BriefGenerator()

    async def get_briefs_for_trend(self, trend_id: str, user_id: str) -> list[ContentBrief]:
        """Get all briefs for a trend created by a user."""
        result = await self.db.execute(
            select(ContentBrief).where(
                and_(
                    ContentBrief.trend_id == trend_id,
                    ContentBrief.user_id == user_id,
                )
            ).order_by(desc(ContentBrief.created_at))
        )
        return list(result.scalars().all())

    async def generate_brief(
        self,
        trend_id: str,
        user_id: str,
        trend_data: dict,
        format: str = "article",
        target_audience: str = "content creators",
    ) -> Optional[ContentBrief]:
        """Generate and store a new content brief."""
        brief_data = await self.generator.generate(
            topic=trend_data.get("topic", ""),
            category=trend_data.get("category", "Technology"),
            trend_score=trend_data.get("trend_score", 0),
            predicted_growth=trend_data.get("predicted_growth", 0),
            active_sources=trend_data.get("active_sources", []),
            status=trend_data.get("status", "active"),
            format=format,
            target_audience=target_audience,
        )

        if not brief_data:
            return None

        brief = ContentBrief(
            trend_id=trend_id,
            user_id=user_id,
            format=format,
            title=brief_data.get("title", ""),
            hook=brief_data.get("hook", ""),
            key_points=brief_data.get("key_points", []),
            structure=brief_data.get("structure", {}),
            seo_keywords=brief_data.get("seo_keywords", []),
            hashtags=brief_data.get("hashtags", []),
            recommended_platforms=brief_data.get("recommended_platforms", []),
            optimal_timing=brief_data.get("optimal_timing", ""),
            target_audience=target_audience,
            tone=brief_data.get("tone", "informative"),
            word_count_target=brief_data.get("word_count_target"),
            full_brief=str(brief_data),
        )
        self.db.add(brief)
        await self.db.flush()
        return brief
