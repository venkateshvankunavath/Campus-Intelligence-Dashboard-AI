"use client";
import { useQuery } from "@tanstack/react-query";
import { MapPin, Clock } from "lucide-react";
import { api } from "@/lib/api";

export default function EventsPage() {
  const { data = [] } = useQuery({ queryKey: ["events"], queryFn: api.events });
  return (
    <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
      {data.map((e: any) => (
        <div key={e.id} className="card">
          <div className="mb-2 flex items-center justify-between">
            <h3 className="font-semibold">{e.title}</h3>
            <span className="rounded-full bg-brand/10 px-2 py-0.5 text-xs text-brand">{e.category}</span>
          </div>
          <p className="text-sm text-zinc-500">{e.description}</p>
          <div className="mt-3 flex flex-wrap gap-4 text-sm text-zinc-500">
            <span className="flex items-center gap-1"><Clock size={14} /> {new Date(e.starts_at).toLocaleString()}</span>
            <span className="flex items-center gap-1"><MapPin size={14} /> {e.location}</span>
          </div>
        </div>
      ))}
    </div>
  );
}
