from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.config import settings, ensure_directories
from backend.app.db.session import engine, Base
from backend.app.api.routes import subjects, documents, qa, feedback, eval

# Create database tables automatically on startup
ensure_directories()
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Academic QA RAG System API",
    description="Backend API & SQLite Database for Academic Question Answering System Using RAG",
    version="1.0.0"
)

# Enable CORS for Streamlit / React frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(subjects.router)
app.include_router(documents.router)
app.include_router(qa.router)
app.include_router(feedback.router)
app.include_router(eval.router)

@app.get("/", tags=["Health Check"])
def root():
    return {
        "status": "online",
        "message": "Academic QA RAG System Backend & Database are active.",
        "docs_url": "/docs"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.app.main:app", host="0.0.0.0", port=8000, reload=True)
