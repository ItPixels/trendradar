import httpx
from datetime import datetime, timezone
from app.core.signals.base import BaseSignalAdapter, RawSignal

DEVTO_API = "https://dev.to/api"


class DevToAdapter(BaseSignalAdapter):
    source_name = "devto"
    weight = 0.55
    tier = 2

    async def fetch_signals(self) -> list[RawSignal]:
        signals = []
        seen_ids = set()

        async with httpx.AsyncClient(timeout=30) as client:
            # Fetch top articles for today and rising
            endpoints = [
                {"path": "/articles", "params": {"top": 1, "per_page": 25}, "label": "top_today"},
                {"path": "/articles", "params": {"state": "rising", "per_page": 25}, "label": "rising"},
            ]

            for endpoint in endpoints:
                try:
                    resp = await client.get(
                        f"{DEVTO_API}{endpoint['path']}",
                        params=endpoint["params"],
                    )
                    if resp.status_code != 200:
                        continue

                    articles = resp.json()

                    for position, article in enumerate(articles):
                        article_id = article.get("id")
                        if not article_id or article_id in seen_ids:
                            continue
                        seen_ids.add(article_id)

                        reactions = article.get("positive_reactions_count", 0)
                        comments = article.get("comments_count", 0)
                        reading_time = article.get("reading_time_minutes", 0)
                        tags = article.get("tag_list", [])

                        published = article.get("published_at", "")
                        try:
                            pub_dt = datetime.fromisoformat(published.replace("Z", "+00:00"))
                        except Exception:
                            pub_dt = datetime.now(timezone.utc)

                        age_hours = max((datetime.now(timezone.utc) - pub_dt).total_seconds() / 3600, 0.1)

                        reaction_velocity = reactions / age_hours

                        reaction_score = min(reactions / 5, 25)
                        velocity_score = min(reaction_velocity * 2, 25)
                        comment_score = min(comments * 2, 20)
                        position_score = max(0, (25 - position) / 25) * 15
                        rising_bonus = 10 if endpoint["label"] == "rising" else 0

                        strength = min(100, reaction_score + velocity_score + comment_score + position_score + rising_bonus)

                        signals.append(RawSignal(
                            source="devto",
                            source_id=str(article_id),
                            title=article.get("title", ""),
                            url=article.get("url", ""),
                            content=article.get("description", "")[:500],
                            metrics={
                                "reactions": reactions,
                                "comments": comments,
                                "reading_time": reading_time,
                                "tags": tags,
                                "user": article.get("user", {}).get("username", ""),
                                "type": endpoint["label"],
                                "age_hours": round(age_hours, 2),
                                "reaction_velocity": round(reaction_velocity, 2),
                                "position": position,
                            },
                            signal_strength=round(strength, 2),
                            detected_at=pub_dt,
                        ))
                except Exception:
                    continue

        return signals

    async def health_check(self) -> bool:
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                resp = await client.get(f"{DEVTO_API}/articles", params={"per_page": 1})
                return resp.status_code == 200
        except Exception:
            return False
