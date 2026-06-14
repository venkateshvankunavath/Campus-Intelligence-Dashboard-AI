"use client";
import { useState } from "react";
import { signIn } from "next-auth/react";
import { useRouter } from "next/navigation";

export default function LoginPage() {
  const [email, setEmail] = useState("student@campus.edu");
  const [password, setPassword] = useState("student123");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const router = useRouter();

  async function submit() {
    setLoading(true); setError("");
    const res = await signIn("credentials", { email, password, redirect: false });
    setLoading(false);
    if (res?.error) setError("Invalid credentials");
    else router.push("/");
  }

  return (
    <div className="grid min-h-screen place-items-center p-6">
      <div className="card w-full max-w-sm space-y-4">
        <div className="text-center">
          <div className="mx-auto mb-2 grid h-12 w-12 place-items-center rounded-2xl bg-brand text-xl font-bold text-white">C</div>
          <h1 className="text-xl font-semibold">CampusIQ Login</h1>
          <p className="text-sm text-zinc-500">Sign in to your campus account</p>
        </div>
        <input className="input" value={email} onChange={(e) => setEmail(e.target.value)} placeholder="Email" />
        <input className="input" type="password" value={password} onChange={(e) => setPassword(e.target.value)} placeholder="Password" onKeyDown={(e) => e.key === "Enter" && submit()} />
        {error && <p className="text-sm text-red-500">{error}</p>}
        <button onClick={submit} disabled={loading} className="btn w-full">{loading ? "Signing in…" : "Sign in"}</button>
        <p className="text-center text-xs text-zinc-500">
          Demo: student@campus.edu / student123 · admin@campus.edu / admin123
        </p>
      </div>
    </div>
  );
}
