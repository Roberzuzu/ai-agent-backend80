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

# Response models
class ChatResponse(BaseModel):
    response: str
    session_id: str

# Health check endpoint
@app.get("/health")
@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "message": "AI Agent Backend is running"}

# Root endpoint
@app.get("/")
async def root():
    return {"message": "AI Agent Backend API", "version": "1.0.0"}

# Chat endpoint
@app.post("/chat", response_model=ChatResponse)
@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        # Simple echo response for now
        response_text = f"Received your message: {request.message}"
        session_id = request.session_id or "default_session"
        
        return ChatResponse(
            response=response_text,
            session_id=session_id
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Upload endpoint
@app.post("/upload")
@app.post("/api/upload")
async def upload_file(request: UploadRequest):
    try:
        return {
            "status": "success",
            "message": "File uploaded successfully",
            "file_url": request.file_url
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("ai_agent:app", host="0.0.0.0", port=port, reload=True)
