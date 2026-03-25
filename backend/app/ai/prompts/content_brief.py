"""Prompts for AI content brief generation."""

BRIEF_SYSTEM_PROMPT = """You are TrendRadar's content strategist AI. You create actionable content briefs for trending topics.

Your briefs help content creators (YouTubers, bloggers, Twitter/X influencers, newsletter writers) capitalize on emerging trends BEFORE they peak.

Guidelines:
- Be specific and actionable — not generic advice
- Include concrete hooks, angles, and structures
- Tailor to the requested format (article, tweet thread, video script, etc.)
- Reference the trend data to justify why NOW is the right time
- Include SEO keywords and hashtags that are relevant
- Consider the trend's velocity and predicted peak timing"""

BRIEF_FORMATS = {
    "article": "blog article (1500-2000 words)",
    "twitter_thread": "Twitter/X thread (8-12 tweets)",
    "youtube_script": "YouTube video script (8-12 minutes)",
    "tiktok": "TikTok/Reels video (60-90 seconds)",
    "linkedin": "LinkedIn post (300-500 words)",
    "newsletter": "newsletter edition (800-1200 words)",
    "podcast_outline": "podcast episode outline (20-30 minutes)",
}

BRIEF_USER_PROMPT = """Create a content brief for this trending topic:

**Topic:** {topic}
**Category:** {category}
**Trend Score:** {trend_score}/100
**Predicted Growth:** {predicted_growth}% in next {timeframe_hours}h
**Active Sources:** {active_sources}
**Status:** {status}
**Key Signals:**
{key_signals}

**Format requested:** {format_description}
**Target audience:** {target_audience}

Generate the brief as JSON:
{{
  "title": "<compelling title>",
  "hook": "<opening hook that grabs attention>",
  "key_points": [
    {{"point": "<point>", "detail": "<supporting detail>", "source": "<data source>"}}
  ],
  "structure": {{
    "intro": "<intro approach>",
    "sections": ["<section 1>", "<section 2>", ...],
    "conclusion": "<conclusion approach>",
    "cta": "<call to action>"
  }},
  "seo_keywords": ["<keyword 1>", "<keyword 2>", ...],
  "hashtags": ["#tag1", "#tag2", ...],
  "recommended_platforms": ["<platform 1>", ...],
  "optimal_timing": "<when to publish and why>",
  "tone": "<recommended tone>",
  "word_count_target": <number>,
  "unique_angle": "<what makes this brief different from generic coverage>"
}}"""
