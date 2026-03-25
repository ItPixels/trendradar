"""Signal Source Registry with weights and correlation multipliers."""

# Signal sources organized by tier with their weights
SIGNAL_SOURCES = {
    # Tier 1: High-signal, low-noise sources (weight 3x)
    "google_trends": {
        "name": "Google Trends",
        "tier": 1,
        "weight": 3.0,
        "enabled": True,
        "description": "Search interest over time from Google",
    },
    "patent_filings": {
        "name": "Patent Filings",
        "tier": 1,
        "weight": 3.0,
        "enabled": True,
        "description": "New patent applications and grants",
    },
    "academic_papers": {
        "name": "Academic Papers",
        "tier": 1,
        "weight": 3.0,
        "enabled": True,
        "description": "Research papers from arXiv, PubMed, etc.",
    },
    "venture_capital": {
        "name": "Venture Capital Funding",
        "tier": 1,
        "weight": 3.0,
        "enabled": True,
        "description": "VC funding rounds and investment data",
    },
    # Tier 2: Medium-signal sources (weight 2x)
    "reddit": {
        "name": "Reddit",
        "tier": 2,
        "weight": 2.0,
        "enabled": True,
        "description": "Reddit posts and discussions",
    },
    "hacker_news": {
        "name": "Hacker News",
        "tier": 2,
        "weight": 2.0,
        "enabled": True,
        "description": "Hacker News stories and comments",
    },
    "github": {
        "name": "GitHub",
        "tier": 2,
        "weight": 2.0,
        "enabled": True,
        "description": "GitHub repositories, stars, and activity",
    },
    "stack_overflow": {
        "name": "Stack Overflow",
        "tier": 2,
        "weight": 2.0,
        "enabled": True,
        "description": "Stack Overflow questions and tags",
    },
    "product_hunt": {
        "name": "Product Hunt",
        "tier": 2,
        "weight": 2.0,
        "enabled": True,
        "description": "Product Hunt launches and upvotes",
    },
    "youtube": {
        "name": "YouTube",
        "tier": 2,
        "weight": 2.0,
        "enabled": True,
        "description": "YouTube video trends and view counts",
    },
    # Tier 3: High-noise sources (weight 1x)
    "twitter": {
        "name": "Twitter/X",
        "tier": 3,
        "weight": 1.0,
        "enabled": True,
        "description": "Twitter/X posts and hashtag trends",
    },
    "news_rss": {
        "name": "News RSS Feeds",
        "tier": 3,
        "weight": 1.0,
        "enabled": True,
        "description": "News articles from RSS feeds",
    },
    "tiktok": {
        "name": "TikTok",
        "tier": 3,
        "weight": 1.0,
        "enabled": True,
        "description": "TikTok hashtag and content trends",
    },
}

# Correlation multipliers: when multiple sources confirm a signal,
# the composite score is boosted
CORRELATION_MULTIPLIERS = {
    2: 1.2,   # 2 sources confirming = 1.2x boost
    3: 1.5,   # 3 sources = 1.5x
    4: 1.8,   # 4 sources = 1.8x
    5: 2.0,   # 5+ sources = 2.0x
}


def get_correlation_multiplier(source_count: int) -> float:
    """Get the correlation multiplier for a given number of confirming sources."""
    if source_count < 2:
        return 1.0
    for threshold in sorted(CORRELATION_MULTIPLIERS.keys(), reverse=True):
        if source_count >= threshold:
            return CORRELATION_MULTIPLIERS[threshold]
    return 1.0


def get_source_weight(source_key: str) -> float:
    """Get the weight for a given signal source."""
    source = SIGNAL_SOURCES.get(source_key)
    if source is None:
        return 1.0
    return source["weight"]
