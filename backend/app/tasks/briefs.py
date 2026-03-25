"""Content brief generation tasks."""
import asyncio
import logging
from app.tasks.celery_app import celery_app
from app.core.brief_generator.engine import BriefGenerator

logger = logging.getLogger(__name__)


def _run_async(coro):
    loop = asyncio.new_event_loop()
    try:
        return loop.run_until_complete(coro)
    finally:
        loop.close()


@celery_app.task(name="app.tasks.briefs.generate_brief")
def generate_brief(
    topic: str,
    category: str = "Technology",
    trend_score: float = 0,
    predicted_growth: float = 0,
    timeframe_hours: int = 24,
    active_sources: list[str] = None,
    format: str = "article",
    target_audience: str = "content creators and marketers",
):
    """Generate a content brief for a trend."""
    generator = BriefGenerator()

    result = _run_async(generator.generate(
        topic=topic,
        category=category,
        trend_score=trend_score,
        predicted_growth=predicted_growth,
        timeframe_hours=timeframe_hours,
        active_sources=active_sources,
        format=format,
        target_audience=target_audience,
    ))

    if result:
        logger.info(f"Generated {format} brief for '{topic}'")
    else:
        logger.warning(f"Failed to generate brief for '{topic}'")

    return result
