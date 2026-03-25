import httpx
from datetime import datetime, timezone
from app.core.signals.base import BaseSignalAdapter, RawSignal

STEAMSPY_API = "https://steamspy.com/api.php"


class SteamChartsAdapter(BaseSignalAdapter):
    source_name = "steam_charts"
    weight = 0.60
    tier = 2

    async def fetch_signals(self) -> list[RawSignal]:
        signals = []

        async with httpx.AsyncClient(timeout=30) as client:
            try:
                resp = await client.get(STEAMSPY_API, params={"request": "top100in2weeks"})
                if resp.status_code != 200:
                    return signals

                data = resp.json()

                # Sort by players in 2 weeks
                sorted_games = sorted(
                    data.items(),
                    key=lambda x: x[1].get("ccu", 0),
                    reverse=True,
                )

                for position, (app_id, game) in enumerate(sorted_games[:25]):
                    name = game.get("name", "")
                    if not name:
                        continue

                    ccu = game.get("ccu", 0)  # concurrent users
                    players_2weeks = game.get("players_2weeks", 0)
                    players_forever = game.get("players_forever", 0)

                    # Ratio of recent to total players indicates trending
                    recency_ratio = players_2weeks / max(players_forever, 1)

                    ccu_score = min(ccu / 10000, 30)
                    position_score = max(0, (25 - position) / 25) * 25
                    recency_score = min(recency_ratio * 100, 25)

                    strength = min(100, ccu_score + position_score + recency_score + 10)

                    signals.append(RawSignal(
                        source="steam_charts",
                        source_id=str(app_id),
                        title=name,
                        url=f"https://store.steampowered.com/app/{app_id}",
                        metrics={
                            "concurrent_users": ccu,
                            "players_2weeks": players_2weeks,
                            "players_forever": players_forever,
                            "recency_ratio": round(recency_ratio, 4),
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
                resp = await client.get(STEAMSPY_API, params={"request": "top100in2weeks"})
                return resp.status_code == 200
        except Exception:
            return False
