from pydantic import BaseModel
from datetime import datetime
from uuid import UUID
from typing import Optional


class TrendResponse(BaseModel):
    id: UUID
    topic: str
    topic_slug: str
    description: Optional[str] = None
    summary: Optional[str] = None
    category_id: Optional[UUID] = None
    status: str = "active"
    trend_score: float = 0
    velocity_24h: float = 0
    acceleration: float = 0
    signal_count_24h: int = 0
    source_count: int = 0
    active_sources: list[str] = []
    tags: list[str] = []
    first_seen_at: Optional[datetime] = None
    is_viral: bool = False
    is_breaking: bool = False
    view_count: int = 0
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


class TrendListResponse(BaseModel):
    items: list[TrendResponse]
    total: int
    offset: int = 0
    limit: int = 50
