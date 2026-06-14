"""Academics MCP Server — notices, exam schedule, attendance rules.

Some academic facts (attendance %, grading policy) are semi-static rules. The
agent answers those either from this service or, when a deeper policy document
has been uploaded, from the RAG layer (search_documents).
"""
from fastapi import APIRouter, Depends
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.auth.security import require_admin
from app.database import get_db
from app.models import AcademicNotice
from app.search_utils import keywords
from app.schemas import NoticeCreate, NoticeOut

router = APIRouter(prefix="/academics", tags=["Academics MCP"])

# Static institutional rules. In production these would live in config/CMS.
ATTENDANCE_RULES = {
    "minimum_attendance_percent": 75,
    "detained_below_percent": 60,
    "medical_leave_buffer_percent": 10,
    "summary": (
        "Students must maintain at least 75% attendance per course. Falling below "
        "60% results in being detained from the end-semester exam. A medical leave "
        "buffer of 10% may be granted with valid documentation."
    ),
}

EXAM_SCHEDULE = [
    {"course": "DBMS", "type": "Mid-Sem", "date": "2026-07-02", "time": "10:00 AM", "venue": "Hall A"},
    {"course": "Operating Systems", "type": "Mid-Sem", "date": "2026-07-04", "time": "10:00 AM", "venue": "Hall B"},
    {"course": "Computer Networks", "type": "Mid-Sem", "date": "2026-07-06", "time": "02:00 PM", "venue": "Hall A"},
]


def _search_notices(db: Session, q: str | None = None):
    query = db.query(AcademicNotice)
    kws = keywords(q)
    if kws:
        conds = []
        for k in kws:
            like = f"%{k}%"
            conds += [AcademicNotice.title.ilike(like), AcademicNotice.body.ilike(like)]
        query = query.filter(or_(*conds))
    return query.order_by(AcademicNotice.published_at.desc()).all()


@router.get("/notices", response_model=list[NoticeOut])
def list_notices(q: str | None = None, db: Session = Depends(get_db)):
    return _search_notices(db, q)


@router.post("/notices", response_model=NoticeOut, dependencies=[Depends(require_admin)])
def create_notice(payload: NoticeCreate, db: Session = Depends(get_db)):
    notice = AcademicNotice(**payload.model_dump())
    db.add(notice)
    db.commit()
    db.refresh(notice)
    return notice


@router.get("/exam-schedule")
def exam_schedule():
    return {"exams": EXAM_SCHEDULE}


@router.get("/attendance-rules")
def attendance_rules():
    return ATTENDANCE_RULES


def tool_search_academics(db: Session, query: str) -> str:
    """Agent entry point for academic questions."""
    q = query.lower()
    if "attend" in q:
        return ATTENDANCE_RULES["summary"]
    if "exam" in q or "schedule" in q:
        lines = [f"• {e['course']} {e['type']} — {e['date']} {e['time']} @ {e['venue']}" for e in EXAM_SCHEDULE]
        return "Exam schedule:\n" + "\n".join(lines)
    notices = _search_notices(db, query if query.strip() else None)
    if not notices:
        return "No academic notices found."
    lines = [f"• [{n.category}] {n.title} — {n.published_at:%d %b}" for n in notices[:6]]
    return "Academic notices:\n" + "\n".join(lines)
