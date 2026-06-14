# Architecture

## MCP-style services (no single central DB access layer)

Each campus domain is an **independent service** with its own router, its own
query logic, and its own agent-tool surface. They share one Postgres instance
for the demo, but each is isolated at the code boundary and could trivially be
split into its own process / repo / database — exactly the MCP philosophy of
many small, single-responsibility services rather than one monolith.

```
                         ┌──────────────────────────┐
                         │   Next.js 15 Frontend     │
                         │  (Dashboard, Chat, RBAC)  │
                         └─────────────┬─────────────┘
                                       │ HTTPS / JSON
                         ┌─────────────▼─────────────┐
                         │        FastAPI API         │
                         │  ┌──────────────────────┐  │
   user query  ───────►  │  │   AI Agent (Gemini)  │  │
                         │  │  decides ONE tool ▼  │  │
                         │  └──┬────┬────┬────┬────┘  │
                         │     │    │    │    │       │
       ┌─────────────────┼─────┘    │    │    └───────┼────────────────┐
       ▼                 ▼          ▼    ▼            ▼                ▼
 ┌───────────┐    ┌───────────┐ ┌────────┐ ┌────────────┐    ┌────────────────┐
 │  Library  │    │  Events   │ │Cafeteria│ │ Academics  │    │  RAG / Docs    │
 │   MCP     │    │   MCP     │ │  MCP    │ │   MCP      │    │ ChromaDB +     │
 │           │    │           │ │         │ │            │    │ Sentence-Trans │
 └─────┬─────┘    └─────┬─────┘ └───┬─────┘ └─────┬──────┘    └───────┬────────┘
       └────────────────┴───────────┴─────────────┘                  │
                          PostgreSQL (SQLAlchemy)             persisted vectors
```

## Agent decision flow

1. Receive user query at `POST /api/v1/chat`.
2. Gemini 2.5 Flash is given five function declarations (one per service) and
   chooses **exactly one** via function calling.
3. The chosen tool executes against live data (DB or vector store).
4. The tool result is fed back to Gemini for a natural-language synthesis.
5. Answer + `tool_used` returned and persisted to `chat_history`.

If `GEMINI_API_KEY` is absent, a deterministic keyword router selects the tool
so the system stays fully demoable offline — the architecture is identical, only
the selector swaps.

## RAG pipeline

`Upload PDF → extract text (pypdf) → chunk (sliding window) → embed
(all-MiniLM-L6-v2) → store in ChromaDB → retrieve top-k → synthesize answer.`
