import httpx
from datetime import datetime, timezone, timedelta
from app.core.signals.base import BaseSignalAdapter, RawSignal

WIKI_API = "https://wikimedia.org/api/rest_v1"

# Pages to exclude (always high traffic but not signals)
EXCLUDED_PAGES = {
    "Main_Page", "Special:Search", "-", "Wikipedia:Featured_pictures",
    "Special:CreateAccount", "Portal:Current_events", "Special:Watchlist",
}


class WikipediaAdapter(BaseSignalAdapter):
    source_name = "wikipedia"
    weight = 0.75
    tier = 1

    async def fetch_signals(self) -> list[RawSignal]:
        signals = []
        headers = {"User-Agent": "TrendRadar/1.0 (trend prediction platform; contact@trendradar.io)"}

        # Get yesterday's data (today might be incomplete)
        yesterday = datetime.now(timezone.utc) - timedelta(days=1)
        date_path = yesterday.strftime("%Y/%m/%d")

        async with httpx.AsyncClient(timeout=30, headers=headers) as client:
            try:
                url = f"{WIKI_API}/metrics/pageviews/top/en.wikipedia/all-access/{date_path}"
                resp = await client.get(url)
                if resp.status_code != 200:
                    return signals

                data = resp.json()
                articles = data.get("items", [{}])[0].get("articles", [])

                for position, article in enumerate(articles[:50]):
                    title = article.get("article", "")
                    views = article.get("views", 0)

                    # Skip excluded pages
                    if title in EXCLUDED_PAGES or title.startswith("Special:") or title.startswith("Wikipedia:"):
                        continue

                    # Clean title
                    display_title = title.replace("_", " ")

                    # Signal strength based on views and position
                    # Top Wikipedia pages get millions of views, so normalize
                    view_score = min(views / 100000, 40)  # Cap at 40 for 4M+ views
                    position_score = max(0, (50 - position) / 50) * 30

                    strength = min(100, view_score + position_score + 10)

                    signal = RawSignal(
                        source="wikipedia",
                        source_id=title,
                        title=display_title,
                        url=f"https://en.wikipedia.org/wiki/{title}",
                        content=None,
                        metrics={
                            "views": views,
                            "position": position,
                            "date": yesterday.strftime("%Y-%m-%d"),
                        },
                        detected_at=yesterday.replace(hour=23, minute=59),
                        signal_strength=round(strength, 2),
                    )
                    signals.append(signal)
            except Exception:
                pass

        return signals

    async def health_check(self) -> bool:
        try:
            headers = {"User-Agent": "TrendRadar/1.0"}
            yesterday = datetime.now(timezone.utc) - timedelta(days=1)
            date_path = yesterday.strftime("%Y/%m/%d")
            async with httpx.AsyncClient(timeout=10, headers=headers) as client:
                resp = await client.get(f"{WIKI_API}/metrics/pageviews/top/en.wikipedia/all-access/{date_path}")
                return resp.status_code == 200
        except Exception:
            return False
