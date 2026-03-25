import uuid
from sqlalchemy import Column, String, DateTime, text
from sqlalchemy.dialects.postgresql import UUID, JSONB
from app.database import Base
from app.models.base import TimestampMixin


class User(Base, TimestampMixin):
    """Maps to Supabase auth.users with additional profile data."""
    __tablename__ = "user_profiles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    supabase_user_id = Column(UUID(as_uuid=True), unique=True, nullable=False, index=True)
    email = Column(String(255), nullable=False, index=True)
    full_name = Column(String(255), nullable=True)
    avatar_url = Column(String(1000), nullable=True)
    subscription_tier = Column(String(50), nullable=False, default="free", server_default="free")
    stripe_customer_id = Column(String(255), nullable=True, unique=True)
    stripe_subscription_id = Column(String(255), nullable=True, unique=True)
    preferences = Column(JSONB, nullable=True, default={})
    last_login_at = Column(DateTime(timezone=True), nullable=True)

    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}', tier='{self.subscription_tier}')>"
