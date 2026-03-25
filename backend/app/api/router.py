from fastapi import APIRouter
from app.api.v1 import trends, predictions, alerts, health, sources, briefs, categories, search, billing, collect

api_router = APIRouter()

api_router.include_router(health.router, prefix="/v1", tags=["health"])
api_router.include_router(trends.router, prefix="/v1/trends", tags=["trends"])
api_router.include_router(predictions.router, prefix="/v1/predictions", tags=["predictions"])
api_router.include_router(alerts.router, prefix="/v1/alerts", tags=["alerts"])
api_router.include_router(sources.router, prefix="/v1/sources", tags=["sources"])
api_router.include_router(briefs.router, prefix="/v1/briefs", tags=["briefs"])
api_router.include_router(categories.router, prefix="/v1/categories", tags=["categories"])
api_router.include_router(search.router, prefix="/v1/search", tags=["search"])
api_router.include_router(billing.router, prefix="/v1/billing", tags=["billing"])
api_router.include_router(collect.router, prefix="/v1/collect", tags=["collect"])
