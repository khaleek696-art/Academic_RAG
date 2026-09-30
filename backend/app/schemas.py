from datetime import datetime
from typing import List, Optional, Any
from pydantic import BaseModel, Field

# Subject Schemas
class SubjectCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255, description="Name of the academic subject")

class SubjectResponse(BaseModel):
    id: int
    name: str
    created_at: datetime

    class Config:
        from_attributes = True

# Document & Chunk Schemas
class ChunkResponse(BaseModel):
    id: int
    document_id: int
    page: int
    text: str
    embedding_ref: Optional[str] = None

    class Config:
        from_attributes = True

class DocumentResponse(BaseModel):
    id: int
    subject_id: int
    filename: str
    pages: int
    indexed_at: datetime
    chunks_count: Optional[int] = 0

    class Config:
        from_attributes = True

# Question Answering Schemas
class AskRequest(BaseModel):
    question: str = Field(..., min_length=1, description="Student question")
    subject_id: Optional[int] = Field(None, description="Optional subject filter ID")
    mode: Optional[str] = Field("detailed", description="Answer mode: short, detailed, exam")
    chat_history: Optional[List[dict]] = Field(default_factory=list, description="Previous messages")

class Citation(BaseModel):
    document_name: str
    page_number: int
    snippet: Optional[str] = None

class AskResponse(BaseModel):
    answer: str
    citations: List[Citation]
    confidence: float
    message_id: Optional[int] = None
    refused: bool = False

# Feedback Schemas
class FeedbackCreate(BaseModel):
    message_id: int
    helpful: bool
    comment: Optional[str] = None

class FeedbackResponse(BaseModel):
    id: int
    message_id: int
    helpful: bool
    comment: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True

# Evaluation Schemas
class EvalResponse(BaseModel):
    total_questions: int
    recall_at_5: float
    faithfulness_score: float
    correct_refusal_rate: float
