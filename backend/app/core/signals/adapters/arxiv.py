import httpx
import feedparser
from datetime import datetime, timezone
from app.core.signals.base import BaseSignalAdapter, RawSignal

ARXIV_API = "http://export.arxiv.org/api/query"

CATEGORIES = [
    {"query": "cat:cs.AI", "name": "AI", "weight": 1.0},
    {"query": "cat:cs.LG", "name": "Machine Learning", "weight": 0.95},
    {"query": "cat:cs.CL", "name": "NLP", "weight": 0.9},
    {"query": "cat:cs.CV", "name": "Computer Vision", "weight": 0.85},
]


class ArXivAdapter(BaseSignalAdapter):
    source_name = "arxiv"
    weight = 0.60
    tier = 2

    async def fetch_signals(self) -> list[RawSignal]:
        signals = []
        seen_ids = set()

        async with httpx.AsyncClient(timeout=30) as client:
            for cat_info in CATEGORIES:
                try:
                    params = {
                        "search_query": cat_info["query"],
                        "sortBy": "submittedDate",
                        "sortOrder": "descending",
                        "max_results": 15,
                    }
                    resp = await client.get(ARXIV_API, params=params)
                    if resp.status_code != 200:
                        continue

                    feed = feedparser.parse(resp.text)

                    for position, entry in enumerate(feed.entries):
                        arxiv_id = entry.get("id", "").split("/abs/")[-1]
                        if not arxiv_id or arxiv_id in seen_ids:
                            continue
                        seen_ids.add(arxiv_id)

                        title = entry.get("title", "").replace("\n", " ").strip()
                        summary = entry.get("summary", "").replace("\n", " ").strip()
                        authors = [a.get("name", "") for a in entry.get("authors", [])]

                        # Parse published date
                        published = entry.get("published", "")
                        try:
                            pub_dt = datetime.fromisoformat(published.replace("Z", "+00:00"))
                        except Exception:
                            pub_dt = datetime.now(timezone.utc)

                        age_hours = max((datetime.now(timezone.utc) - pub_dt).total_seconds() / 3600, 0.1)

                        # Categories from the paper
                        paper_cats = [t.get("term", "") for t in entry.get("tags", [])]

                        recency = max(0, 40 - age_hours * 0.5)
                        position_score = max(0, (15 - position) / 15) * 25
                        cat_weight = cat_info["weight"] * 20

                        strength = min(100, recency + position_score + cat_weight + 10)

                        signals.append(RawSignal(
                            source="arxiv",
                            source_id=arxiv_id,
                            title=title,
                            url=entry.get("id", ""),
                            content=summary[:500],
                            metrics={
                                "authors": authors[:5],
                                "categories": paper_cats,
                                "category_name": cat_info["name"],
                                "position": position,
                                "age_hours": round(age_hours, 2),
                                "author_count": len(authors),
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
                resp = await client.get(ARXIV_API, params={"search_query": "cat:cs.AI", "max_results": 1})
                return resp.status_code == 200
        except Exception:
            return False
