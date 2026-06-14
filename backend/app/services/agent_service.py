"""AI Agent — Gemini 2.5 Flash with function/tool calling over the MCP services.

The agent receives a user query, lets Gemini decide which campus tool to call
(library / events / cafeteria / academics / documents), executes that tool
against the live data, then returns a natural-language answer.

Fallback: when GEMINI_API_KEY is missing OR the google-genai SDK is not
installed, a deterministic keyword router picks the tool so the product remains
fully demoable offline. This means the architecture (dynamic tool selection)
is identical; only the "brain" choosing the tool swaps out.
"""
from __future__ import annotations

from sqlalchemy.orm import Session

from app.config import settings
from app.mcp.library_service import tool_search_library
from app.mcp.events_service import tool_search_events
from app.mcp.cafeteria_service import tool_search_menu
from app.mcp.academics_service import tool_search_academics
from app.services.rag_service import tool_search_documents

# Tool registry: name -> (callable, needs_db, description)
TOOLS = {
    "search_library": (tool_search_library, True, "Search the campus library for books, availability, authors, categories."),
    "search_events": (tool_search_events, True, "Find campus events, fests, hackathons, deadlines and their timings."),
    "search_menu": (tool_search_menu, True, "Get the cafeteria menu, today's food, prices, veg/non-veg by meal."),
    "search_academics": (tool_search_academics, True, "Academic notices, exam schedule, attendance rules and policies."),
    "search_documents": (tool_search_documents, False, "Search uploaded PDFs / handbooks / rules / course material (RAG)."),
}

SYSTEM_PROMPT = (
    "You are the Campus Intelligence Assistant. You answer student questions by "
    "calling exactly one of the available campus tools, then summarising the result "
    "in a friendly, concise way. Always prefer a tool over guessing. If a question "
    "is about policy documents or uploaded material, use search_documents."
)


def _run_tool(name: str, query: str, db: Session) -> str:
    fn, needs_db, _ = TOOLS[name]
    return fn(db, query) if needs_db else fn(query)


# ---------------- Fallback router (no API key needed) ----------------
def _keyword_route(message: str) -> str:
    m = message.lower()
    if any(w in m for w in ("book", "library", "borrow", "isbn", "author", "novel")):
        return "search_library"
    if any(w in m for w in ("event", "fest", "hackathon", "workshop", "seminar", "fest")):
        return "search_events"
    if any(w in m for w in ("lunch", "dinner", "breakfast", "menu", "food", "cafeteria", "canteen", "eat")):
        return "search_menu"
    if any(w in m for w in ("attendance", "exam", "schedule", "notice", "deadline", "grade", "marks")):
        return "search_academics"
    if any(w in m for w in ("handbook", "rule", "policy", "document", "pdf", "syllabus", "course material")):
        return "search_documents"
    return "search_academics"  # safe default


def _fallback(message: str, db: Session) -> dict:
    tool = _keyword_route(message)
    result = _run_tool(tool, message, db)
    return {"answer": result, "tool_used": tool, "sources": []}


# ---------------- Gemini-powered agent ----------------
def _gemini_agent(message: str, db: Session) -> dict:
    from google import genai
    from google.genai import types

    client = genai.Client(api_key=settings.gemini_api_key)

    function_declarations = [
        types.FunctionDeclaration(
            name=name,
            description=desc,
            parameters={
                "type": "object",
                "properties": {"query": {"type": "string", "description": "The user's search query"}},
                "required": ["query"],
            },
        )
        for name, (_, _, desc) in TOOLS.items()
    ]
    tools = [types.Tool(function_declarations=function_declarations)]

    config = types.GenerateContentConfig(system_instruction=SYSTEM_PROMPT, tools=tools)
    contents = [types.Content(role="user", parts=[types.Part(text=message)])]

    resp = client.models.generate_content(model=settings.gemini_model, contents=contents, config=config)

    candidate = resp.candidates[0]
    fcall = next((p.function_call for p in candidate.content.parts if getattr(p, "function_call", None)), None)

    if not fcall:
        return {"answer": resp.text or "I couldn't determine a tool to use.", "tool_used": None, "sources": []}

    tool_name = fcall.name
    query = (fcall.args or {}).get("query", message)
    tool_result = _run_tool(tool_name, query, db)

    # Feed the tool result back for a natural-language synthesis
    contents.append(candidate.content)
    contents.append(
        types.Content(
            role="user",
            parts=[types.Part.from_function_response(name=tool_name, response={"result": tool_result})],
        )
    )
    final = client.models.generate_content(model=settings.gemini_model, contents=contents, config=config)
    return {"answer": final.text or tool_result, "tool_used": tool_name, "sources": []}


def run_agent(message: str, db: Session) -> dict:
    """Public entry point used by the chat endpoint."""
    if not settings.gemini_api_key:
        return _fallback(message, db)
    try:
        return _gemini_agent(message, db)
    except Exception as e:  # never let the demo crash on an API hiccup
        result = _fallback(message, db)
        result["answer"] += f"\n\n(Note: fell back to local routing — {type(e).__name__})"
        return result
