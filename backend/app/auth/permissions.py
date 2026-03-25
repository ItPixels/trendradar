"""Permission checks based on user plan."""
from fastapi import HTTPException

PLAN_HIERARCHY = ["free", "creator", "pro", "business", "enterprise"]

def require_plan(user_plan: str, minimum_plan: str):
    """Check if user's plan meets the minimum requirement."""
    if PLAN_HIERARCHY.index(user_plan) < PLAN_HIERARCHY.index(minimum_plan):
        raise HTTPException(
            status_code=403,
            detail=f"This feature requires the {minimum_plan} plan or higher. "
                   f"Your current plan: {user_plan}",
        )

def check_daily_limit(current_count: int, limit: int, feature: str):
    """Check if user has exceeded daily limit."""
    if limit == -1:  # unlimited
        return
    if current_count >= limit:
        raise HTTPException(
            status_code=429,
            detail=f"Daily {feature} limit reached ({limit}). Upgrade your plan for more.",
        )
