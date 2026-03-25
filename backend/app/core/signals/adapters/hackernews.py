import httpx
from datetime import datetime, timezone
from app.core.signals.base import BaseSignalAdapter, RawSignal

HN_API = "https://hacker-news.firebaseio.com/v0"


class HackerNewsAdapter(BaseSignalAdapter):
    source_name = "hackernews"
    weight = 0.85
    tier = 1

    async def fetch_signals(self) -> list[RawSignal]:
        signals = []
        async with httpx.AsyncClient(timeout=30) as client:
            # Get top story IDs
            resp = await client.get(f"{HN_API}/topstories.json")
            story_ids = resp.json()[:30]  # Top 30

            # Fetch each story
            for position, story_id in enumerate(story_ids):
                try:
                    resp = await client.get(f"{HN_API}/item/{story_id}.json")
                    item = resp.json()
                    if not item or item.get("type") != "story":
                        continue

                    score = item.get("score", 0)
                    comments = item.get("descendants", 0)
                    created = datetime.fromtimestamp(item.get("time", 0), tz=timezone.utc)
                    age_hours = max((datetime.now(timezone.utc) - created).total_seconds() / 3600, 0.1)

                    # Signal strength: score velocity + position bonus + comment engagement
                    score_velocity = score / age_hours
                    position_bonus = max(0, (30 - position) / 30)  # Higher for top positions
                    comment_ratio = comments / max(score, 1)

                    strength = min(100, (
                        score_velocity * 0.4 +
                        position_bonus * 30 +
                        comment_ratio * 20 +
                        min(score / 10, 30)
                    ))

                    signals.append(RawSignal(
                        source="hackernews",
                        source_id=str(story_id),
                        title=item.get("title", ""),
                        url=item.get("url", f"https://news.ycombinator.com/item?id={story_id}"),
                        content=None,
                        metrics={
                            "score": score,
                            "comments": comments,
                            "position": position,
                            "score_velocity": round(score_velocity, 2),
                            "age_hours": round(age_hours, 2),
                        },
                        detected_at=created,
                        signal_strength=round(strength, 2),
                    ))
                except Exception:
                    continue

        return signals

    async def health_check(self) -> bool:
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                resp = await client.get(f"{HN_API}/topstories.json")
                return resp.status_code == 200
        except Exception:
            return False
