"""RAG pipeline: PDF -> chunk -> embed -> ChromaDB -> retrieve.

Designed to degrade gracefully: if chromadb / sentence-transformers / pypdf are
not installed (e.g. a lightweight demo box), the module still imports and the
API returns a clear message instead of crashing the whole app.
"""
from __future__ import annotations

import os
from typing import Optional

from app.config import settings

_AVAILABLE = True
_IMPORT_ERROR = ""

try:
    import chromadb
    from chromadb.utils import embedding_functions
    from pypdf import PdfReader
except Exception as e:  # pragma: no cover
    _AVAILABLE = False
    _IMPORT_ERROR = str(e)


def _chunk_text(text: str, chunk_size: int = 800, overlap: int = 120) -> list[str]:
    """Simple sliding-window chunker (LangChain RecursiveCharacterTextSplitter-style)."""
    text = " ".join(text.split())
    chunks, start = [], 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start = end - overlap
    return [c for c in chunks if c.strip()]


class RagService:
    def __init__(self) -> None:
        self.ready = _AVAILABLE
        if not self.ready:
            return
        os.makedirs(settings.chroma_persist_dir, exist_ok=True)
        self.client = chromadb.PersistentClient(path=settings.chroma_persist_dir)
        self.embed_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name=settings.embedding_model
        )
        self.collection = self.client.get_or_create_collection(
            name="campus_docs", embedding_function=self.embed_fn
        )

    def ingest_pdf(self, file_path: str, doc_name: str) -> dict:
        if not self.ready:
            return {"ok": False, "error": f"RAG dependencies unavailable: {_IMPORT_ERROR}"}
        reader = PdfReader(file_path)
        full_text = "\n".join(page.extract_text() or "" for page in reader.pages)
        chunks = _chunk_text(full_text)
        if not chunks:
            return {"ok": False, "error": "No extractable text in PDF."}
        ids = [f"{doc_name}-{i}" for i in range(len(chunks))]
        metadatas = [{"source": doc_name, "chunk": i} for i in range(len(chunks))]
        self.collection.add(documents=chunks, ids=ids, metadatas=metadatas)
        return {"ok": True, "doc": doc_name, "chunks": len(chunks)}

    def retrieve(self, query: str, k: int = 4) -> tuple[str, list[str]]:
        if not self.ready:
            return ("", [])
        try:
            res = self.collection.query(query_texts=[query], n_results=k)
        except Exception:
            return ("", [])
        docs = (res.get("documents") or [[]])[0]
        metas = (res.get("metadatas") or [[]])[0]
        context = "\n---\n".join(docs)
        sources = sorted({m.get("source", "doc") for m in metas})
        return context, sources


_rag: Optional[RagService] = None


def get_rag() -> RagService:
    global _rag
    if _rag is None:
        _rag = RagService()
    return _rag


def tool_search_documents(query: str) -> str:
    """Agent entry point for uploaded-document questions."""
    rag = get_rag()
    if not rag.ready:
        return "Document search is unavailable (RAG dependencies not installed)."
    context, sources = rag.retrieve(query)
    if not context:
        return "No relevant content found in the uploaded documents."
    src = f" (sources: {', '.join(sources)})" if sources else ""
    return f"From uploaded documents{src}:\n{context}"
