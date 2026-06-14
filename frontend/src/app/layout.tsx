import "./globals.css";
import type { Metadata } from "next";
import { Providers } from "./providers";

export const metadata: Metadata = {
  title: "Campus Intelligence",
  description: "Unified Campus Intelligence Dashboard with AI Assistant",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className="min-h-screen text-zinc-900 antialiased dark:text-zinc-100">
        <Providers>{children}</Providers>
      </body>
    </html>
  );
}
