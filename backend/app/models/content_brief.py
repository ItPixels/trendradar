import uuid
from sqlalchemy import Column, String, Text, Integer, DateTime, ForeignKey, text
from sqlalchemy.dialects.postgresql import UUID, JSONB, ARRAY
from sqlalchemy.orm import relationship
from app.database import Base
from app.models.base import TimestampMixin


class ContentBrief(Base, TimestampMixin):
    __tablename__ = "content_briefs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, server_default=text("gen_random_uuid()"))
    trend_id = Column(UUID(as_uuid=True), ForeignKey("trends.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    format = Column(String(50), nullable=False, default="article", server_default="article")
    title = Column(String(500), nullable=False)
    hook = Column(Text, nullable=True)
    key_points = Column(JSONB, nullable=True, default=[])
    structure = Column(JSONB, nullable=True, default={})
    seo_keywords = Column(ARRAY(String), nullable=True, default=[])
    hashtags = Column(ARRAY(String), nullable=True, default=[])
    recommended_platforms = Column(ARRAY(String), nullable=True, default=[])
    optimal_timing = Column(Text, nullable=True)
    target_audience = Column(Text, nullable=True)
    tone = Column(String(50), default="informative", server_default="informative")
    word_count_target = Column(Integer, nullable=True)
    full_brief = Column(Text, nullable=True)
    model_version = Column(String(50), default="v1", server_default="v1")

    trend = relationship("Trend")

    def __repr__(self):
        return f"<ContentBrief(id={self.id}, trend_id={self.trend_id}, format='{self.format}')>"
