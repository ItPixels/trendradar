"""Predictions API endpoints — returns predictions with trend info."""
import logging
import traceback
from fastapi import APIRouter, Query
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from sqlalchemy import select, desc
from sqlalchemy.orm import joinedload
from app.database import _create_engine
from app.models.prediction import Prediction
from app.models.trend import Trend

logger = logging.getLogger(__name__)
router = APIRouter()


def _prediction_to_dict(pred: Prediction, trend: Optional[Trend] = None) -> dict:
    """Convert prediction + trend to API response dict."""
    factors = []
    features = {}
    if pred.input_features:
        factors = pred.input_features.get("factors", [])
        features = pred.input_features.get("features", {})

    result = {
        "id": str(pred.id),
        "trend_id": str(pred.trend_id),
        "predicted_growth": pred.predicted_growth,
        "confidence_score": pred.confidence_score,
        "timeframe_hours": pred.timeframe_hours,
        "predicted_peak_at": pred.predicted_peak_at.isoformat() if pred.predicted_peak_at else None,
        "model_version": pred.model_version,
        "status": pred.status,
        "factors": factors,
        "created_at": pred.created_at.isoformat() if pred.created_at else None,
    }

    if trend:
        result["trend"] = {
            "id": str(trend.id),
            "topic": trend.topic,
            "topic_slug": trend.topic_slug,
            "trend_score": trend.trend_score,
            "source_count": trend.source_count,
            "active_sources": trend.active_sources or [],
            "status": trend.status,
            "category_id": str(trend.category_id) if trend.category_id else None,
        }

    return result


@router.get("")
async def list_predictions(
    status: Optional[str] = Query(None),
    min_confidence: float = Query(0, ge=0, le=100),
    limit: int = Query(20, ge=1, le=50),
    offset: int = Query(0, ge=0),
):
    """Get predictions with filters, including trend info."""
    engine = _create_engine()
    session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    try:
        async with session_maker() as db:
            query = (
                select(Prediction, Trend)
                .join(Trend, Prediction.trend_id == Trend.id)
                .where(Trend.deleted_at.is_(None))
            )

            if status:
                query = query.where(Prediction.status == status)
            if min_confidence > 0:
                query = query.where(Prediction.confidence_score >= min_confidence)

            query = query.order_by(desc(Prediction.confidence_score))
            query = query.limit(limit).offset(offset)

            result = await db.execute(query)
            rows = result.all()

            items = [_prediction_to_dict(pred, trend) for pred, trend in rows]

            # Get total count
            count_query = select(Prediction)
            if status:
                count_query = count_query.where(Prediction.status == status)
            if min_confidence > 0:
                count_query = count_query.where(Prediction.confidence_score >= min_confidence)
            count_result = await db.execute(count_query)
            total = len(count_result.scalars().all())

            return {"items": items, "total": total, "limit": limit, "offset": offset}
    except Exception as e:
        logger.error(f"Predictions list error: {e}\n{traceback.format_exc()}")
        return {"items": [], "total": 0, "error": str(e)}
    finally:
        await engine.dispose()


@router.get("/trend/{trend_id}")
async def get_trend_predictions(trend_id: str):
    """Get all predictions for a specific trend."""
    engine = _create_engine()
    session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    try:
        async with session_maker() as db:
            result = await db.execute(
                select(Prediction)
                .where(Prediction.trend_id == trend_id)
                .order_by(desc(Prediction.created_at))
            )
            predictions = result.scalars().all()
            return {
                "items": [_prediction_to_dict(p) for p in predictions],
                "trend_id": trend_id,
            }
    finally:
        await engine.dispose()


@router.get("/trend/{trend_id}/latest")
async def get_latest_prediction(trend_id: str):
    """Get the latest prediction for a trend."""
    engine = _create_engine()
    session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    try:
        async with session_maker() as db:
            result = await db.execute(
                select(Prediction, Trend)
                .join(Trend, Prediction.trend_id == Trend.id)
                .where(Prediction.trend_id == trend_id)
                .order_by(desc(Prediction.created_at))
                .limit(1)
            )
            row = result.first()
            if not row:
                return {"error": "No prediction found", "status": 404}
            pred, trend = row
            return _prediction_to_dict(pred, trend)
    finally:
        await engine.dispose()
