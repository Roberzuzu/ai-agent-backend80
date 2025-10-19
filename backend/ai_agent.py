"""
AI Agent - Cerebro Central del Sistema
Usa Claude 3.5 Sonnet para interpretar comandos y ejecutar acciones
Sistema de Memoria con RAG para recordar y buscar contexto
"""

import os
import json
import asyncio
import uuid
from typing import Dict, List, Any, Optional
import httpx
from datetime import datetime, timedelta
from motor.motor_asyncio import AsyncIOMotorClient
from openai import OpenAI
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# APIs disponibles
OPENROUTER_KEY = os.getenv("OPENROUTER_API_KEY")
PERPLEXITY_KEY = os.getenv("PERPLEXITY_API_KEY")
OPENAI_KEY = os.getenv("OPENAI_API_KEY")
FAL_KEY = os.getenv("FAL_API_KEY")
ABACUS_KEY = os.getenv("ABACUS_API_KEY")

# MongoDB para memoria
MONGO_URL = os.getenv("MONGO_URL")
mongo_client = AsyncIOMotorClient(MONGO_URL)
db = mongo_client[os.getenv("DB_NAME", "social_media_monetization")]

# OpenAI para embeddings
openai_client = OpenAI(api_key=OPENAI_KEY) if OPENAI_KEY else None

# WooCommerce
WC_KEY = "ck_4f50637d85ec404fff441fceb7b113b5050431ea"
WC_SECRET = "cs_e59ef18ea20d80ffdf835803ad2fdd834a4ba19f"
WC_URL = "https://herramientasyaccesorios.store/wp-json/wc/v3"

# WordPress
WP_USER = "agenteweb@herramientasyaccesorios.store"
WP_PASS = "RWWLW1eVi8whOS5OsUosb5AU"
WP_URL = "https://herramientasyaccesorios.store/wp-json/wp/v2"


class AIAgent:
    """Agente inteligente que interpreta y ejecuta comandos con memoria persistente"""
    
    def __init__(self):
        self.openrouter_url = "https://openrouter.ai/api/v1/chat/completions"
        self.conversations_collection = db["conversations"]
        self.memory_collection = db["agent_memory"]
    
    async def get_embedding(self, text: str) -> List[float]:
        """Genera embedding de un texto usando OpenAI"""
        if not openai_client:
            return []
        
        try:
            response = openai_client.embeddings.create(
                model="text-embedding-3-small",
                input=text
            )
            return response.data[0].embedding
        except Exception as e:
            print(f"Error generando embedding: {e}")
            return []
    
    async def save_to_memory(self, user_id: str, command: str, response: str, plan: Dict[str, Any]):
        """Guarda interacción en memoria con embedding para búsqueda"""
        try:
            # Generar embedding del comando y respuesta
            combined_text = f"{command} {response}"
            embedding = await self.get_embedding(combined_text)
            
            memory_entry = {
                "user_id": user_id,
                "command": command,
                "response": response,
                "plan": plan,
                "embedding": embedding,
                "timestamp": datetime.utcnow()
            }
            
            await self.memory_collection.insert_one(memory_entry)
        except Exception as e:
            print(f"Error guardando memoria: {e}")
    
    async def search_relevant_memories(self, user_id: str, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Busca memorias relevantes usando similaridad semántica (RAG)"""
        try:
            # Generar embedding de la query
            query_embedding = await self.get_embedding(query)
            if not query_embedding:
                return []
            
            # Obtener todas las memorias del usuario
            memories = await self.memory_collection.find(
                {"user_id": user_id, "embedding": {"$exists": True, "$ne": []}}
            ).sort("timestamp", -1).limit(50).to_list(50)
            
            if not memories:
                return []
            
            # Calcular similaridad
            memories_with_similarity = []
            query_vec = np.array(query_embedding).reshape(1, -1)
            
            for memory in memories:
                memory_vec = np.array(memory["embedding"]).reshape(1, -1)
                similarity = cosine_similarity(query_vec, memory_vec)[0][0]
                
                memories_with_similarity.append({
                    "command": memory["command"],
                    "response": memory["response"],
                    "timestamp": memory["timestamp"],
                    "similarity": float(similarity)
                })
            
            # Ordenar por similaridad y retornar top N
            memories_with_similarity.sort(key=lambda x: x["similarity"], reverse=True)
            return memories_with_similarity[:limit]
        
        except Exception as e:
            print(f"Error buscando memorias: {e}")
            return []
    
    async def get_conversation_history(self, user_id: str, limit: int = 10) -> List[Dict[str, str]]:
        """Obtiene el historial reciente de conversación"""
        try:
            conversations = await self.conversations_collection.find(
                {"user_id": user_id}
            ).sort("timestamp", -1).limit(limit).to_list(limit)
            
            # Invertir para orden cronológico
            conversations.reverse()
            
            history = []
            for conv in conversations:
                history.append({"role": "user", "content": conv["command"]})
                if conv.get("response"):
                    history.append({"role": "assistant", "content": conv["response"]})
            
            return history
        except Exception as e:
            print(f"Error obteniendo historial: {e}")
            return []
    
    async def save_conversation(self, user_id: str, command: str, response: str, plan: Dict[str, Any]):
        """Guarda conversación en MongoDB"""
        try:
            conversation_entry = {
                "user_id": user_id,
                "command": command,
                "response": response,
                "plan": plan,
                "timestamp": datetime.utcnow()
            }
            
            await self.conversations_collection.insert_one(conversation_entry)
        except Exception as e:
            print(f"Error guardando conversación: {e}")
    
    async def think(self, command: str, user_id: str) -> Dict[str, Any]:
        """
        El cerebro del agente - usa Claude 3.5 con memoria y contexto relevante (RAG)
        para analizar el comando y decidir qué acciones tomar
        """
        
        # Buscar memorias relevantes (RAG)
        relevant_memories = await self.search_relevant_memories(user_id, command, limit=3)
        
        # Obtener historial reciente de conversación
        recent_history = await self.get_conversation_history(user_id, limit=5)
        
        # Construir contexto de memoria
        memory_context = ""
        if relevant_memories:
            memory_context = "\n\n📚 CONTEXTO DE MEMORIAS RELEVANTES:\n"
            for idx, mem in enumerate(relevant_memories, 1):
                memory_context += f"{idx}. Comando anterior: {mem['command']}\n"
                memory_context += f"   Respuesta: {mem['response'][:200]}...\n"
                memory_context += f"   Similaridad: {mem['similarity']:.2f}\n\n"
        
        # Definir las herramientas disponibles (ahora con 17 herramientas)
        tools_description = """
Tienes acceso a estas HERRAMIENTAS:

**PRODUCTOS:**
1. **procesar_producto(product_id)** - Procesa un producto con AI (descripción, precio, imágenes)
2. **crear_producto(datos)** - Crea un nuevo producto en WooCommerce
3. **actualizar_producto(product_id, datos)** - Actualiza un producto existente
4. **eliminar_producto(product_id)** - Elimina un producto de WooCommerce
5. **obtener_productos(filtros)** - Lista productos de WooCommerce
6. **buscar_productos(query, filtros)** - Búsqueda avanzada de productos
7. **gestionar_inventario(operacion, datos)** - Gestión de stock y precios en bulk

**ANÁLISIS E INTELIGENCIA:**
8. **buscar_tendencias(categoria, pais)** - Busca productos tendencia con Perplexity
9. **analizar_precios(producto, categoria)** - Analiza precios óptimos con Abacus AI
10. **analizar_competencia(producto, categoria)** - Análisis de competencia con Perplexity
11. **obtener_estadisticas(tipo)** - Estadísticas del sitio (ventas, productos, visitas)
12. **analizar_ventas(periodo, filtros)** - Reportes detallados de ventas

**MARKETING:**
13. **crear_campana(tipo, producto_id, presupuesto)** - Crea campaña publicitaria
14. **crear_descuento(tipo, valor, productos)** - Crea cupones y promociones
15. **generar_contenido(tipo, tema)** - Crea blogs, emails, posts sociales

**CREATIVIDAD:**
16. **generar_imagenes(descripcion, cantidad)** - Genera imágenes con Fal AI

**INTEGRACIONES:**
17. **sincronizar_wordpress(accion, datos)** - Sincronización con WordPress
18. **optimizar_seo(producto_id)** - Optimiza SEO del producto

INSTRUCCIONES:
- Analiza el comando del usuario
- Usa el contexto de memorias relevantes para entender mejor
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
        
        # Crear el prompt para Claude con contexto completo
        messages = recent_history + [
            {
                "role": "user",
                "content": f"{tools_description}\n\n{memory_context}\n\nComando del usuario: {command}\n\nAnaliza usando el contexto de memorias y crea el plan de ejecución."
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
                    
                    # Extraer JSON del mensaje
                    try:
                        # Buscar JSON en el texto
                        json_start = assistant_message.find("{")
                        json_end = assistant_message.rfind("}") + 1
                        if json_start >= 0 and json_end > json_start:
                            plan_json = json.loads(assistant_message[json_start:json_end])
                            
                            # Guardar en memoria
                            await self.save_conversation(user_id, command, assistant_message, plan_json)
                            await self.save_to_memory(user_id, command, assistant_message, plan_json)
                            
                            return {
                                "success": True,
                                "plan": plan_json
                            }
                    except:
                        pass
                    
                    # Guardar incluso si no hay JSON
                    plan_fallback = {
                        "plan": "Ejecutar comando",
                        "respuesta_usuario": assistant_message,
                        "acciones": []
                    }
                    await self.save_conversation(user_id, command, assistant_message, plan_fallback)
                    await self.save_to_memory(user_id, command, assistant_message, plan_fallback)
                    
                    return {
                        "success": True,
                        "plan": plan_fallback
                    }
                
                return {"success": False, "error": f"Error: {response.status_code}"}
        
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def execute_action(self, action: Dict[str, Any]) -> Dict[str, Any]:
        """Ejecuta una acción específica usando las herramientas disponibles"""
        
        herramienta = action.get("herramienta")
        parametros = action.get("parametros", {})
        
        try:
            # PRODUCTOS
            if herramienta == "procesar_producto":
                return await self._procesar_producto(parametros.get("product_id"))
            
            elif herramienta == "crear_producto":
                return await self._crear_producto(parametros)
            
            elif herramienta == "actualizar_producto":
                return await self._actualizar_producto(
                    parametros.get("product_id"),
                    parametros.get("datos", {})
                )
            
            elif herramienta == "eliminar_producto":
                return await self._eliminar_producto(parametros.get("product_id"))
            
            elif herramienta == "obtener_productos":
                return await self._obtener_productos(parametros.get("filtros", {}))
            
            elif herramienta == "buscar_productos":
                return await self._buscar_productos(
                    parametros.get("query"),
                    parametros.get("filtros", {})
                )
            
            elif herramienta == "gestionar_inventario":
                return await self._gestionar_inventario(
                    parametros.get("operacion"),
                    parametros.get("datos", {})
                )
            
            # ANÁLISIS E INTELIGENCIA
            elif herramienta == "buscar_tendencias":
                return await self._buscar_tendencias(
                    parametros.get("categoria"),
                    parametros.get("pais", "España")
                )
            
            elif herramienta == "analizar_precios":
                return await self._analizar_precios(
                    parametros.get("producto"),
                    parametros.get("categoria")
                )
            
            elif herramienta == "analizar_competencia":
                return await self._analizar_competencia(
                    parametros.get("producto"),
                    parametros.get("categoria")
                )
            
            elif herramienta == "obtener_estadisticas":
                return await self._obtener_estadisticas(parametros.get("tipo"))
            
            elif herramienta == "analizar_ventas":
                return await self._analizar_ventas(
                    parametros.get("periodo"),
                    parametros.get("filtros", {})
                )
            
            # MARKETING
            elif herramienta == "crear_campana":
                return await self._crear_campana(
                    parametros.get("tipo"),
                    parametros.get("producto_id"),
                    parametros.get("presupuesto")
                )
            
            elif herramienta == "crear_descuento":
                return await self._crear_descuento(
                    parametros.get("tipo"),
                    parametros.get("valor"),
                    parametros.get("productos", [])
                )
            
            elif herramienta == "generar_contenido":
                return await self._generar_contenido(
                    parametros.get("tipo"),
                    parametros.get("tema")
                )
            
            # CREATIVIDAD
            elif herramienta == "generar_imagenes":
                return await self._generar_imagenes(
                    parametros.get("descripcion"),
                    parametros.get("cantidad", 2)
                )
            
            # INTEGRACIONES
            elif herramienta == "sincronizar_wordpress":
                return await self._sincronizar_wordpress(
                    parametros.get("accion"),
                    parametros.get("datos", {})
                )
            
            elif herramienta == "optimizar_seo":
                return await self._optimizar_seo(parametros.get("producto_id"))
            
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
    
    # ==========================================
    # NUEVAS HERRAMIENTAS
    # ==========================================
    
    async def _actualizar_producto(self, product_id: int, datos: Dict[str, Any]) -> Dict[str, Any]:
        """Actualiza un producto existente en WooCommerce"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.put(
                    f"{WC_URL}/products/{product_id}",
                    json=datos,
                    auth=(WC_KEY, WC_SECRET)
                )
                
                if response.status_code == 200:
                    product = response.json()
                    return {
                        "success": True,
                        "product_id": product.get("id"),
                        "name": product.get("name"),
                        "mensaje": f"Producto {product_id} actualizado correctamente"
                    }
                
                return {"success": False, "error": f"Error actualizando: {response.text}"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def _eliminar_producto(self, product_id: int) -> Dict[str, Any]:
        """Elimina un producto de WooCommerce"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.delete(
                    f"{WC_URL}/products/{product_id}",
                    params={"force": True},
                    auth=(WC_KEY, WC_SECRET)
                )
                
                if response.status_code == 200:
                    return {
                        "success": True,
                        "mensaje": f"Producto {product_id} eliminado correctamente"
                    }
                
                return {"success": False, "error": "Error eliminando producto"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def _buscar_productos(self, query: str, filtros: Dict[str, Any]) -> Dict[str, Any]:
        """Búsqueda avanzada de productos en WooCommerce"""
        try:
            params = {
                "search": query,
                "per_page": filtros.get("limite", 20),
                "orderby": filtros.get("ordenar_por", "relevance")
            }
            
            if filtros.get("categoria"):
                params["category"] = filtros["categoria"]
            if filtros.get("min_precio"):
                params["min_price"] = filtros["min_precio"]
            if filtros.get("max_precio"):
                params["max_price"] = filtros["max_precio"]
            if filtros.get("en_oferta"):
                params["on_sale"] = True
            
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
                        "total": len(productos),
                        "productos": [
                            {
                                "id": p.get("id"),
                                "nombre": p.get("name"),
                                "precio": p.get("regular_price"),
                                "precio_oferta": p.get("sale_price"),
                                "stock": p.get("stock_quantity"),
                                "url": p.get("permalink")
                            }
                            for p in productos
                        ]
                    }
                
                return {"success": False, "error": "Error en búsqueda"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def _gestionar_inventario(self, operacion: str, datos: Dict[str, Any]) -> Dict[str, Any]:
        """Gestión de inventario en bulk (stock, precios)"""
        try:
            resultados = []
            
            if operacion == "actualizar_stock":
                # datos = {"productos": [{"id": 123, "stock": 50}, ...]}
                for item in datos.get("productos", []):
                    async with httpx.AsyncClient() as client:
                        response = await client.put(
                            f"{WC_URL}/products/{item['id']}",
                            json={"stock_quantity": item["stock"]},
                            auth=(WC_KEY, WC_SECRET)
                        )
                        
                        resultados.append({
                            "id": item["id"],
                            "success": response.status_code == 200
                        })
            
            elif operacion == "actualizar_precios":
                # datos = {"productos": [{"id": 123, "precio": 29.99}, ...]}
                for item in datos.get("productos", []):
                    async with httpx.AsyncClient() as client:
                        response = await client.put(
                            f"{WC_URL}/products/{item['id']}",
                            json={"regular_price": str(item["precio"])},
                            auth=(WC_KEY, WC_SECRET)
                        )
                        
                        resultados.append({
                            "id": item["id"],
                            "success": response.status_code == 200
                        })
            
            return {
                "success": True,
                "operacion": operacion,
                "resultados": resultados,
                "actualizados": sum(1 for r in resultados if r["success"])
            }
        
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def _obtener_estadisticas(self, tipo: str) -> Dict[str, Any]:
        """Obtiene estadísticas del sitio"""
        try:
            async with httpx.AsyncClient() as client:
                # Obtener productos
                productos_response = await client.get(
                    f"{WC_URL}/products",
                    params={"per_page": 100},
                    auth=(WC_KEY, WC_SECRET)
                )
                
                # Obtener órdenes
                ordenes_response = await client.get(
                    f"{WC_URL}/orders",
                    params={"per_page": 100},
                    auth=(WC_KEY, WC_SECRET)
                )
                
                productos = productos_response.json() if productos_response.status_code == 200 else []
                ordenes = ordenes_response.json() if ordenes_response.status_code == 200 else []
                
                # Calcular estadísticas
                total_productos = len(productos)
                productos_sin_stock = sum(1 for p in productos if p.get("stock_quantity", 0) <= 0)
                productos_en_oferta = sum(1 for p in productos if p.get("on_sale", False))
                
                total_ventas = len([o for o in ordenes if o.get("status") == "completed"])
                ingresos_totales = sum(float(o.get("total", 0)) for o in ordenes if o.get("status") == "completed")
                
                return {
                    "success": True,
                    "tipo": tipo,
                    "productos": {
                        "total": total_productos,
                        "sin_stock": productos_sin_stock,
                        "en_oferta": productos_en_oferta
                    },
                    "ventas": {
                        "total_ordenes": total_ventas,
                        "ingresos_totales": ingresos_totales,
                        "ticket_promedio": ingresos_totales / total_ventas if total_ventas > 0 else 0
                    }
                }
        
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def _analizar_ventas(self, periodo: str, filtros: Dict[str, Any]) -> Dict[str, Any]:
        """Análisis detallado de ventas"""
        try:
            # Configurar rango de fechas según periodo
            now = datetime.utcnow()
            if periodo == "hoy":
                after = now.replace(hour=0, minute=0, second=0)
            elif periodo == "semana":
                after = now - timedelta(days=7)
            elif periodo == "mes":
                after = now - timedelta(days=30)
            elif periodo == "año":
                after = now - timedelta(days=365)
            else:
                after = now - timedelta(days=30)
            
            params = {
                "per_page": 100,
                "after": after.isoformat(),
                "status": "completed"
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{WC_URL}/orders",
                    params=params,
                    auth=(WC_KEY, WC_SECRET)
                )
                
                if response.status_code == 200:
                    ordenes = response.json()
                    
                    # Análisis
                    total_ordenes = len(ordenes)
                    ingresos = sum(float(o.get("total", 0)) for o in ordenes)
                    
                    # Productos más vendidos
                    productos_vendidos = {}
                    for orden in ordenes:
                        for item in orden.get("line_items", []):
                            prod_id = item.get("product_id")
                            cantidad = item.get("quantity", 0)
                            productos_vendidos[prod_id] = productos_vendidos.get(prod_id, 0) + cantidad
                    
                    top_productos = sorted(
                        productos_vendidos.items(),
                        key=lambda x: x[1],
                        reverse=True
                    )[:5]
                    
                    return {
                        "success": True,
                        "periodo": periodo,
                        "resumen": {
                            "total_ordenes": total_ordenes,
                            "ingresos_totales": ingresos,
                            "ticket_promedio": ingresos / total_ordenes if total_ordenes > 0 else 0
                        },
                        "top_productos": [
                            {"product_id": pid, "unidades_vendidas": cant}
                            for pid, cant in top_productos
                        ]
                    }
                
                return {"success": False, "error": "Error obteniendo ventas"}
        
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def _crear_campana(self, tipo: str, producto_id: int, presupuesto: float) -> Dict[str, Any]:
        """Crea una campaña publicitaria en MongoDB"""
        try:
            campana = {
                "id": str(uuid.uuid4()),
                "tipo": tipo,
                "producto_id": producto_id,
                "presupuesto": presupuesto,
                "estado": "activa",
                "created_at": datetime.utcnow()
            }
            
            await db["campaigns"].insert_one(campana)
            
            return {
                "success": True,
                "campana_id": campana["id"],
                "mensaje": f"Campaña {tipo} creada con presupuesto de ${presupuesto}"
            }
        
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def _crear_descuento(self, tipo: str, valor: float, productos: List[int]) -> Dict[str, Any]:
        """Crea cupón de descuento en WooCommerce"""
        try:
            import random
            import string
            
            # Generar código único
            codigo = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
            
            cupon_data = {
                "code": codigo,
                "discount_type": tipo,  # percent, fixed_cart, fixed_product
                "amount": str(valor),
                "individual_use": True,
                "product_ids": productos,
                "usage_limit": 100
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{WC_URL}/coupons",
                    json=cupon_data,
                    auth=(WC_KEY, WC_SECRET)
                )
                
                if response.status_code == 201:
                    cupon = response.json()
                    return {
                        "success": True,
                        "codigo": codigo,
                        "cupon_id": cupon.get("id"),
                        "mensaje": f"Cupón {codigo} creado: {valor}{'%' if tipo == 'percent' else '€'} de descuento"
                    }
                
                return {"success": False, "error": "Error creando cupón"}
        
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def _sincronizar_wordpress(self, accion: str, datos: Dict[str, Any]) -> Dict[str, Any]:
        """Sincronización con WordPress"""
        try:
            if accion == "publicar_articulo":
                post_data = {
                    "title": datos.get("titulo"),
                    "content": datos.get("contenido"),
                    "status": "publish"
                }
                
                async with httpx.AsyncClient() as client:
                    response = await client.post(
                        f"{WP_URL}/posts",
                        json=post_data,
                        auth=(WP_USER, WP_PASS)
                    )
                    
                    if response.status_code == 201:
                        post = response.json()
                        return {
                            "success": True,
                            "post_id": post.get("id"),
                            "url": post.get("link"),
                            "mensaje": "Artículo publicado en WordPress"
                        }
            
            return {"success": False, "error": "Acción no soportada"}
        
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def _optimizar_seo(self, producto_id: int) -> Dict[str, Any]:
        """Optimiza SEO de un producto"""
        from ai_integrations import generate_seo_content
        
        try:
            # Obtener producto
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{WC_URL}/products/{producto_id}",
                    auth=(WC_KEY, WC_SECRET)
                )
                
                if response.status_code != 200:
                    return {"success": False, "error": "Producto no encontrado"}
                
                producto = response.json()
                
                # Generar contenido SEO
                seo_result = await generate_seo_content(
                    producto.get("name"),
                    producto.get("categories", [{}])[0].get("name", "general")
                )
                
                if seo_result.get("success"):
                    # Actualizar producto con contenido SEO
                    update_data = {
                        "description": seo_result.get("description"),
                        "short_description": seo_result.get("meta_description")
                    }
                    
                    update_response = await client.put(
                        f"{WC_URL}/products/{producto_id}",
                        json=update_data,
                        auth=(WC_KEY, WC_SECRET)
                    )
                    
                    if update_response.status_code == 200:
                        return {
                            "success": True,
                            "mensaje": f"SEO optimizado para producto {producto_id}",
                            "keywords": seo_result.get("keywords", [])
                        }
                
                return {"success": False, "error": "Error optimizando SEO"}
        
        except Exception as e:
            return {"success": False, "error": str(e)}


# Instancia global del agente
agent = AIAgent()
