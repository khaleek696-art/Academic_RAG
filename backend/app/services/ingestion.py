import os
from pathlib import Path
from typing import Dict, Any, List
from sqlalchemy.orm import Session
from pypdf import PdfReader
from backend.app.db.models import Document, Chunk
from backend.app.services.chunker import chunker
from backend.app.services.vector_index import qdrant_service
from backend.app.services.bm25_index import bm25_service

class IngestionService:
    """Orchestrates PDF text extraction, chunking, SQLite persistence, Qdrant vector indexing, and BM25 indexing."""

    def process_pdf(self, file_path: str, document_id: int, subject_id: int, filename: str, db: Session) -> Dict[str, Any]:
        reader = PdfReader(file_path)
        pages_data = []

        for i, page in enumerate(reader.pages):
            text = page.extract_text() or ""
            pages_data.append({"page": i + 1, "text": text})

        # 1. Chunk pages
        chunk_dicts = chunker.chunk_pages(pages_data, document_id, subject_id, filename)

        # 2. Persist chunks in SQLite
        db_chunks = []
        for c in chunk_dicts:
            chunk_obj = Chunk(
                document_id=document_id,
                page=c["page"],
                text=c["text"],
                embedding_ref=f"qdrant_{document_id}_{c['chunk_index']}"
            )
            db.add(chunk_obj)
            db_chunks.append(chunk_obj)
        
        db.commit()

        # Update chunk_dicts with SQLite IDs
        for idx, chunk_obj in enumerate(db_chunks):
            chunk_dicts[idx]["id"] = chunk_obj.id

        # 3. Index in Qdrant Vector Store
        qdrant_service.add_chunks(chunk_dicts)

        # 4. Update BM25 Index
        all_chunks = db.query(Chunk).all()
        formatted_chunks = []
        for chunk in all_chunks:
            doc = db.query(Document).filter(Document.id == chunk.document_id).first()
            formatted_chunks.append({
                "id": chunk.id,
                "document_id": chunk.document_id,
                "subject_id": doc.subject_id if doc else subject_id,
                "filename": doc.filename if doc else filename,
                "page": chunk.page,
                "text": chunk.text
            })
        bm25_service.build_index(formatted_chunks)

        return {
            "document_id": document_id,
            "filename": filename,
            "total_pages": len(pages_data),
            "chunks_count": len(chunk_dicts)
        }

ingestion_service = IngestionService()
