"use client";

import { useState, useEffect } from "react";
import { PageHeader } from "@/components/layout/page-header";
import { TrendFeed } from "@/components/trends/trend-feed";
import { TrendFilters } from "@/components/trends/trend-filters";
import { getTrends } from "@/lib/api/trends";
import type { Trend } from "@/lib/types/trend";

export default function ExplorePage() {
  const [category, setCategory] = useState<string | undefined>(undefined);
  const [timeRange, setTimeRange] = useState("24h");
  const [sortBy, setSortBy] = useState("score");
  const [trends, setTrends] = useState<Trend[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;

    async function fetchTrends() {
      setLoading(true);
      setError(null);
      try {
        const data = await getTrends({
          category,
          timeRange: timeRange as "24h" | "7d" | "30d",
          sortBy: sortBy as "score" | "velocity" | "newest" | "sources",
        });
        if (!cancelled) {
          setTrends(data.items);
        }
      } catch (err) {
        if (!cancelled) {
          setError(err instanceof Error ? err.message : "Failed to load trends");
          setTrends([]);
        }
      } finally {
        if (!cancelled) setLoading(false);
      }
    }

    fetchTrends();
    return () => { cancelled = true; };
  }, [category, timeRange, sortBy]);

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

      {error && (
        <div className="mb-4 rounded-lg border border-red-200 bg-red-50 p-3 text-sm text-red-600 dark:border-red-800 dark:bg-red-950 dark:text-red-400">
          {error}
        </div>
      )}

      <TrendFeed trends={trends} loading={loading} showRank />
    </div>
  );
}
