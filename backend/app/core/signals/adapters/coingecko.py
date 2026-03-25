import httpx
from datetime import datetime, timezone
from app.core.signals.base import BaseSignalAdapter, RawSignal

CG_API = "https://api.coingecko.com/api/v3"


class CoinGeckoAdapter(BaseSignalAdapter):
    source_name = "coingecko"
    weight = 0.75
    tier = 2

    async def fetch_signals(self) -> list[RawSignal]:
        signals = []
        seen_ids = set()

        async with httpx.AsyncClient(timeout=30) as client:
            # 1. Trending coins
            try:
                resp = await client.get(f"{CG_API}/search/trending")
                if resp.status_code == 200:
                    data = resp.json()
                    for position, item in enumerate(data.get("coins", [])):
                        coin = item.get("item", {})
                        coin_id = coin.get("id", "")
                        if not coin_id:
                            continue
                        seen_ids.add(coin_id)

                        market_cap_rank = coin.get("market_cap_rank") or 999

                        # Trending coins are already filtered by CoinGecko
                        position_score = max(0, (10 - position) / 10) * 40
                        rank_score = max(0, min(30, (500 - market_cap_rank) / 500 * 30))

                        strength = min(100, position_score + rank_score + 25)

                        signals.append(RawSignal(
                            source="coingecko",
                            source_id=coin_id,
                            title=f"{coin.get('name', '')} ({coin.get('symbol', '').upper()})",
                            url=f"https://www.coingecko.com/en/coins/{coin_id}",
                            metrics={
                                "type": "trending",
                                "symbol": coin.get("symbol", ""),
                                "market_cap_rank": market_cap_rank,
                                "position": position,
                                "price_btc": coin.get("price_btc", 0),
                            },
                            signal_strength=round(strength, 2),
                            detected_at=datetime.now(timezone.utc),
                        ))
            except Exception:
                pass

            # 2. Top movers (biggest price changes)
            try:
                resp = await client.get(f"{CG_API}/coins/markets", params={
                    "vs_currency": "usd",
                    "order": "volume_desc",
                    "per_page": 50,
                    "page": 1,
                    "price_change_percentage": "24h,7d",
                })
                if resp.status_code == 200:
                    coins = resp.json()
                    # Sort by absolute price change to find biggest movers
                    coins.sort(key=lambda x: abs(x.get("price_change_percentage_24h") or 0), reverse=True)

                    for position, coin in enumerate(coins[:20]):
                        coin_id = coin.get("id", "")
                        if coin_id in seen_ids:
                            continue
                        seen_ids.add(coin_id)

                        price_change_24h = coin.get("price_change_percentage_24h") or 0
                        market_cap_rank = coin.get("market_cap_rank") or 999
                        volume = coin.get("total_volume") or 0

                        # Signal strength: bigger moves = stronger signal
                        change_score = min(abs(price_change_24h) * 2, 40)
                        volume_score = min(volume / 1_000_000_000, 25)
                        rank_score = max(0, (200 - market_cap_rank) / 200 * 20)

                        strength = min(100, change_score + volume_score + rank_score + 10)

                        signals.append(RawSignal(
                            source="coingecko",
                            source_id=coin_id,
                            title=f"{coin.get('name', '')} ({coin.get('symbol', '').upper()}) — {price_change_24h:+.1f}% 24h",
                            url=f"https://www.coingecko.com/en/coins/{coin_id}",
                            metrics={
                                "type": "top_mover",
                                "symbol": coin.get("symbol", ""),
                                "price_usd": coin.get("current_price", 0),
                                "price_change_24h": round(price_change_24h, 2),
                                "market_cap": coin.get("market_cap", 0),
                                "market_cap_rank": market_cap_rank,
                                "volume_24h": volume,
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
                resp = await client.get(f"{CG_API}/ping")
                return resp.status_code == 200
        except Exception:
            return False
