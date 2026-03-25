"""
Extracts topics from raw signal data.

Uses a combination of:
1. Keyword extraction (NLP-lite, no heavy dependencies)
2. Named entity recognition patterns
3. Signal source-specific extraction rules
"""
import re
from typing import Optional

# Common stop words to filter out
STOP_WORDS = {
    "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for",
    "of", "with", "by", "from", "is", "are", "was", "were", "be", "been",
    "being", "have", "has", "had", "do", "does", "did", "will", "would",
    "could", "should", "may", "might", "can", "shall", "it", "its",
    "this", "that", "these", "those", "i", "you", "he", "she", "we",
    "they", "me", "him", "her", "us", "them", "my", "your", "his",
    "our", "their", "what", "which", "who", "whom", "how", "when",
    "where", "why", "all", "each", "every", "both", "few", "more",
    "most", "other", "some", "such", "no", "not", "only", "own",
    "same", "so", "than", "too", "very", "just", "about", "above",
    "after", "again", "also", "as", "because", "before", "between",
    "into", "through", "during", "here", "there", "then", "now",
    "new", "show", "shows", "get", "gets", "got", "use", "uses",
    "used", "using", "make", "makes", "made", "like", "one", "two",
    "first", "way", "even", "go", "going", "think", "know", "see",
    "come", "take", "want", "look", "give", "still", "many", "much",
    "need", "try", "ask", "find", "tell", "let", "say", "help",
}

# Patterns for known entities and topics
KNOWN_PATTERNS = [
    # AI models and products
    r'\b(GPT-?[0-9]+[a-z]?)\b',
    r'\b(Claude\s*[0-9]*\.?[0-9]*)\b',
    r'\b(Gemini\s*[0-9]*\.?[0-9]*)\b',
    r'\b(Llama\s*[0-9]*\.?[0-9]*)\b',
    r'\b(ChatGPT)\b',
    r'\b(Stable\s*Diffusion\s*[0-9]*\.?[0-9]*)\b',
    r'\b(Midjourney)\b',
    r'\b(DALL-?E\s*[0-9]*)\b',

    # Tech companies/products
    r'\b(Apple|Google|Microsoft|Amazon|Meta|Netflix|Tesla|SpaceX|OpenAI|Anthropic|NVIDIA)\b',
    r'\b(iPhone\s*[0-9]*)\b',
    r'\b(React|Next\.js|Vue|Angular|Svelte)\b',
    r'\b(Rust|Go|Python|TypeScript|JavaScript|Swift|Kotlin)\b',
    r'\b(Docker|Kubernetes|Terraform)\b',
    r'\b(VS\s*Code|Cursor|Neovim)\b',

    # Crypto
    r'\b(Bitcoin|Ethereum|Solana|Cardano|Polygon|Dogecoin)\b',
    r'\b(BTC|ETH|SOL|ADA|DOGE)\b',

    # Common topic phrases
    r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)\b',  # Multi-word proper nouns
]


class TopicExtractor:
    """Extracts topics from raw signal data."""

    def extract_topics(self, signal_title: str, signal_content: str = "", source: str = "") -> list[str]:
        """
        Extract topic keywords/phrases from a signal.

        Returns list of topic strings, ordered by relevance.
        """
        text = f"{signal_title} {signal_content}"
        topics = []
        seen = set()

        # 1. Extract known entity patterns
        for pattern in KNOWN_PATTERNS:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                normalized = match.strip()
                if normalized.lower() not in seen and len(normalized) > 1:
                    seen.add(normalized.lower())
                    topics.append(normalized)

        # 2. Extract capitalized phrases (likely proper nouns/topics)
        cap_phrases = re.findall(r'([A-Z][a-zA-Z0-9]*(?:[\s-][A-Z][a-zA-Z0-9]*)*)', text)
        for phrase in cap_phrases:
            normalized = phrase.strip()
            if (
                normalized.lower() not in seen
                and normalized.lower() not in STOP_WORDS
                and len(normalized) > 2
            ):
                seen.add(normalized.lower())
                topics.append(normalized)

        # 3. Source-specific extraction
        source_topics = self._extract_source_specific(signal_title, source)
        for topic in source_topics:
            if topic.lower() not in seen:
                seen.add(topic.lower())
                topics.append(topic)

        # 4. Extract significant n-grams from title
        title_topics = self._extract_ngrams(signal_title)
        for topic in title_topics:
            if topic.lower() not in seen:
                seen.add(topic.lower())
                topics.append(topic)

        return topics[:10]  # Limit to top 10 topics per signal

    def _extract_source_specific(self, title: str, source: str) -> list[str]:
        """Extract topics using source-specific rules."""
        topics = []

        if source == "github_trending":
            # GitHub: repo name is usually the topic
            # Format: "repo-name: description"
            if ":" in title:
                repo_name = title.split(":")[0].strip()
                topics.append(repo_name)

        elif source == "npm_registry" or source == "pypi_stats":
            # Package name is the topic
            # Format: "package@version: description"
            if "@" in title:
                pkg_name = title.split("@")[0].strip()
                topics.append(pkg_name)
            elif "\u2014" in title:
                pkg_name = title.split("\u2014")[0].strip()
                topics.append(pkg_name)

        elif source == "arxiv":
            # ArXiv: extract key terms from paper titles
            # Remove common paper title prefixes
            cleaned = re.sub(r'^(towards|on|a|the|an)\s+', '', title, flags=re.IGNORECASE)
            # Extract the main topic phrase (usually first few words)
            words = cleaned.split()[:5]
            if words:
                topics.append(" ".join(words))

        elif source == "coingecko":
            # Crypto: coin name and symbol
            match = re.match(r'(.+?)\s*\((\w+)\)', title)
            if match:
                topics.append(match.group(1))
                topics.append(match.group(2))

        return topics

    def _extract_ngrams(self, text: str, min_n: int = 2, max_n: int = 3) -> list[str]:
        """Extract significant word n-grams from text."""
        # Clean and tokenize
        words = re.findall(r'[a-zA-Z0-9]+(?:[-\.][a-zA-Z0-9]+)*', text)
        words = [w for w in words if w.lower() not in STOP_WORDS and len(w) > 2]

        topics = []
        for n in range(min_n, min(max_n + 1, len(words) + 1)):
            for i in range(len(words) - n + 1):
                ngram = " ".join(words[i:i + n])
                if len(ngram) > 5:  # Skip very short n-grams
                    topics.append(ngram)

        return topics[:5]  # Limit

    def extract_primary_topic(self, signal_title: str, signal_content: str = "", source: str = "") -> Optional[str]:
        """Extract the single most relevant topic from a signal."""
        topics = self.extract_topics(signal_title, signal_content, source)
        return topics[0] if topics else None
