// Thin fetch wrapper around the FastAPI backend.
const BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

async function request<T>(path: string, options: RequestInit = {}): Promise<T> {
  const res = await fetch(`${BASE}${path}`, {
    headers: { "Content-Type": "application/json", ...(options.headers || {}) },
    ...options,
  });
  if (!res.ok) throw new Error(`API ${res.status}: ${await res.text()}`);
  return res.json() as Promise<T>;
}

export const api = {
  // Chat / agent
  chat: (message: string, studentId?: number) =>
    request<{ answer: string; tool_used?: string; sources: string[] }>("/chat", {
      method: "POST",
      body: JSON.stringify({ message, student_id: studentId }),
    }),

  // MCP services
  books: (q = "") => request<any[]>(`/library/books${q ? `?q=${encodeURIComponent(q)}` : ""}`),
  events: () => request<any[]>("/events?upcoming=true"),
  menu: () => request<any[]>("/cafeteria/menu?today=true"),
  notices: () => request<any[]>("/academics/notices"),
  attendanceRules: () => request<any>("/academics/attendance-rules"),
  examSchedule: () => request<{ exams: any[] }>("/academics/exam-schedule"),

  // Analytics
  overview: () => request<any>("/analytics/overview"),
  mostRequestedBooks: () => request<any[]>("/analytics/most-requested-books"),
  popularQueries: () => request<any[]>("/analytics/popular-queries"),
  menuPopularity: () => request<any[]>("/analytics/menu-popularity"),
  eventsAttendance: () => request<any[]>("/analytics/events-attendance"),
};
