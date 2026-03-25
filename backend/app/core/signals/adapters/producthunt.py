import httpx
from bs4 import BeautifulSoup
from datetime import datetime, timezone
from app.core.signals.base import BaseSignalAdapter, RawSignal


class ProductHuntAdapter(BaseSignalAdapter):
    source_name = "producthunt"
    weight = 0.70
    tier = 2

    async def fetch_signals(self) -> list[RawSignal]:
        signals = []

        async with httpx.AsyncClient(timeout=30, follow_redirects=True) as client:
            try:
                headers = {
                    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
                    "Accept": "text/html",
                }
                resp = await client.get(
                    "https://www.producthunt.com", headers=headers
                )
                if resp.status_code != 200:
                    return signals

                soup = BeautifulSoup(resp.text, "html.parser")

                # PH uses data attributes and structured markup
                # Look for product items - they typically have data-test attributes
                items = soup.select(
                    "[data-test='post-item']"
                ) or soup.select("main section div[class*='styles_item']")

                # Fallback: try finding links with product patterns
                if not items:
                    # Try finding all product links
                    links = soup.select("a[href^='/posts/']")
                    seen = set()
                    for position, link in enumerate(links[:25]):
                        href = link.get("href", "")
                        if href in seen or not href.startswith("/posts/"):
                            continue
                        seen.add(href)

                        title = link.get_text(strip=True)
                        if not title or len(title) < 3:
                            continue

                        slug = href.replace("/posts/", "")

                        strength = max(0, (25 - position) / 25) * 60 + 20

                        signals.append(
                            RawSignal(
                                source="producthunt",
                                source_id=slug,
                                title=title,
                                url=f"https://www.producthunt.com{href}",
                                metrics={
                                    "position": position,
                                },
                                signal_strength=round(strength, 2),
                                detected_at=datetime.now(timezone.utc),
                            )
                        )
                else:
                    for position, item in enumerate(items[:25]):
                        title_el = item.select_one("h3") or item.select_one("a")
                        if not title_el:
                            continue
                        title = title_el.get_text(strip=True)

                        link_el = item.select_one("a[href^='/posts/']")
                        href = link_el.get("href", "") if link_el else ""
                        slug = (
                            href.replace("/posts/", "") if href else str(position)
                        )

                        # Try to find vote count
                        vote_el = item.select_one(
                            "button[data-test='vote-button']"
                        ) or item.select_one("[class*='vote']")
                        votes = 0
                        if vote_el:
                            vote_text = vote_el.get_text(strip=True)
                            votes = int(
                                "".join(filter(str.isdigit, vote_text)) or "0"
                            )

                        strength = min(
                            100,
                            (
                                max(0, (25 - position) / 25) * 40
                                + min(votes / 10, 40)
                                + 20
                            ),
                        )

                        signals.append(
                            RawSignal(
                                source="producthunt",
                                source_id=slug,
                                title=title,
                                url=f"https://www.producthunt.com{href}"
                                if href
                                else "https://www.producthunt.com",
                                metrics={
                                    "votes": votes,
                                    "position": position,
                                },
                                signal_strength=round(strength, 2),
                                detected_at=datetime.now(timezone.utc),
                            )
                        )
            except Exception:
                pass

        return signals

    async def health_check(self) -> bool:
        try:
            async with httpx.AsyncClient(
                timeout=10, follow_redirects=True
            ) as client:
                resp = await client.get("https://www.producthunt.com")
                return resp.status_code == 200
        except Exception:
            return False
