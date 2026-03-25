-- Initial schema migration
-- Extracted from backend/alembic/versions/001_initial_schema.py

-- updated_at trigger function
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Enable pgcrypto for gen_random_uuid
CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- categories table
CREATE TABLE public.categories (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    slug TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL,
    description TEXT,
    icon TEXT,
    color TEXT NOT NULL DEFAULT '#6366f1',
    parent_id UUID REFERENCES public.categories(id),
    sort_order INTEGER DEFAULT 0,
    is_default BOOLEAN DEFAULT false,
    is_active BOOLEAN DEFAULT true,
    trend_count_24h INTEGER DEFAULT 0,
    trend_count_7d INTEGER DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);
CREATE INDEX idx_categories_slug ON public.categories(slug);
CREATE TRIGGER categories_updated_at BEFORE UPDATE ON public.categories
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();

-- Seed default categories
INSERT INTO public.categories (slug, name, icon, color, is_default, sort_order) VALUES
    ('tech', 'Technology', 'Cpu', '#6366f1', true, 1),
    ('ai', 'Artificial Intelligence', 'Brain', '#8b5cf6', true, 2),
    ('crypto', 'Crypto & Web3', 'Bitcoin', '#f59e0b', true, 3),
    ('business', 'Business', 'Briefcase', '#10b981', true, 4),
    ('science', 'Science', 'Atom', '#06b6d4', true, 5),
    ('health', 'Health & Wellness', 'Heart', '#ef4444', true, 6),
    ('culture', 'Culture & Entertainment', 'Music', '#ec4899', true, 7),
    ('politics', 'Politics', 'Landmark', '#64748b', true, 8),
    ('gaming', 'Gaming', 'Gamepad2', '#84cc16', true, 9),
    ('finance', 'Finance & Markets', 'TrendingUp', '#0ea5e9', true, 10),
    ('sports', 'Sports', 'Trophy', '#f97316', true, 11),
    ('design', 'Design & UX', 'Palette', '#d946ef', true, 12),
    ('devtools', 'Developer Tools', 'Code', '#22d3ee', true, 13),
    ('opensource', 'Open Source', 'GitBranch', '#a3e635', true, 14);

-- trends table
CREATE TABLE public.trends (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    topic TEXT NOT NULL,
    topic_slug TEXT NOT NULL,
    description TEXT,
    summary TEXT,
    category_id UUID REFERENCES public.categories(id),
    subcategory TEXT,
    tags TEXT[] DEFAULT '{}',
    trend_score FLOAT NOT NULL DEFAULT 0,
    velocity_score FLOAT DEFAULT 0,
    correlation_score FLOAT DEFAULT 0,
    signal_strength FLOAT DEFAULT 0,
    sentiment_score FLOAT DEFAULT 0,
    signal_count_1h INTEGER DEFAULT 0,
    signal_count_6h INTEGER DEFAULT 0,
    signal_count_24h INTEGER DEFAULT 0,
    signal_count_7d INTEGER DEFAULT 0,
    velocity_1h FLOAT DEFAULT 0,
    velocity_6h FLOAT DEFAULT 0,
    velocity_24h FLOAT DEFAULT 0,
    acceleration FLOAT DEFAULT 0,
    active_sources TEXT[] DEFAULT '{}',
    source_count INTEGER DEFAULT 0,
    first_source TEXT,
    first_seen_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    status TEXT DEFAULT 'active' CHECK (status IN ('emerging', 'active', 'peaking', 'declining', 'dead')),
    peak_at TIMESTAMPTZ,
    is_viral BOOLEAN DEFAULT false,
    is_breaking BOOLEAN DEFAULT false,
    ai_analysis JSONB DEFAULT '{}',
    last_ai_update TIMESTAMPTZ,
    view_count INTEGER DEFAULT 0,
    share_count INTEGER DEFAULT 0,
    bookmark_count INTEGER DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    deleted_at TIMESTAMPTZ
);
CREATE INDEX idx_trends_score ON public.trends(trend_score DESC) WHERE deleted_at IS NULL;
CREATE INDEX idx_trends_velocity ON public.trends(velocity_24h DESC) WHERE deleted_at IS NULL;
CREATE INDEX idx_trends_category ON public.trends(category_id) WHERE deleted_at IS NULL;
CREATE INDEX idx_trends_status ON public.trends(status) WHERE deleted_at IS NULL;
CREATE INDEX idx_trends_topic_slug ON public.trends(topic_slug);
CREATE INDEX idx_trends_first_seen ON public.trends(first_seen_at DESC);
CREATE INDEX idx_trends_sources ON public.trends USING GIN(active_sources);
CREATE INDEX idx_trends_tags ON public.trends USING GIN(tags);
CREATE TRIGGER trends_updated_at BEFORE UPDATE ON public.trends
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();

-- signal_events table
CREATE TABLE public.signal_events (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    trend_id UUID REFERENCES public.trends(id) ON DELETE CASCADE,
    source TEXT NOT NULL,
    source_id TEXT,
    title TEXT NOT NULL,
    url TEXT,
    content TEXT,
    author TEXT,
    metrics JSONB DEFAULT '{}',
    extracted_topics TEXT[] DEFAULT '{}',
    signal_strength FLOAT DEFAULT 0,
    raw_data JSONB DEFAULT '{}',
    processed BOOLEAN DEFAULT false,
    detected_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    created_at TIMESTAMPTZ DEFAULT NOW()
);
CREATE INDEX idx_signals_trend ON public.signal_events(trend_id);
CREATE INDEX idx_signals_source ON public.signal_events(source);
CREATE INDEX idx_signals_detected ON public.signal_events(detected_at DESC);
CREATE INDEX idx_signals_topics ON public.signal_events USING GIN(extracted_topics);
CREATE INDEX idx_signals_source_id ON public.signal_events(source, source_id);

-- predictions table
CREATE TABLE public.predictions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    trend_id UUID NOT NULL REFERENCES public.trends(id) ON DELETE CASCADE,
    predicted_growth FLOAT NOT NULL,
    confidence_score FLOAT NOT NULL DEFAULT 0,
    timeframe_hours INTEGER NOT NULL DEFAULT 24,
    predicted_peak_at TIMESTAMPTZ,
    model_version TEXT DEFAULT 'v1',
    input_features JSONB DEFAULT '{}',
    status TEXT DEFAULT 'pending' CHECK (status IN ('pending', 'correct', 'partially_correct', 'incorrect', 'expired')),
    actual_growth FLOAT,
    evaluated_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);
CREATE INDEX idx_predictions_trend ON public.predictions(trend_id);
CREATE INDEX idx_predictions_status ON public.predictions(status);
CREATE INDEX idx_predictions_confidence ON public.predictions(confidence_score DESC);
CREATE TRIGGER predictions_updated_at BEFORE UPDATE ON public.predictions
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();

-- prediction_factors table
CREATE TABLE public.prediction_factors (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    prediction_id UUID NOT NULL REFERENCES public.predictions(id) ON DELETE CASCADE,
    factor TEXT NOT NULL,
    impact TEXT NOT NULL CHECK (impact IN ('positive', 'negative', 'neutral')),
    weight FLOAT NOT NULL DEFAULT 0,
    description TEXT,
    source_type TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
CREATE INDEX idx_pred_factors_prediction ON public.prediction_factors(prediction_id);

-- alerts table
CREATE TABLE public.alerts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL,
    name TEXT NOT NULL,
    description TEXT,
    categories TEXT[] DEFAULT '{}',
    keywords TEXT[] DEFAULT '{}',
    excluded_keywords TEXT[] DEFAULT '{}',
    min_score FLOAT DEFAULT 50,
    min_velocity FLOAT DEFAULT 0,
    min_sources INTEGER DEFAULT 2,
    channels TEXT[] DEFAULT '{email}',
    webhook_url TEXT,
    is_active BOOLEAN DEFAULT true,
    trigger_count INTEGER DEFAULT 0,
    last_triggered_at TIMESTAMPTZ,
    cooldown_minutes INTEGER DEFAULT 60,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    deleted_at TIMESTAMPTZ
);
CREATE INDEX idx_alerts_user ON public.alerts(user_id) WHERE deleted_at IS NULL;
CREATE INDEX idx_alerts_active ON public.alerts(is_active) WHERE deleted_at IS NULL;
CREATE TRIGGER alerts_updated_at BEFORE UPDATE ON public.alerts
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();

-- alert_triggers table
CREATE TABLE public.alert_triggers (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    alert_id UUID NOT NULL REFERENCES public.alerts(id) ON DELETE CASCADE,
    trend_id UUID NOT NULL REFERENCES public.trends(id) ON DELETE CASCADE,
    matched_score FLOAT,
    matched_velocity FLOAT,
    matched_sources TEXT[] DEFAULT '{}',
    notification_sent BOOLEAN DEFAULT false,
    channels_sent TEXT[] DEFAULT '{}',
    triggered_at TIMESTAMPTZ DEFAULT NOW()
);
CREATE INDEX idx_alert_triggers_alert ON public.alert_triggers(alert_id);
CREATE INDEX idx_alert_triggers_trend ON public.alert_triggers(trend_id);

-- content_briefs table
CREATE TABLE public.content_briefs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    trend_id UUID NOT NULL REFERENCES public.trends(id) ON DELETE CASCADE,
    user_id UUID NOT NULL,
    format TEXT NOT NULL DEFAULT 'article' CHECK (format IN ('article', 'twitter_thread', 'youtube_script', 'tiktok', 'linkedin', 'newsletter', 'podcast_outline')),
    title TEXT NOT NULL,
    hook TEXT,
    key_points JSONB DEFAULT '[]',
    structure JSONB DEFAULT '{}',
    seo_keywords TEXT[] DEFAULT '{}',
    hashtags TEXT[] DEFAULT '{}',
    recommended_platforms TEXT[] DEFAULT '{}',
    optimal_timing TEXT,
    target_audience TEXT,
    tone TEXT DEFAULT 'informative',
    word_count_target INTEGER,
    full_brief TEXT,
    model_version TEXT DEFAULT 'v1',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);
CREATE INDEX idx_briefs_trend ON public.content_briefs(trend_id);
CREATE INDEX idx_briefs_user ON public.content_briefs(user_id);
CREATE TRIGGER briefs_updated_at BEFORE UPDATE ON public.content_briefs
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();

-- scan_logs table
CREATE TABLE public.scan_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    source TEXT NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('success', 'partial', 'failed')),
    signals_found INTEGER DEFAULT 0,
    signals_new INTEGER DEFAULT 0,
    duration_ms INTEGER,
    error_message TEXT,
    metadata JSONB DEFAULT '{}',
    scanned_at TIMESTAMPTZ DEFAULT NOW()
);
CREATE INDEX idx_scan_logs_source ON public.scan_logs(source);
CREATE INDEX idx_scan_logs_scanned ON public.scan_logs(scanned_at DESC);

-- source_health table
CREATE TABLE public.source_health (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    source TEXT NOT NULL UNIQUE,
    is_healthy BOOLEAN DEFAULT true,
    last_success_at TIMESTAMPTZ,
    last_failure_at TIMESTAMPTZ,
    consecutive_failures INTEGER DEFAULT 0,
    avg_response_ms FLOAT,
    total_requests INTEGER DEFAULT 0,
    total_failures INTEGER DEFAULT 0,
    error_rate FLOAT DEFAULT 0,
    last_error TEXT,
    updated_at TIMESTAMPTZ DEFAULT NOW()
);
CREATE TRIGGER source_health_updated_at BEFORE UPDATE ON public.source_health
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();

-- usage_logs table
CREATE TABLE public.usage_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL,
    action TEXT NOT NULL,
    resource_type TEXT,
    resource_id UUID,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW()
);
CREATE INDEX idx_usage_user ON public.usage_logs(user_id);
CREATE INDEX idx_usage_action ON public.usage_logs(action);
CREATE INDEX idx_usage_created ON public.usage_logs(created_at DESC);
