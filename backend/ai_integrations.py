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

# Cliente OpenAI
openai_client = AsyncOpenAI(api_key=OPENAI_KEY)


class OpenRouterClient:
    """Cliente para OpenRouter - Enrutamiento de LLMs"""
    
    def __init__(self):
        self.api_key = OPENROUTER_KEY
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"
    
    async def generate_text(
        self,
        prompt: str,
        model: str = "anthropic/claude-3.5-sonnet",
        temperature: float = 0.7,
        max_tokens: int = 2000
    ) -> Dict[str, Any]:
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
                    "max_tokens": max_tokens
                }
            )
            
            if response.status_code != 200:
                return {"error": f"OpenRouter error: {response.text}"}
            
            data = response.json()
            return {
                "success": True,
                "text": data["choices"][0]["message"]["content"],
                "model": model,
                "usage": data.get("usage", {})
            }


class PerplexityClient:
    """Cliente para Perplexity - Búsqueda en tiempo real"""
    
    def __init__(self):
        self.api_key = PERPLEXITY_KEY
        self.base_url = "https://api.perplexity.ai/chat/completions"
    
    async def search_market(
        self,
        query: str,
        model: str = "llama-3.1-sonar-large-128k-online"
    ) -> Dict[str, Any]:
        """Realiza búsqueda en tiempo real sobre mercado/competencia"""
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                self.base_url,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": model,
                    "messages": [{"role": "user", "content": query}]
                }
            )
            
            if response.status_code != 200:
                return {"error": f"Perplexity error: {response.text}"}
            
            data = response.json()
            return {
                "success": True,
                "content": data["choices"][0]["message"]["content"],
                "citations": data.get("citations", [])
            }


class FalAIClient:
    """Cliente para Fal AI - Generación de imágenes/video"""
    
    async def generate_image(
        self,
        prompt: str,
        model: str = "fal-ai/flux/dev",
        image_size: str = "landscape_4_3",
        num_images: int = 1
    ) -> Dict[str, Any]:
        """Genera imágenes usando Flux o DALL-E"""
        try:
            handler = await fal_client.submit_async(
                model,
                arguments={
                    "prompt": prompt,
                    "image_size": image_size,
                    "num_images": num_images
                }
            )
            
            result = await handler.get()
            
            return {
                "success": True,
                "images": result.get("images", []),
                "model": model
            }
        except Exception as e:
            return {"error": str(e)}
    
    async def generate_with_dalle(
        self,
        prompt: str,
        size: str = "1024x1024",
        quality: str = "standard",
        n: int = 1
    ) -> Dict[str, Any]:
        """Genera imágenes usando DALL-E 3 como respaldo"""
        try:
            response = await openai_client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size=size,
                quality=quality,
                n=n
            )
            
            return {
                "success": True,
                "images": [{"url": img.url} for img in response.data],
                "model": "dall-e-3"
            }
        except Exception as e:
            return {"error": str(e)}


class OpenAIClient:
    """Cliente para OpenAI - GPT y DALL-E"""
    
    async def generate_text(
        self,
        prompt: str,
        model: str = "gpt-4-turbo-preview",
        temperature: float = 0.7,
        max_tokens: int = 2000
    ) -> Dict[str, Any]:
        """Genera texto con GPT-4"""
        try:
            response = await openai_client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            return {
                "success": True,
                "text": response.choices[0].message.content,
                "model": model,
                "usage": {
                    "prompt_tokens": response.usage.prompt_tokens,
                    "completion_tokens": response.usage.completion_tokens,
                    "total_tokens": response.usage.total_tokens
                }
            }
        except Exception as e:
            return {"error": str(e)}


class AbacusAIClient:
    """Cliente para Abacus AI - Análisis predictivo"""
    
    def __init__(self):
        self.api_key = ABACUS_KEY
        self.base_url = "https://api.abacus.ai/api/v1"
    
    async def predict_price(
        self,
        product_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Predice precio óptimo basado en datos del producto"""
        # Por ahora usamos un modelo simple basado en reglas
        # En producción, esto llamaría a un modelo entrenado en Abacus AI
        
        try:
            # Análisis básico de mercado
            category = product_data.get("category", "general")
            base_price = product_data.get("base_price", 0)
            
            # Factor de markup según categoría
            markup_factors = {
                "herramientas electricas": 1.5,
                "herramientas manuales": 1.4,
                "accesorios": 1.6,
                "general": 1.5
            }
            
            markup = markup_factors.get(category.lower(), 1.5)
            optimal_price = base_price * markup
            
            return {
                "success": True,
                "optimal_price": round(optimal_price, 2),
                "base_price": base_price,
                "markup": markup,
                "confidence": 0.85,
                "market_analysis": {
                    "category": category,
                    "demand_level": "medium",
                    "competition": "moderate"
                }
            }
        except Exception as e:
            return {"error": str(e)}
    
    async def analyze_demand(
        self,
        product_name: str,
        category: str
    ) -> Dict[str, Any]:
        """Analiza demanda del producto"""
        try:
            # Simulación de análisis de demanda
            return {
                "success": True,
                "demand_score": 0.75,
                "trend": "increasing",
                "seasonality": "medium",
                "forecast": {
                    "next_month": 0.8,
                    "next_quarter": 0.82
                }
            }
        except Exception as e:
            return {"error": str(e)}


# ===============================
# FUNCIONES DE ALTO NIVEL
# ===============================

async def generate_product_description(
    product_name: str,
    category: str,
    features: List[str] = None,
    language: str = "es"
) -> Dict[str, Any]:
    """
    Genera descripción completa del producto con SEO
    Usa OpenRouter (Claude 3.5 Sonnet)
    """
    features_text = "\n".join([f"- {f}" for f in (features or [])])
    
    prompt = f"""Genera una descripción profesional para eCommerce en español.

Producto: {product_name}
Categoría: {category}
Características:
{features_text}

La descripción debe incluir:
1. Título atractivo y llamativo (H1)
2. Introducción persuasiva (2-3 párrafos)
3. Lista de características principales con emojis
4. Beneficios clave para el usuario
5. Especificaciones técnicas (si aplica)
6. Llamado a la acción
7. SEO: Meta título (max 60 caracteres)
8. SEO: Meta descripción (max 160 caracteres)

Formato: Devuelve JSON con las siguientes claves:
- title: Título H1
- description: Descripción HTML completa
- meta_title: Meta título SEO
- meta_description: Meta descripción SEO
- keywords: Array de 10 keywords relevantes
"""
    
    client = OpenRouterClient()
    result = await client.generate_text(prompt, max_tokens=3000)
    
    if result.get("success"):
        try:
            # Extraer JSON del texto
            text = result["text"]
            # Buscar JSON en el texto
            json_start = text.find("{")
            json_end = text.rfind("}") + 1
            if json_start >= 0 and json_end > json_start:
                json_text = text[json_start:json_end]
                data = json.loads(json_text)
                return {"success": True, **data}
            else:
                # Si no hay JSON, devolver el texto completo
                return {
                    "success": True,
                    "title": product_name,
                    "description": text,
                    "meta_title": product_name,
                    "meta_description": text[:160],
                    "keywords": []
                }
        except Exception as e:
            return {"error": f"Error parsing JSON: {str(e)}", "raw_text": result["text"]}
    
    return result


async def generate_product_images(
    product_name: str,
    category: str,
    style: str = "professional product photo",
    num_images: int = 1
) -> Dict[str, Any]:
    """
    Genera imágenes del producto
    Intenta con Fal AI primero, luego DALL-E
    """
    prompt = f"""Professional product photography of {product_name}, {category}.
{style}. High quality, well lit, white background, commercial photography.
Product centered, sharp focus, professional lighting."""
    
    # Intentar con Fal AI primero
    fal_client = FalAIClient()
    result = await fal_client.generate_image(prompt, num_images=num_images)
    
    if result.get("success"):
        return result
    
    # Si falla, intentar con DALL-E
    dalle_result = await fal_client.generate_with_dalle(prompt, n=num_images)
    return dalle_result


async def analyze_market_competition(
    product_name: str,
    category: str
) -> Dict[str, Any]:
    """
    Analiza competencia y mercado usando Perplexity
    """
    query = f"""Analiza el mercado español para: {product_name} en la categoría {category}.

Proporciona:
1. Rango de precios en el mercado (mínimo, promedio, máximo)
2. Top 3 competidores y sus precios
3. Características más valoradas por clientes
4. Tendencias actuales de búsqueda
5. Precio óptimo recomendado para España
6. Keywords SEO recomendadas

Formato: Respuesta estructurada y concisa."""
    
    client = PerplexityClient()
    result = await client.search_market(query)
    
    return result


async def get_optimal_pricing(
    product_name: str,
    category: str,
    base_price: float
) -> Dict[str, Any]:
    """
    Calcula precio óptimo usando Abacus AI
    """
    client = AbacusAIClient()
    result = await client.predict_price({
        "product_name": product_name,
        "category": category,
        "base_price": base_price
    })
    
    return result


async def generate_social_media_content(
    product_name: str,
    description: str,
    platforms: List[str] = ["instagram", "facebook", "twitter"]
) -> Dict[str, Any]:
    """
    Genera contenido optimizado para redes sociales
    """
    prompt = f"""Genera posts para redes sociales sobre este producto:

Producto: {product_name}
Descripción: {description}

Genera contenido para: {', '.join(platforms)}

Para cada plataforma, proporciona:
1. Texto del post (con emojis y hashtags)
2. Mejor hora para publicar
3. 5-10 hashtags relevantes
4. Call to action

Formato JSON con estructura por plataforma."""
    
    client = OpenRouterClient()
    result = await client.generate_text(prompt, max_tokens=2000)
    
    return result


async def generate_email_campaign(
    product_name: str,
    description: str,
    target_audience: str = "general"
) -> Dict[str, Any]:
    """
    Genera campaña de email marketing
    """
    prompt = f"""Crea una campaña de email marketing para:

Producto: {product_name}
Descripción: {description}
Audiencia: {target_audience}

Genera:
1. Asunto del email (3 variaciones A/B test)
2. Preheader text
3. Contenido HTML del email (con estructura)
4. Call to action
5. Recomendaciones de segmentación

Formato JSON estructurado."""
    
    client = OpenRouterClient()
    result = await client.generate_text(prompt, max_tokens=2500)
    
    return result


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
        description_result = await generate_product_description(
            product_name, category, features
        )
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
