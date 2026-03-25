"use client";

import { CATEGORY_COLORS } from "@/lib/utils/constants";

interface TrendFiltersProps {
  selectedCategory?: string;
  selectedTimeRange: string;
  selectedSort: string;
  onCategoryChange: (category?: string) => void;
  onTimeRangeChange: (range: string) => void;
  onSortChange: (sort: string) => void;
}

const categories = [
  { slug: undefined, label: "All" },
  { slug: "tech", label: "Tech" },
  { slug: "ai", label: "AI" },
  { slug: "crypto", label: "Crypto" },
  { slug: "business", label: "Business" },
  { slug: "science", label: "Science" },
  { slug: "gaming", label: "Gaming" },
  { slug: "devtools", label: "DevTools" },
  { slug: "culture", label: "Culture" },
  { slug: "finance", label: "Finance" },
];

const timeRanges = [
  { value: "1h", label: "1h" },
  { value: "6h", label: "6h" },
  { value: "24h", label: "24h" },
  { value: "7d", label: "7d" },
  { value: "30d", label: "30d" },
];

const sortOptions = [
  { value: "score", label: "Score" },
  { value: "velocity", label: "Velocity" },
  { value: "newest", label: "Newest" },
  { value: "sources", label: "Sources" },
];

export function TrendFilters({
  selectedCategory,
  selectedTimeRange,
  selectedSort,
  onCategoryChange,
  onTimeRangeChange,
  onSortChange,
}: TrendFiltersProps) {
  return (
    <div className="space-y-3 mb-6">
      {/* Categories */}
      <div className="flex items-center gap-1.5 overflow-x-auto pb-1">
        {categories.map((cat) => (
          <button
            key={cat.slug ?? "all"}
            onClick={() => onCategoryChange(cat.slug)}
            className={`shrink-0 rounded-full px-3 py-1 text-xs font-medium transition-colors ${
              selectedCategory === cat.slug
                ? "bg-primary text-primary-foreground"
                : "bg-muted text-muted-foreground hover:bg-accent"
            }`}
          >
            {cat.label}
          </button>
        ))}
      </div>

      {/* Time range + Sort */}
      <div className="flex items-center gap-4">
        <div className="flex items-center gap-1 rounded-lg bg-muted p-0.5">
          {timeRanges.map((range) => (
            <button
              key={range.value}
              onClick={() => onTimeRangeChange(range.value)}
              className={`rounded-md px-2.5 py-1 text-xs font-medium transition-colors ${
                selectedTimeRange === range.value
                  ? "bg-background text-foreground shadow-sm"
                  : "text-muted-foreground hover:text-foreground"
              }`}
            >
              {range.label}
            </button>
          ))}
        </div>

        <div className="flex items-center gap-1 rounded-lg bg-muted p-0.5">
          {sortOptions.map((sort) => (
            <button
              key={sort.value}
              onClick={() => onSortChange(sort.value)}
              className={`rounded-md px-2.5 py-1 text-xs font-medium transition-colors ${
                selectedSort === sort.value
                  ? "bg-background text-foreground shadow-sm"
                  : "text-muted-foreground hover:text-foreground"
              }`}
            >
              {sort.label}
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}
