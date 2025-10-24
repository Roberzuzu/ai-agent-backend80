"""AI Agent Backend - FastAPI Application"""
import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from ai_integrations import AIRouter

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
        # Generate AI response using AIRouter (multi-platform intelligent routing)
        router = AIRouter()
        ai_result = await router.generate_text(request.message)
        
        if ai_result["success"]:
            response_text = ai_result["text"]
        else:
            response_text = f"Error generating response: {ai_result.get('error', 'Unknown error')}"
        
        session_id = request.session_id or "default_session"
        
        return ChatResponse(response=response_text, session_id=session_id)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
