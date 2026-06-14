"""Events MCP Server — campus events, with search and upcoming filter."""
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.auth.security import require_admin
from app.database import get_db
from app.models import Event
from app.search_utils import keywords
from app.schemas import EventCreate, EventOut

router = APIRouter(prefix="/events", tags=["Events MCP"])


def _search_events(db: Session, q: str | None = None, upcoming_only: bool = True):
    query = db.query(Event)
    if upcoming_only:
        query = query.filter(Event.starts_at >= datetime.utcnow())
    kws = keywords(q)
    if kws:
        conds = []
        for k in kws:
            like = f"%{k}%"
            conds += [Event.title.ilike(like), Event.description.ilike(like), Event.category.ilike(like)]
        query = query.filter(or_(*conds))
    return query.order_by(Event.starts_at).all()


@router.get("", response_model=list[EventOut])
def list_events(q: str | None = None, upcoming: bool = True, db: Session = Depends(get_db)):
    return _search_events(db, q, upcoming)


@router.get("/{event_id}", response_model=EventOut)
def get_event(event_id: int, db: Session = Depends(get_db)):
    event = db.query(Event).get(event_id)
    if not event:
        raise HTTPException(404, "Event not found")
    return event


@router.post("", response_model=EventOut, dependencies=[Depends(require_admin)])
def create_event(payload: EventCreate, db: Session = Depends(get_db)):
    event = Event(**payload.model_dump())
    db.add(event)
    db.commit()
    db.refresh(event)
    return event


def tool_search_events(db: Session, query: str) -> str:
    """Agent entry point for event questions (defaults to upcoming)."""
    events = _search_events(db, query if query.strip() else None, upcoming_only=True)
    if not events:
        return "No upcoming events found."
    lines = [
        f"• {e.title} — {e.starts_at.strftime('%a %d %b, %I:%M %p')} @ {e.location or 'TBA'} ({e.category or 'General'})"
        for e in events[:6]
    ]
    return "Upcoming events:\n" + "\n".join(lines)
