"""Celery application configuration."""
from celery import Celery
from celery.schedules import crontab
from app.config import settings

celery_app = Celery(
    "trendradar",
    broker=settings.redis_url,
    backend=settings.redis_url,
    include=[
        "app.tasks.signal_collection",
        "app.tasks.correlation",
        "app.tasks.velocity",
        "app.tasks.predictions",
        "app.tasks.alerts",
        "app.tasks.briefs",
        "app.tasks.cleanup",
        "app.tasks.source_health",
    ],
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=300,  # 5 min max per task
    task_soft_time_limit=240,
    worker_prefetch_multiplier=1,
    worker_max_tasks_per_child=100,
)

# Beat schedule (periodic tasks)
celery_app.conf.beat_schedule = {
    # Signal collection: every 15 minutes
    "collect-signals-tier1": {
        "task": "app.tasks.signal_collection.collect_tier1_signals",
        "schedule": crontab(minute="*/15"),
    },
    # Tier 2 signals: every 30 minutes
    "collect-signals-tier2": {
        "task": "app.tasks.signal_collection.collect_tier2_signals",
        "schedule": crontab(minute="*/30"),
    },
    # Correlation analysis: every 20 minutes
    "run-correlation": {
        "task": "app.tasks.correlation.analyze_correlations",
        "schedule": crontab(minute="*/20"),
    },
    # Velocity recalculation: every 10 minutes
    "recalculate-velocity": {
        "task": "app.tasks.velocity.recalculate_velocities",
        "schedule": crontab(minute="*/10"),
    },
    # Predictions: every hour
    "generate-predictions": {
        "task": "app.tasks.predictions.generate_predictions",
        "schedule": crontab(minute=0),
    },
    # Alert checking: every 5 minutes
    "check-alerts": {
        "task": "app.tasks.alerts.check_alerts",
        "schedule": crontab(minute="*/5"),
    },
    # Source health check: every hour
    "check-source-health": {
        "task": "app.tasks.source_health.check_all_sources",
        "schedule": crontab(minute=30),
    },
    # Cleanup old data: daily at 3 AM
    "cleanup-old-data": {
        "task": "app.tasks.cleanup.cleanup_old_signals",
        "schedule": crontab(hour=3, minute=0),
    },
    # Evaluate expired predictions: every 6 hours
    "evaluate-predictions": {
        "task": "app.tasks.predictions.evaluate_expired",
        "schedule": crontab(hour="*/6", minute=15),
    },
}
