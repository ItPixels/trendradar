"""
Topic normalization -- maps variant spellings/forms to canonical topics.

"GPT-5", "GPT5", "gpt 5" -> "GPT-5"
"Next.js", "nextjs", "next js" -> "Next.js"
"""
import re
from typing import Optional

# Known canonical forms and their variants
CANONICAL_FORMS: dict[str, list[str]] = {
    "GPT-4": ["gpt4", "gpt 4", "gpt-4o", "gpt4o"],
    "GPT-5": ["gpt5", "gpt 5"],
    "ChatGPT": ["chatgpt", "chat gpt", "chat-gpt"],
    "Claude": ["claude", "claude 3", "claude 4", "claude ai"],
    "Gemini": ["gemini", "google gemini", "bard"],
    "Llama": ["llama", "llama 2", "llama 3", "llama2", "llama3", "meta llama"],
    "Stable Diffusion": ["stablediffusion", "stable-diffusion", "sd", "sdxl"],
    "Midjourney": ["midjourney", "mid journey", "mid-journey"],
    "DALL-E": ["dalle", "dall e", "dall-e 3", "dalle3"],
    "OpenAI": ["openai", "open ai", "open-ai"],
    "Anthropic": ["anthropic"],
    "NVIDIA": ["nvidia", "nvda"],
    "Next.js": ["nextjs", "next js", "next.js"],
    "React": ["react", "reactjs", "react.js"],
    "Vue.js": ["vue", "vuejs", "vue.js"],
    "Svelte": ["svelte", "sveltekit"],
    "TypeScript": ["typescript", "ts"],
    "JavaScript": ["javascript", "js"],
    "Rust": ["rust", "rust-lang", "rustlang"],
    "Python": ["python", "python3"],
    "Docker": ["docker"],
    "Kubernetes": ["kubernetes", "k8s"],
    "Bitcoin": ["bitcoin", "btc"],
    "Ethereum": ["ethereum", "eth"],
    "Solana": ["solana", "sol"],
    "Apple": ["apple"],
    "Google": ["google", "alphabet"],
    "Microsoft": ["microsoft", "msft"],
    "Tesla": ["tesla", "tsla"],
    "SpaceX": ["spacex", "space x"],
    "VS Code": ["vscode", "vs code", "visual studio code"],
    "Cursor": ["cursor", "cursor ai"],
    "Linux": ["linux", "gnu/linux"],
    "AI": ["artificial intelligence", "ai"],
    "Machine Learning": ["machine learning", "ml"],
    "LLM": ["large language model", "llm", "large language models"],
    "AGI": ["agi", "artificial general intelligence"],
    "Web3": ["web3", "web 3", "web3.0"],
    "DeFi": ["defi", "decentralized finance"],
    "NFT": ["nft", "nfts", "non-fungible token"],
}

# Build reverse lookup
_VARIANT_TO_CANONICAL: dict[str, str] = {}
for canonical, variants in CANONICAL_FORMS.items():
    for variant in variants:
        _VARIANT_TO_CANONICAL[variant.lower()] = canonical
    _VARIANT_TO_CANONICAL[canonical.lower()] = canonical


class TopicNormalizer:
    """Normalizes topic strings to canonical forms."""

    def normalize(self, topic: str) -> str:
        """
        Normalize a topic string to its canonical form.

        1. Check known canonical forms
        2. Clean whitespace and punctuation
        3. Capitalize appropriately
        """
        if not topic:
            return topic

        # Check known forms
        lower = topic.lower().strip()
        if lower in _VARIANT_TO_CANONICAL:
            return _VARIANT_TO_CANONICAL[lower]

        # Try partial matches for multi-word topics
        for variant, canonical in _VARIANT_TO_CANONICAL.items():
            if variant in lower and len(variant) > 3:
                return canonical

        # Clean and standardize
        cleaned = self._clean_topic(topic)

        return cleaned

    def normalize_batch(self, topics: list[str]) -> list[str]:
        """Normalize a batch of topics."""
        return [self.normalize(t) for t in topics]

    def create_slug(self, topic: str) -> str:
        """Create a URL-safe slug from a topic."""
        # Normalize first
        normalized = self.normalize(topic)

        # Create slug
        slug = normalized.lower()
        slug = re.sub(r'[^a-z0-9\s-]', '', slug)
        slug = re.sub(r'[\s]+', '-', slug)
        slug = re.sub(r'-+', '-', slug)
        slug = slug.strip('-')

        return slug or "unknown"

    def are_same_topic(self, topic_a: str, topic_b: str) -> bool:
        """Check if two topic strings refer to the same topic."""
        norm_a = self.normalize(topic_a).lower()
        norm_b = self.normalize(topic_b).lower()

        if norm_a == norm_b:
            return True

        # Check if one contains the other (for partial matches)
        if len(norm_a) > 3 and len(norm_b) > 3:
            if norm_a in norm_b or norm_b in norm_a:
                return True

        return False

    def _clean_topic(self, topic: str) -> str:
        """Clean a topic string."""
        # Remove extra whitespace
        cleaned = re.sub(r'\s+', ' ', topic.strip())

        # Capitalize first letter of each word (title case) for unknown topics
        if not any(c.isupper() for c in cleaned[1:]):
            cleaned = cleaned.title()

        return cleaned
