"use client";
import { useQuery } from "@tanstack/react-query";
import {
  BarChart, Bar, PieChart, Pie, Cell, XAxis, YAxis, Tooltip,
  ResponsiveContainer, CartesianGrid,
} from "recharts";
import { api } from "@/lib/api";

const COLORS = ["#245FFF", "#22c55e", "#f59e0b", "#ef4444", "#8b5cf6", "#06b6d4"];

function ChartCard({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <div className="card">
      <h3 className="mb-3 font-semibold">{title}</h3>
      <div className="h-64">
        <ResponsiveContainer width="100%" height="100%">{children as any}</ResponsiveContainer>
      </div>
    </div>
  );
}

export default function AdminPage() {
  const books = useQuery({ queryKey: ["a-books"], queryFn: api.mostRequestedBooks });
  const queries = useQuery({ queryKey: ["a-queries"], queryFn: api.popularQueries });
  const menu = useQuery({ queryKey: ["a-menu"], queryFn: api.menuPopularity });
  const events = useQuery({ queryKey: ["a-events"], queryFn: api.eventsAttendance });

  return (
    <div className="space-y-6">
      <h2 className="text-lg font-semibold">Analytics Dashboard</h2>
      <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
        <ChartCard title="Most Requested Books">
          <BarChart data={books.data || []}>
            <CartesianGrid strokeDasharray="3 3" opacity={0.2} />
            <XAxis dataKey="name" hide /><YAxis /><Tooltip />
            <Bar dataKey="value" fill="#245FFF" radius={[6, 6, 0, 0]} />
          </BarChart>
        </ChartCard>

        <ChartCard title="Popular Queries (by service)">
          <PieChart>
            <Pie data={queries.data || []} dataKey="value" nameKey="name" outerRadius={90} label>
              {(queries.data || []).map((_: any, i: number) => <Cell key={i} fill={COLORS[i % COLORS.length]} />)}
            </Pie>
            <Tooltip />
          </PieChart>
        </ChartCard>

        <ChartCard title="Events Attendance">
          <BarChart data={events.data || []}>
            <CartesianGrid strokeDasharray="3 3" opacity={0.2} />
            <XAxis dataKey="name" hide /><YAxis /><Tooltip />
            <Bar dataKey="value" fill="#22c55e" radius={[6, 6, 0, 0]} />
          </BarChart>
        </ChartCard>

        <ChartCard title="Menu Popularity">
          <BarChart data={menu.data || []} layout="vertical">
            <CartesianGrid strokeDasharray="3 3" opacity={0.2} />
            <XAxis type="number" /><YAxis dataKey="name" type="category" width={120} /><Tooltip />
            <Bar dataKey="value" fill="#f59e0b" radius={[0, 6, 6, 0]} />
          </BarChart>
        </ChartCard>
      </div>
    </div>
  );
}
