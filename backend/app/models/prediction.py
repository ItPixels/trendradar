import uuid
from sqlalchemy import Column, String, Text, Float, Integer, DateTime, ForeignKey, text
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from app.database import Base
from app.models.base import TimestampMixin


class Prediction(Base, TimestampMixin):
    __tablename__ = "predictions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, server_default=text("gen_random_uuid()"))
    trend_id = Column(UUID(as_uuid=True), ForeignKey("trends.id", ondelete="CASCADE"), nullable=False)
    predicted_growth = Column(Float, nullable=False)
    confidence_score = Column(Float, nullable=False, default=0, server_default="0")
    timeframe_hours = Column(Integer, nullable=False, default=24, server_default="24")
    predicted_peak_at = Column(DateTime(timezone=True), nullable=True)
    model_version = Column(String(50), default="v1", server_default="v1")
    input_features = Column(JSONB, nullable=True, default={})
    status = Column(String(50), default="pending", server_default="pending")
    actual_growth = Column(Float, nullable=True)
    evaluated_at = Column(DateTime(timezone=True), nullable=True)

    trend = relationship("Trend")

    def __repr__(self):
        return f"<Prediction(id={self.id}, trend_id={self.trend_id}, confidence={self.confidence_score})>"
