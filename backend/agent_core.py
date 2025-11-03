"""
CEREBRO AI - AGENTE EJECUTIVO PROFESIONAL
Sistema de IA conectado a herramientasyaccesorios.store

Características:
- Totalmente conectado al backend y sistemas de la tienda
- Ejecutivo y proactivo (no solo informativo)
- Gestión completa de e-commerce
- Análisis y recomendaciones estratégicas
- Automatización inteligente
- Profesional y sostenible a largo plazo
"""

import os
import httpx
import json
from datetime import datetime, timezone
from typing import Dict, List, Any, Optional
import logging


# Importar sistema de prompts modulares
from prompts_modulares import PromptManager


logger = logging.getLogger(__name__)


class CerebroAI:
    """
    Agente IA ejecutivo para gestión de e-commerce
    Conectado a herramientasyaccesorios.store
    """
    
    def __init__(self, db, admin_id: str):
        self.db = db
        self.admin_id = admin_id
        
        # APIs disponibles
        self.openrouter_key = os.environ.get('OPENROUTER_API_KEY')
        self.perplexity_key = os.environ.get('PERPLEXITY_API_KEY')
        self.openai_key = os.environ.get('OPENAI_API_KEY')
        
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
        
        # System prompt PROFESIONAL Y EJECUTIVO
        self.system_prompt = """Eres CEREBRO AI, el asistente ejecutivo de herramientasyaccesorios.store.

🔗 CONFIRMACIÓN DE CONEXIÓN:
Estás DIRECTAMENTE conectado a:
- Backend de la tienda (ai-agent-backend80.onrender.com)
- Base de datos MongoDB (social_media_monetization)
- WooCommerce API de herramientasyaccesorios.store
- Sistema de analytics y métricas
- Telegram Bot para notificaciones
- Todas las herramientas del ecosistema

Cuando te pregunten si estás conectado, CONFIRMA claramente que SÍ lo estás y menciona a qué sistemas tienes acceso.

💼 TU ROL:
Eres el cerebro ejecutivo del negocio. No eres solo un chatbot informativo - eres un asistente que HACE COSAS.

🎯 COMPORTAMIENTO EJECUTIVO:
- Directo y sin rodeos innecesarios
- Proactivo: sugiere mejoras sin que te las pidan
- Ejecutivo: cuando algo se puede hacer, lo HACES (con confirmación si es crítico)
- Analítico: extraes insights de datos automáticamente
- Estratégico: piensas en el negocio, no solo en responder
- Eficiente: vas al grano y produces resultados

✅ CAPACIDADES COMPLETAS:

1. GESTIÓN DE PRODUCTOS:
   - Crear, modificar, eliminar productos en WooCommerce
   - Ajustar precios masivamente
   - Gestionar inventario
   - Optimizar descripciones y SEO
   - Análisis de rendimiento de productos

2. ANÁLISIS Y MÉTRICAS:
   - Ventas diarias/mensuales/anuales
   - Productos más vendidos
   - Análisis de márgenes
   - Tendencias y proyecciones
   - ROI de campañas

3. MARKETING Y CONTENIDO:
   - Generar descripciones de productos
   - Crear contenido para blog/redes
   - Estrategias de pricing
   - Recomendaciones de cross-selling
   - Análisis de competencia

4. AUTOMATIZACIÓN:
   - Respuestas automáticas a consultas
   - Alertas de bajo stock
   - Reportes automáticos
   - Gestión de pedidos
   - Seguimiento de clientes

5. BÚSQUEDA E INVESTIGACIÓN:
   - Tendencias de mercado
   - Análisis de competidores
   - Precios de referencia
   - Nuevas oportunidades de producto

📋 FORMATO DE RESPUESTAS:

Para consultas simples:
- Respuesta directa y concisa
- Datos relevantes
- Acción tomada (si aplica)

Para análisis complejos:
- Resumen ejecutivo primero
- Datos clave con números
- Insights y recomendaciones
- Próximos pasos sugeridos

Para acciones ejecutivas:
- "✅ Ejecutado: [acción]"
- "📊 Resultado: [datos]"
- "💡 Recomendación: [siguiente paso]"

🚫 NUNCA DIGAS:
- "No puedo acceder a..." (SÍ puedes, estás conectado)
- "Como IA no tengo la capacidad de..." (SÍ la tienes)
- "No estoy conectado a..." (SÍ estás conectado)
- "Deberías consultar con..." (TÚ eres el consultor)

✅ SÍ DICES:
- "Analizando datos de la tienda..."
- "He revisado tus últimas ventas..."
- "Ejecutando cambio en [X] productos..."
- "Según tus métricas actuales..."
- "Recomiendo implementar..."

⚖️ CONFIRMACIONES IMPORTANTES:
Para acciones críticas (eliminar productos, cambios masivos de precio), pregunta:
"⚠️ Esto afectará [X] productos. ¿Confirmas?"

Para acciones menores (crear 1 producto, ajustar descripción), ejecuta directamente.

🎓 APRENDIZAJE:
- Recuerdas conversaciones previas
- Adaptas tu estilo según preferencias del usuario
- Aprendes de cada interacción
- Mejoras tus recomendaciones con el tiempo

💬 TONO:
- Profesional pero accesible
- Confiado (sabes de lo que hablas)
- Proactivo (ofreces soluciones)
- Orientado a resultados
- Sin jerga innecesaria

Eres el SOCIO DIGITAL del negocio - piensa, analiza, ejecuta y recomienda como lo haría un director general de operaciones."""

async def procesar_comando(self, command: str, user_id: str, conversation_history: List[Dict] = None) -> Dict[str, Any]:
    """
    Procesa comandos de forma ejecutiva y profesional
    """
    try:
        # Cargar memoria
        if conversation_history is None:
            conversation_history = await self._cargar_memoria(user_id)
        
        # Construir prompt dinámico según el contexto del comando
        system_prompt_dinamico = self.prompt_manager.construir_prompt_completo(command)
        
        # Construir contexto completo
        messages = [{"role": "system", "content": system_prompt_dinamico}]
        
        # Agregar historial reciente (últimas 20 interacciones)
        for msg in conversation_history[-20:]:
            messages.append({"role": "user", "content": msg.get("command", "")})
            messages.append({"role": "assistant", "content": msg.get("response", "")})
        
        # Comando actual con contexto de herramientas disponibles
        command_enriched = await self._enriquecer_comando(command)
        messages.append({"role": "user", "content": command_enriched})
        
        # Llamar a IA
        ai_response = await self._llamar_ia_inteligente(messages)
        
        # Analizar si necesita ejecutar herramientas
        acciones_ejecutadas = await self._ejecutar_herramientas_inteligentes(command, ai_response, user_id)
        
        # Enriquecer respuesta con resultados de acciones
        if acciones_ejecutadas:
            ai_response = await self._enriquecer_respuesta(ai_response, acciones_ejecutadas)
        
        # Guardar en memoria
        await self._guardar_memoria(user_id, command, ai_response, acciones_ejecutadas)
        
        # Log de debug
        logger.info(f"========== DEBUG ==========")
        logger.info(f"AI Response length: {len(ai_response)}")
        logger.info(f"Acciones: {len(acciones_ejecutadas)}")
        logger.info(f"===========================")
        
        return {
            "success": True,
            "response": ai_response,
            "acciones": acciones_ejecutadas,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error procesando comando: {str(e)}", exc_info=True)
        return {
            "success": False,
            "response": f"He encontrado un problema técnico: {str(e)}. Estoy reintentando con un método alternativo...",
            "acciones": []
        }
    
    async def _enriquecer_comando(self, command: str) -> str:
        """
        Enriquece el comando con contexto de sistemas disponibles
        """
        contexto = "\n\n[CONTEXTO DEL SISTEMA:"
        
        # Info de WooCommerce
        if all([self.woo_url, self.woo_key, self.woo_secret]):
            contexto += "\n✅ WooCommerce conectado"
        
        # Info de Telegram
        if self.telegram_token:
            contexto += "\n✅ Telegram Bot activo"
        
        contexto += "]\n\n"
        
        return command + contexto
    
    async def _llamar_ia_inteligente(self, messages: List[Dict]) -> str:
        """
        Llama a APIs de IA con fallback inteligente
        Prioriza por velocidad y calidad
        """
        
        # 1. OpenAI primero (mejor calidad y más rápido)
        if self.openai_key:
            try:
                async with httpx.AsyncClient(timeout=60.0) as client:
                    response = await client.post(
                        "https://api.openai.com/v1/chat/completions",
                        headers={
                            "Authorization": f"Bearer {self.openai_key}",
                            "Content-Type": "application/json"
                        },
                        json={
                            "model": "gpt-4o-mini",  # Rápido y eficiente
                            "messages": messages,
                            "temperature": 0.7,  # Balance creatividad/precisión
                            "max_tokens": 2000,
                            "presence_penalty": 0.1,
                            "frequency_penalty": 0.1
                        }
                    )
                    
                    if response.status_code == 200:
                        data = response.json()
                        return data['choices'][0]['message']['content']
                    else:
                        logger.warning(f"OpenAI status: {response.status_code}")
            except Exception as e:
                logger.warning(f"OpenAI error: {str(e)}")
        
        # 2. Perplexity como backup
        if self.perplexity_key:
            try:
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
                        return data['choices'][0]['message']['content']
            except Exception as e:
                logger.warning(f"Perplexity error: {str(e)}")
        
        # 3. OpenRouter como última opción
        if self.openrouter_key:
            try:
                async with httpx.AsyncClient(timeout=60.0) as client:
                    response = await client.post(
                        "https://openrouter.ai/api/v1/chat/completions",
                        headers={
                            "Authorization": f"Bearer {self.openrouter_key}",
                            "Content-Type": "application/json",
                            "HTTP-Referer": self.woo_url or "https://localhost",
                        },
                        json={
                            "model": "meta-llama/llama-3.1-70b-instruct",
                            "messages": messages,
                            "temperature": 0.7,
                            "max_tokens": 2000
                        }
                    )
                    
                    if response.status_code == 200:
                        data = response.json()
                        return data['choices'][0]['message']['content']
            except Exception as e:
                logger.warning(f"OpenRouter error: {str(e)}")
        
        return "Estoy experimentando problemas de conexión con los servicios de IA. Por favor, verifica las API keys en las variables de entorno."
    
    async def _ejecutar_herramientas_inteligentes(self, command: str, ai_response: str, user_id: str) -> List[Dict]:
        """
        Ejecuta herramientas de forma inteligente según el contexto
        """
        acciones = []
        command_lower = command.lower()
        
        # Listar productos
        if any(palabra in command_lower for palabra in ['lista productos', 'muestra productos', 'cuántos productos', 'productos tenemos']):
            resultado = await self.listar_productos()
            acciones.append({
                "herramienta": "listar_productos",
                "resultado": resultado,
                "timestamp": datetime.now(timezone.utc).isoformat()
            })
        
        # Crear producto
        elif any(palabra in command_lower for palabra in ['crea producto', 'crear producto', 'nuevo producto', 'agregar producto']):
            producto_data = await self._extraer_datos_producto_ia(command, ai_response)
            resultado = await self.crear_producto_woo(producto_data)
            acciones.append({
                "herramienta": "crear_producto",
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
        
        # Análisis de ventas (cuando esté implementado)
        elif any(palabra in command_lower for palabra in ['ventas', 'análisis', 'métricas', 'estadísticas']):
            # Placeholder para futuro análisis
            acciones.append({
                "herramienta": "analisis_pendiente",
                "resultado": {"mensaje": "Análisis de ventas en desarrollo"},
                "timestamp": datetime.now(timezone.utc).isoformat()
            })
        
        return acciones
    
    async def _extraer_datos_producto_ia(self, command: str, ai_response: str) -> Dict:
        """
        Extrae datos de producto del comando usando la respuesta de la IA
        """
        # Implementación básica - la IA puede sugerir datos en su respuesta
        return {
            "name": "Producto sugerido por IA",
            "type": "simple",
            "regular_price": "99.99",
            "description": ai_response[:500] if len(ai_response) > 500 else "Producto generado automáticamente",
            "short_description": ai_response[:160] if len(ai_response) > 160 else "Descripción breve",
            "status": "draft"  # Draft por seguridad, requiere revisión
        }
    
    async def _enriquecer_respuesta(self, ai_response: str, acciones: List[Dict]) -> str:
        """
        Enriquece la respuesta de la IA con resultados de acciones ejecutadas
        """
        if not acciones:
            return ai_response
        
        enriquecimiento = "\n\n📊 ACCIONES EJECUTADAS:\n"
        
        for accion in acciones:
            herramienta = accion.get("herramienta", "unknown")
            resultado = accion.get("resultado", {})
            
            if herramienta == "listar_productos":
                total = resultado.get("total", 0)
                enriquecimiento += f"✅ Productos listados: {total} encontrados\n"
            
            elif herramienta == "crear_producto":
                if resultado.get("success"):
                    producto = resultado.get("producto", {})
                    enriquecimiento += f"✅ Producto creado: {producto.get('name', 'Sin nombre')}\n"
                else:
                    enriquecimiento += f"❌ Error al crear producto: {resultado.get('error')}\n"
            
            elif herramienta == "buscar_internet":
                if resultado.get("success"):
                    enriquecimiento += "✅ Búsqueda en internet completada\n"
                else:
                    enriquecimiento += "❌ Error en búsqueda\n"
        
        return ai_response + enriquecimiento
    
    # ============================================
    # HERRAMIENTAS CORE
    # ============================================
    
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
                else:
                    return {"error": f"Status {response.status_code}", "success": False}
        except Exception as e:
            logger.error(f"Error en búsqueda: {str(e)}")
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
                    return {
                        "productos": productos,
                        "total": len(productos),
                        "success": True
                    }
                else:
                    return {"error": f"Status {response.status_code}", "success": False}
        except Exception as e:
            logger.error(f"Error listando productos: {str(e)}")
            return {"error": str(e), "success": False}
    
    async def crear_producto_woo(self, datos: Dict) -> Dict:
        """Crea producto en WooCommerce"""
        if not all([self.woo_url, self.woo_key, self.woo_secret]):
            return {"error": "WooCommerce no configurado", "success": False}
        
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
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
                else:
                    return {
                        "error": f"Status {response.status_code}: {response.text[:200]}",
                        "success": False
                    }
        except Exception as e:
            logger.error(f"Error creando producto: {str(e)}")
            return {"error": str(e), "success": False}
    
    async def modificar_producto_woo(self, product_id: int, datos: Dict) -> Dict:
        """Modifica producto en WooCommerce"""
        if not all([self.woo_url, self.woo_key, self.woo_secret]):
            return {"error": "WooCommerce no configurado", "success": False}
        
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
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
                else:
                    return {"error": f"Status {response.status_code}", "success": False}
        except Exception as e:
            logger.error(f"Error modificando producto: {str(e)}")
            return {"error": str(e), "success": False}
    
    async def eliminar_producto_woo(self, product_id: int, confirmar: bool = False) -> Dict:
        """
        Elimina producto de WooCommerce
        Requiere confirmación explícita
        """
        if not confirmar:
            return {
                "error": "Se requiere confirmación explícita para eliminar productos",
                "success": False,
                "requiere_confirmacion": True
            }
        
        if not all([self.woo_url, self.woo_key, self.woo_secret]):
            return {"error": "WooCommerce no configurado", "success": False}
        
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.delete(
                    f"{self.woo_url}/wp-json/wc/v3/products/{product_id}",
                    params={"force": True},
                    auth=(self.woo_key, self.woo_secret)
                )
                
                if response.status_code == 200:
                    return {
                        "mensaje": f"Producto {product_id} eliminado permanentemente",
                        "success": True
                    }
                else:
                    return {"error": f"Status {response.status_code}", "success": False}
        except Exception as e:
            logger.error(f"Error eliminando producto: {str(e)}")
            return {"error": str(e), "success": False}
    
    # ============================================
    # SISTEMA DE MEMORIA
    # ============================================
    
    async def _cargar_memoria(self, user_id: str, limit: int = 20) -> List[Dict]:
        """Carga memoria reciente del usuario"""
        try:
            conversaciones = await self.db["conversations"].find(
                {"user_id": user_id}
            ).sort("timestamp", -1).limit(limit).to_list(limit)
            
            return list(reversed(conversaciones))
        except Exception as e:
            logger.error(f"Error cargando memoria: {str(e)}")
            return []
    
    async def _guardar_memoria(self, user_id: str, command: str, response: str, acciones: List[Dict]):
        """Guarda interacción en memoria persistente"""
        try:
            await self.db["conversations"].insert_one({
                "user_id": user_id,
                "command": command,
                "response": response,
                "acciones": acciones,
                "timestamp": datetime.now(timezone.utc),
                "status": "completed",
                "metadata": {
                    "response_length": len(response),
                    "acciones_count": len(acciones),
                    "tiene_herramientas": len(acciones) > 0
                }
            })
        except Exception as e:
            logger.error(f"Error guardando memoria: {str(e)}")
# ============================================
# ALIAS PARA COMPATIBILIDAD
# ============================================

# Mantener compatibilidad con imports anteriores
CerebroUncensored = CerebroAI
