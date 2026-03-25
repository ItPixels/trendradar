import uuid
from sqlalchemy import Column, String, Text, Float, Integer, DateTime, ForeignKey, Enum, text
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from app.database import Base
from app.models.base import TimestampMixin, SoftDeleteMixin


class Trend(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "trends"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, server_default=text("gen_random_uuid()"))
    name = Column(String(500), nullable=False, index=True)
    slug = Column(String(500), unique=True, nullable=False, index=True)
    description = Column(Text, nullable=True)
    category_id = Column(UUID(as_uuid=True), ForeignKey("categories.id"), nullable=True)
    status = Column(
        String(50),
        nullable=False,
        default="emerging",
        server_default="emerging",
    )
    composite_score = Column(Float, nullable=False, default=0.0, server_default="0")
    velocity = Column(Float, nullable=False, default=0.0, server_default="0")
    acceleration = Column(Float, nullable=False, default=0.0, server_default="0")
    signal_count = Column(Integer, nullable=False, default=0, server_default="0")
    source_diversity = Column(Integer, nullable=False, default=0, server_default="0")
    first_detected_at = Column(DateTime(timezone=True), nullable=True)
    peak_score = Column(Float, nullable=True)
    peak_at = Column(DateTime(timezone=True), nullable=True)
    metadata_ = Column("metadata", JSONB, nullable=True, default={})
    tags = Column(JSONB, nullable=True, default=[])

    # Relationships
    category = relationship("Category", back_populates="trends")
    signal_events = relationship("SignalEvent", back_populates="trend")

    def __repr__(self):
        return f"<Trend(id={self.id}, name='{self.name}', status='{self.status}')>"
