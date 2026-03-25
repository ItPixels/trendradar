import Link from "next/link";

export default function NotFound() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center px-4">
      <h1 className="mb-2 text-6xl font-bold text-foreground">404</h1>
      <p className="mb-8 text-lg text-muted-foreground">
        This page could not be found.
      </p>
      <Link
        href="/"
        className="inline-flex h-10 items-center justify-center rounded-md bg-primary px-6 text-sm font-medium text-primary-foreground transition-colors hover:bg-primary/90"
      >
        Go Home
      </Link>
    </main>
  );
}
