"use client";
import { useState, useRef, useEffect } from "react";
import { Send, Mic, Volume2, Bot, User2 } from "lucide-react";
import { useStore } from "@/lib/store";
import { api } from "@/lib/api";

const TOOL_LABEL: Record<string, string> = {
  search_library: "📚 Library",
  search_events: "📅 Events",
  search_menu: "🍴 Cafeteria",
  search_academics: "🎓 Academics",
  search_documents: "📄 Documents (RAG)",
};

export function ChatWindow() {
  const { messages, addMessage, clearChat } = useStore();
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const endRef = useRef<HTMLDivElement>(null);

  useEffect(() => endRef.current?.scrollIntoView({ behavior: "smooth" }), [messages]);

  async function send(text: string) {
    if (!text.trim() || loading) return;
    addMessage({ role: "user", content: text });
    setInput("");
    setLoading(true);
    try {
      const res = await api.chat(text);
      addMessage({ role: "assistant", content: res.answer, tool: res.tool_used || undefined });
    } catch (e: any) {
      addMessage({ role: "assistant", content: `Error: ${e.message}` });
    } finally {
      setLoading(false);
    }
  }

  // --- Bonus: Speech-to-Text (Web Speech API) ---
  function startVoice() {
    const SR = (window as any).webkitSpeechRecognition || (window as any).SpeechRecognition;
    if (!SR) return alert("Speech recognition not supported in this browser.");
    const rec = new SR();
    rec.lang = "en-US";
    rec.onresult = (e: any) => setInput(e.results[0][0].transcript);
    rec.start();
  }

  // --- Bonus: Text-to-Speech ---
  function speak(text: string) {
    if (!("speechSynthesis" in window)) return;
    speechSynthesis.speak(new SpeechSynthesisUtterance(text));
  }

  const suggestions = [
    "Is the DBMS book available?",
    "What is today's lunch?",
    "When is the hackathon?",
    "What is the attendance requirement?",
  ];

  return (
    <div className="card flex h-[calc(100vh-10rem)] flex-col">
      <div className="mb-3 flex items-center justify-between">
        <h2 className="font-semibold">AI Campus Assistant</h2>
        <button onClick={clearChat} className="text-xs text-zinc-500 hover:underline">Clear</button>
      </div>

      <div className="flex-1 space-y-4 overflow-y-auto pr-1">
        {messages.length === 0 && (
          <div className="space-y-3">
            <p className="text-sm text-zinc-500">Ask me anything about campus. I'll route your question to the right service.</p>
            <div className="flex flex-wrap gap-2">
              {suggestions.map((s) => (
                <button key={s} onClick={() => send(s)} className="rounded-full border border-black/10 px-3 py-1 text-xs hover:bg-zinc-100 dark:border-white/15 dark:hover:bg-zinc-800">
                  {s}
                </button>
              ))}
            </div>
          </div>
        )}

        {messages.map((m, i) => (
          <div key={i} className={`flex gap-3 ${m.role === "user" ? "flex-row-reverse" : ""}`}>
            <div className={`grid h-8 w-8 shrink-0 place-items-center rounded-full ${m.role === "user" ? "bg-zinc-200 dark:bg-zinc-700" : "bg-brand text-white"}`}>
              {m.role === "user" ? <User2 size={16} /> : <Bot size={16} />}
            </div>
            <div className={`max-w-[80%] rounded-2xl px-4 py-2 text-sm ${m.role === "user" ? "bg-brand text-white" : "bg-zinc-100 dark:bg-zinc-800"}`}>
              {m.tool && <div className="mb-1 text-xs opacity-70">{TOOL_LABEL[m.tool] || m.tool}</div>}
              <p className="whitespace-pre-wrap">{m.content}</p>
              {m.role === "assistant" && (
                <button onClick={() => speak(m.content)} className="mt-1 inline-flex items-center gap-1 text-xs opacity-60 hover:opacity-100">
                  <Volume2 size={12} /> Listen
                </button>
              )}
            </div>
          </div>
        ))}
        {loading && <div className="text-sm text-zinc-500">Assistant is thinking…</div>}
        <div ref={endRef} />
      </div>

      <div className="mt-3 flex items-center gap-2">
        <button onClick={startVoice} className="grid h-10 w-10 place-items-center rounded-xl border border-black/10 hover:bg-zinc-100 dark:border-white/15 dark:hover:bg-zinc-800">
          <Mic size={18} />
        </button>
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && send(input)}
          placeholder="Ask about books, events, food, academics…"
          className="input"
        />
        <button onClick={() => send(input)} disabled={loading} className="btn">
          <Send size={16} />
        </button>
      </div>
    </div>
  );
}
