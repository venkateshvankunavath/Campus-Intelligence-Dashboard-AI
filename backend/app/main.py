"""FastAPI application entrypoint — wires the 4 MCP services + agent + RAG."""
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import Base, engine
from app.mcp import academics_service, cafeteria_service, events_service, library_service
from app.routers import analytics, auth, chat, rag


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create tables on startup (use Alembic migrations in production).
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    description=(
        "Unified Campus Intelligence Dashboard backend. Four independent MCP-style "
        "services (Library, Events, Cafeteria, Academics) plus a Gemini-powered AI "
        "agent that dynamically selects which service to call, and a ChromaDB RAG layer."
    ),
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

P = settings.api_v1_prefix
# Auth + AI
app.include_router(auth.router, prefix=P)
app.include_router(chat.router, prefix=P)
app.include_router(rag.router, prefix=P)
app.include_router(analytics.router, prefix=P)
# The four independent MCP services
app.include_router(library_service.router, prefix=P)
app.include_router(events_service.router, prefix=P)
app.include_router(cafeteria_service.router, prefix=P)
app.include_router(academics_service.router, prefix=P)


@app.get("/", tags=["Health"])
def root():
    return {"status": "ok", "service": settings.app_name, "docs": "/docs"}


@app.get("/health", tags=["Health"])
def health():
    return {"status": "healthy", "gemini": bool(settings.gemini_api_key)}
