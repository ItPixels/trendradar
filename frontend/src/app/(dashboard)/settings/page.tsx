import { PageHeader } from "@/components/layout/page-header";
import Link from "next/link";
import { User, CreditCard, Bell, Key, Users, Puzzle } from "lucide-react";

const settingsSections = [
  { href: "/settings/profile", label: "Profile", description: "Your name, email, and avatar", icon: User },
  { href: "/settings/billing", label: "Billing", description: "Manage your subscription", icon: CreditCard },
  { href: "/settings/notifications", label: "Notifications", description: "Email and push preferences", icon: Bell },
  { href: "/settings/api-keys", label: "API Keys", description: "Manage API access (Pro+)", icon: Key },
  { href: "/settings/team", label: "Team", description: "Team members (Business+)", icon: Users },
  { href: "/settings/integrations", label: "Integrations", description: "Connected services", icon: Puzzle },
];

export default function SettingsPage() {
  return (
    <div>
      <PageHeader title="Settings" description="Manage your account and preferences" />

      <div className="grid gap-3">
        {settingsSections.map((section) => (
          <Link
            key={section.href}
            href={section.href}
            className="flex items-center gap-4 rounded-xl border border-border bg-card p-4 hover:border-primary/30 transition-colors"
          >
            <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-muted">
              <section.icon className="h-5 w-5 text-muted-foreground" />
            </div>
            <div>
              <h3 className="font-medium">{section.label}</h3>
              <p className="text-sm text-muted-foreground">{section.description}</p>
            </div>
          </Link>
        ))}
      </div>
    </div>
  );
}
