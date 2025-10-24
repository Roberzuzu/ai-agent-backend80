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
# AIRouter inteligente
# ===============================
class AIRouter:
    """
    Router inteligente que usa OpenRouter, Perplexity y OpenAI.
    - Detecta tipo de consulta: e-commerce, factual (web), creativo/código, general.
    - Respuestas contextuales para e-commerce: catálogo, fichas, comparativas, pricing, SEO, UX de compra.
    """
    def __init__(self):
        self.openrouter = OpenRouterClient()
        self.perplexity = PerplexityClient()
        self.openai = OpenAIClient()
    @staticmethod
    def _classify(query: str) -> str:
        q = (query or "").lower()
        ecommerce_terms = [
            "precio", "oferta", "comprar", "carrito", "stock", "envío", "devolución",
            "producto", "catálogo", "inventario", "sku", "ecommerce", "tienda",
            "ficha", "comparativa", "reseña", "opiniones", "descuento"
        ]
        factual_terms = ["qué es", "quien es", "fecha", "número", "estadística", "último", "noticia"]
        code_terms = ["código", "snippet", "bug", "error", "stack", "api", "sdk", "python", "javascript"]
        if any(t in q for t in ecommerce_terms):
            return "ecommerce"
        if any(t in q for t in factual_terms):
            return "factual"
        if any(t in q for t in code_terms) or q.strip().startswith(("def ", "class ")):
            return "code"
        return "general"
    @staticmethod
    def _ecommerce_system_prompt(context: Optional[Dict[str, Any]] = None) -> str:
        ctx = context or {}
        brand = ctx.get("brand") or ctx.get("store_name") or "la tienda"
        currency = ctx.get("currency", "€")
        locale = ctx.get("locale", "es-ES")
        return (
            f"Eres un asistente experto en e-commerce para {brand}. "
            f"Responde en {locale} con tono claro y accionable. "
            f"Incluye: intención de compra, atributos clave del producto, variantes, compatibilidades, "
            f"políticas (envío/devoluciones), y precios en {currency}. "
            f"Cuando sea útil, devuelve bloques estructurados (JSON) para catálogo/ficha/comparativa."
        )
    async def route(self, query: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Enruta la consulta al proveedor más adecuado y compone una respuesta útil.
        context puede incluir: {brand, store_name, currency, locale, catalog (list), user_profile, constraints}
        """
        qtype = self._classify(query)
        result: Dict[str, Any] = {"type": qtype}
        # E-commerce: combinamos Perplexity (datos/competencia) + OpenRouter/OpenAI para redacción SEO/UX
        if qtype == "ecommerce":
            sys_prompt = self._ecommerce_system_prompt(context)
            # 1) Buscar señales del mercado si hay intención de compra/comparativa
            market_snippet = None
            try:
                px = await self.perplexity.search(query, system_prompt="Eres analista de mercado e-commerce. Resume fuentes.")
                if not px.get("error"):
                    market_snippet = px.get("content")
            except Exception as e:
                market_snippet = f"[perplexity_error]: {e}"
            # 2) Generar respuesta rica con OpenRouter (o OpenAI fallback)
            enriched_prompt = (
                f"{sys_prompt}\n\nConsulta usuario: {query}\n\n"
                f"Contexto disponible: {json.dumps(context or {}, ensure_ascii=False)[:2000]}\n\n"
                f"Inteligencia de mercado: {market_snippet or 'N/A'}\n\n"
                "Devuelve:\n- Resumen ejecutivo\n- Recomendación\n- Pros/Contras\n- Siguiente acción (CTA)\n- Si aplica, JSON con campos: {type: 'product|comparison|catalog', items: [...]}"
            )
            llm = await self.openrouter.generate_text(enriched_prompt)
            if llm.get("error"):
                llm = await self.openai.chat(enriched_prompt)
            result.update({"content": llm.get("content"), "market": market_snippet, "raw": {"llm": llm}})
            return result
        # Factual/actualidad: Perplexity
        if qtype == "factual":
            px = await self.perplexity.search(query)
            return {**result, **px}
        # Código/técnico: OpenRouter por diversidad de modelos, fallback OpenAI
        if qtype == "code":
            prompt = (
                "Actúa como senior engineer. Explica, propone alternativa y da snippet comentado.\n\n"
                f"Pregunta: {query}"
            )
            llm = await self.openrouter.generate_text(prompt, model="qwen/qwen-2.5-coder-32b-instruct")
            if llm.get("error"):
                llm = await self.openai.chat(prompt, model="gpt-4o-mini")
            return {**result, **llm}
        # General: OpenRouter default, fallback OpenAI
        llm = await self.openrouter.generate_text(query)
        if llm.get("error"):
            llm = await self.openai.chat(query)
        return {**result, **llm}
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
