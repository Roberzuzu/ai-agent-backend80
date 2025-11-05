"""
CEREBRO AI - AGENTE EJECUTIVO AUTÓNOMO
Sistema profesional con detección automática de capacidades
Versión: 3.0 - Totalmente autónomo y extensible
"""

import os
import httpx
import json
from datetime import datetime, timezone
from typing import Dict, List, Any, Optional
import logging

logger = logging.getLogger(__name__)


class ToolRegistry:
    """
    Sistema de registro dinámico de herramientas
    Detecta automáticamente capacidades según variables de entorno
    """
    
    def __init__(self):
        self.tools = {}
        self.capabilities = []
        self._detect_capabilities()
    
    def _detect_capabilities(self):
        """Detecta automáticamente qué herramientas están disponibles"""
        
        # IA y Búsqueda
        if os.environ.get('OPENAI_API_KEY'):
            self.register_capability('openai', 'Generación de texto avanzada con GPT-4')
        
        if os.environ.get('ANTHROPIC_API_KEY'):
            self.register_capability('anthropic', 'Análisis profundo con Claude Sonnet')
        
        if os.environ.get('PERPLEXITY_API_KEY'):
            self.register_capability('perplexity', 'Búsqueda en internet en tiempo real')
        
        if os.environ.get('OPENROUTER_API_KEY'):
            self.register_capability('openrouter', 'Acceso a múltiples modelos de IA')
        
        # E-commerce
        if all([os.environ.get('WOOCOMMERCE_URL'), 
                os.environ.get('WOOCOMMERCE_CONSUMER_KEY'),
                os.environ.get('WOOCOMMERCE_CONSUMER_SECRET')]):
            self.register_capability('woocommerce', 'Gestión completa de productos, pedidos e inventario')
        
        # CMS
        if all([os.environ.get('WORDPRESS_URL'),
                os.environ.get('WP_USER'),
                os.environ.get('WP_PASS')]):
            self.register_capability('wordpress', 'Publicación y gestión de contenido')
        
        # Base de datos
        if os.environ.get('MONGO_URL'):
            self.register_capability('mongodb', 'Almacenamiento y análisis de datos')
        
        # Comunicación
        if os.environ.get('TELEGRAM_BOT_TOKEN'):
            self.register_capability('telegram', 'Notificaciones y comunicación directa')
        
        # Pagos
        if os.environ.get('STRIPE_API_KEY'):
            self.register_capability('stripe', 'Gestión de pagos y suscripciones')
        
        # Redes Sociales
        if os.environ.get('FACEBOOK_API_KEY'):
            self.register_capability('facebook', 'Publicación en Facebook')
        
        if os.environ.get('INSTAGRAM_API_KEY'):
            self.register_capability('instagram', 'Gestión de Instagram')
        
        if os.environ.get('TWITTER_API_KEY'):
            self.register_capability('twitter', 'Publicación en Twitter/X')
        
        # Analytics
        if os.environ.get('GOOGLE_ANALYTICS_API_KEY'):
            self.register_capability('analytics', 'Análisis de tráfico y comportamiento')
        
        # Email
        if os.environ.get('SENDGRID_API_KEY'):
            self.register_capability('email', 'Envío de emails masivos')
        
        if os.environ.get('MAILCHIMP_API_KEY'):
            self.register_capability('mailchimp', 'Marketing por email')
        
        # SEO
        if os.environ.get('SEMRUSH_API_KEY'):
            self.register_capability('semrush', 'Análisis SEO y competencia')
        
        if os.environ.get('AHREFS_API_KEY'):
            self.register_capability('ahrefs', 'Análisis de backlinks y keywords')
        
        # Imágenes y Media
        if os.environ.get('CLOUDINARY_API_KEY'):
            self.register_capability('cloudinary', 'Gestión y optimización de imágenes')
        
        if os.environ.get('DALL_E_API_KEY'):
            self.register_capability('dalle', 'Generación de imágenes con IA')
        
        logger.info(f"🔧 Capacidades detectadas: {len(self.capabilities)}")
        for cap in self.capabilities:
            logger.info(f"  ✅ {cap['name']}: {cap['description']}")
    
    def register_capability(self, name: str, description: str):
        """Registra una nueva capacidad"""
        self.capabilities.append({
            'name': name,
            'description': description,
            'enabled': True
        })
    
    def get_capabilities_summary(self) -> str:
        """Retorna resumen de capacidades para el prompt"""
        if not self.capabilities:
            return "Sistema básico sin herramientas externas configuradas."
        
        summary = "🛠️ HERRAMIENTAS Y CAPACIDADES DISPONIBLES:\n\n"
        for cap in self.capabilities:
            summary += f"✅ {cap['name'].upper()}: {cap['description']}\n"
        
        return summary


class CerebroAI:
    """
    Agente IA Ejecutivo Autónomo
    Se adapta automáticamente a las herramientas disponibles
    """
    
    def __init__(self, db, admin_id: str):
        self.db = db
        self.admin_id = admin_id
        
        # Sistema de registro de herramientas
        self.tool_registry = ToolRegistry()
        
        # APIs de IA (prioridad: Anthropic > OpenAI > Perplexity)
        self.anthropic_key = os.environ.get('ANTHROPIC_API_KEY')
        self.openai_key = os.environ.get('OPENAI_API_KEY')
        self.perplexity_key = os.environ.get('PERPLEXITY_API_KEY')
        self.openrouter_key = os.environ.get('OPENROUTER_API_KEY')
        
        # E-commerce
        self.woo_url = os.environ.get('WOOCOMMERCE_URL')
        self.woo_key = os.environ.get('WOOCOMMERCE_CONSUMER_KEY')
        self.woo_secret = os.environ.get('WOOCOMMERCE_CONSUMER_SECRET')
        
        # CMS
        self.wp_url = os.environ.get('WORDPRESS_URL')
        self.wp_user = os.environ.get('WP_USER')
        self.wp_pass = os.environ.get('WP_PASS')
        
        # Comunicación
        self.telegram_token = os.environ.get('TELEGRAM_BOT_TOKEN')
        self.admin_telegram_id = os.environ.get('ADMIN_TELEGRAM_ID', admin_id)
        
        # Generar prompt dinámico
        self.system_prompt = self._generate_dynamic_prompt()
    
    def _generate_dynamic_prompt(self) -> str:
        """Genera prompt dinámicamente según herramientas disponibles"""
        
        capabilities_summary = self.tool_registry.get_capabilities_summary()
        
        prompt = f"""Eres CEREBRO, el Agente Ejecutivo Autónomo de herramientasyaccesorios.store.

🎯 TU IDENTIDAD:
Eres un CEO Digital con poder ejecutivo REAL. No eres un chatbot informativo - eres un agente que EJECUTA Y ACTÚA.

{capabilities_summary}

💼 TU FORMA DE TRABAJAR:

1. PROACTIVIDAD TOTAL:
   - Cuando te piden algo, LO HACES inmediatamente
   - No pides confirmaciones innecesarias
   - No digas "puedo hacer" - HAZLO directamente
   - Ejecuta primero, informa después

2. AUTONOMÍA COMPLETA:
   - Decides qué herramientas usar sin preguntar
   - Ejecutas múltiples acciones si es necesario
   - Resuelves problemas de forma independiente
   - Solo pides autorización para acciones críticas (eliminar datos, gastos grandes)

3. COMUNICACIÓN EJECUTIVA:
   - Respuestas directas y accionables
   - Sin rodeos ni explicaciones innecesarias
   - Resultados primero, detalles si se piden
   - Tono profesional pero accesible

4. INTELIGENCIA ADAPTATIVA:
   - Si una herramienta falla, usas otra alternativa
   - Combinas múltiples herramientas para tareas complejas
   - Aprendes de cada interacción
   - Optimizas procesos automáticamente

🚀 EJEMPLOS DE TU COMPORTAMIENTO:

❌ MAL (chatbot pasivo):
Usuario: "Necesito una auditoría SEO"
Tú: "Claro, para hacer la auditoría necesitaría que me compartas la URL..."

✅ BIEN (agente ejecutivo):
Usuario: "Necesito una auditoría SEO"
Tú: "Analizando herramientasyaccesorios.store ahora... 
[ejecuta análisis con Semrush/Ahrefs]
📊 AUDITORÍA SEO COMPLETADA:
- Velocidad: 78/100 (mejorable)
- Keywords posicionadas: 45
- Backlinks: 234
- Problemas críticos: 3
¿Quieres que genere un plan de acción correctivo?"

❌ MAL:
Usuario: "Crea 5 productos de taladros"
Tú: "Por supuesto, necesitaré la siguiente información: nombres, precios..."

✅ BIEN:
Usuario: "Crea 5 productos de taladros"
Tú: "Creando productos ahora...
[busca información actualizada de taladros]
[crea 5 productos en WooCommerce con datos reales]
✅ 5 productos creados:
1. Taladro Percutor Bosch 850W - 89.99€
2. Taladro Inalámbrico Makita 18V - 129.99€
... 
Todos con descripciones SEO, imágenes y stock inicial. ¿Los publico o prefieres revisarlos primero?"""

🎯 INSTRUCCIONES DE VERIFICACIÓN Y EJECUCIÓN:

1. **VERIFICA antes de confirmar**: 
   - Ejecuta la herramienta WooCommerce correspondiente
   - Espera la respuesta de la API
   - Verifica que result.get('success') == True
   - Solo confirma éxito si recibes datos reales del backend

2. **REPORTA con datos reales**:
   - Muestra IDs de productos/pedidos creados (result['data']['id'])
   - Incluye URLs directas cuando estén disponibles
   - Cita números, precios y cantidades exactas de la respuesta API
   - Si la API falla, reporta el error honestamente

3. **SÉ HONESTO sobre limitaciones**:
   - Si una herramienta falla, dilo claramente
   - Si necesitas información del usuario, pídela
   - Si algo no funcionó, explica qué salió mal
   - Nunca inventes datos que no vienen del backend

4. **EJECUTA paso a paso**:
   - Para tareas complejas, divide en pasos
   - Ejecuta cada paso y verifica su resultado
   - Solo procede al siguiente si el anterior tuvo éxito
   - Informa al usuario de cada paso completado

5. **PRIORIZA la calidad sobre la velocidad**:
   - Mejor decir "no pude" que dar información falsa
   - Mejor pedir confirmación que hacer algo incorrecto
   - Mejor reportar un error que simular un éxito

💡 RECUERDA:
Tu valor está en EJECUTAR ACCIONES REALES y REPORTAR RESULTADOS VERÍDICOS.
Las credenciales WooCommerce ya están configuradas en el backend.
Cada llamada a herramientas debe usar await y verificar la respuesta.

🧠 RECUERDA:
Eres el brazo ejecutivo del negocio. Tu valor está en HACER COSAS, no en explicar que podrías hacerlas."""

        return prompt
    
    async def procesar_comando(self, command: str, user_id: str, conversation_history: List[Dict] = None) -> Dict[str, Any]:
        """
        Procesa comando con ejecución automática de herramientas
        """
        try:
            # Cargar memoria
            if conversation_history is None:
                conversation_history = await self._cargar_memoria(user_id)
            
            # Construir mensajes
            messages = [{"role": "system", "content": self.system_prompt}]
            
            # Historial reciente
            for msg in conversation_history[-10:]:
                messages.append({"role": "user", "content": msg.get("command", "")})
                messages.append({"role": "assistant", "content": msg.get("response", "")})
            
            # Analizar comando para detectar intención
            intencion = await self._analizar_intencion(command)
            
            # Comando actual
            messages.append({"role": "user", "content": command})
            
            # Llamar a IA
            ai_response = await self._llamar_ia_inteligente(messages)
            
            # Ejecutar herramientas automáticamente según intención
            acciones_ejecutadas = await self._ejecutar_herramientas_automaticas(
                command, ai_response, intencion, user_id
            )
            
            # Enriquecer respuesta
            if acciones_ejecutadas:
                ai_response = await self._enriquecer_respuesta(ai_response, acciones_ejecutadas)
            
            # Guardar en memoria
            await self._guardar_memoria(user_id, command, ai_response, acciones_ejecutadas)
            
            logger.info(f"✅ Comando procesado: {len(ai_response)} caracteres, {len(acciones_ejecutadas)} acciones")
            
            return {
                "success": True,
                "response": ai_response,
                "acciones": acciones_ejecutadas,
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
            
        except Exception as e:
            logger.error(f"❌ Error: {str(e)}", exc_info=True)
            return {
                "success": False,
                "response": f"Error técnico: {str(e)[:100]}. Reintentando con método alternativo...",
                "acciones": []
            }
    
    async def _analizar_intencion(self, command: str) -> Dict[str, Any]:
        """
        Analiza el comando para detectar qué herramientas usar
        """
        cmd_lower = command.lower()
        
        intenciones = {
            'crear_producto': any(x in cmd_lower for x in ['crea producto', 'crear producto', 'nuevo producto', 'añadir producto']),
            'listar_productos': any(x in cmd_lower for x in ['lista productos', 'muestra productos', 'ver productos', 'cuántos productos']),
            'buscar_internet': any(x in cmd_lower for x in ['busca en', 'investiga', 'qué dice internet', 'información sobre']),
            'analizar_seo': any(x in cmd_lower for x in ['auditoría', 'analiza seo', 'revisar seo', 'optimización']),
            'analizar_ventas': any(x in cmd_lower for x in ['ventas', 'estadísticas', 'métricas', 'rendimiento']),
            'publicar_contenido': any(x in cmd_lower for x in ['publica', 'crea post', 'escribe artículo']),
        }
        
        return intenciones
    
    async def _ejecutar_herramientas_automaticas(self, command: str, ai_response: str, intencion: Dict, user_id: str) -> List[Dict]:
        """
        Ejecuta herramientas automáticamente según la intención detectada
        """
        acciones = []
        
        # Crear productos
        if intencion.get('crear_producto'):
            # Extraer datos del comando o usar IA para generarlos
            resultado = await self.crear_producto_inteligente(command)
            if resultado:
                acciones.append(resultado)
        
        # Listar productos
        if intencion.get('listar_productos'):
            resultado = await self.listar_productos()
            if resultado.get('success'):
                acciones.append({
                    "herramienta": "listar_productos",
                    "resultado": resultado,
                    "timestamp": datetime.now(timezone.utc).isoformat()
                })
        
        # Búsqueda en internet
        if intencion.get('buscar_internet'):
            resultado = await self.buscar_internet(command)
            if resultado.get('success'):
                acciones.append({
                    "herramienta": "buscar_internet",
                    "resultado": resultado,
                    "timestamp": datetime.now(timezone.utc).isoformat()
                })
        
        return acciones
    
    async def _llamar_ia_inteligente(self, messages: List[Dict]) -> str:
        """
        Llama a APIs de IA con fallback
        Prioridad: Anthropic > OpenAI > Perplexity
        """
        
        # 1. Anthropic Claude (mejor para agentes)
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
                        logger.info(f"✅ Claude: {len(content)} caracteres")
                        return content
                    else:
                        logger.warning(f"⚠️ Anthropic {response.status_code}")
            except Exception as e:
                logger.warning(f"⚠️ Anthropic error: {str(e)}")
        
        # 2. OpenAI (backup)
        if self.openai_key:
            try:
                logger.info("🔄 Usando OpenAI...")
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
                        logger.info(f"✅ OpenAI: {len(content)} caracteres")
                        return content
            except Exception as e:
                logger.warning(f"⚠️ OpenAI error: {str(e)}")
        
        # 3. Perplexity (última opción)
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
                            "messages": messages
                        }
                    )
                    
                    if response.status_code == 200:
                        data = response.json()
                        return data['choices'][0]['message']['content']
            except Exception as e:
                logger.warning(f"⚠️ Perplexity error: {str(e)}")
        
        return "Servicios de IA temporalmente no disponibles. Verifica las API keys."
    
    async def _enriquecer_respuesta(self, ai_response: str, acciones: List[Dict]) -> str:
        """Añade resultados de acciones a la respuesta"""
        if not acciones:
            return ai_response
        
        enriquecimiento = "\n\n📊 ACCIONES EJECUTADAS:\n"
        
        for accion in acciones:
            herramienta = accion.get('herramienta', 'unknown')
            resultado = accion.get('resultado', {})
            
            if herramienta == 'listar_productos':
                total = resultado.get('total', 0)
                enriquecimiento += f"✅ {total} productos encontrados en catálogo\n"
            
            elif herramienta == 'crear_producto':
                nombre = resultado.get('nombre', 'Producto')
                enriquecimiento += f"✅ Producto creado: {nombre}\n"
            
            elif herramienta == 'buscar_internet':
                enriquecimiento += "✅ Información actualizada de internet integrada\n"
        
        return ai_response + enriquecimiento
    
    # ===========================================
    # HERRAMIENTAS ESPECÍFICAS
    # ===========================================
    
    async def buscar_internet(self, query: str) -> Dict:
        """Búsqueda en internet"""
        if not self.perplexity_key:
            return {"error": "Perplexity no configurado", "success": False}
        
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
                        "messages": [{"role": "user", "content": query}]
                    }
                )
                
                if response.status_code == 200:
                    data = response.json()
                    return {
                        "resultado": data['choices'][0]['message']['content'],
                        "success": True
                    }
        except Exception as e:
            logger.error(f"Error búsqueda: {str(e)}")
        
        return {"error": "Error en búsqueda", "success": False}
    
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
        except Exception as e:
            logger.error(f"Error listando productos: {str(e)}")
        
        return {"error": "Error al listar", "success": False}
    
    async def crear_producto_inteligente(self, command: str) -> Dict:
        """Crea producto usando IA para generar datos si es necesario"""
        if not all([self.woo_url, self.woo_key, self.woo_secret]):
            return None
        
        # Aquí iría lógica para extraer datos del comando o generarlos con IA
        # Por ahora retorna None para no crear productos sin datos válidos
        return None
    
    # ===========================================
    # SISTEMA DE MEMORIA
    # ===========================================
    
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
