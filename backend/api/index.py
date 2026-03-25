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
