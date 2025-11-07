"""AI Agent Backend - FastAPI Application"""
import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from ai_integrations import AIRouter
from fastapi import Request

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
@app.post('/chat', response_model=ChatResponse)
@app.post('/api/chat', response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        # Generate AI response using AIRouter (multi-platform intelligent routing)
        router = AIRouter()
        ai_result = await router.generate_text(request.message)
        
        if ai_result['success']:
            response_text = ai_result['text']
        else:
            response_text = f"Error generating response: {ai_result.get('error', 'Unknown error')}"
        
        session_id = request.session_id or 'default_session'
        
        return ChatResponse(response=response_text, session_id=session_id)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    # Endpoint para WordPress plugin compatibility
@app.post('/api/agent/execute', response_model=ChatResponse)
async def agent_execute(request: Request):
    """Endpoint compatible con el plugin de WordPress que acepta command/user_id"""
    try:
        # Obtener el body de la petición
        body = await request.json()
        
        # Soportar ambos formatos: {message, session_id} y {command, user_id}
        message_text = body.get('message') or body.get('command', '')
        session_id = body.get('session_id') or body.get('user_id', 'default_session')
        
        if not message_text:
            raise HTTPException(status_code=400, detail="Missing message or command")
        
        # Crear el objeto ChatRequest con el formato correcto
        chat_request = ChatRequest(message=message_text, session_id=session_id)
        
        # Llamar a la función chat existente
        return await chat(chat_request)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
