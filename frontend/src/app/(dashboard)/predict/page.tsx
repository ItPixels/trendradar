"use client";

import { PageHeader } from "@/components/layout/page-header";
import { Brain, TrendingUp, Clock, Target } from "lucide-react";

const DEMO_PREDICTIONS = [
  {
    id: "p1",
    topic: "Claude 4 Release",
    predictedGrowth: 380,
    confidence: 87,
    timeframeHours: 72,
    status: "pending",
    factors: [
      { factor: "Cross-Source Correlation", impact: "positive", weight: 0.9, description: "Detected across 5 sources" },
      { factor: "Signal Velocity", impact: "positive", weight: 0.8, description: "240% growth rate" },
    ],
  },
  {
    id: "p2",
    topic: "Bitcoin ETF Inflows Record",
    predictedGrowth: 220,
    confidence: 75,
    timeframeHours: 48,
    status: "pending",
    factors: [
      { factor: "Crypto Surge Pattern", impact: "positive", weight: 0.85, description: "CoinGecko + Reddit + Google Trends pattern" },
    ],
  },
  {
    id: "p3",
    topic: "Rust 2.0 Announcement",
    predictedGrowth: 150,
    confidence: 68,
    timeframeHours: 24,
    status: "pending",
    factors: [
      { factor: "Tech Breakout Pattern", impact: "positive", weight: 0.75, description: "HN + GitHub + Reddit pattern" },
    ],
  },
];

export default function PredictPage() {
  return (
    <div>
      <PageHeader
        title="AI Predictions"
        description="AI-powered trend predictions for the next 24-72 hours"
      />

      {/* Stats */}
      <div className="grid grid-cols-1 sm:grid-cols-4 gap-4 mb-6">
        {[
          { label: "Active Predictions", value: "12", icon: Brain, color: "text-purple-600" },
          { label: "Avg. Confidence", value: "73%", icon: Target, color: "text-green-600" },
          { label: "Accuracy (30d)", value: "68%", icon: TrendingUp, color: "text-blue-600" },
          { label: "Next Update", value: "23 min", icon: Clock, color: "text-orange-600" },
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

      {/* Predictions list */}
      <div className="space-y-3">
        {DEMO_PREDICTIONS.map((pred) => (
          <div key={pred.id} className="rounded-xl border border-border bg-card p-5 hover:border-primary/30 transition-colors">
            <div className="flex items-start justify-between">
              <div>
                <h3 className="font-semibold text-lg">{pred.topic}</h3>
                <div className="mt-2 flex items-center gap-4 text-sm">
                  <span className="text-green-600 dark:text-green-400 font-semibold">
                    +{pred.predictedGrowth}% predicted
                  </span>
                  <span className="text-muted-foreground">
                    in {pred.timeframeHours}h
                  </span>
                </div>
              </div>
              <div className="text-right">
                <div className="text-2xl font-bold">{pred.confidence}%</div>
                <div className="text-xs text-muted-foreground">confidence</div>
              </div>
            </div>

            {/* Factors */}
            <div className="mt-4 space-y-2">
              {pred.factors.map((factor, i) => (
                <div key={i} className="flex items-center gap-2 text-sm">
                  <div className={`h-1.5 w-1.5 rounded-full ${factor.impact === "positive" ? "bg-green-500" : "bg-red-500"}`} />
                  <span className="font-medium">{factor.factor}:</span>
                  <span className="text-muted-foreground">{factor.description}</span>
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
