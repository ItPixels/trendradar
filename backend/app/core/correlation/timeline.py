from datetime import datetime, timezone

class SpreadTimeline:
    """Builds a timeline of how a topic spread across sources."""

    def build(self, signals_by_source: dict[str, list[dict]]) -> list[dict]:
        """
        Build a chronological timeline of when the topic appeared in each source.

        Returns list of {source, first_seen, signal_count} sorted by first_seen.
        """
        timeline = []

        for source, signals in signals_by_source.items():
            if not signals:
                continue

            # Find the earliest signal from this source
            earliest = None
            for s in signals:
                if isinstance(s, dict):
                    detected = s.get("detected_at")
                else:
                    detected = getattr(s, "detected_at", None)

                if detected is None:
                    continue

                if isinstance(detected, str):
                    try:
                        detected = datetime.fromisoformat(detected)
                    except Exception:
                        continue

                if earliest is None or detected < earliest:
                    earliest = detected

            if earliest:
                timeline.append({
                    "source": source,
                    "first_seen": earliest.isoformat() if isinstance(earliest, datetime) else str(earliest),
                    "signal_count": len(signals),
                })

        # Sort by first_seen
        timeline.sort(key=lambda x: x["first_seen"])

        return timeline
