"""Analytics router: aggregates for the admin charts (Recharts on the frontend)."""
from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Book, ChatHistory, Event, MenuItem

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("/overview")
def overview(db: Session = Depends(get_db)):
    return {
        "books_available": db.query(func.coalesce(func.sum(Book.available_copies), 0)).scalar(),
        "upcoming_events": db.query(Event).count(),
        "menu_items_today": db.query(MenuItem).count(),
        "total_queries": db.query(ChatHistory).filter(ChatHistory.role == "user").count(),
    }


@router.get("/most-requested-books")
def most_requested_books(db: Session = Depends(get_db)):
    rows = db.query(Book).order_by(Book.request_count.desc()).limit(5).all()
    return [{"name": b.title, "value": b.request_count or 0} for b in rows]


@router.get("/popular-queries")
def popular_queries(db: Session = Depends(get_db)):
    rows = (
        db.query(ChatHistory.tool_used, func.count(ChatHistory.id))
        .filter(ChatHistory.tool_used.isnot(None))
        .group_by(ChatHistory.tool_used)
        .all()
    )
    return [{"name": (t or "unknown").replace("search_", ""), "value": c} for t, c in rows]


@router.get("/menu-popularity")
def menu_popularity(db: Session = Depends(get_db)):
    rows = db.query(MenuItem).order_by(MenuItem.popularity.desc()).limit(6).all()
    return [{"name": m.name, "value": m.popularity or 0} for m in rows]


@router.get("/events-attendance")
def events_attendance(db: Session = Depends(get_db)):
    rows = db.query(Event).order_by(Event.attendance_count.desc()).limit(6).all()
    return [{"name": e.title, "value": e.attendance_count or 0} for e in rows]
