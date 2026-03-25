"""Anthropic Claude API client wrapper for TrendRadar."""
import logging
from typing import Optional
import anthropic
from app.config import settings

logger = logging.getLogger(__name__)

# Default model
DEFAULT_MODEL = "claude-sonnet-4-20250514"

class AIClient:
    """Wrapper around Anthropic Claude API for TrendRadar."""

    def __init__(self, model: str = DEFAULT_MODEL):
        self.model = model
        self._client: Optional[anthropic.AsyncAnthropic] = None

    @property
    def client(self) -> anthropic.AsyncAnthropic:
        if self._client is None:
            self._client = anthropic.AsyncAnthropic(api_key=settings.anthropic_api_key)
        return self._client

    async def generate(
        self,
        system: str,
        user_message: str,
        max_tokens: int = 2048,
        temperature: float = 0.7,
    ) -> str:
        """Generate a response from Claude."""
        try:
            response = await self.client.messages.create(
                model=self.model,
                max_tokens=max_tokens,
                system=system,
                messages=[{"role": "user", "content": user_message}],
                temperature=temperature,
            )
            return response.content[0].text
        except anthropic.APIError as e:
            logger.error(f"Claude API error: {e}")
            raise

    async def generate_json(
        self,
        system: str,
        user_message: str,
        max_tokens: int = 2048,
        temperature: float = 0.3,
    ) -> str:
        """Generate a JSON response from Claude (lower temperature for structured output)."""
        system_with_json = f"{system}\n\nIMPORTANT: Respond with valid JSON only. No markdown, no code blocks, just raw JSON."
        return await self.generate(system_with_json, user_message, max_tokens, temperature)

    async def classify(
        self,
        system: str,
        user_message: str,
    ) -> str:
        """Classification task — very low temperature for deterministic output."""
        return await self.generate(system, user_message, max_tokens=100, temperature=0.1)


# Singleton instance
ai_client = AIClient()
