"""
AI Agent - Cerebro Central del Sistema
Usa Claude 3.5 Sonnet para interpretar comandos y ejecutar acciones
Sistema de Memoria con RAG para recordar y buscar contexto
"""

import os
import json
import asyncio
from typing import Dict, List, Any, Optional
import httpx
from datetime import datetime
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
