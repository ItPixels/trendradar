"""Track user feature usage for plan limits."""
from datetime import date
from typing import Optional

class UsageTracker:
    """Track and enforce usage limits."""

    async def check_and_increment(
        self,
        user_id: str,
        feature: str,
        limit: int,
    ) -> bool:
        """
        Check if usage is within limits and increment counter.
        Returns True if allowed, False if limit exceeded.
        """
        if limit == -1:  # Unlimited
            return True

        # TODO: Implement with Redis for fast atomic operations
        # current = await redis.get(f"usage:{user_id}:{feature}:{date.today()}")
        # if int(current or 0) >= limit:
        #     return False
        # await redis.incr(f"usage:{user_id}:{feature}:{date.today()}")
        # await redis.expire(f"usage:{user_id}:{feature}:{date.today()}", 86400)

        return True

usage_tracker = UsageTracker()
