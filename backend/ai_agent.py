"""
AI Agent Backend - FastAPI Application OMNICANAL SUPER CEREBRO
Potenciado para:
- Multi-modalidad y expansión arbitraria de capacidades vía prompts
- Integración directa/segura con https://ai-agent-backend80.onrender.com y otros servicios/funcionales
- Preparado para plugins, memoria extendida, mando de accesorios y gestión de contexto
"""

import os
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any
from ai_integrations import AIRouter  # Mantener la integración base

# ====================================
# Inicialización avanzada del backend
# ====================================

app = FastAPI(
    title="AI Agent Backend Omnicanal",
    description="Backend API para Agente AI Omnicanal potenciado y preparado para expansión dinámica",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =====================
# Modelos de request/response
# =====================

class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None
    # Soporte para modo/contexto y prompts avanzados
    mode: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

class UploadRequest(BaseModel):
    file_url: str

class ChatResponse(BaseModel):
    response: str
    session_id: str
    mode: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

# ====================
# Endpoints principales
# ====================

@app.get("/health")
@app.get("/api/health")
async def health_check():
    # Health monitor, puede ampliarse para más diagnósticos
    return {
        "status": "healthy",
        "message": "AI Agent Backend Omnicanal is running",
        "version": app.version,
        "backend_url": "https://ai-agent-backend80.onrender.com"
    }

@app.get("/")
async def root():
    return {
        "message": "AI Agent Backend Omnicanal API",
        "version": app.version,
        "info": "Potenciado, modular y listo para integración y expansión dinánica."
    }

@app.post("/chat", response_model=ChatResponse)
@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        # Routing inteligente multi-modal y modo/contexto
        router = AIRouter()
        mode = request.mode or "default"
        metadata = request.metadata or {}

        # Expansión: permite prompts con capacidades arbitrarias
        ai_result = await router.generate_text(
            request.message,
            mode=mode,
            metadata=metadata
        )

        # Compatibilidad con respuesta enriquecida
        response_text = ai_result.get('text', '')
        success = ai_result.get('success', False)
        error_str = ai_result.get('error', '')
        session_id = request.session_id or 'default_session'

        if not success:
            response_text = f"Error generating response: {error_str or 'Unknown error'}"

        # Ideal para extensibilidad/futuras mejoras
        return ChatResponse(
            response=response_text,
            session_id=session_id,
            mode=mode,
            metadata=metadata
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ==========================
# Endpoints de expansión y utilidades
# ==========================

@app.post("/upload", response_model=Dict[str, Any])
async def upload(request: UploadRequest):
    # Ejemplo: integración con procesamiento de archivos occidental, plugins, etc.
    file_url = request.file_url
    # Aquí añadir lógica de integración real con backend, plugins y memoria
    return {
        "status": "pong",
        "file_url": file_url,
        "info": "Archivo recibido. Procesamiento pendiente según configuración de plugins."
    }

@app.get("/endpoints")
async def list_endpoints():
    # Para auditoría y autoexpansión
    endpoints = [route.path for route in app.routes]
    return {"available_endpoints": endpoints}

# =================
# Hooks de expansión y autoadaptación futura
# =================
# Puede ampliarse con:
# - Endpoints de plugins/accesorios
# - Gestión avanzada de memoria/contexto y roles
# - Interfaz para prompts y modos extendidos
# - Integración directa con https://ai-agent-backend80.onrender.com para ejecución de herramientas y comandos

