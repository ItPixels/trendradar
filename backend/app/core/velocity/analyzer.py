import logging
from datetime import datetime, timezone, timedelta
from app.core.velocity.calculator import VelocityCalculator
from app.core.velocity.scorer import VelocityScorer
from app.core.velocity.thresholds import VelocityThresholds

logger = logging.getLogger(__name__)

class VelocityAnalyzer:
    """
    Analyzes the velocity (rate of change) of trend signals over time.

    Velocity is key for predictions: it's not about how popular something IS,
    but how FAST it's growing. A topic with moderate popularity but accelerating
    velocity is more likely to trend than an already-popular but plateauing topic.
    """

    def __init__(self):
        self.calculator = VelocityCalculator()
        self.scorer = VelocityScorer()
        self.thresholds = VelocityThresholds()

    def analyze(
        self,
        signal_counts: list[dict],
        current_score: float = 0,
    ) -> dict:
        """
        Analyze velocity from a time series of signal counts.

        Args:
            signal_counts: List of {"timestamp": datetime, "count": int, "score": float}
                          ordered chronologically
            current_score: Current trend score for context

        Returns:
            Dict with velocity metrics, acceleration, and classification
        """
        if len(signal_counts) < 2:
            return self._empty_result()

        # Calculate velocities for different time windows
        velocity_1h = self.calculator.calculate_velocity(signal_counts, hours=1)
        velocity_6h = self.calculator.calculate_velocity(signal_counts, hours=6)
        velocity_24h = self.calculator.calculate_velocity(signal_counts, hours=24)

        # Calculate acceleration (change in velocity)
        acceleration = self.calculator.calculate_acceleration(signal_counts)

        # Calculate momentum
        momentum = self.calculator.calculate_momentum(signal_counts)

        # Score the velocity (0-100)
        velocity_score = self.scorer.score(
            velocity_1h=velocity_1h,
            velocity_6h=velocity_6h,
            velocity_24h=velocity_24h,
            acceleration=acceleration,
        )

        # Classify the trend phase
        phase = self.thresholds.classify_phase(
            velocity_24h=velocity_24h,
            acceleration=acceleration,
            current_score=current_score,
        )

        return {
            "velocity_1h": round(velocity_1h, 4),
            "velocity_6h": round(velocity_6h, 4),
            "velocity_24h": round(velocity_24h, 4),
            "acceleration": round(acceleration, 4),
            "momentum": round(momentum, 4),
            "velocity_score": round(velocity_score, 2),
            "phase": phase,
            "is_accelerating": acceleration > 0,
            "is_decelerating": acceleration < -0.1,
        }

    def _empty_result(self) -> dict:
        return {
            "velocity_1h": 0,
            "velocity_6h": 0,
            "velocity_24h": 0,
            "acceleration": 0,
            "momentum": 0,
            "velocity_score": 0,
            "phase": "unknown",
            "is_accelerating": False,
            "is_decelerating": False,
        }
