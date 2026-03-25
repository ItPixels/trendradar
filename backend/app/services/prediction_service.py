"""Prediction service — business logic for predictions."""
import logging
from typing import Optional
from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.prediction import Prediction

logger = logging.getLogger(__name__)


class PredictionService:
    """Business logic for prediction operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_predictions(
        self,
        status: Optional[str] = None,
        min_confidence: float = 0,
        limit: int = 20,
        offset: int = 0,
    ) -> list[Prediction]:
        """Get predictions with filters."""
        query = select(Prediction)

        if status:
            query = query.where(Prediction.status == status)

        if min_confidence > 0:
            query = query.where(Prediction.confidence_score >= min_confidence)

        query = query.order_by(desc(Prediction.confidence_score))
        query = query.limit(limit).offset(offset)

        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def get_prediction_for_trend(self, trend_id: str) -> Optional[Prediction]:
        """Get the latest prediction for a trend."""
        result = await self.db.execute(
            select(Prediction)
            .where(Prediction.trend_id == trend_id)
            .order_by(desc(Prediction.created_at))
            .limit(1)
        )
        return result.scalar_one_or_none()

    async def get_predictions_for_trend(self, trend_id: str) -> list[Prediction]:
        """Get all predictions for a trend."""
        result = await self.db.execute(
            select(Prediction)
            .where(Prediction.trend_id == trend_id)
            .order_by(desc(Prediction.created_at))
        )
        return list(result.scalars().all())
