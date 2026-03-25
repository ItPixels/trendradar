import uuid
from sqlalchemy import Column, String, Text, Float, Integer, Boolean, DateTime, ForeignKey, text
from sqlalchemy.dialects.postgresql import UUID, JSONB, ARRAY
from sqlalchemy.orm import relationship
from app.database import Base
from app.models.base import TimestampMixin, SoftDeleteMixin


class Trend(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "trends"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, server_default=text("gen_random_uuid()"))
    topic = Column(Text, nullable=False)
    topic_slug = Column(Text, nullable=False)
    description = Column(Text, nullable=True)
    summary = Column(Text, nullable=True)
    category_id = Column(UUID(as_uuid=True), ForeignKey("categories.id"), nullable=True)
    subcategory = Column(Text, nullable=True)
    tags = Column(ARRAY(Text), default=[])
    trend_score = Column(Float, nullable=False, default=0, server_default="0")
    velocity_score = Column(Float, default=0)
    correlation_score = Column(Float, default=0)
    signal_strength = Column(Float, default=0)
    sentiment_score = Column(Float, default=0)
    signal_count_1h = Column(Integer, default=0)
    signal_count_6h = Column(Integer, default=0)
    signal_count_24h = Column(Integer, default=0)
    signal_count_7d = Column(Integer, default=0)
    velocity_1h = Column(Float, default=0)
    velocity_6h = Column(Float, default=0)
    velocity_24h = Column(Float, default=0)
    acceleration = Column(Float, default=0)
    active_sources = Column(ARRAY(Text), default=[])
    source_count = Column(Integer, default=0)
    first_source = Column(Text, nullable=True)
    first_seen_at = Column(DateTime(timezone=True), nullable=False, server_default=text("NOW()"))
    status = Column(Text, default="active", server_default="active")
    peak_at = Column(DateTime(timezone=True), nullable=True)
    is_viral = Column(Boolean, default=False)
    is_breaking = Column(Boolean, default=False)
    ai_analysis = Column(JSONB, default={})
    last_ai_update = Column(DateTime(timezone=True), nullable=True)
    view_count = Column(Integer, default=0)
    share_count = Column(Integer, default=0)
    bookmark_count = Column(Integer, default=0)

    # Relationships
    category = relationship("Category", back_populates="trends")
    signal_events = relationship("SignalEvent", back_populates="trend")

    def __repr__(self):
        return f"<Trend(id={self.id}, topic='{self.topic}', status='{self.status}')>"
