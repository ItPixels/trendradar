"""
Prediction evaluator — runs periodic evaluation of past predictions.
"""
from datetime import datetime, timezone, timedelta
from app.core.predictor.calibrator import PredictionCalibrator

class PredictionEvaluator:
    """Evaluates past predictions against actual outcomes."""

    def __init__(self):
        self.calibrator = PredictionCalibrator()

    async def evaluate_expired_predictions(
        self,
        predictions: list[dict],
        actual_trends: dict[str, dict],
    ) -> list[dict]:
        """
        Evaluate predictions whose timeframe has expired.

        Args:
            predictions: List of prediction dicts with trend_id, predicted_growth, etc.
            actual_trends: Dict mapping trend_id -> current trend data

        Returns:
            List of evaluation results
        """
        results = []

        for prediction in predictions:
            trend_id = prediction.get("trend_id")
            if not trend_id or trend_id not in actual_trends:
                continue

            actual = actual_trends[trend_id]

            # Calculate actual growth
            initial_score = prediction.get("initial_score", 0)
            current_score = actual.get("trend_score", 0)

            if initial_score > 0:
                actual_growth = ((current_score - initial_score) / initial_score) * 100
            else:
                actual_growth = current_score * 10  # Rough estimate

            evaluation = self.calibrator.evaluate_prediction(
                predicted_growth=prediction.get("predicted_growth", 0),
                actual_growth=actual_growth,
                confidence=prediction.get("confidence_score", 0),
            )
            evaluation["prediction_id"] = prediction.get("id")
            evaluation["trend_id"] = trend_id

            results.append(evaluation)

        return results
