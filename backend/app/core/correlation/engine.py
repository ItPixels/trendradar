import logging
from datetime import datetime, timezone, timedelta
from typing import Optional
from app.core.correlation.detector import CrossSourceDetector
from app.core.correlation.scorer import CorrelationScorer
from app.core.correlation.timeline import SpreadTimeline

logger = logging.getLogger(__name__)

class CorrelationEngine:
    """
    Detects and scores cross-source correlations.

    The core insight: when a topic appears across multiple independent sources
    simultaneously, it's a strong predictive signal. A topic trending on both
    HackerNews AND Reddit AND Google Trends is much more significant than
    trending on just one.
    """

    def __init__(self):
        self.detector = CrossSourceDetector()
        self.scorer = CorrelationScorer()
        self.timeline = SpreadTimeline()

    def calculate_correlation(
        self,
        topic: str,
        signals_by_source: dict[str, list[dict]],
        time_window_hours: int = 24,
    ) -> dict:
        """
        Calculate cross-source correlation for a topic.

        Args:
            topic: The topic/trend being analyzed
            signals_by_source: Dict mapping source_name -> list of signal dicts
            time_window_hours: Time window to consider for correlation

        Returns:
            Dict with correlation_score, active_sources, multiplier, details
        """
        active_sources = [
            source for source, signals in signals_by_source.items()
            if len(signals) > 0
        ]

        source_count = len(active_sources)

        if source_count <= 1:
            return {
                "correlation_score": 0,
                "active_sources": active_sources,
                "source_count": source_count,
                "multiplier": 1.0,
                "is_correlated": False,
                "pattern": None,
                "details": {},
            }

        # Calculate base correlation score
        base_score = self.scorer.calculate_base_score(active_sources, signals_by_source)

        # Apply correlation multipliers for known strong patterns
        multiplier = self.scorer.get_pattern_multiplier(active_sources)

        # Apply source count bonus (5+ sources is massive signal)
        if source_count >= 6:
            multiplier = max(multiplier, 2.5)
        elif source_count >= 5:
            multiplier = max(multiplier, 2.0)

        # Calculate final score (0-100)
        final_score = min(100, base_score * multiplier)

        # Detect the pattern type
        pattern = self.detector.detect_pattern(active_sources)

        # Build spread timeline
        spread = self.timeline.build(signals_by_source)

        return {
            "correlation_score": round(final_score, 2),
            "active_sources": active_sources,
            "source_count": source_count,
            "multiplier": round(multiplier, 2),
            "is_correlated": source_count >= 2 and final_score >= 30,
            "pattern": pattern,
            "spread_timeline": spread,
            "details": {
                "base_score": round(base_score, 2),
                "source_scores": self.scorer.get_source_scores(active_sources, signals_by_source),
            },
        }
