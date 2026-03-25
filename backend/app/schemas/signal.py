from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID
from typing import Optional


class SignalEventBase(BaseModel):
    source: str = Field(..., max_length=100)
    source_id: Optional[str] = None
    title: Optional[str] = None
    url: Optional[str] = None
    content: Optional[str] = None
    signal_strength: float = 0.0
    metrics: Optional[dict] = None
    detected_at: datetime


class SignalEventCreate(SignalEventBase):
    trend_id: UUID


class SignalEventResponse(SignalEventBase):
    id: UUID
    trend_id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
