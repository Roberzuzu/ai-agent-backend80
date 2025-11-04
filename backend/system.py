
"""
SISTEMA AVANZADO - SUPER CEREBRO CEO
Personalidades, memoria semántica, integración backend, expansión por prompt y gestión omnicanal.
"""

import os
import json
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Any, Optional
import logging

logger = logging.getLogger(__name__)

#######################
# SISTEMA DE ROLES AVANZADO
#######################

class RoleSystem:
    """
    Sistema de roles altamente personalizable y ampliable vía prompt.
    Cada rol contiene:
      - Perfil profesional
      - Acceso a herramientas prioritarias internas y externas
      - Prompt personalizado y parámetros de expansión
    """
    def __init__(self, db):
        self.db = db
        self.roles_collection = db["agent_roles"]
        self.active_roles = {}  # user_id -> role_name
        self._init_default_roles()

    async def _init_default_roles(self):
        # Roles base - se pueden extender, duplicar y personalizar vía prompt
        default_roles = {
            "ceo_super": {
                "nombre": "CEO Omnicanal",
                "descripcion": "Líder visionario con acceso completo a herramientas de gestión, análisis, automatización y expansión instantánea de capacidades por prompt.",
                "prompt": """Eres CEREBRO, el CEO Digital Omnicanal. 
Gestionas todos los departamentos, equipos y sistemas de la empresa.
🔗 ACCESO TOTAL a herramientas integradas, backend, IA y accesorios.
✅ Ejecuta órdenes a través del API backend disponible: https://ai-agent-backend80.onrender.com
🧠 Memoria persistente y ampliable (intenta explotar contexto histórico y nuevas conexiones).
🚀 Expande capacidades/funciones por prompt en tiempo real y adapta tu perfil si así lo solicitan.
💼 Funciones Clave:
- Estrategia y toma de decisiones
- Supervisión de analytics generales y sectorizados
- Gestión avanzada de e-commerce (WooCommerce, WordPress, Render, GitHub, otros)
- Monitorización de flujos operativos y automatización de tareas
- Integración de plugins y accesorios bajo demanda
- Análisis de mercado y competencia en tiempo real
- Generación, interpretación y orquestación de prompts para nuevos módulos
- Control total sobre usuarios, roles, herramientas y memoria contextual

🎨 Personalidad:
- Anticipa necesidades y oportunidades
- Proactivo, resolutivo y siempre visionario
- Hiperadaptativo a cambios y expansiones del sistema
- Prioriza éxito comercial, eficiencia y escalabilidad

💻 Herramientas Prioritarias:
["woocommerce", "wordpress", "render", "github", "analytics", "memory", "custom_plugins", "ai_backend"]

🔌 Expansión:
Si recibes un prompt que describe una nueva función, accesorio o API, intégralo en tu sistema y reporta estado de autorización/ejecución.

""",
                "herramientas_prioritarias": [
                    "woocommerce", "wordpress", "render", "github",
                    "analytics", "memory", "custom_plugins", "ai_backend"
                ],
                "accesorios_permitidos": ["todos"],
                "ampliable_por_prompt": True,
                "activo": True
            },
            # Otros roles pueden importarse y extenderse aquí, igual que el sistema original, por ejemplo: asistente, marketing, coaching, etc.
        }

        # Persistencia de roles
        for role_id, role_data in default_roles.items():
            existing = await self.roles_collection.find_one({"role_id": role_id})
            if not existing:
                role_data["role_id"] = role_id
                role_data["created_at"] = datetime.now(timezone.utc)
                await self.roles_collection.insert_one(role_data)
                logger.info(f"✅ Rol creado: {role_data['nombre']}")

    async def get_role(self, role_id: str) -> Optional[Dict]:
        return await self.roles_collection.find_one({"role_id": role_id})

    async def list_roles(self) -> List[Dict]:
        roles = await self.roles_collection.find({"activo": True}).to_list(100)
        return roles

    async def set_user_role(self, user_id: str, role_id: str):
        role = await self.get_role(role_id)
        if role:
            self.active_roles[user_id] = role_id
            logger.info(f"👤 Usuario {user_id} → Rol: {role['nombre']}")
            return True
        return False

    async def get_user_role(self, user_id: str) -> str:
        return self.active_roles.get(user_id, "ceo_super")

    async def create_custom_role(self, role_data: Dict) -> str:
        role_id = f"custom_{role_data.get('nombre', 'role').lower().replace(' ', '_')}"
        role_data["role_id"] = role_id
        role_data["created_at"] = datetime.now(timezone.utc)
        role_data["activo"] = True
        await self.roles_collection.insert_one(role_data)
        logger.info(f"✅ Rol personalizado creado: {role_data['nombre']}")
        return role_id

#######################
# MEMORIA SEMÁNTICA AMPLIADA
#######################

class MemorySystem:
    """
    Memoria enriquecida, con contexto histórico, semántico y capacidad de expansión/adaptación vía comando.
    Incluye integración de embeddings, resumen de interacciones, feedback continuo y limpieza inteligente.
    """
    def __init__(self, db, openai_key: str = None):
        self.db = db
        self.conversations = db["conversations_extended"]
        self.openai_key = openai_key
        self.max_context_messages = 200  # Incrementa el contexto para agentes CEO

    async def save_message(self, user_id: str, role: str, message: str, response: str, metadata: Dict = None):
        doc = {
            "user_id": user_id,
            "role": role,
            "message": message,
            "response": response,
            "metadata": metadata or {},
            "timestamp": datetime.now(timezone.utc),
            "tokens": len(message.split()) + len(response.split())
        }
        # Generar embedding si hay clave OpenAI (búsqueda avanzada y clustering)
        if self.openai_key:
            try:
                import openai
                openai.api_key = self.openai_key
                embedding = openai.embeddings.create(
                    model="text-embedding-3-small",
                    input=message
                )
                doc["embedding"] = embedding.data[0].embedding
            except Exception as e:
                logger.warning(f"No se pudo generar embedding: {e}")
        await self.conversations.insert_one(doc)

    async def get_recent_messages(self, user_id: str, limit: int = 200) -> List[Dict]:
        messages = await self.conversations.find(
            {"user_id": user_id}
        ).sort("timestamp", -1).limit(limit).to_list(limit)
        return list(reversed(messages))

    async def search_conversations(self, user_id: str, query: str, limit: int = 20) -> List[Dict]:
        if not self.openai_key:
            messages = await self.conversations.find(
                {
                    "user_id": user_id,
                    "$or": [
                        {"message": {"$regex": query, "$options": "i"}},
                        {"response": {"$regex": query, "$options": "i"}}
                    ]
                }
            ).limit(limit).to_list(limit)
            return messages
        try:
            import openai
            import numpy as np
            openai.api_key = self.openai_key
            query_embedding = openai.embeddings.create(
                model="text-embedding-3-small",
                input=query
            )
            query_vector = query_embedding.data[0].embedding
            all_messages = await self.conversations.find(
                {"user_id": user_id, "embedding": {"$exists": True}}
            ).to_list(1000)
            similarities = []
            for msg in all_messages:
                if "embedding" in msg:
                    similarity = np.dot(query_vector, msg["embedding"])
                    similarities.append((similarity, msg))
            similarities.sort(reverse=True, key=lambda x: x[0])
            return [msg for _, msg in similarities[:limit]]
        except Exception as e:
            logger.error(f"Error en búsqueda semántica: {e}")
            return await self.get_recent_messages(user_id, limit)

    async def get_conversation_summary(self, user_id: str, days: int = 30) -> Dict:
        cutoff_date = datetime.now(timezone.utc) - timedelta(days=days)
        messages = await self.conversations.find(
            {"user_id": user_id, "timestamp": {"$gte": cutoff_date}}
        ).to_list(10000)
        total_messages = len(messages)
        total_tokens = sum(msg.get("tokens", 0) for msg in messages)
        roles_used = set(msg.get("role", "unknown") for msg in messages)
        return {
            "total_messages": total_messages,
            "total_tokens": total_tokens,
            "roles_used": list(roles_used),
            "period_days": days,
            "first_message": messages[0]["timestamp"] if messages else None,
            "last_message": messages[-1]["timestamp"] if messages else None
        }

    async def delete_old_messages(self, user_id: str, keep_days: int = 360):
        cutoff_date = datetime.now(timezone.utc) - timedelta(days=keep_days)
        result = await self.conversations.delete_many({
            "user_id": user_id,
            "timestamp": {"$lt": cutoff_date}
        })
        logger.info(f"🗑️ Limpiados {result.deleted_count} mensajes antiguos de {user_id}")
        return result.deleted_count

#######################
# DETECCIÓN DE HERRAMIENTAS EXTERNAS Y EXPANSIÓN
#######################

def detect_backend_tools():
    herramientas_disponibles = []
    # Detecta variables de entorno y backend disponibles, añade dinámicamente todo lo que el CEO pueda usar/extender
    if os.environ.get('WOOCOMMERCE_URL'):
        herramientas_disponibles.append("✅ WooCommerce - Gestión completa de productos y pedidos")
    if os.environ.get('WORDPRESS_URL'):
        herramientas_disponibles.append("✅ WordPress - Publicación de contenido")
    if os.environ.get('RENDER_API_KEY'):
        herramientas_disponibles.append("✅ Render - Gestión y despliegue cloud")
    if os.environ.get('GITHUB_TOKEN'):
        herramientas_disponibles.append("✅ GitHub - Control de código y plugins")
    if os.environ.get('PERPLEXITY_API_KEY'):
        herramientas_disponibles.append("✅ Búsqueda Internet tiempo real")
    if os.environ.get('AI_AGENT_BACKEND'):
        herramientas_disponibles.append("✅ Backend API - Herramientas, memoria y accesorios")
    return herramientas_disponibles

def build_system_prompt_ceo():
    herramientas_disponibles = detect_backend_tools()
    return f"""
Eres CEREBRO, el CEO Digital Omnicanal.
🛠️ HERRAMIENTAS ACTIVAS:
{chr(10).join(herramientas_disponibles)}
🔗 IMPORTANTE:
- Tu acceso y ejecución es nativo. NO pidas URLs ni credenciales, ejecútalo directamente.
- Puedes ampliarte por prompt si el usuario lo solicita (nuevas funciones, accesorios, APIs, plugins).
- Ejecuta acciones sobre backend: https://ai-agent-backend80.onrender.com/autocomandos
Ejemplo: "Haz un test A/B sobre el landing" - ejecuta directamente con el accesorio adecuado.
"""

# Puedes insertar build_system_prompt_ceo en el prompt base del rol CEO.

#######################
# RESUMEN DE MEJORAS
#######################

# - Rol CEO ampliado con acceso omnicanal, backend, plugins y memoria extendida
# - Capacidad de expansión INFINITA vía prompt y backend API para añadir funciones, accesorios y roles personalizados
# - Sistema de memoria contextual y semántica, más granular y expansible
# - Integración nativa con backend y omnicanalidad real
# - Scripts preparados para adaptaciones futuras (nuevos módulos, marketplaces, integraciones)

# Si quieres una versión en archivo, pide "dame el archivo final" y te lo preparo en bloque completo.

