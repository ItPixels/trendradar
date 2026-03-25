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
