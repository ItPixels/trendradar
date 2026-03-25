import Link from "next/link";

export default function SignupPage() {
  return (
    <div className="rounded-xl border border-border bg-card p-6">
      <h1 className="text-xl font-semibold text-center mb-2">Create your account</h1>
      <p className="text-sm text-muted-foreground text-center mb-6">Start predicting trends for free</p>

      {/* OAuth */}
      <div className="space-y-2 mb-6">
        <button className="w-full flex items-center justify-center gap-2 rounded-lg border border-border py-2.5 text-sm font-medium hover:bg-accent transition-colors">
          Continue with Google
        </button>
        <button className="w-full flex items-center justify-center gap-2 rounded-lg border border-border py-2.5 text-sm font-medium hover:bg-accent transition-colors">
          Continue with GitHub
        </button>
      </div>

      <div className="relative mb-6">
        <div className="absolute inset-0 flex items-center">
          <div className="w-full border-t border-border" />
        </div>
        <div className="relative flex justify-center text-xs">
          <span className="bg-card px-2 text-muted-foreground">or</span>
        </div>
      </div>

      <form className="space-y-4">
        <div>
          <label className="text-sm font-medium" htmlFor="name">Full name</label>
          <input
            id="name"
            type="text"
            placeholder="John Doe"
            className="mt-1 w-full rounded-lg border border-input bg-background px-3 py-2 text-sm outline-none focus:border-primary focus:ring-1 focus:ring-primary"
          />
        </div>
        <div>
          <label className="text-sm font-medium" htmlFor="email">Email</label>
          <input
            id="email"
            type="email"
            placeholder="you@example.com"
            className="mt-1 w-full rounded-lg border border-input bg-background px-3 py-2 text-sm outline-none focus:border-primary focus:ring-1 focus:ring-primary"
          />
        </div>
        <div>
          <label className="text-sm font-medium" htmlFor="password">Password</label>
          <input
            id="password"
            type="password"
            placeholder="Min 8 characters"
            className="mt-1 w-full rounded-lg border border-input bg-background px-3 py-2 text-sm outline-none focus:border-primary focus:ring-1 focus:ring-primary"
          />
        </div>
        <button
          type="submit"
          className="w-full rounded-lg bg-primary py-2.5 text-sm font-medium text-primary-foreground hover:bg-primary/90 transition-colors"
        >
          Create Account
        </button>
      </form>

      <p className="mt-4 text-center text-sm text-muted-foreground">
        Already have an account? <Link href="/login" className="text-primary hover:underline">Sign in</Link>
      </p>
    </div>
  );
}
