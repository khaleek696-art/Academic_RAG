import os
import shutil
from pathlib import Path
from typing import List
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, status
from sqlalchemy.orm import Session
from backend.app.db.session import get_db
from backend.app.db.models import Subject, Document, Chunk
from backend.app.schemas import DocumentResponse, ChunkResponse
from backend.app.config import settings
from backend.app.services.ingestion import ingestion_service

router = APIRouter(prefix="/documents", tags=["Documents"])

MAX_FILE_SIZE = 25 * 1024 * 1024  # 25 MB Limit

@router.post("", response_model=DocumentResponse, status_code=status.HTTP_201_CREATED)
async def upload_document(
    subject_id: int = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    subject = db.query(Subject).filter(Subject.id == subject_id).first()
    if not subject:
        raise HTTPException(status_code=404, detail=f"Subject ID {subject_id} not found.")

    # 1. Sanitize Filename (Path Traversal Prevention)
    clean_filename = os.path.basename(file.filename)
    if not clean_filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Security Warning: Only PDF files (.pdf) are permitted.")

    # 2. File Size Validation (DoS Prevention)
    contents = await file.read()
    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(status_code=413, detail="File too large. Maximum permitted PDF size is 25 MB.")

    upload_dir = Path(settings.UPLOAD_DIR)
    upload_dir.mkdir(parents=True, exist_ok=True)
    file_path = upload_dir / clean_filename

    with open(file_path, "wb") as buffer:
        buffer.write(contents)

    # 3. Create Document Record in DB
    doc = Document(subject_id=subject_id, filename=clean_filename, pages=0)
    db.add(doc)
    db.commit()
    db.refresh(doc)

    # 4. Run Full Ingestion (Parse -> Chunk -> SQLite -> Qdrant -> BM25)
    ingest_result = ingestion_service.process_pdf(
        file_path=str(file_path),
        document_id=doc.id,
        subject_id=subject_id,
        filename=clean_filename,
        db=db
    )

    doc.pages = ingest_result["total_pages"]
    db.commit()

    return DocumentResponse(
        id=doc.id,
        subject_id=doc.subject_id,
        filename=doc.filename,
        pages=doc.pages,
        indexed_at=doc.indexed_at,
        chunks_count=ingest_result["chunks_count"]
    )

@router.get("/{document_id}/chunks", response_model=List[ChunkResponse])
def get_document_chunks(document_id: int, db: Session = Depends(get_db)):
    doc = db.query(Document).filter(Document.id == document_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found.")
    return db.query(Chunk).filter(Chunk.document_id == document_id).all()
