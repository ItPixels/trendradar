"""Alert service — CRUD and matching logic for alerts."""
import logging
from typing import Optional
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.alert import Alert

logger = logging.getLogger(__name__)


class AlertService:
    """Business logic for alert operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_user_alerts(self, user_id: str) -> list[Alert]:
        """Get all alerts for a user."""
        result = await self.db.execute(
            select(Alert).where(
                and_(Alert.user_id == user_id, Alert.deleted_at.is_(None))
            ).order_by(Alert.created_at.desc())
        )
        return list(result.scalars().all())

    async def get_alert(self, alert_id: str, user_id: str) -> Optional[Alert]:
        """Get a single alert."""
        result = await self.db.execute(
            select(Alert).where(
                and_(
                    Alert.id == alert_id,
                    Alert.user_id == user_id,
                    Alert.deleted_at.is_(None),
                )
            )
        )
        return result.scalar_one_or_none()

    async def create_alert(self, user_id: str, **kwargs) -> Alert:
        """Create a new alert."""
        alert = Alert(user_id=user_id, **kwargs)
        self.db.add(alert)
        await self.db.flush()
        return alert

    async def update_alert(self, alert_id: str, user_id: str, **kwargs) -> Optional[Alert]:
        """Update an alert."""
        alert = await self.get_alert(alert_id, user_id)
        if not alert:
            return None

        for key, value in kwargs.items():
            if hasattr(alert, key) and value is not None:
                setattr(alert, key, value)

        await self.db.flush()
        return alert

    async def delete_alert(self, alert_id: str, user_id: str) -> bool:
        """Soft-delete an alert."""
        alert = await self.get_alert(alert_id, user_id)
        if not alert:
            return False

        from datetime import datetime, timezone
        alert.deleted_at = datetime.now(timezone.utc)
        await self.db.flush()
        return True

    async def toggle_alert(self, alert_id: str, user_id: str) -> Optional[Alert]:
        """Toggle alert active/inactive."""
        alert = await self.get_alert(alert_id, user_id)
        if not alert:
            return None

        alert.is_active = not alert.is_active
        await self.db.flush()
        return alert
