import httpx
from datetime import datetime, timezone
from app.core.signals.base import BaseSignalAdapter, RawSignal

NPM_SEARCH = "https://registry.npmjs.org/-/v1/search"
NPM_DOWNLOADS = "https://api.npmjs.org/downloads"

# Hot topics in npm to track
SEARCH_QUERIES = [
    "ai",
    "llm",
    "react",
    "machine learning",
    "crypto",
    "web3",
    "rust",
    "bun",
]


class NpmRegistryAdapter(BaseSignalAdapter):
    source_name = "npm_registry"
    weight = 0.65
    tier = 2

    async def fetch_signals(self) -> list[RawSignal]:
        signals = []
        seen_packages = set()

        async with httpx.AsyncClient(timeout=30) as client:
            for query in SEARCH_QUERIES:
                try:
                    resp = await client.get(
                        NPM_SEARCH,
                        params={
                            "text": query,
                            "size": 10,
                            "popularity": 1.0,
                            "quality": 0.5,
                        },
                    )
                    if resp.status_code != 200:
                        continue

                    data = resp.json()
                    for item in data.get("objects", []):
                        pkg = item.get("package", {})
                        name = pkg.get("name", "")
                        if not name or name in seen_packages:
                            continue
                        seen_packages.add(name)

                        score = item.get("score", {})
                        detail = score.get("detail", {})
                        popularity = detail.get("popularity", 0)
                        quality = detail.get("quality", 0)
                        maintenance = detail.get("maintenance", 0)

                        # Try to get recent downloads
                        downloads_week = 0
                        try:
                            dl_resp = await client.get(
                                f"{NPM_DOWNLOADS}/point/last-week/{name}"
                            )
                            if dl_resp.status_code == 200:
                                downloads_week = dl_resp.json().get(
                                    "downloads", 0
                                )
                        except Exception:
                            pass

                        strength = min(
                            100,
                            (
                                popularity * 40
                                + quality * 15
                                + min(downloads_week / 100000, 30)
                                + 10
                            ),
                        )

                        description = pkg.get("description", "")
                        version = pkg.get("version", "")

                        signals.append(
                            RawSignal(
                                source="npm_registry",
                                source_id=name,
                                title=f"{name}@{version}: {description[:100]}"
                                if description
                                else f"{name}@{version}",
                                url=f"https://www.npmjs.com/package/{name}",
                                content=description[:500]
                                if description
                                else None,
                                metrics={
                                    "downloads_week": downloads_week,
                                    "popularity": round(popularity, 4),
                                    "quality": round(quality, 4),
                                    "maintenance": round(maintenance, 4),
                                    "version": version,
                                    "search_query": query,
                                },
                                signal_strength=round(strength, 2),
                                detected_at=datetime.now(timezone.utc),
                            )
                        )
                except Exception:
                    continue

        return signals

    async def health_check(self) -> bool:
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                resp = await client.get(f"{NPM_SEARCH}?text=react&size=1")
                return resp.status_code == 200
        except Exception:
            return False
