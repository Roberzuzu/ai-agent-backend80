"""
AI Integrations Module - OMNICANAL SUPER CEREBRO
Gestiona todas las integraciones con APIs de IA, accesorios, backend y herramientas extendidas.
Soporta expansión modular por prompt/capacidad, memoria extendida y multi-routing inteligente.
"""

import os
import asyncio
import httpx
import json
from typing import Dict, List, Optional, Any

# Importar clientes base y añadir nuevos según modularidad
from openai import AsyncOpenAI

# =========================
# Configuración de claves y endpoints
# =========================

FAL_KEY = os.getenv("FAL_API_KEY")
OPENROUTER_KEY = os.getenv("OPENROUTER_API_KEY")
PERPLEXITY_KEY = os.getenv("PERPLEXITY_API_KEY")
OPENAI_KEY = os.getenv("OPENAI_API_KEY")
ABACUS_KEY = os.getenv("ABACUS_API_KEY")

BACKEND_URL = os.getenv("AI_AGENT_BACKEND", "https://ai-agent-backend80.onrender.com")

# ===============================
# Cliente OpenRouter - LLM Routing
# ===============================

class OpenRouterClient:
    def __init__(self):
        self.apikey = OPENROUTER_KEY
        self.baseurl = "https://openrouter.ai/api/v1/chat/completions"

    async def generate_text(self, prompt: str, model: str = "anthropic/claude-3.5-sonnet", max_tokens: int = 2500, temperature: float = 0.7) -> Dict[str, Any]:
        if not self.apikey:
            return {"success": False, "error": "OPENROUTER_API_KEY not configured"}
        headers = {
            "Authorization": f"Bearer {self.apikey}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://herramientasyaccesorios.store",
            "X-Title": "Super Cerebro AI"
        }
        payload = {
            "model": model,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "max_tokens": max_tokens,
            "temperature": temperature
        }
        async with httpx.AsyncClient(timeout=60) as client:
            try:
                res = await client.post(self.baseurl, headers=headers, json=payload)
                data = res.json()
                content = data.get("choices", [{}])[0].get("message", {}).get("content")
                if content:
                    return {"success": True, "text": content, "model": data.get("model"), "usage": data.get("usage")}
                return {"success": False, "error": "Empty response from OpenRouter"}
            except Exception as e:
                return {"success": False, "error": str(e)}

# ==============================
# Cliente Perplexity - Search en tiempo real
# ==============================
class PerplexityClient:
    def __init__(self):
        self.apikey = PERPLEXITY_KEY
        self.baseurl = "https://api.perplexity.ai/chat/completions"

    async def search(self, prompt: str, model: str = "sonar", max_tokens: int = 1800) -> Dict[str, Any]:
        if not self.apikey:
            return {"success": False, "error": "PERPLEXITY_API_KEY not configured"}
        headers = {
            "Authorization": f"Bearer {self.apikey}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": "Eres un buscador experto que responde con precisión y citas."},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": max_tokens
        }
        async with httpx.AsyncClient(timeout=60) as client:
            try:
                res = await client.post(self.baseurl, headers=headers, json=payload)
                data = res.json()
                content = data.get("choices", [{}])[0].get("message", {}).get("content")
                citations = data.get("citations", [])
                if content:
                    return {"success": True, "content": content, "citations": citations}
                return {"success": False, "error": "Empty response from Perplexity"}
            except Exception as e:
                return {"success": False, "error": str(e)}

# ==============================
# Cliente OpenAI - para chat avanzado, plugins y memoria extendida
# ==============================
class OpenAIClient:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=OPENAI_KEY) if OPENAI_KEY else None

    async def chat(self, prompt: str, model: str = "gpt-4o-mini", max_tokens: int = 2000, temperature: float = 0.7) -> Dict[str, Any]:
        if not self.client:
            return {"success": False, "error": "OPENAI_API_KEY not configured"}
        try:
            resp = await self.client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_tokens,
                temperature=temperature
            )
            content = resp.choices[0].message.content if resp.choices else None
            if content:
                return {"success": True, "content": content}
            return {"success": False, "error": "Empty response from OpenAI"}
        except Exception as e:
            return {"success": False, "error": str(e)}

# ==============================
# Cliente Fal AI - imágenes/video generación
# ==============================
class FalAIClient:
    def __init__(self):
        self.enabled = bool(FAL_KEY)
        self.api_key = FAL_KEY
        # Se puede añadir endpoint y lógica real según plataforma

    async def generate_image(self, prompt: str) -> Dict[str, Any]:
        if not self.enabled:
            return {"success": False, "error": "FAL_API_KEY not configured"}
        # Lógica real aquí y conexión backend si aplica
        return {"success": True, "url": "https://example.com/image.png"}

# ==============================
# Cliente Abacus AI - analítica predictiva y dashboards avanzados
# ==============================
class AbacusAIClient:
    def __init__(self):
        self.apikey = ABACUS_KEY

    async def analyze(self, data: Dict[str, Any]) -> Dict[str, Any]:
        if not self.apikey:
            return {"success": False, "error": "ABACUS_API_KEY not configured"}
        # Lógica real aquí y conexión backend si aplica
        return {"success": True, "insights": "Placeholder - implementar analítica avanzada."}

# ==============================
# Enrutador Omnicanal con integración backend, prompts y accesorios
# ==============================
class AIRouter:
    def __init__(self):
        self.openrouter = OpenRouterClient()
        self.perplexity = PerplexityClient()
        self.openai = OpenAIClient()
        self.abacus = AbacusAIClient()
        self.fal = FalAIClient()
        self.backend_url = BACKEND_URL

    async def generate_text(self, message: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        context = context or {}
        querytype = self.detect_query_type(message)
        system_context = (
            "Eres Super Cerebro AI, agente omnicanal experto en herramientas, accesorios y monetización. "
            "Siempre conectado a backend: " + self.backend_url + " ."
            "Responde en modo profesional, explicando cada paso. Incluye detalles técnicos, emojis y ejemplos."
        )
        full_prompt = f"{system_context}\n{message}"

        try:
            # Buscar y generar texto/contexto según la petición
            if querytype == "search":
                result = await self.perplexity.search(full_prompt)
                if result.get("content"):
                    return {"success": True, "text": result["content"], "platform_used": "perplexity"}
            result = await self.openrouter.generate_text(full_prompt)
            if result.get("text"):
                return {"success": True, "text": result["text"], "platform_used": "claude"}
            if self.openai:
                result = await self.openai.chat(full_prompt)
                if result.get("content"):
                    return {"success": True, "text": result["content"], "platform_used": "openai"}
            return {"success": False, "text": "Error: No hay respuesta disponible"}
        except Exception as e:
            return {"success": False, "text": f"Error: {str(e)}"}

    def detect_query_type(self, message: str) -> str:
        msg_lower = message.lower()
        if any(w in msg_lower for w in ["buscar", "precio", "mercado", "comparar", "oportunidad", "monetizar"]):
            return "search"
        return "general"

    async def route(self, prompt: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        # Punto único de enrutamiento multi-plataforma y multi-modular
        return await self.generate_text(prompt, context)

    # Expansión: puede integrarse con backend, prompts dinámicos, gestión de herramientas y accesorios
    async def execute_backend_command(self, command: str, params: Dict[str, Any] = None):
        """
        Permite ejecutar comandos directos sobre el backend conectado (expansión arbitraria).
        Ejemplo: auto-integraciones de plugins, memoria, accesorios, reportes, etc.
        """
        params = params or {}
        async with httpx.AsyncClient(timeout=60) as client:
            try:
                res = await client.post(f"{self.backend_url}/api/autocomandos", json={"comando": command, "params": params})
                return res.json()
            except Exception as e:
                return {"success": False, "error": str(e)}
