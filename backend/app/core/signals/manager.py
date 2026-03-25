import asyncio
import logging
from datetime import datetime, timezone
from typing import Optional
from app.core.signals.base import BaseSignalAdapter, RawSignal
from app.core.signals.adapters.hackernews import HackerNewsAdapter
from app.core.signals.adapters.reddit import RedditAdapter
from app.core.signals.adapters.github import GitHubTrendingAdapter
from app.core.signals.adapters.google_news import GoogleNewsAdapter
from app.core.signals.adapters.wikipedia import WikipediaAdapter
from app.core.signals.adapters.youtube import YouTubeAdapter
from app.core.signals.adapters.producthunt import ProductHuntAdapter
from app.core.signals.adapters.npm_registry import NpmRegistryAdapter
from app.core.signals.adapters.pypi_stats import PyPIStatsAdapter
from app.core.signals.adapters.arxiv import ArXivAdapter
from app.core.signals.adapters.coingecko import CoinGeckoAdapter
from app.core.signals.adapters.steam_charts import SteamChartsAdapter
from app.core.signals.adapters.devto import DevToAdapter
from app.core.signals.adapters.lobsters import LobstersAdapter
from app.core.signals.adapters.stackoverflow import StackOverflowAdapter

logger = logging.getLogger(__name__)


class SignalManager:
    """Orchestrates signal collection from all registered adapters."""

    def __init__(self):
        self.adapters: dict[str, BaseSignalAdapter] = {}
        self._register_defaults()

    def _register_defaults(self):
        """Register all default signal adapters."""
        adapters = [
            # Tier 1: Core sources
            HackerNewsAdapter(),
            RedditAdapter(),
            GitHubTrendingAdapter(),
            GoogleNewsAdapter(),
            WikipediaAdapter(),
            YouTubeAdapter(),
            # Tier 2: Vertical sources
            ProductHuntAdapter(),
            NpmRegistryAdapter(),
            PyPIStatsAdapter(),
            ArXivAdapter(),
            CoinGeckoAdapter(),
            SteamChartsAdapter(),
            DevToAdapter(),
            LobstersAdapter(),
            StackOverflowAdapter(),
        ]
        for adapter in adapters:
            self.adapters[adapter.source_name] = adapter

    def register(self, adapter: BaseSignalAdapter):
        """Register a custom signal adapter."""
        self.adapters[adapter.source_name] = adapter

    async def collect_all(self, sources: Optional[list[str]] = None) -> dict[str, list[RawSignal]]:
        """Collect signals from all (or specified) sources concurrently."""
        target_adapters = self.adapters
        if sources:
            target_adapters = {k: v for k, v in self.adapters.items() if k in sources}

        results: dict[str, list[RawSignal]] = {}

        async def _fetch(name: str, adapter: BaseSignalAdapter):
            try:
                start = datetime.now(timezone.utc)
                signals = await adapter.fetch_signals()
                duration = (datetime.now(timezone.utc) - start).total_seconds()
                logger.info(f"[{name}] Collected {len(signals)} signals in {duration:.1f}s")
                return name, signals
            except Exception as e:
                logger.error(f"[{name}] Failed to collect signals: {e}")
                return name, []

        tasks = [_fetch(name, adapter) for name, adapter in target_adapters.items()]
        completed = await asyncio.gather(*tasks)

        for name, signals in completed:
            results[name] = signals

        total = sum(len(s) for s in results.values())
        logger.info(f"Total signals collected: {total} from {len(results)} sources")

        return results

    async def collect_source(self, source_name: str) -> list[RawSignal]:
        """Collect signals from a single source."""
        adapter = self.adapters.get(source_name)
        if not adapter:
            raise ValueError(f"Unknown source: {source_name}")
        return await adapter.fetch_signals()

    async def health_check_all(self) -> dict[str, bool]:
        """Check health of all registered sources."""
        results = {}

        async def _check(name: str, adapter: BaseSignalAdapter):
            try:
                healthy = await adapter.health_check()
                return name, healthy
            except Exception:
                return name, False

        tasks = [_check(name, adapter) for name, adapter in self.adapters.items()]
        completed = await asyncio.gather(*tasks)

        for name, healthy in completed:
            results[name] = healthy

        return results

    def list_sources(self) -> list[dict]:
        """List all registered sources with their info."""
        return [
            adapter.get_source_info()
            for adapter in self.adapters.values()
        ]
