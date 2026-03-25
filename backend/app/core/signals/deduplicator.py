"""
Cross-source signal deduplication.

When multiple sources report on the same topic, we need to:
1. Identify signals that refer to the same underlying topic
2. Group them together
3. Keep the richest signal from each source
"""
from typing import Optional

from app.core.signals.base import RawSignal
from app.core.signals.normalizer import TopicNormalizer
from app.core.signals.topic_extractor import TopicExtractor


class SignalDeduplicator:
    """Deduplicates and groups signals by topic across sources."""

    def __init__(self):
        self.normalizer = TopicNormalizer()
        self.extractor = TopicExtractor()

    def deduplicate(
        self,
        signals_by_source: dict[str, list[RawSignal]],
    ) -> dict[str, list[RawSignal]]:
        """
        Group signals by detected topic across all sources.

        Returns:
            Dict mapping normalized_topic -> list of RawSignals from different sources
        """
        topic_groups: dict[str, list[RawSignal]] = {}

        for source, signals in signals_by_source.items():
            for signal in signals:
                # Extract primary topic
                primary_topic = self.extractor.extract_primary_topic(
                    signal.title,
                    signal.content or "",
                    signal.source,
                )

                if not primary_topic:
                    # Use title as fallback
                    primary_topic = signal.title[:50]

                # Normalize the topic
                normalized = self.normalizer.normalize(primary_topic)

                # Check if this topic matches any existing group
                matched_key = self._find_matching_group(normalized, topic_groups)

                if matched_key:
                    topic_groups[matched_key].append(signal)
                else:
                    topic_groups[normalized] = [signal]

        return topic_groups

    def _find_matching_group(
        self,
        topic: str,
        groups: dict[str, list[RawSignal]],
    ) -> Optional[str]:
        """Find an existing group that matches the given topic."""
        for existing_topic in groups:
            if self.normalizer.are_same_topic(topic, existing_topic):
                return existing_topic
        return None

    def get_cross_source_topics(
        self,
        signals_by_source: dict[str, list[RawSignal]],
        min_sources: int = 2,
    ) -> dict[str, dict]:
        """
        Find topics that appear across multiple sources.

        These are the most interesting signals -- cross-source correlation.

        Returns:
            Dict mapping topic -> {sources: [...], signals: [...], source_count: int}
        """
        topic_groups = self.deduplicate(signals_by_source)

        cross_source = {}
        for topic, signals in topic_groups.items():
            # Count unique sources
            sources = list(set(s.source for s in signals))

            if len(sources) >= min_sources:
                cross_source[topic] = {
                    "topic": topic,
                    "slug": self.normalizer.create_slug(topic),
                    "sources": sources,
                    "source_count": len(sources),
                    "signals": signals,
                    "total_signal_count": len(signals),
                    "max_strength": max(s.signal_strength for s in signals),
                    "avg_strength": sum(s.signal_strength for s in signals) / len(signals),
                }

        # Sort by source_count desc, then by max_strength desc
        cross_source = dict(
            sorted(
                cross_source.items(),
                key=lambda x: (x[1]["source_count"], x[1]["max_strength"]),
                reverse=True,
            )
        )

        return cross_source
