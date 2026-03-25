import uuid
from sqlalchemy import Column, String, Text, Float, Integer, Boolean, DateTime, text
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from app.database import Base
from app.models.base import TimestampMixin, SoftDeleteMixin


class Alert(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "alerts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, server_default=text("gen_random_uuid()"))
    user_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    name = Column(String(500), nullable=False)
    description = Column(Text, nullable=True)
    categories = Column(ARRAY(String), nullable=True, default=[])
    keywords = Column(ARRAY(String), nullable=True, default=[])
    excluded_keywords = Column(ARRAY(String), nullable=True, default=[])
    min_score = Column(Float, default=50, server_default="50")
    min_velocity = Column(Float, default=0, server_default="0")
    min_sources = Column(Integer, default=2, server_default="2")
    channels = Column(ARRAY(String), nullable=True, default=["email"])
    webhook_url = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True, server_default="true")
    trigger_count = Column(Integer, default=0, server_default="0")
    last_triggered_at = Column(DateTime(timezone=True), nullable=True)
    cooldown_minutes = Column(Integer, default=60, server_default="60")

    def __repr__(self):
        return f"<Alert(id={self.id}, name='{self.name}', active={self.is_active})>"
