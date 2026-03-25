"""Signal collection endpoint — triggers collection and saves to DB.

Replaces Celery tasks for Vercel serverless deployment.
"""
import logging
import traceback
from datetime import datetime, timezone
from typing import Optional
from fastapi import APIRouter, Query
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from sqlalchemy import select
from app.database import _create_engine
from app.core.signals.manager import SignalManager
from app.core.signals.deduplicator import SignalDeduplicator
from app.core.signals.normalizer import TopicNormalizer
from app.models.trend import Trend
from app.models.signal_event import SignalEvent
from app.models.category import Category

logger = logging.getLogger(__name__)
router = APIRouter()

# Simple keyword → category slug mapping
CATEGORY_KEYWORDS = {
    "ai": ["ai", "gpt", "llm", "claude", "gemini", "openai", "anthropic", "machine learning",
           "neural", "deep learning", "chatgpt", "llama", "stable diffusion", "midjourney",
           "dall-e", "transformer", "copilot", "artificial intelligence", "agi"],
    "crypto": ["bitcoin", "ethereum", "crypto", "blockchain", "btc", "eth", "solana", "defi",
               "nft", "web3", "token", "mining", "wallet", "cardano", "dogecoin"],
    "tech": ["apple", "google", "microsoft", "amazon", "meta", "iphone", "android",
             "samsung", "chip", "semiconductor", "nvidia", "intel", "amd", "qualcomm"],
    "devtools": ["vscode", "cursor", "neovim", "ide", "git", "docker", "kubernetes",
                 "terraform", "ci/cd", "devops", "github actions"],
    "opensource": ["open source", "linux", "github", "git", "fork", "apache", "mit license"],
    "gaming": ["steam", "gaming", "playstation", "xbox", "nintendo", "game", "esports",
               "twitch", "epic games", "valve", "unity", "unreal"],
    "science": ["nasa", "space", "climate", "physics", "chemistry", "biology", "research",
                "arxiv", "paper", "study", "telescope", "mars", "quantum"],
    "finance": ["stock", "market", "trading", "invest", "fed", "interest rate", "s&p",
                "dow", "nasdaq", "ipo", "earnings", "wall street"],
    "business": ["startup", "funding", "acquisition", "merger", "revenue", "ceo",
                 "layoff", "ipo", "venture", "series a", "unicorn", "saas"],
    "health": ["health", "medical", "drug", "fda", "vaccine", "clinical", "disease",
               "wellness", "fitness", "mental health"],
    "culture": ["movie", "film", "music", "netflix", "spotify", "disney", "concert",
                "celebrity", "oscar", "grammy", "viral", "tiktok"],
    "design": ["design", "figma", "ux", "ui", "typography", "branding", "css",
               "tailwind", "animation"],
}


def _guess_category_slug(topic: str, signals) -> Optional[str]:
    """Guess the best category for a topic based on keywords."""
    text = topic.lower()
    # Also check signal titles
    for s in signals[:5]:
        text += " " + s.title.lower()

    scores = {}
    for slug, keywords in CATEGORY_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw in text)
        if score > 0:
            scores[slug] = score

    if scores:
        return max(scores, key=scores.get)
    return "tech"  # default


@router.post("")
async def collect_signals(
    sources: Optional[list[str]] = Query(
        default=None,
        description="Specific sources to collect from. If empty, collects from fast sources."
    ),
):
    """Trigger signal collection, process, and save to DB.

    Sources available: hackernews, reddit, github_trending, google_news,
    wikipedia, youtube_trending, producthunt, npm_registry, pypi_stats,
    arxiv, coingecko, steam_charts, devto, lobsters, stackoverflow
    """
    try:
        return await _do_collect(sources)
    except Exception as e:
        logger.error(f"Collection error: {e}\n{traceback.format_exc()}")
        return {"error": str(e), "trace": traceback.format_exc()}


async def _do_collect(sources: Optional[list[str]]):
    # Default to fast, reliable sources if none specified
    if not sources:
        sources = [
            "hackernews", "lobsters", "devto", "github_trending",
            "google_news", "coingecko", "npm_registry",
        ]

    # 1. Collect signals (HTTP requests — no DB needed yet)
    manager = SignalManager()
    raw_results = await manager.collect_all(sources=sources)

    # 2. Deduplicate and group by topic
    dedup = SignalDeduplicator()
    topic_groups = dedup.deduplicate(raw_results)

    # 3. Open DB session and do all DB work
    engine = _create_engine()
    session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    trends_created = 0
    trends_updated = 0
    signals_saved = 0

    try:
        async with session_maker() as db:
            # Load category map
            cat_result = await db.execute(select(Category).where(Category.is_active == True))
            categories = {c.slug: c.id for c in cat_result.scalars().all()}

            normalizer = TopicNormalizer()
            now = datetime.now(timezone.utc)

            for topic, signals in topic_groups.items():
                if not signals:
                    continue

                # Skip very short or generic topics
                if len(topic) < 3:
                    continue

                slug = normalizer.create_slug(topic)
                if not slug or slug == "unknown":
                    continue

                # Count unique sources for this topic
                unique_sources = list(set(s.source for s in signals))
                source_count = len(unique_sources)

                # Calculate basic scores
                max_strength = max(s.signal_strength for s in signals)

                # Trend score based on source diversity and signal strength
                trend_score = min(100, (
                    source_count * 15 +
                    max_strength * 30 +
                    min(len(signals), 10) * 3
                ))

                velocity_24h = len(signals)

                # Guess category
                cat_slug = _guess_category_slug(topic, signals)
                category_id = categories.get(cat_slug)

                # Determine status
                if source_count >= 3:
                    status = "active"
                else:
                    status = "emerging"

                is_viral = source_count >= 4 and trend_score > 70
                is_breaking = source_count >= 3 and max_strength > 0.8

                # Check if trend already exists
                existing = await db.execute(
                    select(Trend).where(Trend.topic_slug == slug, Trend.deleted_at.is_(None))
                )
                trend = existing.scalar_one_or_none()

                if trend:
                    trend.trend_score = max(trend.trend_score, trend_score)
                    trend.velocity_24h = velocity_24h
                    trend.source_count = max(trend.source_count or 0, source_count)
                    trend.active_sources = unique_sources
                    trend.signal_count_24h = (trend.signal_count_24h or 0) + len(signals)
                    if status == "active" and trend.status == "emerging":
                        trend.status = status
                    trend.is_viral = trend.is_viral or is_viral
                    trend.is_breaking = trend.is_breaking or is_breaking
                    trend.updated_at = now
                    trends_updated += 1
                else:
                    description = None
                    for s in signals:
                        if len(s.title) > len(topic) + 5:
                            description = s.title[:500]
                            break

                    trend = Trend(
                        topic=topic,
                        topic_slug=slug,
                        description=description,
                        category_id=category_id,
                        trend_score=trend_score,
                        velocity_24h=velocity_24h,
                        source_count=source_count,
                        active_sources=unique_sources,
                        signal_count_24h=len(signals),
                        status=status,
                        is_viral=is_viral,
                        is_breaking=is_breaking,
                        first_seen_at=now,
                        tags=[],
                    )
                    db.add(trend)
                    trends_created += 1

                await db.flush()

                # Create signal events (limit per trend)
                for signal in signals[:10]:
                    event = SignalEvent(
                        trend_id=trend.id,
                        source=signal.source,
                        source_id=signal.source_id,
                        title=signal.title[:1000] if signal.title else None,
                        url=signal.url,
                        content=signal.content[:2000] if signal.content else None,
                        signal_strength=signal.signal_strength,
                        metrics=signal.metrics,
                        detected_at=signal.detected_at or now,
                    )
                    db.add(event)
                    signals_saved += 1

            await db.commit()
    finally:
        await engine.dispose()

    total_raw = sum(len(v) for v in raw_results.values())
    return {
        "status": "ok",
        "sources_scanned": list(raw_results.keys()),
        "raw_signals": total_raw,
        "topics_found": len(topic_groups),
        "trends_created": trends_created,
        "trends_updated": trends_updated,
        "signals_saved": signals_saved,
        "signals_per_source": {k: len(v) for k, v in raw_results.items()},
    }
