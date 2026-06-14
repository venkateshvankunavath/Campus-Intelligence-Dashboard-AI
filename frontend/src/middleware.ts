// Protect everything except the login page and auth/static assets (RBAC entry).
import { auth } from "@/auth";

export default auth((req) => {
  const isAuthed = !!req.auth;
  const isLogin = req.nextUrl.pathname.startsWith("/login");
  if (!isAuthed && !isLogin) {
    const url = new URL("/login", req.nextUrl.origin);
    return Response.redirect(url);
  }
});

export const config = {
  matcher: ["/((?!api|_next/static|_next/image|favicon.ico).*)"],
};
