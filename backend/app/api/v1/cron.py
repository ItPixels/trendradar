"""Vercel Cron endpoint — triggered every 30 min to collect signals + generate predictions."""
import os
import logging
import traceback
from datetime import datetime, timezone
from typing import Optional
from fastapi import APIRouter, Request, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from sqlalchemy import select, desc
from app.database import _create_engine
from app.core.signals.manager import SignalManager
from app.core.signals.deduplicator import SignalDeduplicator
from app.core.signals.normalizer import TopicNormalizer
from app.core.predictor.engine import PredictionEngine
from app.core.correlation.engine import CorrelationEngine
from app.models.trend import Trend
from app.models.signal_event import SignalEvent
from app.models.prediction import Prediction
from app.models.category import Category

logger = logging.getLogger(__name__)
router = APIRouter()

CRON_SECRET = os.environ.get("CRON_SECRET", "")

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
    text = topic.lower()
    for s in signals[:5]:
        text += " " + s.title.lower()
    scores = {}
    for slug, keywords in CATEGORY_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw in text)
        if score > 0:
            scores[slug] = score
    if scores:
        return max(scores, key=scores.get)
    return "tech"


@router.get("/collect")
async def cron_collect(request: Request):
    """Vercel Cron job — collects signals and generates predictions.

    Protected by CRON_SECRET header check.
    """
    # Verify cron secret (Vercel sends Authorization header for cron jobs)
    if CRON_SECRET:
        auth = request.headers.get("authorization", "")
        if auth != f"Bearer {CRON_SECRET}":
            raise HTTPException(status_code=401, detail="Unauthorized")

    try:
        result = await _cron_pipeline()
        return result
    except Exception as e:
        logger.error(f"Cron error: {e}\n{traceback.format_exc()}")
        return {"error": str(e), "trace": traceback.format_exc()}


async def _cron_pipeline():
    """Full pipeline: collect signals → save trends → generate predictions."""
    # 1. Collect signals from fast sources
    sources = ["hackernews", "lobsters", "devto", "github_trending",
               "google_news", "coingecko", "npm_registry"]
    manager = SignalManager()
    raw_results = await manager.collect_all(sources=sources)

    # 2. Deduplicate and group
    dedup = SignalDeduplicator()
    topic_groups = dedup.deduplicate(raw_results)

    # 3. DB work
    engine = _create_engine()
    session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    trends_created = 0
    trends_updated = 0
    signals_saved = 0
    predictions_created = 0

    try:
        async with session_maker() as db:
            # Load categories
            cat_result = await db.execute(select(Category).where(Category.is_active == True))
            categories = {c.slug: c.id for c in cat_result.scalars().all()}

            normalizer = TopicNormalizer()
            now = datetime.now(timezone.utc)
            trend_ids_to_predict = []

            for topic, signals in topic_groups.items():
                if not signals or len(topic) < 3:
                    continue
                slug = normalizer.create_slug(topic)
                if not slug or slug == "unknown":
                    continue

                unique_sources = list(set(s.source for s in signals))
                source_count = len(unique_sources)
                max_strength = max(s.signal_strength for s in signals)
                trend_score = min(100, source_count * 15 + max_strength * 30 + min(len(signals), 10) * 3)
                velocity_24h = len(signals)
                cat_slug = _guess_category_slug(topic, signals)
                category_id = categories.get(cat_slug)
                status = "active" if source_count >= 3 else "emerging"
                is_viral = source_count >= 4 and trend_score > 70
                is_breaking = source_count >= 3 and max_strength > 0.8

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
                        topic=topic, topic_slug=slug, description=description,
                        category_id=category_id, trend_score=trend_score,
                        velocity_24h=velocity_24h, source_count=source_count,
                        active_sources=unique_sources, signal_count_24h=len(signals),
                        status=status, is_viral=is_viral, is_breaking=is_breaking,
                        first_seen_at=now, tags=[],
                    )
                    db.add(trend)
                    trends_created += 1

                await db.flush()
                trend_ids_to_predict.append(trend.id)

                # Save signal events (limit 10 per trend)
                for signal in signals[:10]:
                    event = SignalEvent(
                        trend_id=trend.id, source=signal.source,
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

            # 4. Generate predictions for top trends
            predictions_created = await _generate_predictions(
                db, trend_ids_to_predict, topic_groups, now
            )
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
        "predictions_created": predictions_created,
    }


async def _generate_predictions(
    db: AsyncSession,
    trend_ids: list,
    topic_groups: dict,
    now: datetime,
) -> int:
    """Generate predictions for trends with enough signal data."""
    if not trend_ids:
        return 0

    # Load trends that qualify for prediction (score >= 30 or 2+ sources)
    result = await db.execute(
        select(Trend)
        .where(Trend.id.in_(trend_ids))
        .where(Trend.deleted_at.is_(None))
        .where((Trend.trend_score >= 30) | (Trend.source_count >= 2))
        .order_by(desc(Trend.trend_score))
        .limit(50)
    )
    trends = result.scalars().all()

    if not trends:
        return 0

    prediction_engine = PredictionEngine()
    correlation_engine = CorrelationEngine()
    count = 0

    for trend in trends:
        try:
            # Build trend_data dict from ORM model
            trend_data = {
                "trend_score": trend.trend_score or 0,
                "signal_count_24h": trend.signal_count_24h or 0,
                "source_count": trend.source_count or 0,
                "velocity_24h": trend.velocity_24h or 0,
                "status": trend.status,
            }

            # Build correlation data from active sources
            signals_by_source = {}
            for src in (trend.active_sources or []):
                signals_by_source[src] = [{"source": src}]

            correlation_data = correlation_engine.calculate_correlation(
                topic=trend.topic,
                signals_by_source=signals_by_source,
            )

            # Simplified velocity data from trend fields
            velocity_data = {
                "velocity_1h": 0,
                "velocity_6h": 0,
                "velocity_24h": trend.velocity_24h or 0,
                "acceleration": trend.acceleration or 0,
                "momentum": (trend.velocity_24h or 0) * 0.8,
                "velocity_score": min((trend.velocity_24h or 0) * 10, 100),
                "phase": trend.status if trend.status in ["emerging", "active", "peaking", "declining"] else "active",
                "is_accelerating": (trend.acceleration or 0) > 0,
                "is_decelerating": (trend.acceleration or 0) < -0.1,
            }

            # Generate prediction for 24h
            pred_result = prediction_engine.predict(
                trend_data=trend_data,
                correlation_data=correlation_data,
                velocity_data=velocity_data,
                timeframe_hours=24,
            )

            prediction = Prediction(
                trend_id=trend.id,
                predicted_growth=pred_result["predicted_growth"],
                confidence_score=pred_result["confidence_score"],
                timeframe_hours=pred_result["timeframe_hours"],
                predicted_peak_at=None,  # Will be set if available
                model_version=pred_result["model_version"],
                input_features={
                    "features": pred_result.get("features", {}),
                    "factors": pred_result.get("factors", []),
                },
                status="pending",
            )

            # Parse peak_at if present
            peak_at = pred_result.get("predicted_peak_at")
            if peak_at and isinstance(peak_at, str):
                from dateutil.parser import parse as parse_date
                try:
                    prediction.predicted_peak_at = parse_date(peak_at)
                except Exception:
                    pass

            db.add(prediction)
            count += 1

        except Exception as e:
            logger.warning(f"Failed to predict for trend {trend.topic}: {e}")
            continue

    return count
