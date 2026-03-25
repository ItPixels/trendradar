"""
Prediction calibrator — adjusts prediction model based on past accuracy.

In production, this would compare predictions against actual outcomes
and adjust weights accordingly. For MVP, it tracks prediction results.
"""

class PredictionCalibrator:
    """Tracks and adjusts prediction accuracy over time."""

    def evaluate_prediction(
        self,
        predicted_growth: float,
        actual_growth: float,
        confidence: float,
    ) -> dict:
        """
        Evaluate a past prediction against actual results.

        Returns evaluation metrics.
        """
        error = abs(predicted_growth - actual_growth)
        relative_error = error / max(abs(predicted_growth), 1)

        # Determine accuracy classification
        if relative_error < 0.2:
            status = "correct"
        elif relative_error < 0.5:
            status = "partially_correct"
        else:
            status = "incorrect"

        # Direction accuracy (did we predict the right direction?)
        direction_correct = (
            (predicted_growth > 0 and actual_growth > 0) or
            (predicted_growth < 0 and actual_growth < 0) or
            (predicted_growth == 0 and actual_growth == 0)
        )

        return {
            "status": status,
            "predicted_growth": predicted_growth,
            "actual_growth": actual_growth,
            "error": round(error, 2),
            "relative_error": round(relative_error, 4),
            "direction_correct": direction_correct,
            "confidence_was": confidence,
        }
