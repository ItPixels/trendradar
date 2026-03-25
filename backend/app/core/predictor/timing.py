from datetime import datetime, timezone, timedelta

class PeakTimingEstimator:
    """Estimates when a trend will peak."""

    def estimate(
        self,
        velocity_data: dict,
        predicted_growth: float,
        timeframe_hours: int = 24,
    ) -> dict:
        """
        Estimate peak timing based on velocity and acceleration.

        Logic:
        - If accelerating: peak is further out
        - If decelerating but still positive: peak is soon
        - If negative velocity: already peaked
        """
        now = datetime.now(timezone.utc)
        velocity = velocity_data.get("velocity_24h", 0)
        acceleration = velocity_data.get("acceleration", 0)
        phase = velocity_data.get("phase", "unknown")

        if phase == "declining" or phase == "dead":
            return {
                "peak_at": None,
                "confidence": 30,
                "status": "already_peaked",
            }

        if phase == "peaking":
            # Peak is imminent or happening now
            peak_hours = max(1, timeframe_hours * 0.1)
            return {
                "peak_at": (now + timedelta(hours=peak_hours)).isoformat(),
                "confidence": 60,
                "status": "peaking_now",
            }

        # For emerging and active trends
        if acceleration > 0.5:
            # Strongly accelerating: peak is late in the timeframe
            peak_hours = timeframe_hours * 0.7
            confidence = 50
        elif acceleration > 0:
            # Moderately accelerating
            peak_hours = timeframe_hours * 0.5
            confidence = 45
        elif velocity > 0:
            # Growing but decelerating
            peak_hours = timeframe_hours * 0.3
            confidence = 40
        else:
            peak_hours = timeframe_hours * 0.2
            confidence = 25

        # Higher growth predictions push peak further out
        if predicted_growth > 200:
            peak_hours *= 1.3

        peak_at = now + timedelta(hours=min(peak_hours, timeframe_hours))

        return {
            "peak_at": peak_at.isoformat(),
            "confidence": confidence,
            "status": "predicted",
        }
