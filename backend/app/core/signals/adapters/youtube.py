import httpx
from datetime import datetime, timezone
from app.core.signals.base import BaseSignalAdapter, RawSignal
from app.config import settings

YT_API = "https://www.googleapis.com/youtube/v3"

CATEGORIES = [
    {"id": "0", "name": "all"},
    {"id": "28", "name": "science_tech"},
    {"id": "25", "name": "news"},
    {"id": "20", "name": "gaming"},
]


class YouTubeAdapter(BaseSignalAdapter):
    source_name = "youtube_trending"
    weight = 0.80
    tier = 1

    async def fetch_signals(self) -> list[RawSignal]:
        if not settings.youtube_api_key:
            return []

        signals = []
        seen_ids = set()

        async with httpx.AsyncClient(timeout=30) as client:
            for cat in CATEGORIES:
                try:
                    params = {
                        "part": "snippet,statistics",
                        "chart": "mostPopular",
                        "regionCode": "US",
                        "maxResults": 20,
                        "key": settings.youtube_api_key,
                    }
                    if cat["id"] != "0":
                        params["videoCategoryId"] = cat["id"]

                    resp = await client.get(f"{YT_API}/videos", params=params)
                    if resp.status_code != 200:
                        continue

                    data = resp.json()
                    for position, item in enumerate(data.get("items", [])):
                        video_id = item["id"]
                        if video_id in seen_ids:
                            continue
                        seen_ids.add(video_id)

                        snippet = item.get("snippet", {})
                        stats = item.get("statistics", {})

                        views = int(stats.get("viewCount", 0))
                        likes = int(stats.get("likeCount", 0))
                        comments = int(stats.get("commentCount", 0))

                        published = snippet.get("publishedAt", "")
                        try:
                            pub_dt = datetime.fromisoformat(
                                published.replace("Z", "+00:00")
                            )
                        except Exception:
                            pub_dt = datetime.now(timezone.utc)

                        age_hours = max(
                            (datetime.now(timezone.utc) - pub_dt).total_seconds()
                            / 3600,
                            0.1,
                        )
                        view_velocity = views / age_hours
                        like_ratio = likes / max(views, 1)
                        comment_rate = comments / max(views, 1) * 1000

                        strength = min(
                            100,
                            (
                                min(view_velocity / 10000, 30)
                                + like_ratio * 500
                                + min(comment_rate * 5, 20)
                                + max(0, (20 - position) / 20) * 20
                            ),
                        )

                        signals.append(
                            RawSignal(
                                source="youtube_trending",
                                source_id=video_id,
                                title=snippet.get("title", ""),
                                url=f"https://youtube.com/watch?v={video_id}",
                                content=snippet.get("description", "")[:500],
                                metrics={
                                    "views": views,
                                    "likes": likes,
                                    "comments": comments,
                                    "channel": snippet.get("channelTitle", ""),
                                    "category_id": cat["id"],
                                    "category_name": cat["name"],
                                    "view_velocity": round(view_velocity, 2),
                                    "age_hours": round(age_hours, 2),
                                    "position": position,
                                },
                                signal_strength=round(strength, 2),
                                detected_at=pub_dt,
                            )
                        )
                except Exception:
                    continue

        return signals

    async def health_check(self) -> bool:
        if not settings.youtube_api_key:
            return False
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                resp = await client.get(
                    f"{YT_API}/videos",
                    params={
                        "part": "id",
                        "chart": "mostPopular",
                        "maxResults": 1,
                        "key": settings.youtube_api_key,
                    },
                )
                return resp.status_code == 200
        except Exception:
            return False
