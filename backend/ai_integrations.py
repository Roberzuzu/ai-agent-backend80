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

    async def generate_text(self, prompt: str, model: str = "anthropic/claude-3.5-sonnet", temperature: float = 0.7, max_tokens: int = 2000) -> Dict[str, Any]:
        """Genera texto usando el modelo especificado"""
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                self.base_url,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": model,
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": temperature,
                    "max_tokens": max_tokens,
                },
            )
            response.raise_for_status()
            data = response.json()
            content = data.get("choices", [{}])[0].get("message", {}).get("content", "")
            return {"content": content, "raw": data}

class PerplexityClient:
    """Cliente para Perplexity - Búsqueda de tiempo real"""
    def __init__(self):
        self.api_key = PERPLEXITY_KEY
        self.base_url = "https://api.perplexity.ai/chat/completions"
        self.model = "llama-3.1-sonar-large-128k-online"

    async def search(self, query: str, system_prompt: Optional[str] = None) -> Dict[str, Any]:
        if not self.api_key:
            return {"error": "PERPLEXITY_API_KEY no configurada"}
        payload = {
            "model": self.model,
            "messages": (
                ([{"role": "system", "content": system_prompt}] if system_prompt else [])
                + [{"role": "user", "content": query}]
            ),
            "temperature": 0.2,
        }
        async with httpx.AsyncClient(timeout=60.0) as client:
            resp = await client.post(
                self.base_url,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                },
                json=payload,
            )
            resp.raise_for_status()
            data = resp.json()
            content = data.get("choices", [{}])[0].get("message", {}).get("content", "")
            return {"content": content, "raw": data}

class FalAIClient:
    """Cliente para generación de imágenes/video con FAL"""
    def __init__(self):
        self.available = bool(FAL_KEY)

    async def generate_image(self, prompt: str, num_images: int = 1) -> Dict[str, Any]:
        if not self.available:
            return {"error": "FAL_API_KEY no configurada"}
        # Ejemplo simple (puede ajustarse a la API real de fal_client)
        try:
            result = await fal_client.image.generate(prompt=prompt, num_images=num_images)
            return {"images": result}
        except Exception as e:
            return {"error": str(e)}

class OpenAIClient:
    """Cliente para GPT y herramientas de OpenAI"""
    def __init__(self):
        self.client = openai_client

    async def chat(self, prompt: str, model: str = "gpt-4o-mini", temperature: float = 0.7, max_tokens: int = 1500) -> Dict[str, Any]:
        if not self.client:
            return {"error": "OPENAI_API_KEY no configurada"}
        try:
            completion = await self.client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature,
                max_tokens=max_tokens,
            )
            msg = completion.choices[0].message.content
            return {"content": msg, "raw": completion.model_dump()}
        except Exception as e:
            return {"error": str(e)}

class AbacusAIClient:
    """Cliente para analítica predictiva (placeholder)"""
    def __init__(self):
        self.api_key = ABACUS_KEY

    async def forecast(self, series: List[float]) -> Dict[str, Any]:
        if not self.api_key:
            return {"error": "ABACUS_API_KEY no configurada"}
        # Placeholder de ejemplo
        try:
            avg = sum(series) / max(len(series), 1)
            return {"forecast": [avg for _ in range(3)]}
        except Exception as e:
            return {"error": str(e)}

# ===============================
# FUNCIONES DE NEGOCIO (existentes)
# ===============================
async def generate_product_description(product_name: str, category: str, features: List[str] = None) -> Dict[str, Any]:
    router = AIRouter()
    prompt = (
        "Genera una descripción SEO para e-commerce con bullets, tono claro y CTA.\n"
        f"Producto: {product_name}\n"
        f"Categoría: {category}\n"
        f"Características: {', '.join(features or [])}"
    )
    return await router.route(prompt, context={"type": "description", "category": category})

async def analyze_market_competition(product_name: str, category: str) -> Dict[str, Any]:
    router = AIRouter()
    prompt = (
        "Analiza competencia y mercado para este producto. Devuelve resumen y comparativa JSON.\n"
        f"Producto: {product_name}\nCategoría: {category}"
    )
    return await router.route(prompt, context={"type": "market_analysis", "category": category})

async def get_optimal_pricing(product_name: str, category: str, base_price: float) -> Dict[str, Any]:
    router = AIRouter()
    prompt = (
        "Propón precio óptimo considerando competencia, valor percibido y margen.\n"
        f"Producto: {product_name}\nCategoría: {category}\nPrecio base: {base_price}"
    )
    return await router.route(prompt, context={"type": "pricing", "currency": "€"})

async def generate_product_images(product_name: str, category: str, num_images: int = 2) -> Dict[str, Any]:
    fal = FalAIClient()
    return await fal.generate_image(f"Fotografía de producto profesional: {product_name} ({category})", num_images=num_images)

async def generate_social_media_content(product_name: str, description: str) -> Dict[str, Any]:
    router = AIRouter()
    prompt = (
        "Genera 3 posts para redes (IG, X, TikTok) con variantes de tono y hashtags.\n"
        f"Producto: {product_name}\nDescripción: {description}"
    )
    return await router.route(prompt, context={"type": "social"})

# ===============================
# PROCESAMIENTO COMPLETO
# ===============================
async def process_product_complete(
    product_name: str,
    category: str,
    features: List[str] = None,
    base_price: float = None,
    generate_images: bool = True
) -> Dict[str, Any]:
    """
    Procesa producto completo con todas las integraciones AI
    """
    results = {
        "product_name": product_name,
        "category": category,
        "processing_complete": False
    }
    try:
        # 1. Generar descripción con SEO
        print(f"Generando descripción para {product_name}...")
        description_result = await generate_product_description(product_name, category, features)
        results["description"] = description_result
        # 2. Analizar mercado y competencia
        print(f"Analizando mercado...")
        market_result = await analyze_market_competition(product_name, category)
        results["market_analysis"] = market_result
        # 3. Calcular precio óptimo
        if base_price:
            print(f"Calculando precio óptimo...")
            pricing_result = await get_optimal_pricing(product_name, category, base_price)
            results["pricing"] = pricing_result
        # 4. Generar imágenes
        if generate_images:
            print(f"Generando imágenes...")
            images_result = await generate_product_images(product_name, category, num_images=2)
            results["images"] = images_result
        # 5. Generar contenido para redes sociales
        print(f"Generando contenido de redes sociales...")
        social_result = await generate_social_media_content(
            product_name,
            description_result.get("description", "")
        )
        results["social_media"] = social_result
        results["processing_complete"] = True
        results["success"] = True
    except Exception as e:
        results["error"] = str(e)
        results["success"] = False
    return results



# ====================================
# AI ROUTER - INTELLIGENT CHAT ROUTING  
# ====================================

class AIRouter:
    """
    Intelligent AI Router for e-commerce chat
    Routes queries to the best AI platform based on context
    Provides detailed, professional responses
    """
    
    def __init__(self):
        """Initialize AI Router with all available clients"""
        self.openrouter = OpenRouterClient()
        self.perplexity = PerplexityClient()
        self.openai = OpenAIClient() if OPENAI_KEY else None
        self.abacus = AbacusAIClient()
    
    async def generate_text(self, message: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Main entry point for chat responses"""
        context = context or {}
        query_type = self._detect_query_type(message)
        
        system_context = """Eres Super Cerebro AI, un asistente experto en comercio electrónico especializado en herramientas y accesorios.

🏪 **Tu tienda online es:** Herramientas y Accesorios Store (herramientasyaccesorios.store)

📦 **CATÁLOGO:**
- Herramientas eléctricas profesionales
- Herramientas manuales de alta calidad
- Accesorios y componentes
- Equipos de seguridad
- Sistemas de almacenamiento

✨ **SERVICIOS:**
- Envíos rápidos a toda España
- Garantía oficial en todos los productos
- Asesoramiento técnico profesional
- Soporte post-venta especializado
- Comparativas y recomendaciones personalizadas

🎯 **TU MISIÓN:**
1. Responder de forma profesional, útil y DETALLADA (mínimo 3-4 párrafos)
2. Ofrecer recomendaciones concretas de productos cuando sea relevante
3. Proporcionar información técnica precisa y completa
4. Ayudar al cliente a tomar decisiones de compra informadas
5. Ser proactivo sugiriendo productos complementarios
6. Explicar beneficios, características y casos de uso

💬 **ESTILO DE RESPUESTA:**
- Profesional pero cercano y amigable
- Detallado y muy bien estructurado (usa listas, secciones)
- Usa emojis estratégicamente (🔧 🛠️ ⚡ ✨ 💪 🏆 ✅) para mejor legibilidad
- Incluye llamadas a la acción suaves
- Mínimo 200-300 palabras por respuesta
- Proporciona ejemplos concretos y casos de uso

📋 **FORMATO RECOMENDADO:**
1. Saludo y confirmación de la pregunta
2. Respuesta principal (2-3 párrafos explicativos)
3. Recomendaciones específicas (si aplica)
4. Consejos adicionales o información complementaria
5. Cierre con pregunta abierta para continuar la conversación

Responde SIEMPRE en español de España con un tono experto pero accesible."""

        full_prompt = f"""{system_context}

👤 **Usuario pregunta:** {message}

🤖 **Super Cerebro AI responde (de forma DETALLADA y COMPLETA):**"""
        
        try:
            if query_type == 'search' or query_type == 'market':
                print(f"🔍 Routing to Perplexity for search query: {message[:50]}...")
                result = await self.perplexity.search_market(message)
                if result.get('success'):
                    return {'success': True, 'text': result['content'], 'platform_used': 'perplexity-sonar', 'citations': result.get('citations', []), 'query_type': query_type}
            
            print(f"🤖 Routing to Claude 3.5 Sonnet for query: {message[:50]}...")
            result = await self.openrouter.generate_text(full_prompt, model='anthropic/claude-3.5-sonnet', max_tokens=2500, temperature=0.7)
            
            if result.get('success'):
                response_text = result['text']
                if len(response_text) < 150:
                    response_text += "\n\n💡 **¿Necesitas más información sobre este tema o algún producto en particular?** Estoy aquí para ayudarte a encontrar exactamente lo que necesitas. 😊"
                elif not any(char in response_text[-50:] for char in ['?', '¿']):
                    response_text += "\n\n¿Hay algo más en lo que pueda ayudarte? 😊"
                return {'success': True, 'text': response_text, 'platform_used': 'claude-3.5-sonnet', 'model': result.get('model'), 'usage': result.get('usage', {}), 'query_type': query_type}
            
            if self.openai:
                print(f"⚡ Fallback to OpenAI GPT-4 for query: {message[:50]}...")
                result = await self.openai.generate_text(full_prompt, model='gpt-4-turbo-preview', max_tokens=2500, temperature=0.7)
                if result.get('success'):
                    return {'success': True, 'text': result['text'], 'platform_used': 'openai-gpt4', 'query_type': query_type}
            
            print(f"❌ All AI providers failed for query: {message[:50]}")
            return {'success': False, 'error': 'No AI provider available or all failed', 'text': '''Lo siento mucho, estoy experimentando dificultades técnicas temporales. 😔

Por favor, intenta de nuevo en unos momentos. Si el problema persiste, puedes:

📧 Contactarnos directamente en: info@herramientasyaccesorios.store
📞 Llamarnos para atención personalizada

Disculpa las molestias. ¡Estamos trabajando para resolver esto lo antes posible!'''}
            
        except Exception as e:
            print(f"❌ Exception in AIRouter: {str(e)}")
            return {'success': False, 'error': str(e), 'text': f'''Ups, ha ocurrido un error al procesar tu consulta. 😔

**Error técnico:** {str(e)}

Por favor, intenta reformular tu pregunta o contáctanos directamente para ayudarte:
📧 info@herramientasyaccesorios.store

¡Gracias por tu paciencia!'''}
    
    def _detect_query_type(self, message: str) -> str:
        """Detect query intent for intelligent routing"""
        message_lower = message.lower()
        search_keywords = ['buscar', 'search', 'precio', '
