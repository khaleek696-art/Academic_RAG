from typing import List, Dict, Any
from backend.app.config import settings

class PageAwareChunker:
    """Splits document pages into retrievable text chunks preserving page numbers and document metadata."""

    def __init__(self, chunk_size: int = None, chunk_overlap: int = None):
        self.chunk_size = chunk_size or settings.CHUNK_SIZE
        self.chunk_overlap = chunk_overlap or settings.CHUNK_OVERLAP

    def chunk_pages(
        self,
        pages_data: List[Dict[str, Any]], # List of {"page": 1, "text": "..."}
        document_id: int,
        subject_id: int,
        filename: str
    ) -> List[Dict[str, Any]]:
        chunks = []
        global_chunk_idx = 0

        for p in pages_data:
            page_num = p["page"]
            text = p["text"].strip()
            if not text:
                continue

            # Recursive character splitting logic
            words = text.split()
            current_words = []
            current_len = 0

            for word in words:
                current_words.append(word)
                current_len += len(word) + 1

                if current_len >= self.chunk_size:
                    chunk_text = " ".join(current_words)
                    chunks.append({
                        "chunk_index": global_chunk_idx,
                        "document_id": document_id,
                        "subject_id": subject_id,
                        "filename": filename,
                        "page": page_num,
                        "text": chunk_text
                    })
                    global_chunk_idx += 1

                    # Keep overlap
                    overlap_words = current_words[-max(1, self.chunk_overlap // 10):]
                    current_words = list(overlap_words)
                    current_len = sum(len(w) + 1 for w in current_words)

            if current_words:
                chunk_text = " ".join(current_words)
                chunks.append({
                    "chunk_index": global_chunk_idx,
                    "document_id": document_id,
                    "subject_id": subject_id,
                    "filename": filename,
                    "page": page_num,
                    "text": chunk_text
                })
                global_chunk_idx += 1

        return chunks

chunker = PageAwareChunker()
