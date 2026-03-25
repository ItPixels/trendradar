import { PageHeader } from "@/components/layout/page-header";
import { CATEGORY_COLORS } from "@/lib/utils/constants";
import Link from "next/link";
import {
  Cpu, Brain, Bitcoin, Briefcase, Atom, Heart, Music,
  Landmark, Gamepad2, TrendingUp, Trophy, Palette, Code, GitBranch,
} from "lucide-react";

const CATEGORIES = [
  { slug: "tech", name: "Technology", icon: Cpu, count: 47 },
  { slug: "ai", name: "Artificial Intelligence", icon: Brain, count: 63 },
  { slug: "crypto", name: "Crypto & Web3", icon: Bitcoin, count: 28 },
  { slug: "business", name: "Business", icon: Briefcase, count: 19 },
  { slug: "science", name: "Science", icon: Atom, count: 15 },
  { slug: "health", name: "Health & Wellness", icon: Heart, count: 12 },
  { slug: "culture", name: "Culture & Entertainment", icon: Music, count: 34 },
  { slug: "politics", name: "Politics", icon: Landmark, count: 8 },
  { slug: "gaming", name: "Gaming", icon: Gamepad2, count: 22 },
  { slug: "finance", name: "Finance & Markets", icon: TrendingUp, count: 17 },
  { slug: "sports", name: "Sports", icon: Trophy, count: 11 },
  { slug: "design", name: "Design & UX", icon: Palette, count: 9 },
  { slug: "devtools", name: "Developer Tools", icon: Code, count: 31 },
  { slug: "opensource", name: "Open Source", icon: GitBranch, count: 25 },
];

export default function CategoriesPage() {
  return (
    <div>
      <PageHeader
        title="Categories"
        description="Browse trends by topic category"
      />

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        {CATEGORIES.map((cat) => {
          const color = CATEGORY_COLORS[cat.slug] || "#6366f1";
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
                <cat.icon className="h-5 w-5" style={{ color }} />
              </div>
              <h3 className="font-semibold group-hover:text-primary transition-colors">
                {cat.name}
              </h3>
              <p className="text-sm text-muted-foreground mt-1">
                {cat.count} active trends
              </p>
            </Link>
          );
        })}
      </div>
    </div>
  );
}
