"use client";
import { Moon, Sun } from "lucide-react";
import { useStore } from "@/lib/store";

export function ThemeToggle() {
  const { theme, toggleTheme } = useStore();
  return (
    <button
      onClick={toggleTheme}
      aria-label="Toggle theme"
      className="grid h-9 w-9 place-items-center rounded-xl border border-black/10 hover:bg-zinc-100 dark:border-white/15 dark:hover:bg-zinc-800"
    >
      {theme === "dark" ? <Sun size={18} /> : <Moon size={18} />}
    </button>
  );
}
