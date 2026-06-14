"use client";
import { useQuery } from "@tanstack/react-query";
import { BookOpen, CalendarDays, UtensilsCrossed, GraduationCap } from "lucide-react";
import { api } from "@/lib/api";
import { StatCard } from "@/components/StatCard";
import Link from "next/link";

export default function Dashboard() {
  const overview = useQuery({ queryKey: ["overview"], queryFn: api.overview });
  const events = useQuery({ queryKey: ["events"], queryFn: api.events });
  const menu = useQuery({ queryKey: ["menu"], queryFn: api.menu });
  const notices = useQuery({ queryKey: ["notices"], queryFn: api.notices });
  const o = overview.data || {};

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
        <StatCard label="Books Available" value={o.books_available ?? "—"} icon={BookOpen} />
        <StatCard label="Upcoming Events" value={o.upcoming_events ?? "—"} icon={CalendarDays} />
        <StatCard label="Today's Menu Items" value={o.menu_items_today ?? "—"} icon={UtensilsCrossed} />
        <StatCard label="Total Queries" value={o.total_queries ?? "—"} icon={GraduationCap} />
      </div>

      <div className="grid grid-cols-1 gap-6 lg:grid-cols-3">
        <div className="card lg:col-span-2">
          <div className="mb-3 flex items-center justify-between">
            <h3 className="font-semibold">Upcoming Events</h3>
            <Link href="/events" className="text-xs text-brand hover:underline">View all</Link>
          </div>
          <ul className="space-y-3">
            {(events.data || []).slice(0, 4).map((e: any) => (
              <li key={e.id} className="flex items-center justify-between text-sm">
                <span>{e.title}</span>
                <span className="text-zinc-500">{new Date(e.starts_at).toLocaleDateString()}</span>
              </li>
            ))}
          </ul>
        </div>

        <div className="card">
          <h3 className="mb-3 font-semibold">Today's Menu</h3>
          <ul className="space-y-2 text-sm">
            {(menu.data || []).slice(0, 5).map((m: any) => (
              <li key={m.id} className="flex justify-between">
                <span>{m.is_vegetarian ? "🟢" : "🔴"} {m.name}</span>
                <span className="text-zinc-500">₹{m.price}</span>
              </li>
            ))}
          </ul>
        </div>
      </div>

      <div className="card">
        <h3 className="mb-3 font-semibold">Academic Notices</h3>
        <ul className="space-y-2 text-sm">
          {(notices.data || []).slice(0, 4).map((n: any) => (
            <li key={n.id} className="flex items-center gap-2">
              <span className="rounded-full bg-brand/10 px-2 py-0.5 text-xs text-brand">{n.category}</span>
              {n.title}
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}
