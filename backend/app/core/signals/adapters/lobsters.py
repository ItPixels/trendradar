import httpx
from datetime import datetime, timezone
from app.core.signals.base import BaseSignalAdapter, RawSignal


class LobstersAdapter(BaseSignalAdapter):
    source_name = "lobsters"
    weight = 0.55
    tier = 2

    async def fetch_signals(self) -> list[RawSignal]:
        signals = []
        seen_ids = set()

        async with httpx.AsyncClient(timeout=30) as client:
            for endpoint in ["hottest", "newest"]:
                try:
                    resp = await client.get(f"https://lobste.rs/{endpoint}.json")
                    if resp.status_code != 200:
                        continue

                    stories = resp.json()

                    for position, story in enumerate(stories[:25]):
                        story_id = story.get("short_id", "")
                        if not story_id or story_id in seen_ids:
                            continue
                        seen_ids.add(story_id)

                        score = story.get("score", 0)
                        comments = story.get("comment_count", 0)
                        tags = story.get("tags", [])

                        created = story.get("created_at", "")
                        try:
                            created_dt = datetime.fromisoformat(created)
                            if created_dt.tzinfo is None:
                                created_dt = created_dt.replace(tzinfo=timezone.utc)
                        except Exception:
                            created_dt = datetime.now(timezone.utc)

                        age_hours = max((datetime.now(timezone.utc) - created_dt).total_seconds() / 3600, 0.1)
                        score_velocity = score / age_hours

                        score_val = min(score * 3, 30)
                        velocity_val = min(score_velocity * 5, 25)
                        comment_val = min(comments * 2, 15)
                        position_val = max(0, (25 - position) / 25) * 15
                        hottest_bonus = 10 if endpoint == "hottest" else 0

                        strength = min(100, score_val + velocity_val + comment_val + position_val + hottest_bonus)

                        signals.append(RawSignal(
                            source="lobsters",
                            source_id=story_id,
                            title=story.get("title", ""),
                            url=story.get("url", "") or story.get("comments_url", ""),
                            content=story.get("description", "")[:500] if story.get("description") else None,
                            metrics={
                                "score": score,
                                "comments": comments,
                                "tags": tags,
                                "submitter": story.get("submitter_user", {}).get("username", "") if isinstance(story.get("submitter_user"), dict) else "",
                                "type": endpoint,
                                "age_hours": round(age_hours, 2),
                                "score_velocity": round(score_velocity, 2),
                                "position": position,
                            },
                            signal_strength=round(strength, 2),
                            detected_at=created_dt,
                        ))
                except Exception:
                    continue

        return signals

    async def health_check(self) -> bool:
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                resp = await client.get("https://lobste.rs/hottest.json")
                return resp.status_code == 200
        except Exception:
            return False
