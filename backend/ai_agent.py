"""AI Agent Backend - FastAPI Application"""

import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import uvicorn

# Initialize FastAPI app
app = FastAPI(
    title="AI Agent Backend",
    description="Backend API for AI Agent Chat",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request models
class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None

class UploadRequest(BaseModel):
    file_url: str
    session_id: Optional[str] = None

# Health check endpoint
@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy",
        "message": "Backend conectado"
    }

# Chat endpoint
@app.post("/api/chat")
async def chat(request: ChatRequest):
    try:
        # Simple echo response for now
        return {
            "response": f"Recibí tu mensaje: {request.message}",
            "session_id": request.session_id or "default"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Upload endpoint
@app.post("/api/upload")
async def upload_file(request: UploadRequest):
    try:
        return {
            "status": "success",
            "message": "Archivo recibido",
            "file_url": request.file_url
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "AI Agent Backend is running",
        "endpoints": [
            "/api/health",
            "/api/chat",
            "/api/upload"
        ]
    }
