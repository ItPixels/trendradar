import uuid
from datetime import datetime
from sqlalchemy import Column, DateTime, text
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base


class TimestampMixin:
    created_at = Column(DateTime(timezone=True), server_default=text("NOW()"), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=text("NOW()"), onupdate=datetime.utcnow, nullable=False)


class SoftDeleteMixin:
    deleted_at = Column(DateTime(timezone=True), nullable=True)
