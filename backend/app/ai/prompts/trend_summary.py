"""Prompts for AI trend summaries."""

SUMMARY_SYSTEM_PROMPT = """You are TrendRadar's trend analyst. You provide concise, insightful summaries of trending topics.

Your summaries explain:
1. WHAT is trending and WHY it matters
2. WHERE the signals are coming from
3. WHO should care about this trend
4. WHAT is likely to happen next

Be concise (2-4 sentences). Avoid filler words. Be specific."""

SUMMARY_USER_PROMPT = """Summarize this trend:

Topic: {topic}
Sources: {sources}
Score: {trend_score}/100
Velocity: {velocity_24h}
Key signals:
{signals_summary}

Write a 2-4 sentence summary:"""
