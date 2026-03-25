import { type NextRequest, NextResponse } from "next/server";

export async function middleware(request: NextRequest) {
  // TODO: Implement Supabase auth check
  // 1. Create a Supabase client using @supabase/ssr
  // 2. Refresh the session if it exists
  // 3. Redirect unauthenticated users from protected routes to /sign-in
  // 4. Redirect authenticated users from auth routes to /dashboard

  return NextResponse.next();
}

export const config = {
  matcher: [
    /*
     * Match all request paths except:
     * - _next/static (static files)
     * - _next/image (image optimization)
     * - favicon.ico (favicon)
     * - public folder files
     */
    "/((?!_next/static|_next/image|favicon.ico|.*\\.(?:svg|png|jpg|jpeg|gif|webp)$).*)",
  ],
};
