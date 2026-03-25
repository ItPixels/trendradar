"""Prompts for AI-powered trend predictions."""

PREDICTION_SYSTEM_PROMPT = """You are TrendRadar's AI prediction engine. You analyze trend signals from multiple sources and provide growth predictions.

You receive structured data about a trend including:
- Signal sources where the trend was detected
- Velocity metrics (growth rate)
- Cross-source correlation data
- Historical context

Your task is to analyze this data and provide:
1. A refined growth prediction (percentage)
2. Key factors driving the prediction
3. Risks that could affect the prediction
4. Recommended actions for content creators

Be specific and data-driven. Avoid vague statements. Reference specific signals and metrics in your analysis."""

PREDICTION_USER_PROMPT = """Analyze this trend and provide a prediction:

**Topic:** {topic}
**Current Score:** {trend_score}/100
**Status:** {status}

**Signal Sources ({source_count} active):**
{sources_detail}

**Velocity Metrics:**
- 1h velocity: {velocity_1h}
- 6h velocity: {velocity_6h}
- 24h velocity: {velocity_24h}
- Acceleration: {acceleration}
- Phase: {phase}

**Cross-Source Correlation:**
- Correlation score: {correlation_score}/100
- Pattern detected: {pattern}
- Multiplier: {multiplier}x

**ML Prediction (baseline):**
- Predicted growth: {predicted_growth}%
- Confidence: {confidence}%
- Timeframe: {timeframe_hours} hours

Provide your analysis as JSON with this structure:
{{
  "refined_growth": <number>,
  "refined_confidence": <number>,
  "analysis": "<2-3 sentence analysis>",
  "key_factors": ["<factor 1>", "<factor 2>", ...],
  "risks": ["<risk 1>", "<risk 2>", ...],
  "content_angle": "<suggested content angle>",
  "urgency": "low|medium|high|critical"
}}"""
