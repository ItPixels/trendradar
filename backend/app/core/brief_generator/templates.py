"""Brief generation templates for different content types."""

ARTICLE_TEMPLATE = {
    "structure": {
        "intro": "Hook the reader with the trend's significance and urgency",
        "sections": [
            "What's happening (the trend)",
            "Why it matters (the context)",
            "Key data and signals",
            "What to do about it (actionable takeaways)",
        ],
        "conclusion": "Forward-looking statement with CTA",
    },
}

TWITTER_THREAD_TEMPLATE = {
    "structure": {
        "tweet_1": "Hook tweet with bold claim + emoji",
        "tweets_2_to_8": "Supporting evidence, data points, examples",
        "tweet_9": "Contrarian take or nuance",
        "tweet_10": "Summary + CTA (follow for more, check out TrendRadar)",
    },
}

YOUTUBE_SCRIPT_TEMPLATE = {
    "structure": {
        "hook": "0-30 seconds: attention-grabbing statement",
        "intro": "30-60 seconds: what we're covering and why",
        "body": [
            "Section 1: The trend explained",
            "Section 2: Evidence and data",
            "Section 3: Implications",
        ],
        "conclusion": "Summary + opinion + CTA (like/subscribe)",
    },
}
