import httpx
from datetime import datetime, timezone
from app.core.signals.base import BaseSignalAdapter, RawSignal

SO_API = "https://api.stackexchange.com/2.3"


class StackOverflowAdapter(BaseSignalAdapter):
    source_name = "stackoverflow"
    weight = 0.60
    tier = 2

    async def fetch_signals(self) -> list[RawSignal]:
        signals = []

        async with httpx.AsyncClient(timeout=30) as client:
            # 1. Hot questions
            try:
                resp = await client.get(f"{SO_API}/questions", params={
                    "order": "desc",
                    "sort": "hot",
                    "site": "stackoverflow",
                    "pagesize": 25,
                    "filter": "default",
                })
                if resp.status_code == 200:
                    data = resp.json()
                    for position, q in enumerate(data.get("items", [])):
                        q_id = q.get("question_id", 0)
                        score = q.get("score", 0)
                        views = q.get("view_count", 0)
                        answers = q.get("answer_count", 0)
                        tags = q.get("tags", [])

                        created = q.get("creation_date", 0)
                        created_dt = datetime.fromtimestamp(created, tz=timezone.utc) if created else datetime.now(timezone.utc)

                        age_hours = max((datetime.now(timezone.utc) - created_dt).total_seconds() / 3600, 0.1)
                        view_velocity = views / age_hours

                        view_score = min(view_velocity / 100, 25)
                        score_val = min(score * 3, 20)
                        answer_val = min(answers * 5, 15)
                        position_val = max(0, (25 - position) / 25) * 20

                        strength = min(100, view_score + score_val + answer_val + position_val + 10)

                        signals.append(RawSignal(
                            source="stackoverflow",
                            source_id=str(q_id),
                            title=q.get("title", ""),
                            url=q.get("link", ""),
                            metrics={
                                "score": score,
                                "views": views,
                                "answers": answers,
                                "tags": tags,
                                "is_answered": q.get("is_answered", False),
                                "view_velocity": round(view_velocity, 2),
                                "age_hours": round(age_hours, 2),
                                "position": position,
                            },
                            signal_strength=round(strength, 2),
                            detected_at=created_dt,
                        ))
            except Exception:
                pass

            # 2. Trending tags (by popularity)
            try:
                resp = await client.get(f"{SO_API}/tags", params={
                    "order": "desc",
                    "sort": "popular",
                    "site": "stackoverflow",
                    "pagesize": 30,
                    "filter": "default",
                })
                if resp.status_code == 200:
                    data = resp.json()
                    for position, tag in enumerate(data.get("items", [])):
                        tag_name = tag.get("name", "")
                        count = tag.get("count", 0)

                        if not tag_name:
                            continue

                        # Popular tags by question count
                        count_score = min(count / 100000, 30)
                        position_val = max(0, (30 - position) / 30) * 20

                        strength = min(80, count_score + position_val + 15)

                        signals.append(RawSignal(
                            source="stackoverflow",
                            source_id=f"tag:{tag_name}",
                            title=f"[{tag_name}] — {count:,} questions on Stack Overflow",
                            url=f"https://stackoverflow.com/questions/tagged/{tag_name}",
                            metrics={
                                "type": "tag",
                                "tag": tag_name,
                                "question_count": count,
                                "position": position,
                            },
                            signal_strength=round(strength, 2),
                            detected_at=datetime.now(timezone.utc),
                        ))
            except Exception:
                pass

        return signals

    async def health_check(self) -> bool:
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                resp = await client.get(f"{SO_API}/info", params={"site": "stackoverflow"})
                return resp.status_code == 200
        except Exception:
            return False
