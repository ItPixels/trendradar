class VelocityScorer:
    """Scores velocity metrics into a 0-100 composite score."""

    def score(
        self,
        velocity_1h: float = 0,
        velocity_6h: float = 0,
        velocity_24h: float = 0,
        acceleration: float = 0,
    ) -> float:
        """
        Calculate composite velocity score (0-100).

        Weights recent velocity more heavily.
        Acceleration bonus for rapidly growing trends.
        """
        # Normalize each velocity to 0-25 range
        v1h_score = min(25, max(0, velocity_1h * 10))   # 250% growth/hr = max
        v6h_score = min(20, max(0, velocity_6h * 8))    # 250% growth/6hr = max
        v24h_score = min(15, max(0, velocity_24h * 5))   # 300% growth/day = max

        # Acceleration bonus (0-20)
        accel_score = 0
        if acceleration > 0:
            accel_score = min(20, acceleration * 15)

        # Base score (0-20) to prevent zero for any signal
        base = 10

        total = base + v1h_score + v6h_score + v24h_score + accel_score

        return min(100, max(0, total))
