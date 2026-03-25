import os
import traceback

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="TrendRadar API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health_check():
    return {"status": "ok", "version": "0.1.0"}


@app.get("/api/v1/health")
async def api_health():
    return {"status": "ok"}


@app.get("/debug/env")
async def debug_env():
    db_url = os.environ.get("DATABASE_URL", "NOT SET")
    if db_url != "NOT SET" and "@" in db_url:
        parts = db_url.split("@")
        masked = parts[0].split(":")[0] + ":****@" + parts[1]
    else:
        masked = db_url
    return {
        "DATABASE_URL": masked,
        "APP_ENV": os.environ.get("APP_ENV", "NOT SET"),
        "SUPABASE_URL": os.environ.get("SUPABASE_URL", "NOT SET"),
    }


@app.get("/debug/db")
async def debug_db():
    try:
        import asyncpg
        db_url = os.environ.get("DATABASE_URL", "")
        # Convert SQLAlchemy URL to asyncpg format
        raw_url = db_url.replace("postgresql+asyncpg://", "postgresql://")
        conn = await asyncpg.connect(raw_url, statement_cache_size=0)
        await conn.execute("DEALLOCATE ALL")
        result = await conn.fetchval("SELECT COUNT(*) FROM categories")
        await conn.close()
        return {"status": "connected", "categories_count": result}
    except Exception as e:
        return {"status": "error", "error": str(e), "trace": traceback.format_exc()}


@app.get("/debug/collect-full")
async def debug_collect_full():
    """Test the full pipeline step by step."""
    steps = {}
    try:
        # Step 1: Fetch signals
        from app.core.signals.adapters.hackernews import HackerNewsAdapter
        adapter = HackerNewsAdapter()
        signals = await adapter.fetch_signals()
        steps["1_fetch"] = f"ok: {len(signals)} signals"

        # Step 2: Deduplicate
        from app.core.signals.deduplicator import SignalDeduplicator
        dedup = SignalDeduplicator()
        topic_groups = dedup.deduplicate({"hackernews": signals})
        steps["2_dedup"] = f"ok: {len(topic_groups)} topics"

        # Step 3: DB query (categories)
        from sqlalchemy.ext.asyncio import AsyncSession
        from sqlalchemy import select
        from app.database import _create_engine
        from sqlalchemy.ext.asyncio import async_sessionmaker
        from app.models.category import Category

        engine = _create_engine()
        sm = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
        async with sm() as session:
            cat_result = await session.execute(select(Category).where(Category.is_active == True))
            categories = {c.slug: c.id for c in cat_result.scalars().all()}
            steps["3_db_categories"] = f"ok: {len(categories)} categories"

            # Step 4: Create a trend
            from app.core.signals.normalizer import TopicNormalizer
            normalizer = TopicNormalizer()
            first_topic = list(topic_groups.keys())[0] if topic_groups else None
            if first_topic:
                slug = normalizer.create_slug(first_topic)
                steps["4_normalize"] = f"ok: '{first_topic}' -> '{slug}'"
            else:
                steps["4_normalize"] = "skip: no topics"

            await engine.dispose()
        return {"status": "ok", "steps": steps}
    except Exception as e:
        steps["error"] = str(e)
        return {"status": "error", "steps": steps, "trace": traceback.format_exc()}


@app.get("/debug/collect-fetch")
async def debug_collect_fetch():
    """Test just the signal fetching (no DB)."""
    try:
        from app.core.signals.adapters.hackernews import HackerNewsAdapter
        adapter = HackerNewsAdapter()
        signals = await adapter.fetch_signals()
        return {
            "status": "ok",
            "count": len(signals),
            "sample": [{"title": s.title, "source": s.source} for s in signals[:3]],
        }
    except Exception as e:
        return {"status": "error", "error": str(e), "trace": traceback.format_exc()}


@app.post("/debug/collect-test")
async def debug_collect_test():
    """Test the collect pipeline DB operations without HTTP collection."""
    try:
        from sqlalchemy.ext.asyncio import AsyncSession
        from sqlalchemy import select, text
        from app.database import _create_engine, async_sessionmaker

        engine = _create_engine()
        session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
        async with session_maker() as session:
            # Test 1: raw text query
            r1 = await session.execute(text("SELECT 1"))
            val = r1.scalar()

            # Test 2: ORM query (like collect does)
            from app.models.category import Category
            r2 = await session.execute(select(Category).where(Category.is_active == True))
            cats = r2.scalars().all()

            await engine.dispose()
            return {
                "status": "ok",
                "select_1": val,
                "categories": len(cats),
            }
    except Exception as e:
        return {"status": "error", "error": str(e), "trace": traceback.format_exc()}


# Try to import full app routes
try:
    from app.config import settings
    from app.api.router import api_router
    app.include_router(api_router, prefix="/api")
    _loaded = True
except Exception as e:
    _error = str(e)
    _loaded = False

    @app.get("/api/{path:path}")
    async def api_fallback(path: str = ""):
        return {"error": _error, "loaded": False}
