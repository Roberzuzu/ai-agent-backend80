"""
Cerebro AI - Core Agent con Sistema de Herramientas
Versión completa con autonomía controlada
"""

import os
import httpx
import json
from datetime import datetime, timezone
from typing import Dict, List, Any, Optional
import logging

logger = logging.getLogger(__name__)


class CerebroAgent:
    """
    Agente inteligente con capacidades de:
    - Conversación avanzada
    - Ejecución de acciones en WooCommerce
    - Sistema de autorización para acciones críticas
    - Memoria persistente
    """
    
    def __init__(self, db, admin_telegram_id: str):
        self.db = db
        self.admin_telegram_id = admin_telegram_id
        
        # APIs disponibles
        self.perplexity_key = os.environ.get('PERPLEXITY_API_KEY')
        self.openai_key = os.environ.get('OPENAI_API_KEY')
        self.openrouter_key = os.environ.get('OPENROUTER_API_KEY')
        
        # WooCommerce
        self.woo_url = os.environ.get('WOOCOMMERCE_URL')
        self.woo_key = os.environ.get('WOOCOMMERCE_CONSUMER_KEY')
        self.woo_secret = os.environ.get('WOOCOMMERCE_CONSUMER_SECRET')
        
        # Telegram
        self.telegram_token = os.environ.get('TELEGRAM_BOT_TOKEN')
        
        # Herramientas disponibles
        self.tools = {
            'buscar_internet': self.buscar_internet,
            'crear_producto': self.crear_producto,
            'modificar_producto': self.modificar_producto,
            'listar_productos': self.listar_productos,
            'analizar_ventas': self.analizar_ventas,
            'crear_oferta': self.crear_oferta,
        }
        
        # System prompt personalizado
        self.system_prompt = """Eres Cerebro AI, asistente ejecutivo experto en WooCommerce y e-commerce.

CAPACIDADES:
- Gestión completa de productos (crear, modificar, eliminar)
- Análisis de ventas y métricas
- Búsqueda en internet para información actualizada
- Optimización de catálogos y precios
- Creación de estrategias de marketing

COMPORTAMIENTO:
- Proactivo: sugiere mejoras y oportunidades
- Ejecutivo: tomas decisiones basadas en datos
- Profesional pero cercano
- Siempre explica qué vas a hacer ANTES de hacerlo

REGLAS CRÍTICAS:
1. Para acciones SIMPLES (buscar, listar, analizar): ejecuta directamente
2. Para acciones CRÍTICAS (crear, modificar, eliminar productos/precios): 
   - Primero explica QUÉ vas a hacer y POR QUÉ
   - Pide confirmación
   - Solo ejecutas tras confirmación

MEMORIA:
- Recuerdas conversaciones previas con cada usuario
- Aprendes de las preferencias del administrador
- Mantienes contexto de proyectos en curso

Responde siempre en español, de forma clara y útil."""

    async def procesar_comando(self, command: str, user_id: str, conversation_history: List[Dict] = None) -> Dict[str, Any]:
        """
        Procesa un comando del usuario
        
        Args:
            command: Comando del usuario
            user_id: ID del usuario
            conversation_history: Historial de conversación previo
            
        Returns:
            Dict con respuesta y acciones ejecutadas
        """
        try:
            # Cargar memoria del usuario
            if conversation_history is None:
                conversation_history = await self._cargar_memoria(user_id)
            
            # Construir contexto
            messages = [{"role": "system", "content": self.system_prompt}]
            
            # Agregar historial reciente (últimas 10 interacciones)
            for msg in conversation_history[-10:]:
                messages.append({"role": "user", "content": msg.get("command", "")})
                messages.append({"role": "assistant", "content": msg.get("response", "")})
            
            # Agregar comando actual
            messages.append({"role": "user", "content": command})
            
            # Llamar a la IA para obtener respuesta
            ai_response = await self._llamar_ia(messages)
            
            # Analizar si necesita ejecutar herramientas
            acciones_ejecutadas = await self._analizar_y_ejecutar_herramientas(command, ai_response, user_id)
            
            # Guardar en memoria
            await self._guardar_memoria(user_id, command, ai_response, acciones_ejecutadas)
            
            return {
                "success": True,
                "mensaje": ai_response,
                "acciones": acciones_ejecutadas,
                "requiere_autorizacion": self._requiere_autorizacion(command)
            }
            
        except Exception as e:
            logger.error(f"Error procesando comando: {str(e)}", exc_info=True)
            return {
                "success": False,
                "mensaje": f"Error al procesar tu solicitud: {str(e)}",
                "acciones": []
            }
    
    async def _llamar_ia(self, messages: List[Dict]) -> str:
        """Llama a la API de IA (Perplexity > OpenAI > OpenRouter)"""
        
        # Intentar Perplexity primero (mejor para búsquedas)
        if self.perplexity_key:
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
                            "messages": messages,
                            "temperature": 0.7,
                            "max_tokens": 2000
                        }
                    )
                    
                    if response.status_code == 200:
                        data = response.json()
                        return data['choices'][0]['message']['content']
            except Exception as e:
                logger.warning(f"Perplexity error: {str(e)}")
        
        # Fallback a OpenAI
        if self.openai_key:
            try:
                async with httpx.AsyncClient(timeout=30.0) as client:
                    response = await client.post(
                        "https://api.openai.com/v1/chat/completions",
                        headers={
                            "Authorization": f"Bearer {self.openai_key}",
                            "Content-Type": "application/json"
                        },
                        json={
                            "model": "gpt-4-turbo-preview",
                            "messages": messages,
                            "temperature": 0.7,
                            "max_tokens": 2000
                        }
                    )
                    
                    if response.status_code == 200:
                        data = response.json()
                        return data['choices'][0]['message']['content']
            except Exception as e:
                logger.warning(f"OpenAI error: {str(e)}")
        
        # Fallback a OpenRouter
        if self.openrouter_key:
            try:
                async with httpx.AsyncClient(timeout=30.0) as client:
                    response = await client.post(
                        "https://openrouter.ai/api/v1/chat/completions",
                        headers={
                            "Authorization": f"Bearer {self.openrouter_key}",
                            "Content-Type": "application/json"
                        },
                        json={
                            "model": "anthropic/claude-3-sonnet",
                            "messages": messages
                        }
                    )
                    
                    if response.status_code == 200:
                        data = response.json()
                        return data['choices'][0]['message']['content']
            except Exception as e:
                logger.warning(f"OpenRouter error: {str(e)}")
        
        return "Lo siento, estoy experimentando problemas técnicos. Intenta de nuevo en unos momentos."
    
    async def _analizar_y_ejecutar_herramientas(self, command: str, ai_response: str, user_id: str) -> List[Dict]:
        """
        Analiza si el comando requiere ejecutar herramientas
        y las ejecuta si es apropiado
        """
        acciones = []
        command_lower = command.lower()
        
        # Detección simple de intenciones (puedes mejorar con NLP)
        
        # Búsqueda en internet
        if any(palabra in command_lower for palabra in ['busca', 'investiga', 'encuentra información', 'qué hay de nuevo']):
            resultado = await self.buscar_internet(command)
            acciones.append({
                "herramienta": "buscar_internet",
                "resultado": resultado,
                "timestamp": datetime.now(timezone.utc).isoformat()
            })
        
        # Listar productos (acción segura, no requiere autorización)
        if any(palabra in command_lower for palabra in ['lista productos', 'muestra productos', 'qué productos', 'cuántos productos']):
            resultado = await self.listar_productos()
            acciones.append({
                "herramienta": "listar_productos",
                "resultado": resultado,
                "timestamp": datetime.now(timezone.utc).isoformat()
            })
        
        # Crear producto (requiere autorización si user_id != admin)
        if any(palabra in command_lower for palabra in ['crea producto', 'crear producto', 'nuevo producto', 'agregar producto']):
            if user_id == self.admin_telegram_id:
                # Aquí extraerías los parámetros del comando
                # Por ahora, guardamos la intención para procesar después
                acciones.append({
                    "herramienta": "crear_producto",
                    "estado": "pendiente_parametros",
                    "requiere_autorizacion": False
                })
            else:
                await self._solicitar_autorizacion(user_id, command)
                acciones.append({
                    "herramienta": "crear_producto",
                    "estado": "pendiente_autorizacion"
                })
        
        return acciones
    
    def _requiere_autorizacion(self, command: str) -> bool:
        """Determina si un comando requiere autorización del admin"""
        acciones_criticas = [
            'crear producto', 'eliminar producto', 'modificar precio',
            'crear oferta', 'cambiar stock', 'eliminar', 'borrar'
        ]
        command_lower = command.lower()
        return any(accion in command_lower for accion in acciones_criticas)
    
    async def _solicitar_autorizacion(self, user_id: str, command: str):
        """Envía notificación al admin por Telegram solicitando autorización"""
        if not self.telegram_token:
            return
        
        try:
            mensaje = f"""
🤖 **Solicitud de Autorización**

Usuario: {user_id}
Comando: {command}

¿Autorizar esta acción?
"""
            
            async with httpx.AsyncClient() as client:
                await client.post(
                    f"https://api.telegram.org/bot{self.telegram_token}/sendMessage",
                    json={
                        "chat_id": self.admin_telegram_id,
                        "text": mensaje,
                        "parse_mode": "Markdown"
                    }
                )
        except Exception as e:
            logger.error(f"Error enviando notificación Telegram: {str(e)}")
    
    async def _cargar_memoria(self, user_id: str) -> List[Dict]:
        """Carga el historial de conversación del usuario desde MongoDB"""
        try:
            conversaciones = await self.db["conversations"].find(
                {"user_id": user_id}
            ).sort("timestamp", -1).limit(20).to_list(20)
            
            return list(reversed(conversaciones))
        except Exception as e:
            logger.error(f"Error cargando memoria: {str(e)}")
            return []
    
    async def _guardar_memoria(self, user_id: str, command: str, response: str, acciones: List[Dict]):
        """Guarda la interacción en MongoDB"""
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
    
    # ============================================
    # HERRAMIENTAS DISPONIBLES
    # ============================================
    
    async def buscar_internet(self, query: str) -> Dict:
        """Busca información en internet usando Perplexity"""
        if not self.perplexity_key:
            return {"error": "API de búsqueda no configurada"}
        
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
                        "messages": [
                            {"role": "user", "content": f"Busca información actualizada sobre: {query}"}
                        ]
                    }
                )
                
                if response.status_code == 200:
                    data = response.json()
                    return {
                        "resultado": data['choices'][0]['message']['content'],
                        "success": True
                    }
        except Exception as e:
            return {"error": str(e), "success": False}
    
    async def listar_productos(self, limit: int = 10) -> Dict:
        """Lista productos de WooCommerce"""
        if not all([self.woo_url, self.woo_key, self.woo_secret]):
            return {"error": "WooCommerce no configurado"}
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.woo_url}/wp-json/wc/v3/products",
                    params={"per_page": limit},
                    auth=(self.woo_key, self.woo_secret)
                )
                
                if response.status_code == 200:
                    productos = response.json()
                    return {
                        "productos": productos,
                        "total": len(productos),
                        "success": True
                    }
        except Exception as e:
            return {"error": str(e), "success": False}
    
    async def crear_producto(self, datos: Dict) -> Dict:
        """Crea un producto en WooCommerce"""
        if not all([self.woo_url, self.woo_key, self.woo_secret]):
            return {"error": "WooCommerce no configurado"}
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.woo_url}/wp-json/wc/v3/products",
                    json=datos,
                    auth=(self.woo_key, self.woo_secret)
                )
                
                if response.status_code == 201:
                    return {
                        "producto": response.json(),
                        "success": True
                    }
        except Exception as e:
            return {"error": str(e), "success": False}
    
    async def modificar_producto(self, product_id: int, datos: Dict) -> Dict:
        """Modifica un producto en WooCommerce"""
        if not all([self.woo_url, self.woo_key, self.woo_secret]):
            return {"error": "WooCommerce no configurado"}
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.put(
                    f"{self.woo_url}/wp-json/wc/v3/products/{product_id}",
                    json=datos,
                    auth=(self.woo_key, self.woo_secret)
                )
                
                if response.status_code == 200:
                    return {
                        "producto": response.json(),
                        "success": True
                    }
        except Exception as e:
            return {"error": str(e), "success": False}
    
    async def analizar_ventas(self, periodo: str = "month") -> Dict:
        """Analiza ventas de WooCommerce"""
        if not all([self.woo_url, self.woo_key, self.woo_secret]):
            return {"error": "WooCommerce no configurado"}
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.woo_url}/wp-json/wc/v3/reports/sales",
                    params={"period": periodo},
                    auth=(self.woo_key, self.woo_secret)
                )
                
                if response.status_code == 200:
                    return {
                        "ventas": response.json(),
                        "success": True
                    }
        except Exception as e:
            return {"error": str(e), "success": False}
    
    async def crear_oferta(self, product_id: int, precio_oferta: float, fecha_inicio: str, fecha_fin: str) -> Dict:
        """Crea una oferta para un producto"""
        datos = {
            "sale_price": str(precio_oferta),
            "date_on_sale_from": fecha_inicio,
            "date_on_sale_to": fecha_fin
        }
        return await self.modificar_producto(product_id, datos)
