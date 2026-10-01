import html
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.app.db.session import get_db
from backend.app.db.models import Chat, Subject
from backend.app.schemas import AskRequest, AskResponse, Citation
from backend.app.services.answer_generator import answer_generator

router = APIRouter(prefix="/ask", tags=["Question Answering"])

MAX_QUERY_LENGTH = 1500

@router.post("", response_model=AskResponse)
def ask_question(payload: AskRequest, db: Session = Depends(get_db)):
    # 1. Input Sanitization & Length Check
    clean_question = payload.question.strip()
    if len(clean_question) > MAX_QUERY_LENGTH:
        raise HTTPException(status_code=400, detail=f"Question exceeds maximum limit of {MAX_QUERY_LENGTH} characters.")

    # Escape raw HTML tags to prevent XSS injection
    sanitized_question = html.escape(clean_question)

    if payload.subject_id:
        subj = db.query(Subject).filter(Subject.id == payload.subject_id).first()
        if not subj:
            raise HTTPException(status_code=404, detail=f"Subject ID {payload.subject_id} not found.")

    # 2. Execute Hybrid RAG Pipeline (BM25 + Qdrant + RRF + Reranker + Gate + LLM + Verifier)
    result = answer_generator.generate_answer(
        question=sanitized_question,
        subject_id=payload.subject_id,
        mode=payload.mode or "detailed"
    )

    citations_data = [
        Citation(
            document_name=c.get("document_name") or c.get("filename") or "Textbook.pdf",
            page_number=c.get("page_number") or c.get("page") or 1,
            filename=c.get("document_name") or c.get("filename") or "Textbook.pdf",
            page=c.get("page_number") or c.get("page") or 1,
            snippet=c.get("snippet") or c.get("text") or ""
        )
        for c in result.get("citations", [])
    ]

    chat = Chat(
        subject_id=payload.subject_id,
        question=sanitized_question,
        answer=result["answer"],
        citations_json=[c.dict() for c in citations_data],
        confidence=result["confidence"]
    )
    db.add(chat)
    db.commit()
    db.refresh(chat)

    return AskResponse(
        answer=result["answer"],
        citations=citations_data,
        confidence=result["confidence"],
        message_id=chat.id,
        refused=result["refused"]
    )

@router.get("/history")
def get_chat_history(db: Session = Depends(get_db)):
    chats = db.query(Chat).order_by(Chat.created_at.desc()).limit(20).all()
    return [
        {
            "id": c.id,
            "question": c.question,
            "answer": c.answer,
            "confidence": c.confidence,
            "created_at": c.created_at.isoformat() if c.created_at else None,
            "subject_id": c.subject_id
        }
        for c in chats
    ]

