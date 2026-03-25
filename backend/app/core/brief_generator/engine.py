"""Content brief generation engine."""
import json
import logging
from typing import Optional
from app.ai.client import ai_client
from app.ai.prompts.content_brief import (
    BRIEF_SYSTEM_PROMPT,
    BRIEF_USER_PROMPT,
    BRIEF_FORMATS,
)
from app.ai.guardrails import guardrails
from app.ai.rate_limiter import ai_rate_limiter, AIRateLimiter

logger = logging.getLogger(__name__)

class BriefGenerator:
    """Generates AI-powered content briefs for trending topics."""

    async def generate(
        self,
        topic: str,
        category: str = "Technology",
        trend_score: float = 0,
        predicted_growth: float = 0,
        timeframe_hours: int = 24,
        active_sources: list[str] = None,
        status: str = "active",
        key_signals: str = "",
        format: str = "article",
        target_audience: str = "content creators and marketers",
    ) -> Optional[dict]:
        """Generate a content brief for a trend."""

        # Check guardrails
        if not guardrails.is_topic_allowed(topic):
            logger.warning(f"Topic blocked by guardrails: {topic}")
            return None

        # Check rate limit
        if not ai_rate_limiter.check_rate_limit("brief", 50):
            logger.warning("Brief generation rate limit exceeded")
            return None

        format_description = BRIEF_FORMATS.get(format, BRIEF_FORMATS["article"])

        prompt = BRIEF_USER_PROMPT.format(
            topic=topic,
            category=category,
            trend_score=trend_score,
            predicted_growth=predicted_growth,
            timeframe_hours=timeframe_hours,
            active_sources=", ".join(active_sources or []),
            status=status,
            key_signals=key_signals or "No specific signals provided",
            format_description=format_description,
            target_audience=target_audience,
        )

        try:
            response = await ai_client.generate_json(
                system=BRIEF_SYSTEM_PROMPT,
                user_message=prompt,
                max_tokens=3000,
            )

            # Parse JSON response
            brief = json.loads(response)

            # Validate
            if not guardrails.validate_brief_output(brief):
                logger.warning(f"Invalid brief output for topic: {topic}")
                return None

            # Record the API call
            ai_rate_limiter.record_call("brief")

            # Add metadata
            brief["format"] = format
            brief["model_version"] = "v1"

            return brief

        except json.JSONDecodeError:
            logger.error(f"Failed to parse brief JSON for topic: {topic}")
            return None
        except Exception as e:
            logger.error(f"Failed to generate brief for topic {topic}: {e}")
            return None
