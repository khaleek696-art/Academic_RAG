from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.app.db.session import get_db
from backend.app.db.models import Chat, Subject
from backend.app.schemas import AskRequest, AskResponse, Citation
from backend.app.services.answer_generator import answer_generator

router = APIRouter(prefix="/ask", tags=["Question Answering"])

@router.post("", response_model=AskResponse)
def ask_question(payload: AskRequest, db: Session = Depends(get_db)):
    if payload.subject_id:
        subj = db.query(Subject).filter(Subject.id == payload.subject_id).first()
        if not subj:
            raise HTTPException(status_code=404, detail=f"Subject ID {payload.subject_id} not found.")

    # Execute Hybrid RAG Pipeline (BM25 + Qdrant + RRF + Reranker + Gate + LLM + Verifier)
    result = answer_generator.generate_answer(
        question=payload.question,
        subject_id=payload.subject_id,
        mode=payload.mode or "detailed"
    )

    citations_data = [
        Citation(
            document_name=c["document_name"],
            page_number=c["page_number"],
            snippet=c.get("snippet")
        )
        for c in result["citations"]
    ]

    chat = Chat(
        subject_id=payload.subject_id,
        question=payload.question,
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
