import httpx
import asyncio
from datetime import datetime, timezone
from app.core.signals.base import BaseSignalAdapter, RawSignal

SUBREDDITS = [
    {"path": "r/all/rising", "weight": 1.0},
    {"path": "r/technology/hot", "weight": 0.9},
    {"path": "r/programming/hot", "weight": 0.85},
    {"path": "r/artificial/hot", "weight": 0.9},
    {"path": "r/MachineLearning/hot", "weight": 0.85},
    {"path": "r/worldnews/rising", "weight": 0.8},
]


class RedditAdapter(BaseSignalAdapter):
    source_name = "reddit"
    weight = 0.85
    tier = 1

    async def fetch_signals(self) -> list[RawSignal]:
        signals = []
        headers = {"User-Agent": "TrendRadar/1.0 (Signal Intelligence Platform)"}

        async with httpx.AsyncClient(timeout=30, headers=headers) as client:
            for sub_info in SUBREDDITS:
                try:
                    url = f"https://www.reddit.com/{sub_info['path']}.json?limit=25"
                    resp = await client.get(url)
                    if resp.status_code != 200:
                        continue

                    data = resp.json()
                    posts = data.get("data", {}).get("children", [])

                    for post_data in posts:
                        post = post_data.get("data", {})
                        if post.get("stickied") or post.get("is_self") and not post.get("selftext"):
                            continue

                        score = post.get("score", 0)
                        comments = post.get("num_comments", 0)
                        upvote_ratio = post.get("upvote_ratio", 0.5)
                        created = datetime.fromtimestamp(post.get("created_utc", 0), tz=timezone.utc)
                        age_hours = max((datetime.now(timezone.utc) - created).total_seconds() / 3600, 0.1)

                        score_velocity = score / age_hours
                        engagement = comments / max(score, 1)

                        strength = min(100, (
                            score_velocity * 0.3 +
                            upvote_ratio * 20 +
                            engagement * 15 +
                            min(score / 50, 25) +
                            sub_info["weight"] * 10
                        ))

                        signal = RawSignal(
                            source="reddit",
                            source_id=post.get("id", ""),
                            title=post.get("title", ""),
                            url=f"https://reddit.com{post.get('permalink', '')}",
                            content=post.get("selftext", "")[:500] if post.get("selftext") else None,
                            metrics={
                                "score": score,
                                "comments": comments,
                                "upvote_ratio": upvote_ratio,
                                "subreddit": post.get("subreddit", ""),
                                "score_velocity": round(score_velocity, 2),
                                "age_hours": round(age_hours, 2),
                                "awards": post.get("total_awards_received", 0),
                            },
                            detected_at=created,
                            signal_strength=round(strength, 2),
                        )
                        signals.append(signal)

                    # Rate limiting: wait between subreddit requests
                    await asyncio.sleep(2)

                except Exception:
                    continue

        return signals

    async def health_check(self) -> bool:
        try:
            headers = {"User-Agent": "TrendRadar/1.0"}
            async with httpx.AsyncClient(timeout=10, headers=headers) as client:
                resp = await client.get("https://www.reddit.com/r/all/rising.json?limit=1")
                return resp.status_code == 200
        except Exception:
            return False
