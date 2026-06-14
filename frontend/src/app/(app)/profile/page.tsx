"use client";
import { useSession } from "next-auth/react";
import { useStore } from "@/lib/store";

export default function ProfilePage() {
  const { data: session } = useSession();
  const bookmarks = useStore((s) => s.bookmarks);
  return (
    <div className="max-w-lg space-y-6">
      <div className="card">
        <h3 className="mb-3 font-semibold">Profile</h3>
        <dl className="space-y-2 text-sm">
          <div className="flex justify-between"><dt className="text-zinc-500">Name</dt><dd>{session?.user?.name}</dd></div>
          <div className="flex justify-between"><dt className="text-zinc-500">Email</dt><dd>{session?.user?.email}</dd></div>
          <div className="flex justify-between"><dt className="text-zinc-500">Role</dt><dd className="capitalize">{(session?.user as any)?.role}</dd></div>
        </dl>
      </div>
      <div className="card">
        <h3 className="mb-3 font-semibold">Bookmarks ({bookmarks.length})</h3>
        {bookmarks.length === 0 ? (
          <p className="text-sm text-zinc-500">No bookmarks yet.</p>
        ) : (
          <ul className="space-y-1 text-sm">{bookmarks.map((b) => <li key={b}>{b}</li>)}</ul>
        )}
      </div>
    </div>
  );
}
