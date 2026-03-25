class ConfidenceCalculator:
    """Calculates confidence scores for predictions."""

    def calculate(self, features: dict, predicted_growth: float) -> float:
        """
        Calculate prediction confidence (0-100).

        Higher confidence when:
        - More data sources confirm the trend
        - Velocity is consistent (not erratic)
        - Known correlation patterns match
        - Predicted growth is moderate (extreme predictions are less confident)
        """
        confidence = 0.0

        # Source count confidence (more sources = more confident)
        source_count = features.get("source_count", 0)
        source_confidence = min(source_count * 12, 35)  # Max 35 from sources
        confidence += source_confidence

        # Correlation confidence
        if features.get("is_correlated"):
            confidence += 15
        if features.get("has_pattern"):
            confidence += 10

        # Velocity consistency confidence
        v1h = features.get("velocity_1h", 0)
        v6h = features.get("velocity_6h", 0)
        v24h = features.get("velocity_24h", 0)

        # If all velocities point in same direction, higher confidence
        if v1h > 0 and v6h > 0 and v24h > 0:
            confidence += 15
        elif v1h < 0 and v6h < 0 and v24h < 0:
            confidence += 10  # Confident in decline too

        # Data volume confidence
        signal_count = features.get("signal_count_24h", 0)
        data_confidence = min(signal_count * 2, 15)
        confidence += data_confidence

        # Penalty for extreme predictions (less confident)
        if abs(predicted_growth) > 500:
            confidence *= 0.7
        elif abs(predicted_growth) > 300:
            confidence *= 0.85

        # Minimum confidence floor
        confidence = max(confidence, 5)

        return min(100, confidence)
