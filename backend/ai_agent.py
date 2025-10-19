"""
AI Agent - Cerebro Central del Sistema
Usa Claude 3.5 Sonnet para interpretar comandos y ejecutar acciones
"""

import os
import json
import asyncio
from typing import Dict, List, Any, Optional
import httpx
from datetime import datetime

# APIs disponibles
OPENROUTER_KEY = os.getenv("OPENROUTER_API_KEY")
PERPLEXITY_KEY = os.getenv("PERPLEXITY_API_KEY")
OPENAI_KEY = os.getenv("OPENAI_API_KEY")
FAL_KEY = os.getenv("FAL_API_KEY")
ABACUS_KEY = os.getenv("ABACUS_API_KEY")

# WooCommerce
WC_KEY = "ck_4f50637d85ec404fff441fceb7b113b5050431ea"
WC_SECRET = "cs_e59ef18ea20d80ffdf835803ad2fdd834a4ba19f"
WC_URL = "https://herramientasyaccesorios.store/wp-json/wc/v3"

# WordPress
WP_USER = "agenteweb@herramientasyaccesorios.store"
WP_PASS = "RWWLW1eVi8whOS5OsUosb5AU"
WP_URL = "https://herramientasyaccesorios.store/wp-json/wp/v2"


class AIAgent:
    """Agente inteligente que interpreta y ejecuta comandos"""
    
    def __init__(self):
        self.openrouter_url = "https://openrouter.ai/api/v1/chat/completions"
        self.conversation_history = {}
    
    async def think(self, command: str, user_id: str) -> Dict[str, Any]:
        """
        El cerebro del agente - usa Claude 3.5 para analizar el comando
        y decidir qué acciones tomar
        """
        
        # Obtener historial de conversación
        history = self.conversation_history.get(user_id, [])
        
        # Definir las herramientas disponibles
        tools_description = """
Tienes acceso a estas HERRAMIENTAS:

1. **procesar_producto(product_id)** - Procesa un producto con AI (descripción, precio, imágenes)
2. **buscar_tendencias(categoria, pais)** - Busca productos tendencia con Perplexity
3. **crear_producto(datos)** - Crea un nuevo producto en WooCommerce
4. **analizar_precios(producto, categoria)** - Analiza precios óptimos con Abacus AI
5. **generar_imagenes(descripcion, cantidad)** - Genera imágenes con Fal AI
6. **crear_campana(tipo, producto_id, presupuesto)** - Crea campaña publicitaria
7. **obtener_productos(filtros)** - Lista productos de WooCommerce
8. **analizar_competencia(producto, categoria)** - Análisis de competencia con Perplexity
9. **optimizar_seo(producto_id)** - Optimiza SEO del producto
10. **generar_contenido(tipo, tema)** - Crea blogs, emails, posts sociales

INSTRUCCIONES:
- Analiza el comando del usuario
- Decide qué herramientas usar y en qué orden
- Devuelve un plan de ejecución en JSON

Formato de respuesta:
{
  "plan": "Descripción breve del plan",
  "acciones": [
    {
      "herramienta": "nombre_herramienta",
      "parametros": {...},
      "orden": 1
    }
  ],
  "respuesta_usuario": "Mensaje para el usuario explicando qué vas a hacer"
}
"""
        
        # Crear el prompt para Claude
        messages = history + [
            {
                "role": "user",
                "content": f"{tools_description}\n\nComando del usuario: {command}\n\nAnaliza y crea el plan de ejecución."
            }
        ]
        
        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(
                    self.openrouter_url,
                    headers={
                        "Authorization": f"Bearer {OPENROUTER_KEY}",
                        "Content-Type": "application/json",
                    },
                    json={
                        "model": "anthropic/claude-3.5-sonnet",
                        "messages": messages,
                        "temperature": 0.7,
                        "max_tokens": 2000
                    }
                )
                
                if response.status_code == 200:
                    data = response.json()
                    assistant_message = data["choices"][0]["message"]["content"]
                    
                    # Guardar en historial
                    history.append({"role": "user", "content": command})
                    history.append({"role": "assistant", "content": assistant_message})
                    self.conversation_history[user_id] = history[-10:]  # Mantener últimos 10 mensajes
                    
                    # Extraer JSON del mensaje
                    try:
                        # Buscar JSON en el texto
                        json_start = assistant_message.find("{")
                        json_end = assistant_message.rfind("}") + 1
                        if json_start >= 0 and json_end > json_start:
                            plan_json = json.loads(assistant_message[json_start:json_end])
                            return {
                                "success": True,
                                "plan": plan_json
                            }
                    except:
                        pass
                    
                    return {
                        "success": True,
                        "plan": {
                            "plan": "Ejecutar comando",
                            "respuesta_usuario": assistant_message,
                            "acciones": []
                        }
                    }
                
                return {"success": False, "error": f"Error: {response.status_code}"}
        
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def execute_action(self, action: Dict[str, Any]) -> Dict[str, Any]:
        """Ejecuta una acción específica usando las herramientas disponibles"""
        
        herramienta = action.get("herramienta")
        parametros = action.get("parametros", {})
        
        try:
            if herramienta == "procesar_producto":
                return await self._procesar_producto(parametros.get("product_id"))
            
            elif herramienta == "buscar_tendencias":
                return await self._buscar_tendencias(
                    parametros.get("categoria"),
                    parametros.get("pais", "España")
                )
            
            elif herramienta == "crear_producto":
                return await self._crear_producto(parametros)
            
            elif herramienta == "analizar_precios":
                return await self._analizar_precios(
                    parametros.get("producto"),
                    parametros.get("categoria")
                )
            
            elif herramienta == "generar_imagenes":
                return await self._generar_imagenes(
                    parametros.get("descripcion"),
                    parametros.get("cantidad", 2)
                )
            
            elif herramienta == "obtener_productos":
                return await self._obtener_productos(parametros.get("filtros", {}))
            
            elif herramienta == "analizar_competencia":
                return await self._analizar_competencia(
                    parametros.get("producto"),
                    parametros.get("categoria")
                )
            
            elif herramienta == "generar_contenido":
                return await self._generar_contenido(
                    parametros.get("tipo"),
                    parametros.get("tema")
                )
            
            else:
                return {
                    "success": False,
                    "error": f"Herramienta '{herramienta}' no implementada"
                }
        
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    # ==========================================
    # HERRAMIENTAS ESPECÍFICAS
    # ==========================================
    
    async def _procesar_producto(self, product_id: int) -> Dict[str, Any]:
        """Procesa un producto con AI"""
        from ai_integrations import process_product_complete
        
        # Obtener producto de WooCommerce
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{WC_URL}/products/{product_id}",
                auth=(WC_KEY, WC_SECRET)
            )
            
            if response.status_code != 200:
                return {"success": False, "error": "Producto no encontrado"}
            
            product = response.json()
            
            # Procesar con AI
            result = await process_product_complete(
                product_name=product.get("name"),
                category=product.get("categories", [{}])[0].get("name", "general"),
                base_price=float(product.get("regular_price") or 40),
                generate_images=True
            )
            
            return result
    
    async def _buscar_tendencias(self, categoria: str, pais: str) -> Dict[str, Any]:
        """Busca productos tendencia con Perplexity"""
        
        query = f"""Busca los 10 productos más vendidos y tendencia en {pais} para la categoría: {categoria}

Para cada producto proporciona:
1. Nombre del producto
2. Rango de precio (mínimo-máximo) en euros
3. Por qué es tendencia
4. Principales características
5. Palabras clave SEO

Formato: Lista estructurada"""
        
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                "https://api.perplexity.ai/chat/completions",
                headers={
                    "Authorization": f"Bearer {PERPLEXITY_KEY}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": "llama-3.1-sonar-large-128k-online",
                    "messages": [{"role": "user", "content": query}]
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "success": True,
                    "resultado": data["choices"][0]["message"]["content"],
                    "citations": data.get("citations", [])
                }
            
            return {"success": False, "error": "Error en búsqueda"}
    
    async def _crear_producto(self, datos: Dict[str, Any]) -> Dict[str, Any]:
        """Crea un nuevo producto en WooCommerce"""
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{WC_URL}/products",
                json=datos,
                auth=(WC_KEY, WC_SECRET)
            )
            
            if response.status_code == 201:
                product = response.json()
                return {
                    "success": True,
                    "product_id": product.get("id"),
                    "name": product.get("name"),
                    "url": product.get("permalink")
                }
            
            return {"success": False, "error": response.text}
    
    async def _analizar_precios(self, producto: str, categoria: str) -> Dict[str, Any]:
        """Analiza precios óptimos"""
        from ai_integrations import get_optimal_pricing
        
        result = await get_optimal_pricing(producto, categoria, 50.0)
        return result
    
    async def _generar_imagenes(self, descripcion: str, cantidad: int) -> Dict[str, Any]:
        """Genera imágenes con Fal AI"""
        from ai_integrations import generate_product_images
        
        result = await generate_product_images(descripcion, "producto", num_images=cantidad)
        return result
    
    async def _obtener_productos(self, filtros: Dict[str, Any]) -> Dict[str, Any]:
        """Obtiene productos de WooCommerce"""
        
        params = {
            "per_page": filtros.get("limite", 10),
            "orderby": filtros.get("ordenar_por", "date"),
            "order": filtros.get("orden", "desc")
        }
        
        if filtros.get("categoria"):
            params["category"] = filtros["categoria"]
        
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{WC_URL}/products",
                params=params,
                auth=(WC_KEY, WC_SECRET)
            )
            
            if response.status_code == 200:
                productos = response.json()
                return {
                    "success": True,
                    "productos": [
                        {
                            "id": p.get("id"),
                            "nombre": p.get("name"),
                            "precio": p.get("regular_price"),
                            "stock": p.get("stock_quantity")
                        }
                        for p in productos
                    ]
                }
            
            return {"success": False, "error": "Error obteniendo productos"}
    
    async def _analizar_competencia(self, producto: str, categoria: str) -> Dict[str, Any]:
        """Analiza competencia con Perplexity"""
        
        query = f"""Analiza la competencia en España para: {producto} ({categoria})

Proporciona:
1. Top 3 competidores directos y sus precios
2. Ventajas competitivas de cada uno
3. Puntos débiles que podemos explotar
4. Estrategia de precio recomendada
5. Diferenciación sugerida

Formato: Análisis estructurado"""
        
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                "https://api.perplexity.ai/chat/completions",
                headers={
                    "Authorization": f"Bearer {PERPLEXITY_KEY}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": "llama-3.1-sonar-large-128k-online",
                    "messages": [{"role": "user", "content": query}]
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "success": True,
                    "analisis": data["choices"][0]["message"]["content"]
                }
            
            return {"success": False, "error": "Error en análisis"}
    
    async def _generar_contenido(self, tipo: str, tema: str) -> Dict[str, Any]:
        """Genera contenido (blog, email, social)"""
        
        prompts = {
            "blog": f"Escribe un artículo de blog profesional sobre: {tema}. Incluye título SEO, introducción, 3 secciones con subtítulos, y conclusión. 800 palabras.",
            "email": f"Crea una campaña de email marketing sobre: {tema}. Incluye 3 asuntos A/B test, preheader, contenido HTML, y CTA.",
            "social": f"Genera 5 posts para redes sociales sobre: {tema}. Para Instagram, Facebook y Twitter. Incluye hashtags y emojis.",
        }
        
        prompt = prompts.get(tipo, f"Genera contenido sobre: {tema}")
        
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                self.openrouter_url,
                headers={
                    "Authorization": f"Bearer {OPENROUTER_KEY}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": "anthropic/claude-3.5-sonnet",
                    "messages": [{"role": "user", "content": prompt}]
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "success": True,
                    "contenido": data["choices"][0]["message"]["content"]
                }
            
            return {"success": False, "error": "Error generando contenido"}


# Instancia global del agente
agent = AIAgent()
