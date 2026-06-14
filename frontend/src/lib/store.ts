import { create } from "zustand";
import { persist } from "zustand/middleware";

type ChatMsg = { role: "user" | "assistant"; content: string; tool?: string };

interface AppState {
  theme: "light" | "dark";
  toggleTheme: () => void;
  messages: ChatMsg[];
  addMessage: (m: ChatMsg) => void;
  clearChat: () => void;
  bookmarks: string[];
  toggleBookmark: (id: string) => void;
}

export const useStore = create<AppState>()(
  persist(
    (set) => ({
      theme: "light",
      toggleTheme: () =>
        set((s) => {
          const next = s.theme === "light" ? "dark" : "light";
          if (typeof document !== "undefined")
            document.documentElement.classList.toggle("dark", next === "dark");
          return { theme: next };
        }),
      messages: [],
      addMessage: (m) => set((s) => ({ messages: [...s.messages, m] })),
      clearChat: () => set({ messages: [] }),
      bookmarks: [],
      toggleBookmark: (id) =>
        set((s) => ({
          bookmarks: s.bookmarks.includes(id)
            ? s.bookmarks.filter((b) => b !== id)
            : [...s.bookmarks, id],
        })),
    }),
    { name: "campus-store" }
  )
);
