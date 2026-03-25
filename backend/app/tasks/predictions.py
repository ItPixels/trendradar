"""Prediction generation and evaluation tasks."""
import logging
from app.tasks.celery_app import celery_app
from app.core.predictor.engine import PredictionEngine

logger = logging.getLogger(__name__)


@celery_app.task(name="app.tasks.predictions.generate_predictions")
def generate_predictions():
    """Generate predictions for trends that qualify."""
    logger.info("Generating predictions for qualifying trends...")

    engine = PredictionEngine()

    # TODO: Fetch qualifying trends (high correlation + velocity)
    # trends = fetch_qualifying_trends(min_correlation=30, min_velocity=0.1)
    # for trend in trends:
    #     correlation_data = get_trend_correlation(trend.id)
    #     velocity_data = get_trend_velocity(trend.id)
    #     prediction = engine.predict(
    #         trend_data=trend.to_dict(),
    #         correlation_data=correlation_data,
    #         velocity_data=velocity_data,
    #         timeframe_hours=24,
    #     )
    #     store_prediction(trend.id, prediction)

    return {"status": "completed"}


@celery_app.task(name="app.tasks.predictions.generate_single")
def generate_single_prediction(
    trend_data: dict,
    correlation_data: dict,
    velocity_data: dict,
    timeframe_hours: int = 24,
):
    """Generate a prediction for a single trend."""
    engine = PredictionEngine()
    prediction = engine.predict(
        trend_data=trend_data,
        correlation_data=correlation_data,
        velocity_data=velocity_data,
        timeframe_hours=timeframe_hours,
    )

    logger.info(
        f"Prediction for '{trend_data.get('topic', 'unknown')}': "
        f"growth={prediction['predicted_growth']}%, confidence={prediction['confidence_score']}%"
    )

    return prediction


@celery_app.task(name="app.tasks.predictions.evaluate_expired")
def evaluate_expired():
    """Evaluate predictions whose timeframe has expired."""
    logger.info("Evaluating expired predictions...")

    # TODO: Fetch expired predictions and compare with actual outcomes
    # from app.core.predictor.evaluator import PredictionEvaluator
    # evaluator = PredictionEvaluator()
    # expired = fetch_expired_predictions()
    # actual = fetch_actual_trends(trend_ids)
    # results = await evaluator.evaluate_expired_predictions(expired, actual)
    # update_prediction_results(results)

    return {"status": "completed"}
