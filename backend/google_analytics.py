"""
Google Analytics 4 - Server Side Tracking
Envía eventos desde el backend a Google Analytics
"""

import os
import httpx
import asyncio
from datetime import datetime
import uuid

MEASUREMENT_ID = os.getenv("GOOGLE_ANALYTICS_MEASUREMENT_ID", "G-EMQDLMQ0S3")
API_SECRET = os.getenv("GOOGLE_ANALYTICS_API_SECRET", "")  # Necesitarás generar esto

class GoogleAnalytics:
    """Cliente para Google Analytics 4 Measurement Protocol"""
    
    def __init__(self):
        self.measurement_id = MEASUREMENT_ID
        self.api_secret = API_SECRET
        self.endpoint = f"https://www.google-analytics.com/mp/collect?measurement_id={self.measurement_id}&api_secret={self.api_secret}"
        self.debug_endpoint = f"https://www.google-analytics.com/debug/mp/collect?measurement_id={self.measurement_id}&api_secret={self.api_secret}"
    
    async def send_event(self, client_id: str, event_name: str, event_params: dict = None, user_properties: dict = None):
        """
        Envía un evento a Google Analytics 4
        
        Args:
            client_id: ID único del cliente (puede ser user_id de Telegram, session_id, etc)
            event_name: Nombre del evento (ej: 'telegram_command', 'ai_query')
            event_params: Parámetros del evento
            user_properties: Propiedades del usuario
        """
        if not self.api_secret:
            print("⚠️ Google Analytics API Secret no configurado")
            return False
        
        payload = {
            "client_id": client_id,
            "events": [{
                "name": event_name,
                "params": event_params or {}
            }]
        }
        
        if user_properties:
            payload["user_properties"] = user_properties
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    self.endpoint,
                    json=payload,
                    timeout=5.0
                )
                
                if response.status_code == 204:
                    return True
                else:
                    print(f"❌ Error enviando evento a GA: {response.status_code}")
                    return False
        
        except Exception as e:
            print(f"❌ Error en Google Analytics: {e}")
            return False
    
    async def track_telegram_command(self, user_id: str, command: str, success: bool = True):
        """Track comando de Telegram"""
        await self.send_event(
            client_id=f"telegram_{user_id}",
            event_name="telegram_command",
            event_params={
                "command": command,
                "success": success,
                "timestamp": datetime.utcnow().isoformat()
            }
        )
    
    async def track_ai_query(self, user_id: str, query: str, tools_used: list, success: bool = True):
        """Track query del AI Agent"""
        await self.send_event(
            client_id=f"telegram_{user_id}",
            event_name="ai_query",
            event_params={
                "query": query[:100],  # Limitar longitud
                "tools_count": len(tools_used),
                "tools": ",".join(tools_used[:5]),  # Primeras 5 herramientas
                "success": success
            }
        )
    
    async def track_product_process(self, user_id: str, product_id: str, success: bool = True):
        """Track procesamiento de producto"""
        await self.send_event(
            client_id=f"telegram_{user_id}",
            event_name="product_process",
            event_params={
                "product_id": product_id,
                "success": success
            }
        )
    
    async def track_error(self, user_id: str, error_type: str, error_message: str):
        """Track errores"""
        await self.send_event(
            client_id=f"telegram_{user_id}",
            event_name="error",
            event_params={
                "error_type": error_type,
                "error_message": error_message[:200]
            }
        )
    
    async def track_conversion(self, user_id: str, conversion_type: str, value: float = 0):
        """Track conversiones"""
        await self.send_event(
            client_id=f"telegram_{user_id}",
            event_name=conversion_type,
            event_params={
                "currency": "EUR",
                "value": value
            }
        )


# Instancia global
ga = GoogleAnalytics()


# Funciones de ayuda
async def track_telegram_event(user_id: str, command: str, success: bool = True):
    """Shortcut para tracking de Telegram"""
    await ga.track_telegram_command(user_id, command, success)


async def track_ai_event(user_id: str, query: str, tools: list, success: bool = True):
    """Shortcut para tracking de AI"""
    await ga.track_ai_query(user_id, query, tools, success)
