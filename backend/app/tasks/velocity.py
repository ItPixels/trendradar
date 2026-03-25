"""Velocity recalculation tasks."""
import logging
from app.tasks.celery_app import celery_app
from app.core.velocity.analyzer import VelocityAnalyzer

logger = logging.getLogger(__name__)


@celery_app.task(name="app.tasks.velocity.recalculate_velocities")
def recalculate_velocities():
    """Recalculate velocity metrics for all active trends."""
    logger.info("Recalculating velocity metrics for active trends...")

    analyzer = VelocityAnalyzer()

    # TODO: Fetch active trends from database
    # trends = fetch_active_trends()
    # for trend in trends:
    #     signal_counts = fetch_signal_counts_for_trend(trend.id)
    #     velocity_data = analyzer.analyze(signal_counts, trend.trend_score)
    #     update_trend_velocity(trend.id, velocity_data)

    return {"status": "completed"}


@celery_app.task(name="app.tasks.velocity.recalculate_single")
def recalculate_single_velocity(trend_id: str, signal_counts: list[dict]):
    """Recalculate velocity for a single trend."""
    analyzer = VelocityAnalyzer()
    result = analyzer.analyze(signal_counts)

    logger.info(f"Velocity for trend {trend_id}: score={result['velocity_score']}, phase={result['phase']}")

    return result
