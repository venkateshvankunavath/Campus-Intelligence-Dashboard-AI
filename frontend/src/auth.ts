// Auth.js (NextAuth v5) — Credentials provider that authenticates against the
// FastAPI backend and stores the backend-issued JWT in the session.
import NextAuth from "next-auth";
import Credentials from "next-auth/providers/credentials";

const BACKEND = process.env.BACKEND_URL || "http://localhost:8000/api/v1";

export const { handlers, signIn, signOut, auth } = NextAuth({
  trustHost: true,
  session: { strategy: "jwt" },
  pages: { signIn: "/login" },
  providers: [
    Credentials({
      credentials: { email: {}, password: {} },
      authorize: async (creds) => {
        try {
          const res = await fetch(`${BACKEND}/auth/login`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email: creds?.email, password: creds?.password }),
          });
          if (!res.ok) return null;
          const data = await res.json();
          return {
            id: String(data.user.id),
            name: data.user.name,
            email: data.user.email,
            role: data.user.role,
            accessToken: data.access_token,
          } as any;
        } catch {
          return null;
        }
      },
    }),
  ],
  callbacks: {
    jwt: ({ token, user }) => {
      if (user) {
        token.role = (user as any).role;
        token.accessToken = (user as any).accessToken;
        token.uid = (user as any).id;
      }
      return token;
    },
    session: ({ session, token }) => {
      (session.user as any).role = token.role;
      (session.user as any).id = token.uid;
      (session as any).accessToken = token.accessToken;
      return session;
    },
  },
});
