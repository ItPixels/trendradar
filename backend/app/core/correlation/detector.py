from typing import Optional

# Pattern definitions
PATTERNS = {
    "tech_breakout": {
        "required": ["hackernews"],
        "any_of": ["github_trending", "reddit", "stackoverflow"],
        "label": "Tech Breakout",
        "description": "Technical topic gaining traction across developer communities",
    },
    "ai_research_adoption": {
        "required": ["arxiv"],
        "any_of": ["hackernews", "github_trending", "reddit"],
        "label": "AI Research -> Adoption",
        "description": "Academic research crossing into practical adoption",
    },
    "mainstream_breakout": {
        "required": ["google_trends"],
        "any_of": ["youtube_trending", "google_news", "reddit", "wikipedia"],
        "label": "Mainstream Breakout",
        "description": "Topic breaking into mainstream awareness",
    },
    "product_launch": {
        "required": ["producthunt"],
        "any_of": ["hackernews", "reddit", "google_trends"],
        "label": "Product Launch",
        "description": "New product gaining widespread attention",
    },
    "crypto_surge": {
        "required": ["coingecko"],
        "any_of": ["reddit", "google_trends", "hackernews"],
        "label": "Crypto Surge",
        "description": "Cryptocurrency gaining significant attention",
    },
    "gaming_trend": {
        "required": ["steam_charts"],
        "any_of": ["reddit", "youtube_trending", "google_trends"],
        "label": "Gaming Trend",
        "description": "Game or gaming topic trending across platforms",
    },
    "breaking_news": {
        "required": ["google_news"],
        "any_of": ["wikipedia", "google_trends", "reddit"],
        "label": "Breaking News",
        "description": "Breaking news story spreading across platforms",
    },
    "developer_ecosystem": {
        "required": [],
        "any_of": ["npm_registry", "pypi_stats", "github_trending", "stackoverflow"],
        "min_match": 3,
        "label": "Developer Ecosystem Shift",
        "description": "Shift in developer tools and ecosystem adoption",
    },
}

class CrossSourceDetector:
    """Detects known cross-source correlation patterns."""

    def detect_pattern(self, active_sources: list[str]) -> Optional[dict]:
        """
        Detect which correlation pattern matches the active sources.
        Returns the strongest matching pattern or None.
        """
        source_set = set(active_sources)
        best_match = None
        best_score = 0

        for pattern_id, pattern in PATTERNS.items():
            required = set(pattern.get("required", []))
            any_of = set(pattern.get("any_of", []))
            min_match = pattern.get("min_match", 1)

            # Check required sources
            if not required.issubset(source_set):
                continue

            # Check any_of matches
            matches = source_set.intersection(any_of)
            if len(matches) < min_match:
                continue

            # Score = required matches + any_of matches
            score = len(required) + len(matches)

            if score > best_score:
                best_score = score
                best_match = {
                    "id": pattern_id,
                    "label": pattern["label"],
                    "description": pattern["description"],
                    "matched_sources": list(required.union(matches)),
                    "match_score": score,
                }

        return best_match

    def detect_all_patterns(self, active_sources: list[str]) -> list[dict]:
        """Detect all matching patterns (not just the best)."""
        source_set = set(active_sources)
        matches = []

        for pattern_id, pattern in PATTERNS.items():
            required = set(pattern.get("required", []))
            any_of = set(pattern.get("any_of", []))
            min_match = pattern.get("min_match", 1)

            if not required.issubset(source_set):
                continue

            any_matches = source_set.intersection(any_of)
            if len(any_matches) < min_match:
                continue

            matches.append({
                "id": pattern_id,
                "label": pattern["label"],
                "description": pattern["description"],
                "matched_sources": list(required.union(any_matches)),
            })

        return matches
