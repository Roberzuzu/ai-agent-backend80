"""
CEREBRO AI - AGENTE EJECUTIVO PROFESIONAL
Sistema de IA conectado a herramientasyaccesorios.store
VERSIÓN SIMPLIFICADA - SIN DEPENDENCIAS EXTERNAS
"""

import os
import httpx
import json
from datetime import datetime, timezone
from typing import Dict, List, Any, Optional
import logging

logger = logging.getLogger(__name__)


# PROMPT PRINCIPAL INTEGRADO
SYSTEM_PROMPT = """Eres CEREBRO, el asistente ejecutivo de herramientasyaccesorios.store.

🎯 TU ROL:
Eres el socio digital del negocio. No solo informas, EJECUTAS y RECOMIENDAS.

💼 CAPACIDADES:
- Gestión completa de productos WooCommerce
- Análisis de ventas y métricas
- Búsqueda en internet en tiempo real
- Automatización de tareas
- Recomendaciones estratégicas

🎨 TONO:
- Ejecutivo pero accesible
- Confiado y proactivo
- Orientado a resultados
- Sin jerga innecesaria

IMPORTANTE: Siempre da respuestas útiles y accionables. Si detectas una oportunidad, señálala."""


class CerebroAI:
    """
    Agente IA ejecutivo para gestión de e-commerce
    """
    
    def __init__(self, db, admin_id: str):
        self.db = db
        self.admin_id = admin_id
        
        # APIs disponibles (PRIORIDAD: Anthropic > OpenAI > Perplexity)
        self.anthropic_key = os.environ.get('ANTHROPIC_API_KEY')
        self.openai_key = os.environ.get('OPENAI_API_KEY')
        self.perplexity_key = os.environ.get('PERPLEXITY_API_KEY')
        self.openrouter_key = os.environ.get('OPENROUTER_API_KEY')
        
        # WooCommerce
        self.woo_url = os.environ.get('WOOCOMMERCE_URL')
        self.woo_key = os.environ.get('WOOCOMMERCE_CONSUMER_KEY')
        self.woo_secret = os.environ.get('WOOCOMMERCE_CONSUMER_SECRET')
        
        # WordPress
        self.wp_url = os.environ.get('WP_URL')
        self.wp_user = os.environ.get('WP_USER')
        self.wp_pass = os.environ.get('WP_PASS')
        
        # Telegram
        self.telegram_token = os.environ.get('TELEGRAM_BOT_TOKEN')
        self.admin_telegram_id = os.environ.get('ADMIN_TELEGRAM_ID', admin_id)

    async def procesar_comando(self, command: str, user_id: str, conversation_history: List[Dict] = None) -> Dict[str, Any]:
        """
        Procesa comandos de forma ejecutiva y profesional
        """
        try:
            # Cargar memoria
            if conversation_history is None:
                conversation_history = await self._cargar_memoria(user_id)
            
            # Construir contexto completo
            messages = [{"role": "system", "content": SYSTEM_PROMPT}]
            
            # Agregar historial reciente (últimas 10 interacciones)
            for msg in conversation_history[-10:]:
                messages.append({"role": "user", "content": msg.get("command", "")})
                messages.append({"role": "assistant", "content": msg.get("response", "")})
            
            # Comando actual
            messages.append({"role": "user", "content": command})
            
            # Llamar a IA
            ai_response = await self._llamar_ia_inteligente(messages)
            
            # Verificar que ai_response no esté vacío
            if not ai_response or len(ai_response.strip()) == 0:
                ai_response = "He recibido tu mensaje pero no pude generar una respuesta adecuada. Por favor, reformula tu pregunta."
            
            # Analizar si necesita ejecutar herramientas
            acciones_ejecutadas = await self._ejecutar_herramientas_inteligentes(command, ai_response, user_id)
            
            # Enriquecer respuesta con resultados de acciones
            if acciones_ejecutadas:
                ai_response = await self._enriquecer_respuesta(ai_response, acciones_ejecutadas)
            
            # Guardar en memoria
            await self._guardar_memoria(user_id, command, ai_response, acciones_ejecutadas)
            
            logger.info(f"✅ Respuesta generada: {len(ai_response)} caracteres")
            
            return {
                "success": True,
                "response": ai_response,
                "acciones": acciones_ejecutadas,
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
            
        except Exception as e:
            logger.error(f"❌ Error procesando comando: {str(e)}", exc_info=True)
            error_response = f"He encontrado un problema técnico: {str(e)[:100]}. Intentando alternativa..."
            return {
                "success": False,
                "response": error_response,
                "acciones": []
            }
    
    async def _llamar_ia_inteligente(self, messages: List[Dict]) -> str:
        """
        Llama a APIs de IA con fallback inteligente
        PRIORIDAD: Anthropic Claude > OpenAI > Perplexity
        """
        
        # 1. ANTHROPIC CLAUDE PRIMERO (mejor para agentes autónomos)
        if self.anthropic_key:
            try:
                logger.info("🔄 Llamando a Anthropic Claude...")
                async with httpx.AsyncClient(timeout=60.0) as client:
                    response = await client.post(
                        "https://api.anthropic.com/v1/messages",
                        headers={
                            "x-api-key": self.anthropic_key,
                            "anthropic-version": "2023-06-01",
                            "Content-Type": "application/json"
                        },
                        json={
                            "model": "claude-sonnet-4-20250514",
                            "max_tokens": 4096,
                            "messages": messages
                        }
                    )
                    
                    if response.status_code == 200:
                        data = response.json()
                        content = data['content'][0]['text']
                        logger.info(f"✅ Claude respondió: {len(content)} caracteres")
                        return content
                    else:
                        logger.warning(f"⚠️ Anthropic status: {response.status_code}")
            except Exception as e:
                logger.warning(f"⚠️ Anthropic error: {str(e)}")
        
        # 2. OpenAI como backup
        if self.openai_key:
            try:
                logger.info("🔄 Llamando a OpenAI...")
                async with httpx.AsyncClient(timeout=60.0) as client:
                    response = await client.post(
                        "https://api.openai.com/v1/chat/completions",
                        headers={
                            "Authorization": f"Bearer {self.openai_key}",
                            "Content-Type": "application/json"
                        },
                        json={
                            "model": "gpt-4o-mini",
                            "messages": messages,
                            "temperature": 0.7,
                            "max_tokens": 2000
                        }
                    )
                    
                    if response.status_code == 200:
                        data = response.json()
                        content = data['choices'][0]['message']['content']
                        logger.info(f"✅ OpenAI respondió: {len(content)} caracteres")
                        return content
                    else:
                        logger.warning(f"⚠️ OpenAI status: {response.status_code}")
            except Exception as e:
                logger.warning(f"⚠️ OpenAI error: {str(e)}")
        
        # 3. Perplexity como última opción
        if self.perplexity_key:
            try:
                logger.info("🔄 Llamando a Perplexity...")
                async with httpx.AsyncClient(timeout=60.0) as client:
                    response = await client.post(
                        "https://api.perplexity.ai/chat/completions",
                        headers={
                            "Authorization": f"Bearer {self.perplexity_key}",
                            "Content-Type": "application/json"
                        },
                        json={
                            "model": "llama-3.1-sonar-large-128k-online",
                            "messages": messages,
                            "temperature": 0.7,
                            "max_tokens": 2000
                        }
                    )
                    
                    if response.status_code == 200:
                        data = response.json()
                        content = data['choices'][0]['message']['content']
                        logger.info(f"✅ Perplexity respondió: {len(content)} caracteres")
                        return content
            except Exception as e:
                logger.warning(f"⚠️ Perplexity error: {str(e)}")
        
        logger.error("❌ Todas las APIs de IA fallaron")
        return "Estoy experimentando problemas de conexión con los servicios de IA. Por favor, verifica las API keys en las variables de entorno."
    
    async def _ejecutar_herramientas_inteligentes(self, command: str, ai_response: str, user_id: str) -> List[Dict]:
        """
        Ejecuta herramientas según el contexto
        """
        acciones = []
        command_lower = command.lower()
        
        # Listar productos
        if any(palabra in command_lower for palabra in ['lista productos', 'muestra productos', 'cuántos productos']):
            resultado = await self.listar_productos()
            acciones.append({
                "herramienta": "listar_productos",
                "resultado": resultado,
                "timestamp": datetime.now(timezone.utc).isoformat()
            })
        
        # Búsqueda en internet
        elif any(palabra in command_lower for palabra in ['busca en internet', 'investiga', 'qué dice internet']):
            resultado = await self.buscar_internet(command)
            acciones.append({
                "herramienta": "buscar_internet",
                "resultado": resultado,
                "timestamp": datetime.now(timezone.utc).isoformat()
            })
        
        return acciones
    
    async def _enriquecer_respuesta(self, ai_response: str, acciones: List[Dict]) -> str:
        """
        Enriquece la respuesta con resultados de acciones
        """
        if not acciones:
            return ai_response
        
        enriquecimiento = "\n\n📊 ACCIONES EJECUTADAS:\n"
        
        for accion in acciones:
            herramienta = accion.get("herramienta", "unknown")
            resultado = accion.get("resultado", {})
            
            if herramienta == "listar_productos":
                total = resultado.get("total", 0)
                enriquecimiento += f"✅ Productos encontrados: {total}\n"
            
            elif herramienta == "buscar_internet":
                if resultado.get("success"):
                    enriquecimiento += "✅ Búsqueda completada\n"
        
        return ai_response + enriquecimiento
    
    # HERRAMIENTAS
    
    async def buscar_internet(self, query: str) -> Dict:
        """Búsqueda en internet usando Perplexity"""
        if not self.perplexity_key:
            return {"error": "API de búsqueda no configurada", "success": False}
        
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    "https://api.perplexity.ai/chat/completions",
                    headers={
                        "Authorization": f"Bearer {self.perplexity_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": "llama-3.1-sonar-large-128k-online",
                        "messages": [{"role": "user", "content": f"Busca: {query}"}]
                    }
                )
                
                if response.status_code == 200:
                    data = response.json()
                    return {"resultado": data['choices'][0]['message']['content'], "success": True}
                return {"error": f"Status {response.status_code}", "success": False}
        except Exception as e:
            return {"error": str(e), "success": False}
    
    async def listar_productos(self, limit: int = 100) -> Dict:
        """Lista productos de WooCommerce"""
        if not all([self.woo_url, self.woo_key, self.woo_secret]):
            return {"error": "WooCommerce no configurado", "success": False}
        
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(
                    f"{self.woo_url}/wp-json/wc/v3/products",
                    params={"per_page": limit},
                    auth=(self.woo_key, self.woo_secret)
                )
                
                if response.status_code == 200:
                    productos = response.json()
                    return {"productos": productos, "total": len(productos), "success": True}
                return {"error": f"Status {response.status_code}", "success": False}
        except Exception as e:
            return {"error": str(e), "success": False}
    
    # MEMORIA
    
    async def _cargar_memoria(self, user_id: str, limit: int = 10) -> List[Dict]:
        """Carga memoria reciente"""
        try:
            conversaciones = await self.db["conversations"].find(
                {"user_id": user_id}
            ).sort("timestamp", -1).limit(limit).to_list(limit)
            
            return list(reversed(conversaciones))
        except Exception as e:
            logger.error(f"Error cargando memoria: {str(e)}")
            return []
    
    async def _guardar_memoria(self, user_id: str, command: str, response: str, acciones: List[Dict]):
        """Guarda interacción en memoria"""
        try:
            await self.db["conversations"].insert_one({
                "user_id": user_id,
                "command": command,
                "response": response,
                "acciones": acciones,
                "timestamp": datetime.now(timezone.utc),
                "status": "completed"
            })
        except Exception as e:
            logger.error(f"Error guardando memoria: {str(e)}")


# Alias para compatibilidad
CerebroUncensored = CerebroAI
