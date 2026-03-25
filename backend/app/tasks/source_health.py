"""Signal source health monitoring tasks."""
import asyncio
import logging
from app.tasks.celery_app import celery_app
from app.core.signals.manager import SignalManager

logger = logging.getLogger(__name__)


def _run_async(coro):
    loop = asyncio.new_event_loop()
    try:
        return loop.run_until_complete(coro)
    finally:
        loop.close()


@celery_app.task(name="app.tasks.source_health.check_all_sources")
def check_all_sources():
    """Check health of all signal sources."""
    manager = SignalManager()
    results = _run_async(manager.health_check_all())

    healthy = [k for k, v in results.items() if v]
    unhealthy = [k for k, v in results.items() if not v]

    logger.info(f"Source health: {len(healthy)} healthy, {len(unhealthy)} unhealthy")
    if unhealthy:
        logger.warning(f"Unhealthy sources: {unhealthy}")

    # TODO: Update source_health table in database
    # for source, is_healthy in results.items():
    #     update_source_health(source, is_healthy)

    return {
        "healthy": healthy,
        "unhealthy": unhealthy,
        "total": len(results),
    }


@celery_app.task(name="app.tasks.source_health.check_single_source")
def check_single_source(source_name: str):
    """Check health of a single source."""
    manager = SignalManager()
    adapter = manager.adapters.get(source_name)

    if not adapter:
        return {"source": source_name, "error": "Unknown source"}

    is_healthy = _run_async(adapter.health_check())

    return {
        "source": source_name,
        "healthy": is_healthy,
    }
