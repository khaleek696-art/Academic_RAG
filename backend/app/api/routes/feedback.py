from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.app.db.session import get_db
from backend.app.db.models import Feedback, Chat
from backend.app.schemas import FeedbackCreate, FeedbackResponse

router = APIRouter(prefix="/feedback", tags=["Feedback"])

@router.post("", response_model=FeedbackResponse, status_code=status.HTTP_201_CREATED)
def submit_feedback(payload: FeedbackCreate, db: Session = Depends(get_db)):
    chat = db.query(Chat).filter(Chat.id == payload.message_id).first()
    if not chat:
        raise HTTPException(status_code=404, detail=f"Message ID {payload.message_id} not found.")

    existing = db.query(Feedback).filter(Feedback.message_id == payload.message_id).first()
    if existing:
        existing.helpful = payload.helpful
        existing.comment = payload.comment
        db.commit()
        db.refresh(existing)
        return existing

    feedback = Feedback(
        message_id=payload.message_id,
        helpful=payload.helpful,
        comment=payload.comment
    )
    db.add(feedback)
    db.commit()
    db.refresh(feedback)
    return feedback
