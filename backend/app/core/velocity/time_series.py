from datetime import datetime, timezone, timedelta
from typing import Optional

def bucket_signals(
    signals: list[dict],
    bucket_size_hours: int = 1,
    lookback_hours: int = 24,
) -> list[dict]:
    """
    Group signals into time buckets.

    Returns list of {"timestamp": datetime, "count": int, "avg_score": float}
    """
    now = datetime.now(timezone.utc)
    start = now - timedelta(hours=lookback_hours)

    # Create empty buckets
    buckets = {}
    current = start
    while current <= now:
        bucket_key = current.replace(minute=0, second=0, microsecond=0)
        buckets[bucket_key] = {"count": 0, "total_score": 0.0}
        current += timedelta(hours=bucket_size_hours)

    # Fill buckets
    for signal in signals:
        ts = signal.get("timestamp") or signal.get("detected_at")
        if isinstance(ts, str):
            try:
                ts = datetime.fromisoformat(ts)
            except Exception:
                continue

        if ts is None or ts < start:
            continue

        bucket_key = ts.replace(minute=0, second=0, microsecond=0)
        if bucket_key in buckets:
            buckets[bucket_key]["count"] += 1
            buckets[bucket_key]["total_score"] += signal.get("score", signal.get("signal_strength", 50))

    # Convert to list
    result = []
    for ts, data in sorted(buckets.items()):
        avg_score = data["total_score"] / max(data["count"], 1)
        result.append({
            "timestamp": ts,
            "count": data["count"],
            "score": round(avg_score, 2),
        })

    return result


def interpolate_missing(series: list[dict]) -> list[dict]:
    """Fill missing data points with linear interpolation."""
    if len(series) < 2:
        return series

    result = []
    for i, point in enumerate(series):
        result.append(point)
        if point["count"] == 0 and i > 0 and i < len(series) - 1:
            prev_count = series[i - 1]["count"]
            next_count = series[i + 1]["count"]
            result[-1]["count"] = (prev_count + next_count) // 2

    return result
