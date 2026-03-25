import uuid
from sqlalchemy import Column, String, Text, Float, Integer, DateTime, ForeignKey, text
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from app.database import Base
from app.models.base import TimestampMixin


class SignalEvent(Base, TimestampMixin):
    __tablename__ = "signal_events"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, server_default=text("gen_random_uuid()"))
    trend_id = Column(UUID(as_uuid=True), ForeignKey("trends.id"), nullable=False, index=True)
    source = Column(String(100), nullable=False, index=True)
    source_id = Column(String(500), nullable=True)
    title = Column(String(1000), nullable=True)
    url = Column(Text, nullable=True)
    content = Column(Text, nullable=True)
    signal_strength = Column(Float, nullable=False, default=0.0, server_default="0")
    metrics = Column(JSONB, nullable=True, default={})
    detected_at = Column(DateTime(timezone=True), nullable=False)

    # Relationships
    trend = relationship("Trend", back_populates="signal_events")

    def __repr__(self):
        return f"<SignalEvent(id={self.id}, source='{self.source}', trend_id={self.trend_id})>"
