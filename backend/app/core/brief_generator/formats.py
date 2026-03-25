"""Content brief format definitions."""

FORMAT_CONFIGS = {
    "article": {
        "name": "Blog Article",
        "word_count": (1500, 2000),
        "sections": 4,
        "seo_focus": True,
    },
    "twitter_thread": {
        "name": "Twitter/X Thread",
        "word_count": (400, 800),
        "sections": 10,  # tweets
        "seo_focus": False,
    },
    "youtube_script": {
        "name": "YouTube Script",
        "word_count": (1200, 1800),
        "sections": 5,
        "seo_focus": True,
    },
    "tiktok": {
        "name": "TikTok/Reels Script",
        "word_count": (100, 200),
        "sections": 3,
        "seo_focus": False,
    },
    "linkedin": {
        "name": "LinkedIn Post",
        "word_count": (300, 500),
        "sections": 1,
        "seo_focus": False,
    },
    "newsletter": {
        "name": "Newsletter Edition",
        "word_count": (800, 1200),
        "sections": 3,
        "seo_focus": True,
    },
    "podcast_outline": {
        "name": "Podcast Outline",
        "word_count": (500, 800),
        "sections": 5,
        "seo_focus": False,
    },
}
