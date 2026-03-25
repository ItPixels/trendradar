"use client";

import { useState, useEffect, useCallback } from "react";
import { PageHeader } from "@/components/layout/page-header";
import { Search as SearchIcon } from "lucide-react";
import { TrendFeed } from "@/components/trends/trend-feed";
import { EmptyState } from "@/components/common/empty-state";
import { searchTrends } from "@/lib/api/trends";
import type { Trend } from "@/lib/types/trend";

export default function SearchPage() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<Trend[]>([]);
  const [loading, setLoading] = useState(false);
  const [searched, setSearched] = useState(false);

  const doSearch = useCallback(async (q: string) => {
    if (q.length < 2) {
      setResults([]);
      setSearched(false);
      return;
    }
    setLoading(true);
    setSearched(true);
    try {
      const data = await searchTrends(q);
      setResults(data.items || []);
    } catch {
      setResults([]);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    const timer = setTimeout(() => doSearch(query), 300);
    return () => clearTimeout(timer);
  }, [query, doSearch]);

  return (
    <div>
      <PageHeader title="Search" description="Find trends across all categories and sources" />

      <div className="relative max-w-2xl mb-8">
        <SearchIcon className="absolute left-4 top-1/2 h-5 w-5 -translate-y-1/2 text-muted-foreground" />
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Search for any topic, technology, or trend..."
          className="w-full rounded-xl border border-input bg-background py-3 pl-12 pr-4 text-base outline-none focus:border-primary focus:ring-2 focus:ring-primary/20"
          autoFocus
        />
      </div>

      {!query && !searched && (
        <EmptyState
          icon={SearchIcon}
          title="Search for trends"
          description="Enter a topic, technology, or keyword to find related trends and predictions."
        />
      )}

      {searched && !loading && results.length === 0 && (
        <EmptyState
          icon={SearchIcon}
          title="No results found"
          description={`No trends matching "${query}". Try a different keyword.`}
        />
      )}

      {(loading || results.length > 0) && (
        <TrendFeed trends={results} loading={loading} />
      )}
    </div>
  );
}
