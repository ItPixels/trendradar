export type TrendStatus = 'emerging' | 'active' | 'peaking' | 'declining' | 'dead';

export type SignalSource =
  | 'google_trends' | 'reddit' | 'hackernews' | 'youtube_trending'
  | 'github_trending' | 'wikipedia' | 'google_news' | 'producthunt'
  | 'npm_registry' | 'pypi_stats' | 'arxiv' | 'coingecko'
  | 'steam_charts' | 'devto' | 'lobsters' | 'stackoverflow';

export interface Trend {
  id: string;
  topic: string;
  topicSlug: string;
  description?: string;
  summary?: string;
  categoryId?: string;
  tags: string[];
  trendScore: number;
  velocityScore: number;
  correlationScore: number;
  signalStrength: number;
  sentimentScore: number;
  signalCount24h: number;
  velocity24h: number;
  acceleration: number;
  activeSources: SignalSource[];
  sourceCount: number;
  firstSource?: SignalSource;
  firstSeenAt: string;
  status: TrendStatus;
  isViral: boolean;
  isBreaking: boolean;
  viewCount: number;
  shareCount: number;
  createdAt: string;
  updatedAt: string;
}

export interface TrendFilters {
  category?: string;
  sources?: SignalSource[];
  status?: TrendStatus;
  minScore?: number;
  timeRange?: '1h' | '6h' | '24h' | '7d' | '30d';
  sortBy?: 'score' | 'velocity' | 'newest' | 'sources';
}
