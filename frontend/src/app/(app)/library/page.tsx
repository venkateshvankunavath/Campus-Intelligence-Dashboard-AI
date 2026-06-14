"use client";
import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { Search, Bookmark } from "lucide-react";
import { api } from "@/lib/api";
import { useStore } from "@/lib/store";

export default function LibraryPage() {
  const [q, setQ] = useState("");
  const { bookmarks, toggleBookmark } = useStore();
  const { data = [] } = useQuery({ queryKey: ["books", q], queryFn: () => api.books(q) });

  return (
    <div className="space-y-4">
      <div className="flex items-center gap-2">
        <div className="relative flex-1">
          <Search size={16} className="absolute left-3 top-3 text-zinc-400" />
          <input value={q} onChange={(e) => setQ(e.target.value)} placeholder="Search books, authors, categories…" className="input pl-9" />
        </div>
      </div>
      <div className="grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-3">
        {data.map((b: any) => (
          <div key={b.id} className="card">
            <div className="flex items-start justify-between">
              <h3 className="font-semibold">{b.title}</h3>
              <button onClick={() => toggleBookmark(`book-${b.id}`)}>
                <Bookmark size={16} className={bookmarks.includes(`book-${b.id}`) ? "fill-brand text-brand" : "text-zinc-400"} />
              </button>
            </div>
            <p className="text-sm text-zinc-500">{b.author}</p>
            <div className="mt-3 flex items-center justify-between text-sm">
              <span className="rounded-full bg-brand/10 px-2 py-0.5 text-xs text-brand">{b.category}</span>
              <span className={b.available_copies > 0 ? "text-green-600" : "text-red-500"}>
                {b.available_copies > 0 ? `${b.available_copies} available` : "Checked out"}
              </span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
