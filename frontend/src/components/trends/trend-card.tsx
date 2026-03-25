"use client";

import { ArrowUp, ArrowDown, ExternalLink, Eye, Share2 } from "lucide-react";
import Link from "next/link";
import type { Trend } from "@/lib/types/trend";
import { SOURCE_DISPLAY_NAMES, SOURCE_COLORS } from "@/lib/utils/constants";

interface TrendCardProps {
  trend: Trend;
  rank?: number;
}

export function TrendCard({ trend, rank }: TrendCardProps) {
  const isPositive = trend.velocity24h >= 0;
  const velocityPercent = Math.abs(trend.velocity24h * 100).toFixed(0);

  return (
    <Link
      href={`/trend/${trend.id}`}
      className="group block rounded-xl border border-border bg-card p-4 transition-all hover:border-primary/30 hover:shadow-md"
    >
      <div className="flex items-start gap-3">
        {/* Rank */}
        {rank !== undefined && (
          <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-lg bg-muted text-sm font-bold text-muted-foreground">
            {rank + 1}
          </div>
        )}

        {/* Content */}
        <div className="flex-1 min-w-0">
          {/* Header */}
          <div className="flex items-start justify-between gap-2">
            <div>
              <h3 className="font-semibold text-foreground group-hover:text-primary transition-colors truncate">
                {trend.topic}
              </h3>
              {trend.description && (
                <p className="text-sm text-muted-foreground line-clamp-2 mt-0.5">
                  {trend.description}
                </p>
              )}
            </div>

            {/* Score */}
            <div className="shrink-0">
              <div
                className={`flex items-center gap-1 rounded-full px-2.5 py-1 text-sm font-semibold ${
                  trend.trendScore >= 70
                    ? "bg-green-500/10 text-green-600 dark:text-green-400"
                    : trend.trendScore >= 40
                    ? "bg-yellow-500/10 text-yellow-600 dark:text-yellow-400"
                    : "bg-muted text-muted-foreground"
                }`}
              >
                {trend.trendScore.toFixed(0)}
              </div>
            </div>
          </div>

          {/* Metrics row */}
          <div className="mt-3 flex items-center gap-4 text-xs text-muted-foreground">
            {/* Velocity */}
            <span className={`flex items-center gap-0.5 font-medium ${isPositive ? "text-green-600 dark:text-green-400" : "text-red-500"}`}>
              {isPositive ? <ArrowUp className="h-3 w-3" /> : <ArrowDown className="h-3 w-3" />}
              {velocityPercent}%
            </span>

            {/* Source count */}
            <span className="flex items-center gap-1">
              <span className="h-1.5 w-1.5 rounded-full bg-primary" />
              {trend.sourceCount} sources
            </span>

            {/* Signal count */}
            <span>{trend.signalCount24h} signals/24h</span>

            {/* Views */}
            <span className="flex items-center gap-0.5">
              <Eye className="h-3 w-3" />
              {trend.viewCount}
            </span>

            {/* Status badge */}
            <span
              className={`rounded-full px-2 py-0.5 text-[10px] font-medium uppercase ${
                trend.status === "emerging"
                  ? "bg-blue-500/10 text-blue-600"
                  : trend.status === "active"
                  ? "bg-green-500/10 text-green-600"
                  : trend.status === "peaking"
                  ? "bg-orange-500/10 text-orange-600"
                  : "bg-muted text-muted-foreground"
              }`}
            >
              {trend.status}
            </span>
          </div>

          {/* Sources */}
          <div className="mt-2 flex items-center gap-1.5 flex-wrap">
            {trend.activeSources.slice(0, 5).map((source) => (
              <span
                key={source}
                className="rounded-md bg-muted px-1.5 py-0.5 text-[10px] font-medium text-muted-foreground"
              >
                {SOURCE_DISPLAY_NAMES[source] || source}
              </span>
            ))}
            {trend.activeSources.length > 5 && (
              <span className="text-[10px] text-muted-foreground">
                +{trend.activeSources.length - 5} more
              </span>
            )}
          </div>
        </div>
      </div>
    </Link>
  );
}
