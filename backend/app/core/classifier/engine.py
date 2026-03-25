import logging
from typing import Optional
from app.core.classifier.categories import CATEGORY_KEYWORDS, DEFAULT_CATEGORIES

logger = logging.getLogger(__name__)

class CategoryClassifier:
    """
    Classifies trends into categories using keyword matching and AI.

    Two-stage classification:
    1. Fast keyword-based classification (no API calls)
    2. AI-based classification for ambiguous cases (uses Claude)
    """

    def classify(
        self,
        topic: str,
        title: str = "",
        content: str = "",
        tags: list[str] = None,
        source: str = "",
    ) -> dict:
        """
        Classify a topic into a category.

        Returns:
            Dict with category_slug, confidence, method
        """
        text = f"{topic} {title} {content} {' '.join(tags or [])}".lower()

        scores = {}
        for category_slug, keywords in CATEGORY_KEYWORDS.items():
            score = 0
            matched_keywords = []

            for keyword, weight in keywords:
                if keyword.lower() in text:
                    score += weight
                    matched_keywords.append(keyword)

            if score > 0:
                scores[category_slug] = {
                    "score": score,
                    "matched_keywords": matched_keywords,
                }

        if not scores:
            return {
                "category_slug": "tech",  # Default fallback
                "confidence": 0.3,
                "method": "default",
                "matched_keywords": [],
            }

        # Get the best match
        best_slug = max(scores, key=lambda k: scores[k]["score"])
        best = scores[best_slug]
        max_possible = sum(w for _, w in CATEGORY_KEYWORDS.get(best_slug, []))
        confidence = min(best["score"] / max(max_possible * 0.3, 1), 1.0)

        return {
            "category_slug": best_slug,
            "confidence": round(confidence, 2),
            "method": "keyword",
            "matched_keywords": best["matched_keywords"],
            "all_scores": {k: v["score"] for k, v in scores.items()},
        }

    def classify_batch(self, items: list[dict]) -> list[dict]:
        """Classify a batch of items."""
        return [
            self.classify(
                topic=item.get("topic", ""),
                title=item.get("title", ""),
                content=item.get("content", ""),
                tags=item.get("tags"),
                source=item.get("source", ""),
            )
            for item in items
        ]
