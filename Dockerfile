# Production Multi-Stage Dockerfile for Academic RAG System

# Stage 1: Build Frontend (React + Vite)
FROM node:20-alpine AS frontend-builder
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm ci
COPY frontend/ ./
RUN npm run build

# Stage 2: Python 3.11 FastAPI Backend
FROM python:3.11-slim AS backend
WORKDIR /app

# Install system dependencies for PyMuPDF & PyTorch
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt-get/lists/*

# Install Python Dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy Project Files
COPY . .

# Copy Built Frontend to static serving location if needed
COPY --from=frontend-builder /app/frontend/dist ./frontend/dist

# Expose FastAPI Port
EXPOSE 8000

# Environment variables
ENV PYTHONUNBUFFERED=1
ENV PORT=8000

# Run FastAPI with Uvicorn
CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
