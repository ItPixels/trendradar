"""Predictions API endpoints."""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from app.database import get_db
from app.services.prediction_service import PredictionService

router = APIRouter()


@router.get("")
async def list_predictions(
    status: Optional[str] = Query(None),
    min_confidence: float = Query(0, ge=0, le=100),
    limit: int = Query(20, ge=1, le=50),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db),
):
    """Get predictions with filters."""
    service = PredictionService(db)
    predictions = await service.get_predictions(
        status=status,
        min_confidence=min_confidence,
        limit=limit,
        offset=offset,
    )
    return {"items": predictions, "total": len(predictions)}


@router.get("/trend/{trend_id}")
async def get_trend_predictions(
    trend_id: str,
    db: AsyncSession = Depends(get_db),
):
    """Get all predictions for a specific trend."""
    service = PredictionService(db)
    predictions = await service.get_predictions_for_trend(trend_id)
    return {"items": predictions, "trend_id": trend_id}


@router.get("/trend/{trend_id}/latest")
async def get_latest_prediction(
    trend_id: str,
    db: AsyncSession = Depends(get_db),
):
    """Get the latest prediction for a trend."""
    service = PredictionService(db)
    prediction = await service.get_prediction_for_trend(trend_id)

    if not prediction:
        raise HTTPException(status_code=404, detail="No prediction found for this trend")

    return prediction
