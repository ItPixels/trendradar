"""Rate limiter for AI API calls to control costs."""
import time
import logging
from collections import defaultdict

logger = logging.getLogger(__name__)

class AIRateLimiter:
    """Simple in-memory rate limiter for AI API calls."""

    def __init__(self):
        self._calls: dict[str, list[float]] = defaultdict(list)

    def check_rate_limit(self, operation: str, max_per_hour: int) -> bool:
        """Check if an operation is within rate limits."""
        now = time.time()
        hour_ago = now - 3600

        # Clean old entries
        self._calls[operation] = [
            t for t in self._calls[operation] if t > hour_ago
        ]

        if len(self._calls[operation]) >= max_per_hour:
            logger.warning(f"Rate limit exceeded for {operation}: {len(self._calls[operation])}/{max_per_hour}")
            return False

        return True

    def record_call(self, operation: str):
        """Record an API call."""
        self._calls[operation].append(time.time())

    def get_usage(self, operation: str) -> dict:
        """Get current usage stats for an operation."""
        now = time.time()
        hour_ago = now - 3600

        recent = [t for t in self._calls[operation] if t > hour_ago]

        return {
            "operation": operation,
            "calls_last_hour": len(recent),
        }


ai_rate_limiter = AIRateLimiter()
