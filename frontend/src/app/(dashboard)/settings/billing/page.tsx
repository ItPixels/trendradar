"use client";

import { PageHeader } from "@/components/layout/page-header";
import { Check, Zap } from "lucide-react";

const PLANS = [
  {
    name: "Free", slug: "free", price: "$0", current: true,
    features: ["3 trends/day", "Basic feed", "Category filters"],
  },
  {
    name: "Creator", slug: "creator", price: "$19/mo", current: false,
    features: ["Unlimited trends", "24h predictions", "3 alerts", "5 briefs/day"],
  },
  {
    name: "Pro", slug: "pro", price: "$79/mo", current: false, popular: true,
    features: ["72h predictions", "Unlimited alerts & briefs", "API access", "Export"],
  },
  {
    name: "Business", slug: "business", price: "$299/mo", current: false,
    features: ["5 team seats", "Custom categories", "90-day history", "Priority support"],
  },
];

export default function BillingPage() {
  return (
    <div>
      <PageHeader title="Billing" description="Manage your subscription and payment" />

      {/* Current plan */}
      <div className="rounded-xl border border-border bg-card p-5 mb-8">
        <div className="flex items-center justify-between">
          <div>
            <p className="text-sm text-muted-foreground">Current plan</p>
            <p className="text-xl font-bold mt-1">Free</p>
          </div>
          <div className="flex items-center gap-2 text-sm text-muted-foreground">
            <Zap className="h-4 w-4 text-primary" />
            3 trends remaining today
          </div>
        </div>
      </div>

      {/* Plans grid */}
      <div className="grid md:grid-cols-4 gap-4">
        {PLANS.map((plan) => (
          <div
            key={plan.slug}
            className={`rounded-xl border p-5 ${
              plan.popular ? "border-primary bg-primary/5" : plan.current ? "border-primary/50" : "border-border bg-card"
            }`}
          >
            <h3 className="font-semibold">{plan.name}</h3>
            <p className="text-2xl font-bold mt-2 mb-4">{plan.price}</p>
            <ul className="space-y-2 mb-6">
              {plan.features.map((f) => (
                <li key={f} className="flex items-center gap-2 text-sm">
                  <Check className="h-3.5 w-3.5 text-primary" />
                  {f}
                </li>
              ))}
            </ul>
            <button
              className={`w-full rounded-lg py-2 text-sm font-medium transition-colors ${
                plan.current
                  ? "border border-border text-muted-foreground cursor-default"
                  : plan.popular
                  ? "bg-primary text-primary-foreground hover:bg-primary/90"
                  : "border border-border hover:bg-accent"
              }`}
              disabled={plan.current}
            >
              {plan.current ? "Current Plan" : "Upgrade"}
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}
