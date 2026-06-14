"""Chat router: agent endpoint + persisted chat history."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import ChatHistory
from app.schemas import ChatHistoryOut, ChatRequest, ChatResponse
from app.services.agent_service import run_agent

router = APIRouter(prefix="/chat", tags=["Chat"])


@router.post("", response_model=ChatResponse)
def chat(payload: ChatRequest, db: Session = Depends(get_db)):
    result = run_agent(payload.message, db)
    if payload.student_id:
        db.add(ChatHistory(student_id=payload.student_id, role="user", content=payload.message))
        db.add(ChatHistory(
            student_id=payload.student_id, role="assistant",
            content=result["answer"], tool_used=result.get("tool_used"),
        ))
        db.commit()
    return ChatResponse(**result)


@router.get("/history/{student_id}", response_model=list[ChatHistoryOut])
def history(student_id: int, db: Session = Depends(get_db)):
    return (
        db.query(ChatHistory)
        .filter(ChatHistory.student_id == student_id)
        .order_by(ChatHistory.created_at)
        .all()
    )
