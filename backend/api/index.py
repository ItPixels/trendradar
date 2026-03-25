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


@app.get("/migrate")
async def run_migrations():
    """Run pending schema migrations. Remove after all tables are created."""
    try:
        import asyncpg
        db_url = os.environ.get("DATABASE_URL", "")
        raw_url = db_url.replace("postgresql+asyncpg://", "postgresql://")
        conn = await asyncpg.connect(raw_url, statement_cache_size=0)
        await conn.execute("DEALLOCATE ALL")

        results = []
        migrations = [
            """CREATE TABLE IF NOT EXISTS predictions (
                id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                trend_id UUID NOT NULL REFERENCES trends(id) ON DELETE CASCADE,
                predicted_growth FLOAT NOT NULL,
                confidence_score FLOAT NOT NULL DEFAULT 0,
                timeframe_hours INTEGER NOT NULL DEFAULT 24,
                predicted_peak_at TIMESTAMPTZ,
                model_version VARCHAR(50) DEFAULT 'v1',
                input_features JSONB DEFAULT '{}',
                status VARCHAR(50) DEFAULT 'pending',
                actual_growth FLOAT,
                evaluated_at TIMESTAMPTZ,
                created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
                updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
            )""",
            "CREATE INDEX IF NOT EXISTS idx_predictions_trend ON predictions(trend_id)",
            "CREATE INDEX IF NOT EXISTS idx_predictions_confidence ON predictions(confidence_score DESC)",
            """CREATE TABLE IF NOT EXISTS alerts (
                id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                user_id UUID NOT NULL,
                name VARCHAR(500) NOT NULL,
                description TEXT,
                categories TEXT[] DEFAULT '{}',
                keywords TEXT[] DEFAULT '{}',
                excluded_keywords TEXT[] DEFAULT '{}',
                min_score FLOAT DEFAULT 50,
                min_velocity FLOAT DEFAULT 0,
                min_sources INTEGER DEFAULT 2,
                channels TEXT[] DEFAULT '{email}',
                webhook_url TEXT,
                is_active BOOLEAN DEFAULT true,
                trigger_count INTEGER DEFAULT 0,
                last_triggered_at TIMESTAMPTZ,
                cooldown_minutes INTEGER DEFAULT 60,
                created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
                updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
                deleted_at TIMESTAMPTZ
            )""",
            "CREATE INDEX IF NOT EXISTS idx_alerts_user ON alerts(user_id)",
        ]
        for sql in migrations:
            try:
                await conn.execute(sql)
                results.append({"sql": sql[:80], "status": "ok"})
            except Exception as e:
                results.append({"sql": sql[:80], "status": "error", "error": str(e)})

        await conn.close()
        return {"status": "ok", "migrations": results}
    except Exception as e:
        return {"status": "error", "error": str(e), "trace": traceback.format_exc()}


# Import full app routes
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
