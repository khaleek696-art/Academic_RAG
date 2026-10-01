import logging
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from backend.app.config import settings, ensure_directories
from backend.app.db.session import engine, Base
from backend.app.api.routes import subjects, documents, qa, feedback, eval, auth

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

# Global Anti-Crash Exception Handler (Keeps Uvicorn Server 100% Online)
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logging.error(f"Unhandled exception caught on {request.url}: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "An unexpected server error occurred. The system is resilient and remains online."}
    )

# Include Routers
app.include_router(auth.router)
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
