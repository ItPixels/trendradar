"""Signal collection tasks — fetch signals from all sources."""
import asyncio
import logging
from app.tasks.celery_app import celery_app
from app.core.signals.manager import SignalManager
from app.core.signals.topic_extractor import TopicExtractor
from app.core.signals.normalizer import TopicNormalizer

logger = logging.getLogger(__name__)

TIER1_SOURCES = [
    "hackernews", "reddit", "github_trending",
    "google_news", "wikipedia", "youtube_trending",
]

TIER2_SOURCES = [
    "producthunt", "npm_registry", "pypi_stats", "arxiv",
    "coingecko", "steam_charts", "devto", "lobsters", "stackoverflow",
]


def _run_async(coro):
    """Run an async function in a sync context (Celery task)."""
    loop = asyncio.new_event_loop()
    try:
        return loop.run_until_complete(coro)
    finally:
        loop.close()


@celery_app.task(name="app.tasks.signal_collection.collect_tier1_signals")
def collect_tier1_signals():
    """Collect signals from Tier 1 (core) sources."""
    return _run_async(_collect_signals(TIER1_SOURCES))


@celery_app.task(name="app.tasks.signal_collection.collect_tier2_signals")
def collect_tier2_signals():
    """Collect signals from Tier 2 (vertical) sources."""
    return _run_async(_collect_signals(TIER2_SOURCES))


@celery_app.task(name="app.tasks.signal_collection.collect_single_source")
def collect_single_source(source_name: str):
    """Collect signals from a single source."""
    return _run_async(_collect_signals([source_name]))


async def _collect_signals(sources: list[str]) -> dict:
    """Internal async signal collection."""
    manager = SignalManager()
    extractor = TopicExtractor()
    normalizer = TopicNormalizer()

    results = await manager.collect_all(sources=sources)

    total_signals = 0
    total_topics = 0

    for source, signals in results.items():
        for signal in signals:
            # Extract topics from each signal
            topics = extractor.extract_topics(
                signal.title,
                signal.content or "",
                signal.source,
            )
            # Normalize topics
            normalized_topics = [normalizer.normalize(t) for t in topics]
            signal.extracted_topics = normalized_topics

            total_signals += 1
            total_topics += len(normalized_topics)

    # TODO: Store signals in database
    # For now, just log the results
    logger.info(
        f"Collected {total_signals} signals with {total_topics} topics "
        f"from {len(results)} sources: {list(results.keys())}"
    )

    return {
        "sources_scanned": list(results.keys()),
        "total_signals": total_signals,
        "total_topics": total_topics,
        "signals_per_source": {k: len(v) for k, v in results.items()},
    }
