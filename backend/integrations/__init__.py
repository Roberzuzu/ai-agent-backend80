"""
Super Cerebro AI Backend v2.0 - FASE 1
Solo PostgreSQL (sin R2 todavía)

Features:
- PostgreSQL para conversaciones y prompts
- Múltiples AIs (Perplexity, OpenAI, Anthropic)
- Sistema de prompts personalizados
- Memoria persistente
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import os
import httpx
import asyncpg
from datetime import datetime
import json

# ============================================
# CONFIGURACIÓN
# ============================================

app = FastAPI(title="Super Cerebro AI v2.0 - FASE 1")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Variables de entorno
DATABASE_URL = os.getenv("DATABASE_URL")
PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
BACKEND_API_KEY = os.getenv("BACKEND_API_KEY")

# Pool de conexiones global
db_pool = None

# ============================================
# MODELOS
# ============================================

class ChatRequest(BaseModel):
    message: str
    user_id: str = "default_user"
    conversation_id: Optional[str] = None
    prompt_id: Optional[str] = None

class PromptRequest(BaseModel):
    name: str
    content: str
    category: Optional[str] = "general"

# ============================================
# DATABASE
# ============================================

async def get_db_pool():
    """Obtener pool de conexiones"""
    global db_pool
    if db_pool is None:
        db_pool = await asyncpg.create_pool(DATABASE_URL, min_size=1, max_size=10)
    return db_pool

async def init_database():
    """Inicializar tablas"""
    if not DATABASE_URL:
        print("⚠️ DATABASE_URL no configurada")
        return
    
    try:
        pool = await get_db_pool()
        
        async with pool.acquire() as conn:
            # Tabla de conversaciones
            await conn.execute('''
                CREATE TABLE IF NOT EXISTS conversations (
                    id SERIAL PRIMARY KEY,
                    conversation_id VARCHAR(255) UNIQUE NOT NULL,
                    user_id VARCHAR(255) NOT NULL,
                    created_at TIMESTAMP DEFAULT NOW(),
                    updated_at TIMESTAMP DEFAULT NOW()
                )
            ''')
            
            # Tabla de mensajes
            await conn.execute('''
                CREATE TABLE IF NOT EXISTS messages (
                    id SERIAL PRIMARY KEY,
                    conversation_id VARCHAR(255) NOT NULL,
                    role VARCHAR(50) NOT NULL,
                    content TEXT NOT NULL,
                    ai_provider VARCHAR(50),
                    prompt_used VARCHAR(255),
                    created_at TIMESTAMP DEFAULT NOW()
                )
            ''')
            
            # Tabla de prompts
            await conn.execute('''
                CREATE TABLE IF NOT EXISTS prompts (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(255) UNIQUE NOT NULL,
                    content TEXT NOT NULL,
                    category VARCHAR(100),
                    is_active BOOLEAN DEFAULT TRUE,
                    usage_count INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT NOW()
                )
            ''')
            
            # Insertar prompts predefinidos
            prompts = [
                ('experto_ecommerce', 'Eres un experto en comercio electrónico, WooCommerce, SEO y estrategias de venta. Analizas tiendas online, optimizas productos y aumentas ventas. Das consejos específicos y accionables.', 'ecommerce'),
                ('analista_productos', 'Eres un analista experto en investigación de productos, análisis de mercado, precios competitivos y tendencias. Encuentras oportunidades de negocio y productos ganadores.', 'productos'),
                ('copywriter', 'Eres un copywriter profesional especializado en ecommerce. Creas descripciones de productos que venden, títulos atractivos y contenido persuasivo que convierte visitantes en clientes.', 'contenido'),
                ('seo_expert', 'Eres un experto en SEO y posicionamiento web. Optimizas contenido para buscadores, investigas keywords rentables y mejoras la visibilidad online de tiendas.', 'seo')
            ]
            
            for name, content, category in prompts:
                try:
                    await conn.execute(
                        'INSERT INTO prompts (name, content, category) VALUES ($1, $2, $3) ON CONFLICT (name) DO NOTHING',
                        name, content, category
                    )
                except:
                    pass
        
        print("✅ Base de datos inicializada correctamente")
        print("✅ 4 prompts predefinidos cargados")
        
    except Exception as e:
        print(f"❌ Error inicializando BD: {e}")

# ============================================
# AI PROVIDERS
# ============================================

async def call_perplexity(message: str, system_prompt: str = None) -> dict:
    """Llamar a Perplexity AI"""
    if not PERPLEXITY_API_KEY:
        return {"success": False, "error": "Perplexity API key not configured"}
    
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": message})
    
    async with httpx.AsyncClient(timeout=60.0) as client:
        try:
            response = await client.post(
                "https://api.perplexity.ai/chat/completions",
                headers={
                    "Authorization": f"Bearer {PERPLEXITY_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "sonar-pro",
                    "messages": messages,
                    "max_tokens": 2000,
                    "temperature": 0.7
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "success": True,
                    "content": data["choices"][0]["message"]["content"],
                    "provider": "perplexity"
                }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    return {"success": False, "error": "Perplexity request failed"}

async def call_openai(message: str, system_prompt: str = None) -> dict:
    """Llamar a OpenAI"""
    if not OPENAI_API_KEY:
        return {"success": False, "error": "OpenAI API key not configured"}
    
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": message})
    
    async with httpx.AsyncClient(timeout=60.0) as client:
        try:
            response = await client.post(
                "https://api.openai.com/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {OPENAI_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "gpt-4o",
                    "messages": messages,
                    "max_tokens": 2000,
                    "temperature": 0.7
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "success": True,
                    "content": data["choices"][0]["message"]["content"],
                    "provider": "openai"
                }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    return {"success": False, "error": "OpenAI request failed"}

async def call_anthropic(message: str, system_prompt: str = None) -> dict:
    """Llamar a Anthropic Claude"""
    if not ANTHROPIC_API_KEY:
        return {"success": False, "error": "Anthropic API key not configured"}
    
    async with httpx.AsyncClient(timeout=60.0) as client:
        try:
            payload = {
                "model": "claude-3-5-sonnet-20241022",
                "max_tokens": 2000,
                "messages": [{"role": "user", "content": message}]
            }
            
            if system_prompt:
                payload["system"] = system_prompt
            
            response = await client.post(
                "https://api.anthropic.com/v1/messages",
                headers={
                    "x-api-key": ANTHROPIC_API_KEY,
                    "anthropic-version": "2023-06-01",
                    "Content-Type": "application/json"
                },
                json=payload
            )
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "success": True,
                    "content": data["content"][0]["text"],
                    "provider": "anthropic"
                }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    return {"success": False, "error": "Anthropic request failed"}

async def process_with_ai(message: str, system_prompt: str = None) -> dict:
    """Procesar con múltiples AIs en cascada"""
    
    # 1. Intentar Perplexity
    result = await call_perplexity(message, system_prompt)
    if result["success"]:
        return result
    
    # 2. Intentar OpenAI
    result = await call_openai(message, system_prompt)
    if result["success"]:
        return result
    
    # 3. Intentar Anthropic
    result = await call_anthropic(message, system_prompt)
    if result["success"]:
        return result
    
    return {"success": False, "error": "All AI providers failed"}

# ============================================
# ENDPOINTS
# ============================================

@app.on_event("startup")
async def startup():
    """Inicializar al arrancar"""
    await init_database()

@app.get("/")
async def root():
    return {
        "service": "Super Cerebro AI Backend v2.0 - FASE 1",
        "status": "operational",
        "version": "2.0.0-phase1",
        "features": [
            "PostgreSQL database",
            "Multiple AI providers",
            "Custom prompts",
            "Persistent memory"
        ]
    }

@app.get("/health")
async def health():
    db_status = "connected" if DATABASE_URL else "not configured"
    
    # Test DB connection
    if DATABASE_URL:
        try:
            pool = await get_db_pool()
            async with pool.acquire() as conn:
                await conn.fetchval("SELECT 1")
            db_status = "connected"
        except:
            db_status = "error"
    
    return {
        "status": "healthy",
        "database": db_status,
        "ai_providers": {
            "perplexity": bool(PERPLEXITY_API_KEY),
            "openai": bool(OPENAI_API_KEY),
            "anthropic": bool(ANTHROPIC_API_KEY)
        }
    }

@app.post("/api/chat")
async def chat(request: ChatRequest):
    """Endpoint principal de chat con memoria"""
    
    if not DATABASE_URL:
        # Fallback sin BD
        ai_result = await process_with_ai(request.message)
        if ai_result["success"]:
            return {
                "success": True,
                "response": ai_result["content"],
                "ai_provider": ai_result["provider"],
                "note": "Running without database"
            }
        else:
            raise HTTPException(status_code=500, detail=ai_result["error"])
    
    pool = await get_db_pool()
    
    try:
        async with pool.acquire() as conn:
            # Obtener prompt si se especificó
            system_prompt = None
            if request.prompt_id:
                prompt = await conn.fetchrow(
                    "SELECT content FROM prompts WHERE name = $1 AND is_active = TRUE",
                    request.prompt_id
                )
                if prompt:
                    system_prompt = prompt['content']
                    await conn.execute(
                        "UPDATE prompts SET usage_count = usage_count + 1 WHERE name = $1",
                        request.prompt_id
                    )
            
            # Crear conversación si no existe
            if not request.conversation_id:
                request.conversation_id = f"conv_{int(datetime.now().timestamp())}"
                await conn.execute(
                    "INSERT INTO conversations (conversation_id, user_id) VALUES ($1, $2)",
                    request.conversation_id, request.user_id
                )
            
            # Guardar mensaje del usuario
            await conn.execute(
                "INSERT INTO messages (conversation_id, role, content) VALUES ($1, $2, $3)",
                request.conversation_id, "user", request.message
            )
            
            # Procesar con AI
            ai_result = await process_with_ai(request.message, system_prompt)
            
            if ai_result["success"]:
                # Guardar respuesta del asistente
                await conn.execute(
                    """INSERT INTO messages (conversation_id, role, content, ai_provider, prompt_used) 
                       VALUES ($1, $2, $3, $4, $5)""",
                    request.conversation_id, "assistant", ai_result["content"], 
                    ai_result["provider"], request.prompt_id
                )
                
                return {
                    "success": True,
                    "response": ai_result["content"],
                    "ai_provider": ai_result["provider"],
                    "conversation_id": request.conversation_id,
                    "prompt_used": request.prompt_id
                }
            else:
                raise HTTPException(status_code=500, detail=ai_result["error"])
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/prompts")
async def get_prompts():
    """Obtener lista de prompts"""
    if not DATABASE_URL:
        return {"success": False, "error": "Database not configured"}
    
    pool = await get_db_pool()
    
    async with pool.acquire() as conn:
        prompts = await conn.fetch(
            "SELECT id, name, content, category, usage_count FROM prompts WHERE is_active = TRUE ORDER BY usage_count DESC"
        )
    
    return {
        "success": True,
        "prompts": [dict(p) for p in prompts]
    }

@app.get("/api/conversations/{user_id}")
async def get_conversations(user_id: str):
    """Obtener historial de conversaciones"""
    if not DATABASE_URL:
        return {"success": False, "error": "Database not configured"}
    
    pool = await get_db_pool()
    
    async with pool.acquire() as conn:
        conversations = await conn.fetch(
            """SELECT c.conversation_id, c.created_at, COUNT(m.id) as message_count
               FROM conversations c
               LEFT JOIN messages m ON c.conversation_id = m.conversation_id
               WHERE c.user_id = $1
               GROUP BY c.conversation_id, c.created_at
               ORDER BY c.created_at DESC
               LIMIT 20""",
            user_id
        )
    
    return {
        "success": True,
        "conversations": [dict(c) for c in conversations]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
"""
Integrations package
FAL AI, WooCommerce, Dropshipping automation
"""
from .fal_ai import FALAIClient, get_fal_client
from .woocommerce import WooCommerceClient, get_woo_client, ProductContentGenerator
from .dropshipping_pricing import DropshippingPriceCalculator, calculate_price, calculate_bulk
from .automated_dropshipping import AutomatedDropshippingSystem, create_dropshipping_system

__all__ = [
    'FALAIClient',
    'get_fal_client',
    'WooCommerceClient',
    'get_woo_client',
    'ProductContentGenerator',
    'DropshippingPriceCalculator',
    'calculate_price',
    'calculate_bulk',
    'AutomatedDropshippingSystem',
    'create_dropshipping_system',
]
