"""Signal sources API endpoints."""
from fastapi import APIRouter
from app.core.signals.manager import SignalManager
from app.core.signals.registry import SIGNAL_SOURCES

router = APIRouter()


@router.get("")
async def list_sources():
    """List all available signal sources with metadata."""
    manager = SignalManager()
    sources = manager.list_sources()

    # Enrich with registry data
    enriched = []
    for source in sources:
        registry_info = SIGNAL_SOURCES.get(source["name"], {})
        enriched.append({
            **source,
            "display_name": registry_info.get("display_name", source["name"]),
            "description": registry_info.get("description", ""),
            "icon": registry_info.get("icon", ""),
            "url": registry_info.get("url", ""),
            "cost": registry_info.get("cost", "$0"),
        })

    return {"sources": enriched, "total": len(enriched)}


@router.get("/health")
async def check_sources_health():
    """Check health of all signal sources."""
    manager = SignalManager()
    # Note: This is async but FastAPI handles it
    import asyncio
    health = await manager.health_check_all()

    return {
        "sources": health,
        "healthy_count": sum(1 for v in health.values() if v),
        "total": len(health),
    }
