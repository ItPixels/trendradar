import httpx
from bs4 import BeautifulSoup
from datetime import datetime, timezone
from app.core.signals.base import BaseSignalAdapter, RawSignal

TRENDING_URLS = [
    {"url": "https://github.com/trending", "lang": "all"},
    {"url": "https://github.com/trending/python", "lang": "python"},
    {"url": "https://github.com/trending/typescript", "lang": "typescript"},
]


class GitHubTrendingAdapter(BaseSignalAdapter):
    source_name = "github_trending"
    weight = 0.80
    tier = 1

    async def fetch_signals(self) -> list[RawSignal]:
        signals = []
        seen_repos = set()

        async with httpx.AsyncClient(timeout=30) as client:
            for trending_info in TRENDING_URLS:
                try:
                    resp = await client.get(trending_info["url"])
                    if resp.status_code != 200:
                        continue

                    soup = BeautifulSoup(resp.text, "html.parser")
                    articles = soup.select("article.Box-row")

                    for position, article in enumerate(articles[:25]):
                        try:
                            # Repo name
                            h2 = article.select_one("h2 a")
                            if not h2:
                                continue
                            repo_path = h2.get("href", "").strip("/")
                            if not repo_path or repo_path in seen_repos:
                                continue
                            seen_repos.add(repo_path)

                            repo_name = repo_path.split("/")[-1] if "/" in repo_path else repo_path

                            # Description
                            desc_el = article.select_one("p")
                            description = desc_el.get_text(strip=True) if desc_el else ""

                            # Language
                            lang_el = article.select_one("[itemprop='programmingLanguage']")
                            language = lang_el.get_text(strip=True) if lang_el else ""

                            # Stars today
                            stars_today_el = article.select_one("span.d-inline-block.float-sm-right")
                            stars_today_text = stars_today_el.get_text(strip=True) if stars_today_el else "0"
                            stars_today = int("".join(filter(str.isdigit, stars_today_text.split("star")[0])) or "0")

                            # Total stars & forks from links
                            star_links = article.select("a.Link--muted")
                            total_stars = 0
                            forks = 0
                            for link in star_links:
                                text = link.get_text(strip=True).replace(",", "")
                                href = link.get("href", "")
                                if "/stargazers" in href:
                                    total_stars = int(text) if text.isdigit() else 0
                                elif "/forks" in href:
                                    forks = int(text) if text.isdigit() else 0

                            # Signal strength
                            position_bonus = max(0, (25 - position) / 25) * 20
                            stars_score = min(stars_today / 10, 30)
                            momentum = min(stars_today / max(total_stars / 1000, 1), 30) if total_stars > 0 else stars_score

                            strength = min(100, position_bonus + stars_score + momentum + 10)

                            signal = RawSignal(
                                source="github_trending",
                                source_id=repo_path,
                                title=f"{repo_name}: {description[:100]}" if description else repo_name,
                                url=f"https://github.com/{repo_path}",
                                content=description,
                                metrics={
                                    "stars_today": stars_today,
                                    "total_stars": total_stars,
                                    "forks": forks,
                                    "language": language,
                                    "position": position,
                                    "trending_category": trending_info["lang"],
                                },
                                detected_at=datetime.now(timezone.utc),
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
                resp = await client.get("https://github.com/trending")
                return resp.status_code == 200
        except Exception:
            return False
