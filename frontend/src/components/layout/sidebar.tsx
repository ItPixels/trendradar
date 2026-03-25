"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  Compass,
  Brain,
  Bell,
  Grid3X3,
  Search,
  History,
  Settings,
  Zap,
  BarChart3,
  ChevronLeft,
} from "lucide-react";
import { useState } from "react";

const navItems = [
  { href: "/explore", label: "Explore", icon: Compass, description: "Real-time trends" },
  { href: "/predict", label: "Predict", icon: Brain, description: "AI predictions" },
  { href: "/alerts", label: "Alerts", icon: Bell, description: "Custom alerts" },
  { href: "/categories", label: "Categories", icon: Grid3X3, description: "Browse by topic" },
  { href: "/search", label: "Search", icon: Search, description: "Find trends" },
  { href: "/history", label: "History", icon: History, description: "Past trends" },
];

const bottomItems = [
  { href: "/settings", label: "Settings", icon: Settings },
];

export function Sidebar() {
  const pathname = usePathname();
  const [collapsed, setCollapsed] = useState(false);

  return (
    <aside
      className={`hidden md:flex flex-col border-r border-border bg-card transition-all duration-200 ${
        collapsed ? "w-16" : "w-64"
      }`}
    >
      {/* Logo */}
      <div className="flex h-14 items-center gap-2 border-b border-border px-4">
        <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-primary">
          <Zap className="h-4 w-4 text-primary-foreground" />
        </div>
        {!collapsed && (
          <span className="font-semibold text-lg">
            Trend<span className="text-primary">Radar</span>
          </span>
        )}
      </div>

      {/* Navigation */}
      <nav className="flex-1 space-y-1 px-2 py-4">
        {navItems.map((item) => {
          const isActive = pathname.startsWith(item.href);
          return (
            <Link
              key={item.href}
              href={item.href}
              className={`flex items-center gap-3 rounded-lg px-3 py-2 text-sm font-medium transition-colors ${
                isActive
                  ? "bg-primary/10 text-primary"
                  : "text-muted-foreground hover:bg-accent hover:text-foreground"
              }`}
            >
              <item.icon className="h-4 w-4 shrink-0" />
              {!collapsed && <span>{item.label}</span>}
            </Link>
          );
        })}
      </nav>

      {/* Bottom */}
      <div className="border-t border-border px-2 py-4 space-y-1">
        {bottomItems.map((item) => (
          <Link
            key={item.href}
            href={item.href}
            className="flex items-center gap-3 rounded-lg px-3 py-2 text-sm font-medium text-muted-foreground hover:bg-accent hover:text-foreground transition-colors"
          >
            <item.icon className="h-4 w-4 shrink-0" />
            {!collapsed && <span>{item.label}</span>}
          </Link>
        ))}

        <button
          onClick={() => setCollapsed(!collapsed)}
          className="flex w-full items-center gap-3 rounded-lg px-3 py-2 text-sm text-muted-foreground hover:bg-accent transition-colors"
        >
          <ChevronLeft className={`h-4 w-4 transition-transform ${collapsed ? "rotate-180" : ""}`} />
          {!collapsed && <span>Collapse</span>}
        </button>
      </div>
    </aside>
  );
}
