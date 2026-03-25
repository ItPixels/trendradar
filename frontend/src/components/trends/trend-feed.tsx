"use client";

import { TrendCard } from "./trend-card";
import type { Trend } from "@/lib/types/trend";
import { LoadingSpinner } from "@/components/common/loading-spinner";
import { EmptyState } from "@/components/common/empty-state";
import { Compass } from "lucide-react";

interface TrendFeedProps {
  trends: Trend[];
  loading?: boolean;
  showRank?: boolean;
}

export function TrendFeed({ trends, loading, showRank = true }: TrendFeedProps) {
  if (loading) return <LoadingSpinner />;

  if (trends.length === 0) {
    return (
      <EmptyState
        icon={Compass}
        title="No trends found"
        description="Try adjusting your filters or check back later for new trends."
      />
    );
  }

  return (
    <div className="space-y-3">
      {trends.map((trend, index) => (
        <TrendCard
          key={trend.id}
          trend={trend}
          rank={showRank ? index : undefined}
        />
      ))}
    </div>
  );
}
