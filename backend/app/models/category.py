import uuid
import sqlalchemy
from sqlalchemy import Column, String, Text, Integer, ForeignKey, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.database import Base
from app.models.base import TimestampMixin


class Category(Base, TimestampMixin):
    __tablename__ = "categories"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, server_default=text("gen_random_uuid()"))
    name = Column(String(255), nullable=False, unique=True)
    slug = Column(String(255), nullable=False, unique=True, index=True)
    description = Column(Text, nullable=True)
    icon = Column(String(100), nullable=True)
    color = Column(String(50), nullable=True, default="#6366f1")
    parent_id = Column(UUID(as_uuid=True), ForeignKey("categories.id"), nullable=True)
    sort_order = Column(Integer, nullable=False, default=0, server_default="0")
    is_default = Column(sqlalchemy.Boolean, default=False)
    is_active = Column(sqlalchemy.Boolean, default=True)

    # Relationships
    parent = relationship("Category", remote_side="Category.id", backref="children")
    trends = relationship("Trend", back_populates="category")

    def __repr__(self):
        return f"<Category(id={self.id}, name='{self.name}')>"
