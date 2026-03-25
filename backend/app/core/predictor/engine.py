import logging
from datetime import datetime, timezone, timedelta
from typing import Optional
from app.core.predictor.features import FeatureExtractor
from app.core.predictor.confidence import ConfidenceCalculator
from app.core.predictor.timing import PeakTimingEstimator

logger = logging.getLogger(__name__)

class PredictionEngine:
    """
    Predicts future trend growth based on signal features.

    Uses a combination of:
    1. Feature-based scoring (velocity, correlation, source patterns)
    2. Historical pattern matching
    3. AI reasoning (Claude) for context and nuance
    """

    def __init__(self):
        self.feature_extractor = FeatureExtractor()
        self.confidence_calculator = ConfidenceCalculator()
        self.timing_estimator = PeakTimingEstimator()

    def predict(
        self,
        trend_data: dict,
        correlation_data: dict,
        velocity_data: dict,
        timeframe_hours: int = 24,
    ) -> dict:
        """
        Generate a prediction for a trend.

        Args:
            trend_data: Current trend info (topic, score, sources, etc.)
            correlation_data: Output from CorrelationEngine
            velocity_data: Output from VelocityAnalyzer
            timeframe_hours: Prediction timeframe (24, 48, or 72 hours)

        Returns:
            Prediction dict with growth, confidence, factors, timing
        """
        # Extract ML features
        features = self.feature_extractor.extract(
            trend_data=trend_data,
            correlation_data=correlation_data,
            velocity_data=velocity_data,
        )

        # Calculate predicted growth
        predicted_growth = self._calculate_growth(features, timeframe_hours)

        # Calculate confidence score
        confidence = self.confidence_calculator.calculate(features, predicted_growth)

        # Estimate peak timing
        peak_timing = self.timing_estimator.estimate(
            velocity_data=velocity_data,
            predicted_growth=predicted_growth,
            timeframe_hours=timeframe_hours,
        )

        # Extract key factors driving the prediction
        factors = self._extract_factors(features, correlation_data, velocity_data)

        return {
            "predicted_growth": round(predicted_growth, 1),
            "confidence_score": round(confidence, 1),
            "timeframe_hours": timeframe_hours,
            "predicted_peak_at": peak_timing.get("peak_at"),
            "peak_confidence": peak_timing.get("confidence"),
            "factors": factors,
            "features": features,
            "model_version": "v1",
        }

    def _calculate_growth(self, features: dict, timeframe_hours: int) -> float:
        """
        Calculate predicted growth percentage based on features.

        Uses a weighted formula combining key signals.
        """
        # Feature weights for growth prediction
        velocity_weight = 0.30
        correlation_weight = 0.25
        acceleration_weight = 0.20
        source_weight = 0.15
        momentum_weight = 0.10

        velocity_factor = features.get("velocity_score", 0) * velocity_weight
        correlation_factor = features.get("correlation_score", 0) * correlation_weight
        acceleration_factor = max(0, features.get("acceleration", 0)) * 100 * acceleration_weight
        source_factor = min(features.get("source_count", 0) * 10, 50) * source_weight
        momentum_factor = min(features.get("momentum", 0) * 10, 50) * momentum_weight

        # Base growth prediction (as percentage)
        base_growth = (
            velocity_factor + correlation_factor + acceleration_factor +
            source_factor + momentum_factor
        )

        # Apply timeframe scaling
        # Longer timeframes have more room for growth but more uncertainty
        if timeframe_hours == 72:
            base_growth *= 2.5
        elif timeframe_hours == 48:
            base_growth *= 1.8

        # Apply correlation multiplier if present
        multiplier = features.get("correlation_multiplier", 1.0)
        base_growth *= multiplier

        # Cap at reasonable bounds
        return min(max(base_growth, -50), 1000)

    def _extract_factors(
        self,
        features: dict,
        correlation_data: dict,
        velocity_data: dict,
    ) -> list[dict]:
        """Extract the key factors driving the prediction."""
        factors = []

        # Velocity factor
        velocity = velocity_data.get("velocity_24h", 0)
        if velocity > 0:
            impact = "positive"
            if velocity > 1.0:
                desc = f"Signal velocity extremely high ({velocity:.0%} growth rate)"
                weight = 0.9
            elif velocity > 0.3:
                desc = f"Signal velocity accelerating ({velocity:.0%} growth rate)"
                weight = 0.7
            else:
                desc = f"Signal velocity positive ({velocity:.0%} growth rate)"
                weight = 0.4
        else:
            impact = "negative"
            desc = f"Signal velocity declining ({velocity:.0%})"
            weight = abs(velocity) * 0.5

        factors.append({
            "factor": "Signal Velocity",
            "impact": impact,
            "weight": round(min(weight, 1.0), 2),
            "description": desc,
            "source_type": "velocity",
        })

        # Cross-source correlation
        source_count = correlation_data.get("source_count", 0)
        if source_count >= 3:
            factors.append({
                "factor": "Cross-Source Correlation",
                "impact": "positive",
                "weight": min(source_count * 0.15, 0.9),
                "description": f"Detected across {source_count} independent sources simultaneously",
                "source_type": "correlation",
            })

        # Pattern match
        pattern = correlation_data.get("pattern")
        if pattern:
            factors.append({
                "factor": f"Pattern: {pattern['label']}",
                "impact": "positive",
                "weight": 0.7,
                "description": pattern["description"],
                "source_type": "pattern",
            })

        # Acceleration
        accel = velocity_data.get("acceleration", 0)
        if accel > 0.1:
            factors.append({
                "factor": "Trend Acceleration",
                "impact": "positive",
                "weight": min(accel * 0.5, 0.8),
                "description": "Growth rate is itself increasing — exponential pattern",
                "source_type": "acceleration",
            })
        elif accel < -0.1:
            factors.append({
                "factor": "Trend Deceleration",
                "impact": "negative",
                "weight": min(abs(accel) * 0.3, 0.5),
                "description": "Growth rate is slowing down",
                "source_type": "acceleration",
            })

        # Sort by weight descending
        factors.sort(key=lambda f: f["weight"], reverse=True)

        return factors
