"use client";

import { useState } from "react";
import { PageHeader } from "@/components/layout/page-header";
import { TrendFeed } from "@/components/trends/trend-feed";
import { TrendFilters } from "@/components/trends/trend-filters";
import type { Trend, TrendStatus, SignalSource } from "@/lib/types/trend";

// Demo data for initial UI (will be replaced with API calls)
const DEMO_TRENDS: Trend[] = [
  {
    id: "1",
    topic: "Claude 4 Release",
    topicSlug: "claude-4-release",
    description: "Anthropic announces Claude 4 with major improvements in reasoning and code generation",
    tags: ["ai", "llm", "anthropic"],
    trendScore: 92,
    velocityScore: 85,
    correlationScore: 88,
    signalStrength: 90,
    sentimentScore: 0.8,
    signalCount24h: 347,
    velocity24h: 2.4,
    acceleration: 0.8,
    activeSources: ["hackernews", "reddit", "google_trends", "youtube_trending", "github_trending"],
    sourceCount: 5,
    firstSource: "hackernews",
    firstSeenAt: new Date().toISOString(),
    status: "emerging",
    isViral: true,
    isBreaking: false,
    viewCount: 12453,
    shareCount: 892,
    createdAt: new Date().toISOString(),
    updatedAt: new Date().toISOString(),
  },
  {
    id: "2",
    topic: "Rust 2.0 Announcement",
    topicSlug: "rust-2-0",
    description: "Rust programming language announces version 2.0 with backward-compatible improvements",
    tags: ["rust", "programming", "devtools"],
    trendScore: 78,
    velocityScore: 72,
    correlationScore: 65,
    signalStrength: 75,
    sentimentScore: 0.9,
    signalCount24h: 189,
    velocity24h: 1.2,
    acceleration: 0.3,
    activeSources: ["hackernews", "reddit", "github_trending", "lobsters"],
    sourceCount: 4,
    firstSource: "hackernews",
    firstSeenAt: new Date().toISOString(),
    status: "active",
    isViral: false,
    isBreaking: false,
    viewCount: 5672,
    shareCount: 345,
    createdAt: new Date().toISOString(),
    updatedAt: new Date().toISOString(),
  },
  {
    id: "3",
    topic: "Bitcoin ETF Inflows Record",
    topicSlug: "bitcoin-etf-inflows",
    description: "Bitcoin ETFs see record $2.4B single-day inflows amid institutional adoption surge",
    tags: ["bitcoin", "crypto", "etf", "finance"],
    trendScore: 85,
    velocityScore: 90,
    correlationScore: 72,
    signalStrength: 82,
    sentimentScore: 0.7,
    signalCount24h: 256,
    velocity24h: 3.1,
    acceleration: 1.2,
    activeSources: ["coingecko", "reddit", "google_trends", "google_news"],
    sourceCount: 4,
    firstSource: "coingecko",
    firstSeenAt: new Date().toISOString(),
    status: "emerging",
    isViral: false,
    isBreaking: true,
    viewCount: 8901,
    shareCount: 567,
    createdAt: new Date().toISOString(),
    updatedAt: new Date().toISOString(),
  },
  {
    id: "4",
    topic: "Next.js 15 App Router",
    topicSlug: "nextjs-15-app-router",
    description: "Next.js 15 introduces new App Router features with improved Server Components performance",
    tags: ["nextjs", "react", "webdev"],
    trendScore: 68,
    velocityScore: 55,
    correlationScore: 48,
    signalStrength: 60,
    sentimentScore: 0.75,
    signalCount24h: 142,
    velocity24h: 0.8,
    acceleration: 0.1,
    activeSources: ["hackernews", "reddit", "npm_registry"],
    sourceCount: 3,
    firstSource: "hackernews",
    firstSeenAt: new Date().toISOString(),
    status: "active",
    isViral: false,
    isBreaking: false,
    viewCount: 3421,
    shareCount: 198,
    createdAt: new Date().toISOString(),
    updatedAt: new Date().toISOString(),
  },
  {
    id: "5",
    topic: "GPT-5 Rumors",
    topicSlug: "gpt-5-rumors",
    description: "Reports suggest OpenAI is testing GPT-5 internally with significant reasoning improvements",
    tags: ["openai", "gpt", "ai"],
    trendScore: 74,
    velocityScore: 60,
    correlationScore: 55,
    signalStrength: 65,
    sentimentScore: 0.6,
    signalCount24h: 198,
    velocity24h: 1.5,
    acceleration: 0.5,
    activeSources: ["reddit", "google_trends", "youtube_trending", "arxiv"],
    sourceCount: 4,
    firstSource: "reddit",
    firstSeenAt: new Date().toISOString(),
    status: "active",
    isViral: false,
    isBreaking: false,
    viewCount: 7234,
    shareCount: 412,
    createdAt: new Date().toISOString(),
    updatedAt: new Date().toISOString(),
  },
];

export default function ExplorePage() {
  const [category, setCategory] = useState<string | undefined>(undefined);
  const [timeRange, setTimeRange] = useState("24h");
  const [sortBy, setSortBy] = useState("score");

  // TODO: Replace with SWR/API call
  const trends = DEMO_TRENDS;

  return (
    <div>
      <PageHeader
        title="Explore Trends"
        description="Real-time trending topics from 15+ signal sources"
      />

      <TrendFilters
        selectedCategory={category}
        selectedTimeRange={timeRange}
        selectedSort={sortBy}
        onCategoryChange={setCategory}
        onTimeRangeChange={setTimeRange}
        onSortChange={setSortBy}
      />

      <TrendFeed trends={trends} showRank />
    </div>
  );
}
