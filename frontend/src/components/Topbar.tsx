"use client";
import { signOut, useSession } from "next-auth/react";
import { Bell, LogOut } from "lucide-react";
import { ThemeToggle } from "./ThemeToggle";

export function Topbar() {
  const { data: session } = useSession();
  return (
    <header className="flex items-center justify-between border-b border-black/5 bg-white px-6 py-3 dark:border-white/10 dark:bg-zinc-900">
      <h1 className="text-sm font-medium text-zinc-500">Unified Campus Intelligence</h1>
      <div className="flex items-center gap-3">
        <button className="relative grid h-9 w-9 place-items-center rounded-xl border border-black/10 hover:bg-zinc-100 dark:border-white/15 dark:hover:bg-zinc-800">
          <Bell size={18} />
          <span className="absolute right-2 top-2 h-2 w-2 rounded-full bg-brand" />
        </button>
        <ThemeToggle />
        {session?.user && (
          <div className="flex items-center gap-2">
            <span className="hidden text-sm sm:block">{session.user.name}</span>
            <button onClick={() => signOut({ callbackUrl: "/login" })} className="grid h-9 w-9 place-items-center rounded-xl border border-black/10 hover:bg-zinc-100 dark:border-white/15 dark:hover:bg-zinc-800">
              <LogOut size={18} />
            </button>
          </div>
        )}
      </div>
    </header>
  );
}
