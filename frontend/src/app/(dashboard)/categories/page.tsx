"use client";

import { useState, useEffect } from "react";
import { PageHeader } from "@/components/layout/page-header";
import { CATEGORY_COLORS } from "@/lib/utils/constants";
import { getCategories, type Category } from "@/lib/api/categories";
import Link from "next/link";
import {
  Cpu, Brain, Bitcoin, Briefcase, Atom, Heart, Music,
  Landmark, Gamepad2, TrendingUp, Trophy, Palette, Code, GitBranch,
  type LucideIcon,
} from "lucide-react";

const ICON_MAP: Record<string, LucideIcon> = {
  Cpu, Brain, Bitcoin, Briefcase, Atom, Heart, Music,
  Landmark, Gamepad2, TrendingUp, Trophy, Palette, Code, GitBranch,
};

const SLUG_ICON_MAP: Record<string, LucideIcon> = {
  tech: Cpu, ai: Brain, crypto: Bitcoin, business: Briefcase,
  science: Atom, health: Heart, culture: Music, politics: Landmark,
  gaming: Gamepad2, finance: TrendingUp, sports: Trophy,
  design: Palette, devtools: Code, opensource: GitBranch,
};

export default function CategoriesPage() {
  const [categories, setCategories] = useState<Category[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetch() {
      try {
        const data = await getCategories();
        setCategories(data.items || []);
      } catch {
        // fallback handled by empty state
      } finally {
        setLoading(false);
      }
    }
    fetch();
  }, []);

  return (
    <div>
      <PageHeader
        title="Categories"
        description="Browse trends by topic category"
      />

      {loading ? (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
          {Array.from({ length: 8 }).map((_, i) => (
            <div key={i} className="rounded-xl border border-border bg-card p-5 animate-pulse">
              <div className="h-10 w-10 bg-muted rounded-lg mb-3" />
              <div className="h-5 bg-muted rounded w-2/3 mb-2" />
              <div className="h-4 bg-muted rounded w-1/3" />
            </div>
          ))}
        </div>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
          {categories.map((cat) => {
            const color = cat.color || CATEGORY_COLORS[cat.slug] || "#6366f1";
            const IconComp = (cat.icon ? ICON_MAP[cat.icon] : null) || SLUG_ICON_MAP[cat.slug] || Cpu;
            return (
              <Link
                key={cat.slug}
                href={`/explore?category=${cat.slug}`}
                className="group rounded-xl border border-border bg-card p-5 transition-all hover:border-primary/30 hover:shadow-md"
              >
                <div
                  className="flex h-10 w-10 items-center justify-center rounded-lg mb-3"
                  style={{ backgroundColor: `${color}15` }}
                >
                  <IconComp className="h-5 w-5" style={{ color }} />
                </div>
                <h3 className="font-semibold group-hover:text-primary transition-colors">
                  {cat.name}
                </h3>
                <p className="text-sm text-muted-foreground mt-1">
                  {cat.trendCount} active trends
                </p>
              </Link>
            );
          })}
        </div>
      )}
    </div>
  );
}
