"use client";

import { useState, useEffect } from "react";
import { PageHeader } from "@/components/layout/page-header";
import { Bell, Plus, Trash2, ToggleLeft, ToggleRight, Loader2 } from "lucide-react";
import { getAlerts, createAlert, deleteAlert, toggleAlert } from "@/lib/api/alerts";
import type { Alert } from "@/lib/types/alert";

export default function AlertsPage() {
  const [alerts, setAlerts] = useState<Alert[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showCreate, setShowCreate] = useState(false);
  const [newName, setNewName] = useState("");
  const [newCategories, setNewCategories] = useState("");
  const [newKeywords, setNewKeywords] = useState("");
  const [creating, setCreating] = useState(false);

  async function fetchAlerts() {
    setLoading(true);
    try {
      const data = await getAlerts();
      setAlerts(data.items || []);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load alerts");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => { fetchAlerts(); }, []);

  async function handleCreate() {
    if (!newName.trim()) return;
    setCreating(true);
    try {
      await createAlert({
        name: newName,
        categories: newCategories ? newCategories.split(",").map(s => s.trim()) : [],
        keywords: newKeywords ? newKeywords.split(",").map(s => s.trim()) : [],
        minScore: 50,
        minSources: 2,
        channels: ["email"],
      });
      setNewName("");
      setNewCategories("");
      setNewKeywords("");
      setShowCreate(false);
      await fetchAlerts();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to create alert");
    } finally {
      setCreating(false);
    }
  }

  async function handleToggle(id: string) {
    try {
      const updated = await toggleAlert(id);
      setAlerts(prev => prev.map(a => a.id === id ? updated : a));
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to toggle alert");
    }
  }

  async function handleDelete(id: string) {
    try {
      await deleteAlert(id);
      setAlerts(prev => prev.filter(a => a.id !== id));
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to delete alert");
    }
  }

  return (
    <div>
      <PageHeader
        title="Alerts"
        description="Get notified when trends match your criteria"
      >
        <button
          onClick={() => setShowCreate(!showCreate)}
          className="flex items-center gap-2 rounded-lg bg-primary px-4 py-2 text-sm font-medium text-primary-foreground hover:bg-primary/90 transition-colors"
        >
          <Plus className="h-4 w-4" />
          New Alert
        </button>
      </PageHeader>

      {error && (
        <div className="mb-4 rounded-lg border border-red-200 bg-red-50 p-3 text-sm text-red-600 dark:border-red-800 dark:bg-red-950 dark:text-red-400">
          {error}
          <button onClick={() => setError(null)} className="ml-2 underline">dismiss</button>
        </div>
      )}

      {/* Create form */}
      {showCreate && (
        <div className="mb-4 rounded-xl border border-border bg-card p-4 space-y-3">
          <input
            type="text"
            placeholder="Alert name (e.g. AI Breakouts)"
            value={newName}
            onChange={(e) => setNewName(e.target.value)}
            className="w-full rounded-lg border border-border bg-background px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary"
          />
          <input
            type="text"
            placeholder="Categories (comma-separated: ai, crypto, tech)"
            value={newCategories}
            onChange={(e) => setNewCategories(e.target.value)}
            className="w-full rounded-lg border border-border bg-background px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary"
          />
          <input
            type="text"
            placeholder="Keywords (comma-separated: gpt, claude, llm)"
            value={newKeywords}
            onChange={(e) => setNewKeywords(e.target.value)}
            className="w-full rounded-lg border border-border bg-background px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary"
          />
          <div className="flex gap-2">
            <button
              onClick={handleCreate}
              disabled={creating || !newName.trim()}
              className="flex items-center gap-2 rounded-lg bg-primary px-4 py-2 text-sm font-medium text-primary-foreground hover:bg-primary/90 disabled:opacity-50 transition-colors"
            >
              {creating && <Loader2 className="h-4 w-4 animate-spin" />}
              Create Alert
            </button>
            <button
              onClick={() => setShowCreate(false)}
              className="rounded-lg border border-border px-4 py-2 text-sm hover:bg-muted transition-colors"
            >
              Cancel
            </button>
          </div>
        </div>
      )}

      {/* Loading */}
      {loading && (
        <div className="space-y-3">
          {[1, 2].map((i) => (
            <div key={i} className="rounded-xl border border-border bg-card p-4 animate-pulse">
              <div className="h-5 bg-muted rounded w-1/3 mb-2" />
              <div className="h-4 bg-muted rounded w-1/2" />
            </div>
          ))}
        </div>
      )}

      {/* Empty state */}
      {!loading && alerts.length === 0 && (
        <div className="rounded-xl border border-border bg-card p-8 text-center">
          <Bell className="h-12 w-12 mx-auto text-muted-foreground mb-3" />
          <h3 className="font-semibold text-lg mb-1">No alerts yet</h3>
          <p className="text-muted-foreground text-sm">
            Create your first alert to get notified when trends match your criteria.
          </p>
        </div>
      )}

      {/* Alerts list */}
      {!loading && (
        <div className="space-y-3">
          {alerts.map((alert) => (
            <div key={alert.id} className="rounded-xl border border-border bg-card p-4">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <button
                    onClick={() => handleToggle(alert.id)}
                    className="text-muted-foreground hover:text-foreground"
                  >
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
                    <div className="flex items-center gap-2 mt-1 flex-wrap">
                      {alert.categories?.map((cat) => (
                        <span key={cat} className="rounded-full bg-primary/10 px-2 py-0.5 text-[10px] font-medium text-primary">
                          {cat}
                        </span>
                      ))}
                      {alert.keywords?.map((kw) => (
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
                  <span>{alert.triggerCount || 0} triggers</span>
                  <button
                    onClick={() => handleDelete(alert.id)}
                    className="p-1 hover:text-red-500"
                  >
                    <Trash2 className="h-4 w-4" />
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
