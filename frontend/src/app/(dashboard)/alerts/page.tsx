"use client";

import { PageHeader } from "@/components/layout/page-header";
import { Bell, Plus, Settings, Trash2, ToggleLeft, ToggleRight } from "lucide-react";
import { EmptyState } from "@/components/common/empty-state";

const DEMO_ALERTS = [
  {
    id: "a1",
    name: "AI Breakouts",
    categories: ["ai"],
    keywords: ["gpt", "claude", "llm"],
    minScore: 60,
    minSources: 3,
    channels: ["email", "push"],
    isActive: true,
    triggerCount: 14,
    lastTriggeredAt: "2 hours ago",
  },
  {
    id: "a2",
    name: "Crypto Surges",
    categories: ["crypto"],
    keywords: ["bitcoin", "ethereum"],
    minScore: 70,
    minSources: 2,
    channels: ["email"],
    isActive: true,
    triggerCount: 8,
    lastTriggeredAt: "5 hours ago",
  },
  {
    id: "a3",
    name: "Dev Tool Launches",
    categories: ["devtools", "opensource"],
    keywords: [],
    minScore: 50,
    minSources: 2,
    channels: ["email"],
    isActive: false,
    triggerCount: 3,
    lastTriggeredAt: "2 days ago",
  },
];

export default function AlertsPage() {
  return (
    <div>
      <PageHeader
        title="Alerts"
        description="Get notified when trends match your criteria"
      >
        <button className="flex items-center gap-2 rounded-lg bg-primary px-4 py-2 text-sm font-medium text-primary-foreground hover:bg-primary/90 transition-colors">
          <Plus className="h-4 w-4" />
          New Alert
        </button>
      </PageHeader>

      <div className="space-y-3">
        {DEMO_ALERTS.map((alert) => (
          <div key={alert.id} className="rounded-xl border border-border bg-card p-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                <button className="text-muted-foreground hover:text-foreground">
                  {alert.isActive ? (
                    <ToggleRight className="h-6 w-6 text-primary" />
                  ) : (
                    <ToggleLeft className="h-6 w-6" />
                  )}
                </button>
                <div>
                  <h3 className={`font-semibold ${!alert.isActive ? "text-muted-foreground" : ""}`}>
                    {alert.name}
                  </h3>
                  <div className="flex items-center gap-2 mt-1">
                    {alert.categories.map((cat) => (
                      <span key={cat} className="rounded-full bg-primary/10 px-2 py-0.5 text-[10px] font-medium text-primary">
                        {cat}
                      </span>
                    ))}
                    {alert.keywords.map((kw) => (
                      <span key={kw} className="rounded-full bg-muted px-2 py-0.5 text-[10px] font-medium text-muted-foreground">
                        {kw}
                      </span>
                    ))}
                    <span className="text-xs text-muted-foreground">
                      min score: {alert.minScore} | min sources: {alert.minSources}
                    </span>
                  </div>
                </div>
              </div>
              <div className="flex items-center gap-3 text-sm text-muted-foreground">
                <span>{alert.triggerCount} triggers</span>
                <span>{alert.lastTriggeredAt}</span>
                <button className="p-1 hover:text-foreground"><Settings className="h-4 w-4" /></button>
                <button className="p-1 hover:text-red-500"><Trash2 className="h-4 w-4" /></button>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
