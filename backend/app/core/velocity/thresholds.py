class VelocityThresholds:
    """Classifies trend phase based on velocity and acceleration."""

    # Phase thresholds
    EMERGING_VELOCITY = 0.3    # 30% growth
    ACTIVE_VELOCITY = 0.1     # 10% growth
    PEAKING_VELOCITY = 0.02   # Near zero but still positive
    DECLINING_THRESHOLD = -0.1 # Negative velocity

    def classify_phase(
        self,
        velocity_24h: float,
        acceleration: float,
        current_score: float = 0,
    ) -> str:
        """
        Classify the current phase of a trend.

        Phases:
        - emerging: Low score, high velocity, positive acceleration
        - active: Moderate score, positive velocity
        - peaking: High score, low velocity, decelerating
        - declining: Negative velocity
        - dead: Very negative velocity, low score
        """
        if velocity_24h > self.EMERGING_VELOCITY and acceleration > 0 and current_score < 60:
            return "emerging"

        if velocity_24h > self.ACTIVE_VELOCITY:
            if acceleration > 0.1:
                return "emerging"  # Still accelerating
            return "active"

        if velocity_24h > self.PEAKING_VELOCITY:
            if acceleration < -0.05:
                return "peaking"  # Slowing down
            return "active"

        if velocity_24h > self.DECLINING_THRESHOLD:
            return "peaking"

        if velocity_24h > -0.5:
            return "declining"

        return "dead"
