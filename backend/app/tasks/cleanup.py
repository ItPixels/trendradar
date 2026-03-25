"""Data cleanup tasks."""
import logging
from app.tasks.celery_app import celery_app

logger = logging.getLogger(__name__)


@celery_app.task(name="app.tasks.cleanup.cleanup_old_signals")
def cleanup_old_signals():
    """Clean up signal events older than 30 days."""
    logger.info("Cleaning up old signal events...")

    # TODO: Delete signals older than 30 days
    # from datetime import datetime, timedelta
    # cutoff = datetime.utcnow() - timedelta(days=30)
    # deleted = delete_signals_before(cutoff)
    # logger.info(f"Deleted {deleted} old signal events")

    return {"status": "completed"}


@celery_app.task(name="app.tasks.cleanup.cleanup_dead_trends")
def cleanup_dead_trends():
    """Archive trends that have been 'dead' for more than 7 days."""
    logger.info("Archiving dead trends...")

    # TODO: Soft-delete trends with status='dead' and no signals for 7 days

    return {"status": "completed"}
