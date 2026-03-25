import Link from "next/link";
import {
  Zap, ArrowRight, BarChart3, Brain, Bell, Globe,
  TrendingUp, Shield, Sparkles, Check,
} from "lucide-react";

const SOURCES = [
  "Google Trends", "Reddit", "Hacker News", "YouTube", "GitHub",
  "Wikipedia", "Product Hunt", "ArXiv", "CoinGecko", "npm",
  "PyPI", "Steam", "Dev.to", "Stack Overflow", "Google News",
];

const FEATURES = [
  {
    icon: Globe,
    title: "15+ Signal Sources",
    description: "Cross-platform intelligence from Reddit, HN, GitHub, YouTube, Google Trends, and more — all free.",
  },
  {
    icon: Brain,
    title: "AI Predictions",
    description: "Predict what will trend 24-72 hours before it goes mainstream. Cross-source correlation + ML.",
  },
  {
    icon: Bell,
    title: "Smart Alerts",
    description: "Get notified when topics in your niche start gaining traction across multiple platforms.",
  },
  {
    icon: Sparkles,
    title: "Content Briefs",
    description: "AI-generated content strategies — hooks, key points, SEO keywords, optimal timing.",
  },
];

const PLANS = [
  {
    name: "Free",
    price: "$0",
    description: "Get started",
    features: ["3 trends/day", "Basic feed", "Category filters"],
    cta: "Start Free",
    highlighted: false,
  },
  {
    name: "Creator",
    price: "$19",
    period: "/mo",
    description: "For content creators",
    features: ["Unlimited trends", "24h predictions", "3 alerts", "5 briefs/day", "7-day history"],
    cta: "Start Creating",
    highlighted: false,
  },
  {
    name: "Pro",
    price: "$79",
    period: "/mo",
    description: "For professionals",
    features: ["72h predictions", "Unlimited alerts", "Unlimited briefs", "API access", "Export data", "30-day history"],
    cta: "Go Pro",
    highlighted: true,
  },
  {
    name: "Business",
    price: "$299",
    period: "/mo",
    description: "For teams",
    features: ["Everything in Pro", "5 team seats", "Custom categories", "90-day history", "Priority support"],
    cta: "Contact Sales",
    highlighted: false,
  },
];

const COMPARISONS = [
  { product: "Google Trends", issue: "Shows what already trended — no predictions", us: "Predicts 24-72h ahead" },
  { product: "Exploding Topics", issue: "$299/mo, weekly updates only", us: "From $0, real-time updates" },
  { product: "Twitter Trending", issue: "Noise, politics, bots", us: "15+ sources, AI-filtered" },
  { product: "SparkToro", issue: "Audiences, not trends", us: "Trend predictions + content briefs" },
];

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-background">
      {/* Nav */}
      <nav className="border-b border-border/50 bg-background/80 backdrop-blur-sm sticky top-0 z-50">
        <div className="mx-auto max-w-6xl flex items-center justify-between px-6 py-3">
          <div className="flex items-center gap-2">
            <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-primary">
              <Zap className="h-4 w-4 text-primary-foreground" />
            </div>
            <span className="font-semibold text-lg">TrendRadar</span>
          </div>
          <div className="flex items-center gap-4">
            <Link href="/explore" className="text-sm text-muted-foreground hover:text-foreground">
              Explore
            </Link>
            <Link href="#pricing" className="text-sm text-muted-foreground hover:text-foreground">
              Pricing
            </Link>
            <Link
              href="/explore"
              className="rounded-lg bg-primary px-4 py-1.5 text-sm font-medium text-primary-foreground hover:bg-primary/90"
            >
              Get Started
            </Link>
          </div>
        </div>
      </nav>

      {/* Hero */}
      <section className="mx-auto max-w-6xl px-6 pt-20 pb-16 text-center">
        <div className="inline-flex items-center gap-2 rounded-full border border-border bg-muted/50 px-4 py-1.5 text-sm mb-6">
          <Zap className="h-3.5 w-3.5 text-primary" />
          <span className="text-muted-foreground">Signal Intelligence Platform</span>
        </div>
        <h1 className="text-5xl md:text-6xl font-bold tracking-tight mb-6">
          Predict trends{" "}
          <span className="bg-gradient-to-r from-primary to-purple-600 bg-clip-text text-transparent">
            before they go mainstream
          </span>
        </h1>
        <p className="text-lg text-muted-foreground max-w-2xl mx-auto mb-8">
          TrendRadar monitors 15+ signal sources and uses AI to predict what will trend
          24-72 hours before it happens. Get content briefs, alerts, and predictions — not just data.
        </p>
        <div className="flex items-center justify-center gap-4">
          <Link
            href="/explore"
            className="inline-flex items-center gap-2 rounded-lg bg-primary px-6 py-3 text-sm font-semibold text-primary-foreground hover:bg-primary/90 transition-colors"
          >
            Start Free <ArrowRight className="h-4 w-4" />
          </Link>
          <Link
            href="#how-it-works"
            className="inline-flex items-center gap-2 rounded-lg border border-border px-6 py-3 text-sm font-medium hover:bg-accent transition-colors"
          >
            See How It Works
          </Link>
        </div>

        {/* Source logos strip */}
        <div className="mt-16">
          <p className="text-xs text-muted-foreground uppercase tracking-wider mb-4">
            Powered by 15+ signal sources
          </p>
          <div className="flex flex-wrap items-center justify-center gap-3">
            {SOURCES.map((source) => (
              <span
                key={source}
                className="rounded-full border border-border bg-card px-3 py-1 text-xs text-muted-foreground"
              >
                {source}
              </span>
            ))}
          </div>
        </div>
      </section>

      {/* Features */}
      <section className="mx-auto max-w-6xl px-6 py-20">
        <h2 className="text-3xl font-bold text-center mb-4">Not just data. Predictions.</h2>
        <p className="text-center text-muted-foreground mb-12 max-w-xl mx-auto">
          Unlike tools that show you what already happened, TrendRadar tells you what will happen next.
        </p>
        <div className="grid md:grid-cols-2 gap-6">
          {FEATURES.map((feature) => (
            <div key={feature.title} className="rounded-xl border border-border bg-card p-6">
              <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-primary/10 mb-4">
                <feature.icon className="h-5 w-5 text-primary" />
              </div>
              <h3 className="font-semibold text-lg mb-2">{feature.title}</h3>
              <p className="text-sm text-muted-foreground">{feature.description}</p>
            </div>
          ))}
        </div>
      </section>

      {/* How It Works */}
      <section id="how-it-works" className="mx-auto max-w-6xl px-6 py-20 border-t border-border">
        <h2 className="text-3xl font-bold text-center mb-12">How Signal Intelligence Works</h2>
        <div className="grid md:grid-cols-4 gap-6">
          {[
            { step: "1", title: "Collect", desc: "We scan 15+ free signal sources every 15 minutes" },
            { step: "2", title: "Correlate", desc: "AI detects cross-source patterns — same topic on multiple platforms" },
            { step: "3", title: "Predict", desc: "ML model predicts growth trajectory with confidence score" },
            { step: "4", title: "Act", desc: "Get alerts + AI content briefs to capitalize on trends early" },
          ].map((item) => (
            <div key={item.step} className="text-center">
              <div className="flex h-12 w-12 items-center justify-center rounded-full bg-primary text-primary-foreground font-bold text-lg mx-auto mb-4">
                {item.step}
              </div>
              <h3 className="font-semibold mb-2">{item.title}</h3>
              <p className="text-sm text-muted-foreground">{item.desc}</p>
            </div>
          ))}
        </div>
      </section>

      {/* Comparison */}
      <section className="mx-auto max-w-6xl px-6 py-20 border-t border-border">
        <h2 className="text-3xl font-bold text-center mb-12">Why TrendRadar?</h2>
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-border">
                <th className="text-left py-3 px-4 font-medium text-muted-foreground">Product</th>
                <th className="text-left py-3 px-4 font-medium text-muted-foreground">Limitation</th>
                <th className="text-left py-3 px-4 font-medium text-primary">TrendRadar</th>
              </tr>
            </thead>
            <tbody>
              {COMPARISONS.map((row) => (
                <tr key={row.product} className="border-b border-border/50">
                  <td className="py-3 px-4 font-medium">{row.product}</td>
                  <td className="py-3 px-4 text-muted-foreground">{row.issue}</td>
                  <td className="py-3 px-4 text-primary font-medium">{row.us}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>

      {/* Pricing */}
      <section id="pricing" className="mx-auto max-w-6xl px-6 py-20 border-t border-border">
        <h2 className="text-3xl font-bold text-center mb-4">Simple Pricing</h2>
        <p className="text-center text-muted-foreground mb-12">Start free. Upgrade when you need predictions.</p>
        <div className="grid md:grid-cols-4 gap-6">
          {PLANS.map((plan) => (
            <div
              key={plan.name}
              className={`rounded-xl border p-6 ${
                plan.highlighted
                  ? "border-primary bg-primary/5 shadow-lg shadow-primary/10"
                  : "border-border bg-card"
              }`}
            >
              <h3 className="font-semibold text-lg">{plan.name}</h3>
              <p className="text-sm text-muted-foreground mb-4">{plan.description}</p>
              <div className="mb-6">
                <span className="text-3xl font-bold">{plan.price}</span>
                {plan.period && <span className="text-muted-foreground">{plan.period}</span>}
              </div>
              <ul className="space-y-2 mb-6">
                {plan.features.map((feature) => (
                  <li key={feature} className="flex items-center gap-2 text-sm">
                    <Check className="h-4 w-4 text-primary shrink-0" />
                    {feature}
                  </li>
                ))}
              </ul>
              <Link
                href="/explore"
                className={`block text-center rounded-lg py-2 text-sm font-medium transition-colors ${
                  plan.highlighted
                    ? "bg-primary text-primary-foreground hover:bg-primary/90"
                    : "border border-border hover:bg-accent"
                }`}
              >
                {plan.cta}
              </Link>
            </div>
          ))}
        </div>
      </section>

      {/* CTA */}
      <section className="mx-auto max-w-6xl px-6 py-20 text-center border-t border-border">
        <h2 className="text-3xl font-bold mb-4">Ready to predict the next big trend?</h2>
        <p className="text-muted-foreground mb-8">
          Join thousands of creators who catch trends before they go mainstream.
        </p>
        <Link
          href="/explore"
          className="inline-flex items-center gap-2 rounded-lg bg-primary px-8 py-3 text-sm font-semibold text-primary-foreground hover:bg-primary/90"
        >
          Start Free — No Credit Card <ArrowRight className="h-4 w-4" />
        </Link>
      </section>

      {/* Footer */}
      <footer className="border-t border-border py-8">
        <div className="mx-auto max-w-6xl px-6 flex items-center justify-between text-sm text-muted-foreground">
          <div className="flex items-center gap-2">
            <Zap className="h-4 w-4 text-primary" />
            <span>TrendRadar</span>
          </div>
          <p>Signal Intelligence Platform</p>
        </div>
      </footer>
    </div>
  );
}
