from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Super Cerebro AI",
    description="AI-powered e-commerce automation backend",
    version="1.0.0"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request Models
class ChatMessage(BaseModel):
    message: str
    user_id: str = None

class HealthResponse(BaseModel):
    status: str
    service: str
    timestamp: str
    environment: dict

# Health Check
@app.get("/api/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint for monitoring"""
    return HealthResponse(
        status="ok",
        service="Super Cerebro AI Backend",
        timestamp=datetime.utcnow().isoformat(),
        environment={
            "python_version": "3.11",
            "fastapi": "active",
            "cors": "enabled"
        }
    )

# Chat Endpoint
@app.post("/api/chat")
async def chat(message: ChatMessage):
    """Chat endpoint for AI interactions"""
    logger.info(f"Chat request received: {message.message}")
    
    return {
        "response": f"Recibido: {message.message}. Backend operativo y listo para integraciones.",
        "status": "success",
        "timestamp": datetime.utcnow().isoformat(),
        "message_id": f"msg_{datetime.utcnow().timestamp()}"
    }

# Root endpoint
@app.get("/")
async def root():
    return {
        "service": "Super Cerebro AI",
        "status": "operational",
        "version": "1.0.0",
        "endpoints": [
            "/api/health",
            "/api/chat",
            "/docs"
        ]
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
