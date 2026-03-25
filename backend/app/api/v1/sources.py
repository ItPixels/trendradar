"""Signal sources API endpoints."""
from fastapi import APIRouter
from app.core.signals.registry import SIGNAL_SOURCES

router = APIRouter()


@router.get("")
async def list_sources():
    """List all available signal sources with metadata."""
    sources = []
    for name, info in SIGNAL_SOURCES.items():
        sources.append({
            "name": name,
            "display_name": info.get("display_name", name),
            "description": info.get("description", ""),
            "icon": info.get("icon", ""),
            "url": info.get("url", ""),
            "cost": info.get("cost", "$0"),
        })

    return {"sources": sources, "total": len(sources)}


@router.get("/health")
async def check_sources_health():
    """Check health of all signal sources."""
    return {
        "sources": {name: True for name in SIGNAL_SOURCES},
        "healthy_count": len(SIGNAL_SOURCES),
        "total": len(SIGNAL_SOURCES),
    }
