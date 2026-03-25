class FeatureExtractor:
    """Extracts ML features from trend, correlation, and velocity data."""

    def extract(
        self,
        trend_data: dict,
        correlation_data: dict,
        velocity_data: dict,
    ) -> dict:
        """
        Extract a feature vector from trend analysis data.

        Returns flat dict of numerical features used for prediction.
        """
        return {
            # Trend features
            "trend_score": trend_data.get("trend_score", 0),
            "signal_count_24h": trend_data.get("signal_count_24h", 0),
            "source_count": trend_data.get("source_count", correlation_data.get("source_count", 0)),

            # Velocity features
            "velocity_1h": velocity_data.get("velocity_1h", 0),
            "velocity_6h": velocity_data.get("velocity_6h", 0),
            "velocity_24h": velocity_data.get("velocity_24h", 0),
            "velocity_score": velocity_data.get("velocity_score", 0),
            "acceleration": velocity_data.get("acceleration", 0),
            "momentum": velocity_data.get("momentum", 0),
            "is_accelerating": 1 if velocity_data.get("is_accelerating") else 0,

            # Correlation features
            "correlation_score": correlation_data.get("correlation_score", 0),
            "correlation_multiplier": correlation_data.get("multiplier", 1.0),
            "is_correlated": 1 if correlation_data.get("is_correlated") else 0,
            "has_pattern": 1 if correlation_data.get("pattern") else 0,

            # Derived features
            "velocity_acceleration_product": (
                velocity_data.get("velocity_24h", 0) *
                max(velocity_data.get("acceleration", 0), 0)
            ),
            "source_velocity_product": (
                trend_data.get("source_count", 0) *
                velocity_data.get("velocity_24h", 0)
            ),
        }
