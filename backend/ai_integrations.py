"""
AI Integrations Module - Super Powered
Gestiona todas las integraciones con APIs de IA:
- OpenRouter (LLM routing)
- Perplexity (Real-time search)
- OpenAI (GPT + DALL-E)
- Fal AI (Image/Video generation)
- Abacus AI (Predictive analytics)
"""
import os
import asyncio
import httpx
import fal_client
from typing import Dict, List, Optional, Any
from openai import AsyncOpenAI
import json

# Configurar API keys
FAL_KEY = os.getenv("FAL_API_KEY")
OPENROUTER_KEY = os.getenv("OPENROUTER_API_KEY")
PERPLEXITY_KEY = os.getenv("PERPLEXITY_API_KEY")
OPENAI_KEY = os.getenv("OPENAI_API_KEY")
ABACUS_KEY = os.getenv("ABACUS_API_KEY")

# Configurar Fal Client solo si la key existe
if FAL_KEY:
    os.environ["FAL_KEY"] = FAL_KEY

# Cliente OpenAI - solo si la key existe
openai_client = None
if OPENAI_KEY:
    openai_client = AsyncOpenAI(api_key=OPENAI_KEY)

class OpenRouterClient:
    """Cliente para OpenRouter - Enrutamiento de LLMs"""
    def __init__(self):
        self.api_key = OPENROUTER_KEY
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"

    async def generate_text(self, prompt: str, model: str = 'anthropic/claude-3.5-sonnet', max_tokens: int = 2000, temperature: float = 0.7) -> Dict[str, Any]:
        if not self.api_key:
            return {'success': False, 'error': 'OPENROUTER_API_KEY not configured'}
        headers = {
            "Authorization": f"Bearer {self.api_key}",
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
                res = await client.post(self.base_url, headers=headers, json=payload)
                data = res.json()
                content = data.get('choices', [{}])[0].get('message', {}).get('content')
                if content:
                    return {'success': True, 'text': content, 'model': data.get('model'), 'usage': data.get('usage')}
                return {'success': False, 'error': 'Empty response from OpenRouter'}
            except Exception as e:
                return {'success': False, 'error': str(e)}

class PerplexityClient:
    """Cliente para búsquedas en Perplexity"""
    def __init__(self):
        self.api_key = PERPLEXITY_KEY
        self.base_url = "https://api.perplexity.ai/chat/completions"

    async def search(self, prompt: str, model: str = 'sonar', max_tokens: int = 1800) -> Dict[str, Any]:
        if not self.api_key:
            return {'success': False, 'error': 'PERPLEXITY_API_KEY not configured'}
        headers = {
            "Authorization": f"Bearer {self.api_key}",
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
                res = await client.post(self.base_url, headers=headers, json=payload)
                data = res.json()
                content = data.get('choices', [{}])[0].get('message', {}).get('content')
                citations = data.get('citations') or []
                if content:
                    return {'success': True, 'content': content, 'citations': citations}
                return {'success': False, 'error': 'Empty response from Perplexity'}
            except Exception as e:
                return {'success': False, 'error': str(e)}

class OpenAIClient:
    """Cliente para OpenAI (chat)"""
    def __init__(self):
        self.client = openai_client

    async def chat(self, prompt: str, model: str = 'gpt-4o-mini', max_tokens: int = 2000, temperature: float = 0.7) -> Dict[str, Any]:
        if not self.client:
            return {'success': False, 'error': 'OPENAI_API_KEY not configured'}
        try:
            resp = await self.client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_tokens,
                temperature=temperature
            )
            content = resp.choices[0].message.content if resp.choices else None
            if content:
                return {'success': True, 'content': content}
            return {'success': False, 'error': 'Empty response from OpenAI'}
        except Exception as e:
            return {'success': False, 'error': str(e)}

class FalAIClient:
    """Cliente para Fal AI (imágenes/videos)"""
    def __init__(self):
        self.enabled = bool(FAL_KEY)

    async def generate_image(self, prompt: str) -> Dict[str, Any]:
        if not self.enabled:
            return {'success': False, 'error': 'FAL_API_KEY not configured'}
        # Placeholder: Implementar integración real si es necesario
        return {'success': True, 'url': 'https://example.com/image.png'}

class AbacusAIClient:
    """Cliente para Abacus AI (analítica predictiva)"""
    def __init__(self):
        self.api_key = ABACUS_KEY

    async def analyze(self, data: Dict[str, Any]) -> Dict[str, Any]:
        if not self.api_key:
            return {'success': False, 'error': 'ABACUS_API_KEY not configured'}
        # Placeholder: Implementar integración real si es necesario
        return {'success': True, 'insights': {}}

# ====================================
# AI ROUTER - INTELLIGENT CHAT ROUTING  
# ====================================

from typing import Dict, Any

class AIRouter:
    def __init__(self):
        self.openrouter = OpenRouterClient()
        self.perplexity = PerplexityClient()
        self.openai = OpenAIClient() if OPENAI_KEY else None
        self.abacus = AbacusAIClient()
    
    async def generate_text(self, message: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        context = context or {}
        query_type = self._detect_query_type(message)
        
        system_context = '''Eres Super Cerebro AI, asistente experto en herramientas y accesorios.
Tienda: herramientasyaccesorios.store
Responde de forma profesional, detallada (200+ palabras), con emojis y ejemplos concretos.'''
        
        full_prompt = f"{system_context}\n\nUsuario: {message}\n\nAsistente:"
        
        try:
            # Try Perplexity for search queries
            if query_type == 'search':
                result = await self.perplexity.search(full_prompt)
                if result.get('content'):
                    return {'success': True, 'text': result['content'], 'platform_used': 'perplexity'}
            
            # Primary: Claude 3.5 Sonnet via OpenRouter
            result = await self.openrouter.generate_text(full_prompt, model='anthropic/claude-3.5-sonnet', max_tokens=2500)
            if result.get('text') or result.get('content'):
                # normalize
                content = result.get('text') or result.get('content')
                return {'success': True, 'text': content, 'platform_used': 'claude'}
            
            # Fallback: OpenAI
            if self.openai:
                result = await self.openai.chat(full_prompt, max_tokens=2500)
                if result.get('content'):
                    return {'success': True, 'text': result['content'], 'platform_used': 'openai'}
            
            return {'success': False, 'text': 'Error: No hay respuesta disponible'}
        except Exception as e:
            return {'success': False, 'text': f'Error: {str(e)}'}
    
    def _detect_query_type(self, message: str) -> str:
        msg_lower = message.lower()
        if any(w in msg_lower for w in ['buscar', 'precio', 'mercado', 'comparar']):
            return 'search'
        return 'general'
    
    async def route(self, prompt: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        return await self.generate_text(prompt, context)
