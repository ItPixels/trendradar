"""AI guardrails — safety checks and content filtering."""
import logging

logger = logging.getLogger(__name__)

# Topics that should not get content briefs
BLOCKED_TOPICS = [
    "self-harm", "suicide", "terrorism", "extremism",
    "child exploitation", "illegal drugs", "weapons manufacturing",
]

# Maximum API calls per hour (cost control)
MAX_PREDICTIONS_PER_HOUR = 100
MAX_BRIEFS_PER_HOUR = 50
MAX_CLASSIFICATIONS_PER_HOUR = 500

class AIGuardrails:
    """Safety checks for AI-generated content."""

    def is_topic_allowed(self, topic: str) -> bool:
        """Check if a topic is allowed for content generation."""
        topic_lower = topic.lower()
        for blocked in BLOCKED_TOPICS:
            if blocked in topic_lower:
                logger.warning(f"Blocked topic detected: {topic}")
                return False
        return True

    def validate_prediction_output(self, output: dict) -> bool:
        """Validate AI prediction output is reasonable."""
        growth = output.get("refined_growth", 0)
        confidence = output.get("refined_confidence", 0)

        # Sanity checks
        if abs(growth) > 10000:  # 10000% growth is unrealistic
            logger.warning(f"Unrealistic growth prediction: {growth}%")
            return False

        if confidence < 0 or confidence > 100:
            return False

        return True

    def validate_brief_output(self, output: dict) -> bool:
        """Validate AI brief output."""
        required_fields = ["title", "hook", "key_points"]
        for field in required_fields:
            if field not in output:
                return False
        return True


guardrails = AIGuardrails()
