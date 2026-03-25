from datetime import datetime, timezone, timedelta
import math

class VelocityCalculator:
    """Calculates velocity and acceleration from time-series signal data."""

    def calculate_velocity(
        self,
        signal_counts: list[dict],
        hours: int = 24,
    ) -> float:
        """
        Calculate velocity (rate of change) over a time window.

        Velocity = (recent_count - older_count) / older_count
        Returns percentage change (e.g., 1.5 = 150% growth).
        """
        if len(signal_counts) < 2:
            return 0.0

        now = datetime.now(timezone.utc)
        cutoff = now - timedelta(hours=hours)
        midpoint = now - timedelta(hours=hours / 2)

        # Split into two halves
        first_half = [s for s in signal_counts if self._get_ts(s) < midpoint and self._get_ts(s) >= cutoff]
        second_half = [s for s in signal_counts if self._get_ts(s) >= midpoint]

        first_count = sum(s.get("count", 1) for s in first_half) if first_half else 0
        second_count = sum(s.get("count", 1) for s in second_half) if second_half else 0

        if first_count == 0:
            return second_count * 1.0 if second_count > 0 else 0.0

        return (second_count - first_count) / first_count

    def calculate_acceleration(self, signal_counts: list[dict]) -> float:
        """
        Calculate acceleration (change in velocity over time).

        Positive = velocity increasing (trend accelerating)
        Negative = velocity decreasing (trend decelerating)
        """
        if len(signal_counts) < 4:
            return 0.0

        # Compare recent velocity vs older velocity
        recent_velocity = self.calculate_velocity(signal_counts, hours=6)
        older_velocity = self.calculate_velocity(signal_counts, hours=24)

        if abs(older_velocity) < 0.01:
            return recent_velocity

        return recent_velocity - older_velocity

    def calculate_momentum(self, signal_counts: list[dict]) -> float:
        """
        Calculate momentum: weighted sum of recent signals.
        More recent signals contribute more to momentum.
        """
        if not signal_counts:
            return 0.0

        now = datetime.now(timezone.utc)
        total_momentum = 0.0

        for s in signal_counts:
            ts = self._get_ts(s)
            age_hours = max((now - ts).total_seconds() / 3600, 0.1)
            count = s.get("count", 1)
            score = s.get("score", 50)

            # Exponential decay: recent signals matter much more
            weight = math.exp(-age_hours / 12)  # Half-life of ~12 hours
            total_momentum += count * score * weight / 100

        return total_momentum

    def _get_ts(self, entry: dict) -> datetime:
        """Extract timestamp from signal count entry."""
        ts = entry.get("timestamp")
        if isinstance(ts, datetime):
            return ts
        if isinstance(ts, str):
            try:
                return datetime.fromisoformat(ts)
            except Exception:
                pass
        return datetime.now(timezone.utc)
