from app.core.signals.registry import SIGNAL_SOURCES, CORRELATION_MULTIPLIERS, get_source_weight, get_correlation_multiplier

class CorrelationScorer:
    """Calculates correlation scores based on source weights and multipliers."""

    def calculate_base_score(
        self,
        active_sources: list[str],
        signals_by_source: dict[str, list[dict]],
    ) -> float:
        """
        Calculate base correlation score from active sources and their signals.

        Score formula:
        - Sum of (source_weight * signal_strength) for each source
        - Normalized to 0-100 scale
        """
        if not active_sources:
            return 0.0

        total_weighted_score = 0.0
        max_possible = 0.0

        for source in active_sources:
            weight = get_source_weight(source)
            signals = signals_by_source.get(source, [])

            if signals:
                # Use the strongest signal from each source
                max_strength = max(
                    s.get("signal_strength", 0) if isinstance(s, dict) else getattr(s, "signal_strength", 0)
                    for s in signals
                )
                total_weighted_score += weight * max_strength

            max_possible += weight * 100

        if max_possible == 0:
            return 0.0

        # Normalize to 0-100 and apply source count boost
        base = (total_weighted_score / max_possible) * 100
        source_boost = min(len(active_sources) * 5, 25)  # Up to +25 for many sources

        return min(100, base + source_boost)

    def get_pattern_multiplier(self, active_sources: list[str]) -> float:
        """Get the correlation multiplier for the given set of active sources."""
        source_count = len(active_sources)
        return get_correlation_multiplier(source_count)

    def get_source_scores(
        self,
        active_sources: list[str],
        signals_by_source: dict[str, list[dict]],
    ) -> dict[str, dict]:
        """Get individual source contribution scores."""
        scores = {}
        for source in active_sources:
            weight = get_source_weight(source)
            signals = signals_by_source.get(source, [])

            max_strength = 0
            signal_count = len(signals)

            if signals:
                max_strength = max(
                    s.get("signal_strength", 0) if isinstance(s, dict) else getattr(s, "signal_strength", 0)
                    for s in signals
                )

            scores[source] = {
                "weight": weight,
                "signal_count": signal_count,
                "max_strength": round(max_strength, 2),
                "weighted_score": round(weight * max_strength, 2),
            }

        return scores
