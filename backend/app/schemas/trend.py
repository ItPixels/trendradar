from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID
from typing import Optional


class TrendBase(BaseModel):
    name: str = Field(..., max_length=500)
    description: Optional[str] = None
    category_id: Optional[UUID] = None
    tags: Optional[list[str]] = None


class TrendCreate(TrendBase):
    pass


class TrendResponse(BaseModel):
    id: UUID
    name: str
    slug: str
    description: Optional[str] = None
    category_id: Optional[UUID] = None
    status: str
    composite_score: float
    velocity: float
    acceleration: float
    signal_count: int
    source_diversity: int
    first_detected_at: Optional[datetime] = None
    peak_score: Optional[float] = None
    peak_at: Optional[datetime] = None
    tags: Optional[list[str]] = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class TrendListResponse(BaseModel):
    items: list[TrendResponse]
    total: int
    skip: int
    limit: int
