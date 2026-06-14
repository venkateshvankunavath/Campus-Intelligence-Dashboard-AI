"""Library MCP Server — independent service exposing book inventory endpoints.

In an MCP-style architecture each domain is a self-contained service with its
own router, its own data access, and its own search surface. The AI agent calls
the `tool_*` functions; humans/clients call the HTTP endpoints below. Both share
the same query logic so the agent and the UI never drift apart.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.auth.security import require_admin
from app.database import get_db
from app.models import Book
from app.search_utils import keywords
from app.schemas import BookCreate, BookOut

router = APIRouter(prefix="/library", tags=["Library MCP"])


# ---- shared query logic (used by both HTTP layer and agent tool) ----
def _search_books(db: Session, q: str | None = None, available_only: bool = False):
    query = db.query(Book)
    kws = keywords(q)
    if kws:
        conds = []
        for k in kws:
            like = f"%{k}%"
            conds += [Book.title.ilike(like), Book.author.ilike(like), Book.category.ilike(like)]
        query = query.filter(or_(*conds))
    if available_only:
        query = query.filter(Book.available_copies > 0)
    return query.order_by(Book.title).all()


# ---- HTTP endpoints ----
@router.get("/books", response_model=list[BookOut])
def list_books(q: str | None = None, available: bool = False, db: Session = Depends(get_db)):
    return _search_books(db, q, available)


@router.get("/books/{book_id}", response_model=BookOut)
def get_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(Book).get(book_id)
    if not book:
        raise HTTPException(404, "Book not found")
    return book


@router.post("/books", response_model=BookOut, dependencies=[Depends(require_admin)])
def create_book(payload: BookCreate, db: Session = Depends(get_db)):
    book = Book(**payload.model_dump())
    db.add(book)
    db.commit()
    db.refresh(book)
    return book


@router.put("/books/{book_id}", response_model=BookOut, dependencies=[Depends(require_admin)])
def update_book(book_id: int, payload: BookCreate, db: Session = Depends(get_db)):
    book = db.query(Book).get(book_id)
    if not book:
        raise HTTPException(404, "Book not found")
    for k, v in payload.model_dump().items():
        setattr(book, k, v)
    db.commit()
    db.refresh(book)
    return book


@router.delete("/books/{book_id}", dependencies=[Depends(require_admin)])
def delete_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(Book).get(book_id)
    if not book:
        raise HTTPException(404, "Book not found")
    db.delete(book)
    db.commit()
    return {"deleted": book_id}


# ---- AGENT TOOL surface ----
def tool_search_library(db: Session, query: str) -> str:
    """Natural-language entry point the AI agent calls for any library question."""
    books = _search_books(db, query)
    if not books:
        return f"No books found matching '{query}'."
    # bump request_count for "most requested books" analytics
    for b in books[:5]:
        b.request_count = (b.request_count or 0) + 1
    db.commit()
    lines = []
    for b in books[:5]:
        status = f"{b.available_copies}/{b.total_copies} available" if b.available else "currently checked out"
        lines.append(f"• \"{b.title}\" by {b.author or 'Unknown'} — {status} ({b.category or 'General'})")
    return "Library results:\n" + "\n".join(lines)
