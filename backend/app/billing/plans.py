"""Subscription plan definitions."""

PLANS = {
    "free": {
        "name": "Free",
        "price_monthly": 0,
        "stripe_price_id": None,
        "limits": {
            "trends_per_day": 3,
            "briefs_per_day": 0,
            "alerts": 0,
            "prediction_hours": 0,
            "api_access": False,
            "export": False,
            "history_days": 0,
            "team_seats": 1,
        },
    },
    "creator": {
        "name": "Creator",
        "price_monthly": 1900,  # $19.00 in cents
        "stripe_price_id": "price_creator_monthly",
        "limits": {
            "trends_per_day": -1,
            "briefs_per_day": 5,
            "alerts": 3,
            "prediction_hours": 24,
            "api_access": False,
            "export": False,
            "history_days": 7,
            "team_seats": 1,
        },
    },
    "pro": {
        "name": "Pro",
        "price_monthly": 7900,  # $79.00
        "stripe_price_id": "price_pro_monthly",
        "limits": {
            "trends_per_day": -1,
            "briefs_per_day": -1,
            "alerts": -1,
            "prediction_hours": 72,
            "api_access": True,
            "export": True,
            "history_days": 30,
            "team_seats": 1,
        },
    },
    "business": {
        "name": "Business",
        "price_monthly": 29900,  # $299.00
        "stripe_price_id": "price_business_monthly",
        "limits": {
            "trends_per_day": -1,
            "briefs_per_day": -1,
            "alerts": -1,
            "prediction_hours": 72,
            "api_access": True,
            "export": True,
            "history_days": 90,
            "team_seats": 5,
        },
    },
}

def get_plan(plan_name: str) -> dict:
    return PLANS.get(plan_name, PLANS["free"])

def get_plan_limit(plan_name: str, limit_key: str):
    plan = get_plan(plan_name)
    return plan["limits"].get(limit_key, 0)
