"use client";

import { Search, Bell, Moon, Sun, Menu } from "lucide-react";
import { useTheme } from "next-themes";
import { useState } from "react";
import Link from "next/link";

export function Topbar() {
  const { theme, setTheme } = useTheme();
  const [searchOpen, setSearchOpen] = useState(false);

  return (
    <header className="flex h-14 items-center justify-between border-b border-border bg-card px-4 md:px-6">
      {/* Mobile menu button */}
      <button className="md:hidden">
        <Menu className="h-5 w-5" />
      </button>

      {/* Search bar */}
      <div className="flex flex-1 items-center max-w-md mx-4">
        <div className="relative w-full">
          <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
          <input
            type="text"
            placeholder="Search trends..."
            className="w-full rounded-lg border border-input bg-background py-1.5 pl-9 pr-4 text-sm outline-none focus:border-primary focus:ring-1 focus:ring-primary"
          />
          <kbd className="absolute right-3 top-1/2 -translate-y-1/2 hidden sm:inline-flex h-5 items-center gap-1 rounded border border-border bg-muted px-1.5 font-mono text-[10px] text-muted-foreground">
            <span className="text-xs">⌘</span>K
          </kbd>
        </div>
      </div>

      {/* Actions */}
      <div className="flex items-center gap-2">
        {/* Notifications */}
        <button className="relative rounded-lg p-2 text-muted-foreground hover:bg-accent hover:text-foreground transition-colors">
          <Bell className="h-4 w-4" />
          <span className="absolute right-1 top-1 h-2 w-2 rounded-full bg-red-500" />
        </button>

        {/* Theme toggle */}
        <button
          onClick={() => setTheme(theme === "dark" ? "light" : "dark")}
          className="rounded-lg p-2 text-muted-foreground hover:bg-accent hover:text-foreground transition-colors"
        >
          <Sun className="h-4 w-4 rotate-0 scale-100 transition-transform dark:-rotate-90 dark:scale-0" />
          <Moon className="absolute h-4 w-4 rotate-90 scale-0 transition-transform dark:rotate-0 dark:scale-100" />
        </button>

        {/* User avatar */}
        <Link href="/settings/profile" className="flex items-center gap-2 ml-2">
          <div className="h-8 w-8 rounded-full bg-gradient-to-br from-primary to-purple-600 flex items-center justify-center text-white text-xs font-semibold">
            TR
          </div>
        </Link>
      </div>
    </header>
  );
}
