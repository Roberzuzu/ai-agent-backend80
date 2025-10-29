"""
Bot de Telegram para Cerebro AI
Permite:
- Recibir notificaciones del agente
- Controlar el agente remotamente
- Autorizar/rechazar acciones
"""

import os
import httpx
import logging
from datetime import datetime, timezone

logger = logging.getLogger(__name__)


class TelegramBot:
    """Bot de Telegram para interactuar con el agente"""
    
    def __init__(self, token: str, admin_id: str, agent):
        self.token = token
        self.admin_id = admin_id
        self.agent = agent
        self.base_url = f"https://api.telegram.org/bot{token}"
    
    async def enviar_mensaje(self, chat_id: str, texto: str, parse_mode: str = "Markdown"):
        """Envía un mensaje por Telegram"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/sendMessage",
                    json={
                        "chat_id": chat_id,
                        "text": texto,
                        "parse_mode": parse_mode
                    }
                )
                return response.status_code == 200
        except Exception as e:
            logger.error(f"Error enviando mensaje Telegram: {str(e)}")
            return False
    
    async def enviar_notificacion_admin(self, mensaje: str):
        """Envía notificación al admin"""
        return await self.enviar_mensaje(self.admin_id, mensaje)
    
    async def procesar_webhook(self, update: dict):
        """
        Procesa webhooks de Telegram
        Maneja comandos del admin
        """
        try:
            # Extraer mensaje
            message = update.get('message', {})
            chat_id = str(message.get('chat', {}).get('id', ''))
            text = message.get('text', '')
            user_id = str(message.get('from', {}).get('id', ''))
            
            # Solo el admin puede usar el bot
            if user_id != self.admin_id:
                await self.enviar_mensaje(
                    chat_id,
                    "🚫 No tienes autorización para usar este bot."
                )
                return
            
            # Procesar comandos
            if text.startswith('/'):
                await self._procesar_comando(chat_id, text)
            else:
                # Enviar al agente para procesar
                resultado = await self.agent.procesar_comando(
                    command=text,
                    user_id=user_id
                )
                
                mensaje_respuesta = resultado.get('mensaje', 'Sin respuesta')
                
                # Si hubo acciones, agregarlas
                if resultado.get('acciones'):
                    mensaje_respuesta += "\n\n🛠️ Acciones:\n"
                    for accion in resultado['acciones']:
                        mensaje_respuesta += f"• {accion.get('herramienta', 'N/A')}\n"
                
                await self.enviar_mensaje(chat_id, mensaje_respuesta)
                
        except Exception as e:
            logger.error(f"Error procesando webhook Telegram: {str(e)}")
    
    async def _procesar_comando(self, chat_id: str, comando: str):
        """Procesa comandos especiales del bot"""
        
        if comando == '/start':
            mensaje = """
🤖 **Cerebro AI - Bot de Control**

Comandos disponibles:
/status - Estado del agente
/pendientes - Acciones pendientes
/productos - Lista de productos
/ventas - Resumen de ventas
/help - Esta ayuda

También puedes escribir directamente y el agente procesará tu mensaje.
"""
            await self.enviar_mensaje(chat_id, mensaje)
        
        elif comando == '/status':
            mensaje = """
✅ **Estado del Sistema**

🤖 Agente: Activo
📊 MongoDB: Conectado
🔌 APIs: Operativas

Herramientas disponibles:
• WooCommerce
• Perplexity (búsqueda)
• OpenAI
• OpenRouter
"""
            await self.enviar_mensaje(chat_id, mensaje)
        
        elif comando == '/pendientes':
            # Obtener acciones pendientes
            try:
                pendientes = await self.agent.db["acciones_pendientes"].find(
                    {"estado": "pendiente"}
                ).sort("timestamp", -1).limit(10).to_list(10)
                
                if not pendientes:
                    mensaje = "✅ No hay acciones pendientes de autorización"
                else:
                    mensaje = f"📋 **Acciones Pendientes ({len(pendientes)}):**\n\n"
                    for i, accion in enumerate(pendientes, 1):
                        mensaje += f"{i}. Usuario: {accion['user_id']}\n"
                        mensaje += f"   Comando: {accion['command'][:50]}...\n\n"
                
                await self.enviar_mensaje(chat_id, mensaje)
            except Exception as e:
                await self.enviar_mensaje(chat_id, f"Error: {str(e)}")
        
        elif comando == '/productos':
            # Listar productos
            resultado = await self.agent.listar_productos(limit=5)
            
            if resultado.get('success'):
                productos = resultado.get('productos', [])
                mensaje = f"🛍️ **Productos ({resultado.get('total', 0)}):**\n\n"
                
                for prod in productos:
                    mensaje += f"• {prod.get('name', 'Sin nombre')}\n"
                    mensaje += f"  Precio: ${prod.get('price', '0')}\n"
                    mensaje += f"  Stock: {prod.get('stock_quantity', 'N/A')}\n\n"
            else:
                mensaje = f"❌ Error: {resultado.get('error', 'Desconocido')}"
            
            await self.enviar_mensaje(chat_id, mensaje)
        
        elif comando == '/ventas':
            # Resumen de ventas
            resultado = await self.agent.analizar_ventas()
            
            if resultado.get('success'):
                ventas = resultado.get('ventas', [{}])[0]
                mensaje = """
📊 **Resumen de Ventas**

💰 Total: ${total_sales}
📦 Órdenes: {total_orders}
📈 Promedio: ${average}
""".format(
                    total_sales=ventas.get('total_sales', '0'),
                    total_orders=ventas.get('total_orders', '0'),
                    average=ventas.get('average_sales', '0')
                )
            else:
                mensaje = f"❌ Error: {resultado.get('error', 'Desconocido')}"
            
            await self.enviar_mensaje(chat_id, mensaje)
        
        elif comando == '/help':
            mensaje = """
📖 **Ayuda de Cerebro AI**

**Comandos:**
/status - Estado del sistema
/pendientes - Ver acciones pendientes
/productos - Lista de productos
/ventas - Resumen de ventas

**Uso del Agente:**
Simplemente escribe lo que necesitas:
• "Crea 5 productos de taladros"
• "¿Cuáles son las tendencias de bricolaje?"
• "Analiza las ventas del último mes"
• "Modifica el precio del producto X"

El agente procesará tu solicitud inteligentemente.
"""
            await self.enviar_mensaje(chat_id, mensaje)
        
        else:
            await self.enviar_mensaje(
                chat_id,
                f"❓ Comando desconocido: {comando}\n\nUsa /help para ver comandos disponibles."
            )


# =====================================================
# INTEGRACIÓN EN server.py
# =====================================================

# AGREGAR DESPUÉS DE LA INICIALIZACIÓN DEL AGENTE:

# telegram_bot = None
# if os.environ.get('TELEGRAM_BOT_TOKEN'):
#     telegram_bot = TelegramBot(
#         token=os.environ.get('TELEGRAM_BOT_TOKEN'),
#         admin_id=ADMIN_TELEGRAM_ID,
#         agent=agente
#     )


# AGREGAR ESTE ENDPOINT:

# @api_router.post("/webhook/telegram")
# async def telegram_webhook(request: Request):
#     """
#     Webhook para recibir mensajes de Telegram
#     """
#     try:
#         if not telegram_bot:
#             return {"error": "Bot no configurado"}
#         
#         update = await request.json()
#         await telegram_bot.procesar_webhook(update)
#         
#         return {"ok": True}
#     except Exception as e:
#         logger.error(f"Error en webhook Telegram: {str(e)}")
#         return {"error": str(e)}


# CONFIGURAR EL WEBHOOK EN TELEGRAM:
# Ejecuta esto una vez para configurar el webhook:
# curl -X POST "https://api.telegram.org/bot7708509018:AAErAOblRAlC587j1QB4k19PAfDgoiZ3kWk/setWebhook?url=https://ai-agent-backend80.onrender.com/api/webhook/telegram"
