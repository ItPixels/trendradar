"use client";

import { useState, useEffect } from "react";
import { PageHeader } from "@/components/layout/page-header";
import { Brain, TrendingUp, Clock, Target, ArrowUpRight } from "lucide-react";
import { getPredictions } from "@/lib/api/predictions";
import type { Prediction } from "@/lib/types/prediction";
import Link from "next/link";

export default function PredictPage() {
  const [predictions, setPredictions] = useState<Prediction[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;

    async function fetchPredictions() {
      setLoading(true);
      setError(null);
      try {
        const data = await getPredictions({ limit: 30 });
        if (!cancelled) {
          setPredictions(data.items || []);
        }
      } catch (err) {
        if (!cancelled) {
          setError(err instanceof Error ? err.message : "Failed to load predictions");
        }
      } finally {
        if (!cancelled) setLoading(false);
      }
    }

    fetchPredictions();
    return () => { cancelled = true; };
  }, []);

  const avgConfidence = predictions.length > 0
    ? Math.round(predictions.reduce((sum, p) => sum + p.confidenceScore, 0) / predictions.length)
    : 0;

  const highConfidence = predictions.filter(p => p.confidenceScore >= 60).length;

  return (
    <div>
      <PageHeader
        title="AI Predictions"
        description="AI-powered trend predictions for the next 24-72 hours"
      />

      {/* Stats */}
      <div className="grid grid-cols-1 sm:grid-cols-4 gap-4 mb-6">
        {[
          { label: "Active Predictions", value: loading ? "..." : String(predictions.length), icon: Brain, color: "text-purple-600" },
          { label: "Avg. Confidence", value: loading ? "..." : `${avgConfidence}%`, icon: Target, color: "text-green-600" },
          { label: "High Confidence", value: loading ? "..." : String(highConfidence), icon: TrendingUp, color: "text-blue-600" },
          { label: "Update Interval", value: "30 min", icon: Clock, color: "text-orange-600" },
        ].map((stat) => (
          <div key={stat.label} className="rounded-xl border border-border bg-card p-4">
            <div className="flex items-center gap-2 mb-2">
              <stat.icon className={`h-4 w-4 ${stat.color}`} />
              <span className="text-xs text-muted-foreground">{stat.label}</span>
            </div>
            <div className="text-2xl font-bold">{stat.value}</div>
          </div>
        ))}
      </div>

      {error && (
        <div className="mb-4 rounded-lg border border-red-200 bg-red-50 p-3 text-sm text-red-600 dark:border-red-800 dark:bg-red-950 dark:text-red-400">
          {error}
        </div>
      )}

      {/* Loading state */}
      {loading && (
        <div className="space-y-3">
          {[1, 2, 3].map((i) => (
            <div key={i} className="rounded-xl border border-border bg-card p-5 animate-pulse">
              <div className="h-6 bg-muted rounded w-1/3 mb-3" />
              <div className="h-4 bg-muted rounded w-1/2 mb-4" />
              <div className="h-3 bg-muted rounded w-2/3" />
            </div>
          ))}
        </div>
      )}

      {/* Empty state */}
      {!loading && predictions.length === 0 && !error && (
        <div className="rounded-xl border border-border bg-card p-8 text-center">
          <Brain className="h-12 w-12 mx-auto text-muted-foreground mb-3" />
          <h3 className="font-semibold text-lg mb-1">No predictions yet</h3>
          <p className="text-muted-foreground text-sm">
            Predictions are generated automatically every 30 minutes when trends are collected.
          </p>
        </div>
      )}

      {/* Predictions list */}
      {!loading && (
        <div className="space-y-3">
          {predictions.map((pred) => (
            <Link
              key={pred.id}
              href={pred.trend ? `/trend/${pred.trend.id}` : "#"}
              className="block rounded-xl border border-border bg-card p-5 hover:border-primary/30 transition-colors"
            >
              <div className="flex items-start justify-between">
                <div>
                  <div className="flex items-center gap-2">
                    <h3 className="font-semibold text-lg">
                      {pred.trend?.topic || `Trend ${pred.trendId.slice(0, 8)}`}
                    </h3>
                    <ArrowUpRight className="h-4 w-4 text-muted-foreground" />
                  </div>
                  <div className="mt-2 flex items-center gap-4 text-sm">
                    <span className={`font-semibold ${pred.predictedGrowth > 0 ? "text-green-600 dark:text-green-400" : "text-red-500"}`}>
                      {pred.predictedGrowth > 0 ? "+" : ""}{pred.predictedGrowth}% predicted
                    </span>
                    <span className="text-muted-foreground">
                      in {pred.timeframeHours}h
                    </span>
                    {pred.trend && (
                      <span className="text-muted-foreground">
                        {pred.trend.sourceCount} sources
                      </span>
                    )}
                  </div>
                </div>
                <div className="text-right">
                  <div className={`text-2xl font-bold ${
                    pred.confidenceScore >= 60 ? "text-green-600" :
                    pred.confidenceScore >= 40 ? "text-yellow-600" : "text-muted-foreground"
                  }`}>
                    {Math.round(pred.confidenceScore)}%
                  </div>
                  <div className="text-xs text-muted-foreground">confidence</div>
                </div>
              </div>

              {/* Factors */}
              {pred.factors && pred.factors.length > 0 && (
                <div className="mt-4 space-y-2">
                  {pred.factors.slice(0, 3).map((factor, i) => (
                    <div key={i} className="flex items-center gap-2 text-sm">
                      <div className={`h-1.5 w-1.5 rounded-full ${
                        factor.impact === "positive" ? "bg-green-500" : "bg-red-500"
                      }`} />
                      <span className="font-medium">{factor.factor}:</span>
                      <span className="text-muted-foreground">{factor.description}</span>
                    </div>
                  ))}
                </div>
              )}
            </Link>
          ))}
        </div>
      )}
    </div>
  );
}
