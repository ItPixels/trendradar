import httpx
import feedparser
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from app.core.signals.base import BaseSignalAdapter, RawSignal

FEEDS = [
    {"url": "https://news.google.com/rss", "category": "top", "weight": 1.0},
    {"url": "https://news.google.com/rss/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRGRqTVhZU0FtVnVHZ0pWVXlnQVAB", "category": "technology", "weight": 0.9},
    {"url": "https://news.google.com/rss/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRGx6TVdZU0FtVnVHZ0pWVXlnQVAB", "category": "science", "weight": 0.85},
    {"url": "https://news.google.com/rss/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRFp0Y1RjU0FtVnVHZ0pWVXlnQVAB", "category": "business", "weight": 0.8},
]


class GoogleNewsAdapter(BaseSignalAdapter):
    source_name = "google_news"
    weight = 0.70
    tier = 1

    async def fetch_signals(self) -> list[RawSignal]:
        signals = []

        async with httpx.AsyncClient(timeout=30) as client:
            for feed_info in FEEDS:
                try:
                    resp = await client.get(feed_info["url"])
                    if resp.status_code != 200:
                        continue

                    feed = feedparser.parse(resp.text)

                    for position, entry in enumerate(feed.entries[:20]):
                        try:
                            title = entry.get("title", "")
                            link = entry.get("link", "")

                            # Parse published date
                            published = entry.get("published", "")
                            try:
                                detected_at = parsedate_to_datetime(published)
                                if detected_at.tzinfo is None:
                                    detected_at = detected_at.replace(tzinfo=timezone.utc)
                            except Exception:
                                detected_at = datetime.now(timezone.utc)

                            age_hours = max((datetime.now(timezone.utc) - detected_at).total_seconds() / 3600, 0.1)

                            # Extract source from title (Google News format: "Title - Source")
                            source_name = ""
                            if " - " in title:
                                parts = title.rsplit(" - ", 1)
                                title = parts[0]
                                source_name = parts[1] if len(parts) > 1 else ""

                            # Signal strength: recency + position + category weight
                            recency_score = max(0, 40 - age_hours * 2)  # Fresher = stronger
                            position_score = max(0, (20 - position) / 20) * 30
                            category_score = feed_info["weight"] * 20

                            strength = min(100, recency_score + position_score + category_score)

                            signal = RawSignal(
                                source="google_news",
                                source_id=link,
                                title=title,
                                url=link,
                                content=entry.get("summary", "")[:500] if entry.get("summary") else None,
                                metrics={
                                    "position": position,
                                    "category": feed_info["category"],
                                    "news_source": source_name,
                                    "age_hours": round(age_hours, 2),
                                },
                                detected_at=detected_at,
                                signal_strength=round(strength, 2),
                            )
                            signals.append(signal)
                        except Exception:
                            continue
                except Exception:
                    continue

        return signals

    async def health_check(self) -> bool:
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                resp = await client.get("https://news.google.com/rss")
                return resp.status_code == 200
        except Exception:
            return False
