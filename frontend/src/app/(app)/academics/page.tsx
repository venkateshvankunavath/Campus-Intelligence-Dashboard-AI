"use client";
import { useQuery } from "@tanstack/react-query";
import { api } from "@/lib/api";

export default function AcademicsPage() {
  const notices = useQuery({ queryKey: ["notices"], queryFn: api.notices });
  const rules = useQuery({ queryKey: ["attendance"], queryFn: api.attendanceRules });
  const exams = useQuery({ queryKey: ["exams"], queryFn: api.examSchedule });

  return (
    <div className="grid grid-cols-1 gap-6 lg:grid-cols-3">
      <div className="card lg:col-span-2">
        <h3 className="mb-3 font-semibold">Notices</h3>
        <ul className="space-y-3 text-sm">
          {(notices.data || []).map((n: any) => (
            <li key={n.id}>
              <div className="flex items-center gap-2">
                <span className="rounded-full bg-brand/10 px-2 py-0.5 text-xs text-brand">{n.category}</span>
                <span className="font-medium">{n.title}</span>
              </div>
              <p className="mt-1 text-zinc-500">{n.body}</p>
            </li>
          ))}
        </ul>
      </div>
      <div className="space-y-6">
        <div className="card">
          <h3 className="mb-2 font-semibold">Attendance</h3>
          <p className="text-sm text-zinc-500">{rules.data?.summary}</p>
        </div>
        <div className="card">
          <h3 className="mb-2 font-semibold">Exam Schedule</h3>
          <ul className="space-y-2 text-sm">
            {(exams.data?.exams || []).map((e: any, i: number) => (
              <li key={i} className="flex justify-between">
                <span>{e.course} ({e.type})</span>
                <span className="text-zinc-500">{e.date}</span>
              </li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
}
