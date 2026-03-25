import httpx
import feedparser
from datetime import datetime, timezone
from app.core.signals.base import BaseSignalAdapter, RawSignal

PYPI_RSS = "https://pypi.org/rss/updates.xml"
PYPISTATS_API = "https://pypistats.org/api"

# Key packages to monitor for activity
TRACKED_PACKAGES = [
    "anthropic", "openai", "langchain", "transformers", "torch",
    "fastapi", "django", "flask", "pydantic", "sqlalchemy",
    "numpy", "pandas", "scikit-learn", "tensorflow", "keras",
    "httpx", "uvicorn", "celery", "redis", "boto3",
]


class PyPIStatsAdapter(BaseSignalAdapter):
    source_name = "pypi_stats"
    weight = 0.65
    tier = 2

    async def fetch_signals(self) -> list[RawSignal]:
        signals = []

        async with httpx.AsyncClient(timeout=30) as client:
            # 1. Fetch recent updates via RSS
            try:
                resp = await client.get(PYPI_RSS)
                if resp.status_code == 200:
                    feed = feedparser.parse(resp.text)
                    seen = set()
                    for position, entry in enumerate(feed.entries[:30]):
                        title = entry.get("title", "")
                        # Format: "package X.Y.Z"
                        pkg_name = title.split(" ")[0] if " " in title else title
                        if pkg_name in seen:
                            continue
                        seen.add(pkg_name)

                        link = entry.get("link", "")
                        summary = entry.get("summary", "")

                        strength = max(20, 50 - position)

                        signals.append(RawSignal(
                            source="pypi_stats",
                            source_id=f"update:{pkg_name}",
                            title=title,
                            url=link,
                            content=summary[:300] if summary else None,
                            metrics={
                                "type": "recent_update",
                                "position": position,
                                "package": pkg_name,
                            },
                            signal_strength=round(strength, 2),
                            detected_at=datetime.now(timezone.utc),
                        ))
            except Exception:
                pass

            # 2. Check download stats for tracked packages
            for pkg_name in TRACKED_PACKAGES:
                try:
                    resp = await client.get(
                        f"{PYPISTATS_API}/packages/{pkg_name}/recent",
                        headers={"Accept": "application/json"},
                    )
                    if resp.status_code != 200:
                        continue

                    data = resp.json().get("data", {})
                    last_day = data.get("last_day", 0)
                    last_week = data.get("last_week", 0)
                    last_month = data.get("last_month", 0)

                    # Calculate velocity: compare daily rate vs monthly average
                    monthly_daily_avg = last_month / 30 if last_month > 0 else 1
                    velocity = last_day / monthly_daily_avg if monthly_daily_avg > 0 else 1

                    strength = min(100, (
                        min(last_day / 50000, 30) +
                        min(velocity * 10, 40) +
                        15
                    ))

                    signals.append(RawSignal(
                        source="pypi_stats",
                        source_id=f"stats:{pkg_name}",
                        title=f"{pkg_name} — {last_day:,} downloads today",
                        url=f"https://pypi.org/project/{pkg_name}/",
                        metrics={
                            "type": "download_stats",
                            "downloads_day": last_day,
                            "downloads_week": last_week,
                            "downloads_month": last_month,
                            "velocity": round(velocity, 2),
                            "package": pkg_name,
                        },
                        signal_strength=round(strength, 2),
                        detected_at=datetime.now(timezone.utc),
                    ))
                except Exception:
                    continue

        return signals

    async def health_check(self) -> bool:
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                resp = await client.get(f"{PYPISTATS_API}/packages/numpy/recent")
                return resp.status_code == 200
        except Exception:
            return False
