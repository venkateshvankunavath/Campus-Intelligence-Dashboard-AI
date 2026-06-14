"use client";
import { useQuery } from "@tanstack/react-query";
import { api } from "@/lib/api";

export default function CafeteriaPage() {
  const { data = [] } = useQuery({ queryKey: ["menu"], queryFn: api.menu });
  const cats = ["breakfast", "lunch", "dinner", "snacks"];
  return (
    <div className="grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-4">
      {cats.map((cat) => (
        <div key={cat} className="card">
          <h3 className="mb-3 font-semibold capitalize">{cat}</h3>
          <ul className="space-y-2 text-sm">
            {data.filter((m: any) => m.category === cat).map((m: any) => (
              <li key={m.id} className="flex justify-between">
                <span>{m.is_vegetarian ? "🟢" : "🔴"} {m.name}</span>
                <span className="text-zinc-500">₹{m.price}</span>
              </li>
            ))}
            {data.filter((m: any) => m.category === cat).length === 0 && (
              <li className="text-zinc-400">Nothing listed</li>
            )}
          </ul>
        </div>
      ))}
    </div>
  );
}
