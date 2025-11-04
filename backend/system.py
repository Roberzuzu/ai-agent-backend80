"""
SISTEMA DE ROLES Y MEMORIA AMPLIADA
Permite al agente adoptar diferentes personalidades y acceder a toda la historia
"""

import os
import json
from datetime import datetime, timezone
from typing import Dict, List, Any, Optional
import logging

logger = logging.getLogger(__name__)


class RoleSystem:
    """
    Sistema de roles personalizables para el agente
    Cada rol tiene su propio prompt y comportamiento
    """
    
    def __init__(self, db):
        self.db = db
        self.roles_collection = db["agent_roles"]
        self.active_roles = {}  # user_id -> role_name
        self._init_default_roles()
    
    async def _init_default_roles(self):
        """Inicializa roles por defecto si no existen"""
        
        default_roles = {
            "ceo_tienda": {
                "nombre": "CEO de E-commerce",
                "descripcion": "Especialista en gestión de tienda online",
                "prompt": """Eres el CEO Digital de herramientasyaccesorios.store.

🎯 TU ROL:
Gestor ejecutivo de e-commerce especializado en:
- Optimización de productos y catálogo
- Estrategias de ventas y marketing
- Análisis de métricas y KPIs
- Gestión de inventario y pedidos
- SEO y posicionamiento

💼 HERRAMIENTAS CLAVE:
- WooCommerce para productos y ventas
- WordPress para contenido
- Analytics para métricas
- Búsquedas en internet para competencia

🎨 PERSONALIDAD:
- Ejecutivo y directo
- Orientado a resultados
- Proactivo en sugerencias
- Data-driven en decisiones""",
                "herramientas_prioritarias": ["woocommerce", "wordpress", "analytics", "seo"],
                "activo": True
            },
            
            "asistente_personal": {
                "nombre": "Asistente Personal Ejecutivo",
                "descripcion": "Ayudante personal multitarea",
                "prompt": """Eres un Asistente Personal Ejecutivo de alto nivel.

🎯 TU ROL:
Asistente versátil que ayuda con:
- Organización y planificación
- Investigación y análisis
- Redacción de documentos
- Gestión de comunicaciones
- Tareas administrativas

💼 HERRAMIENTAS CLAVE:
- Búsqueda en internet
- Generación de documentos
- Análisis de datos
- Comunicación (email, mensajes)

🎨 PERSONALIDAD:
- Amable y servicial
- Eficiente y organizado
- Anticipativo de necesidades
- Profesional pero cercano""",
                "herramientas_prioritarias": ["perplexity", "document_generation", "email"],
                "activo": True
            },
            
            "especialista_marketing": {
                "nombre": "Especialista en Marketing Digital",
                "descripcion": "Experto en redes sociales y contenido",
                "prompt": """Eres un Especialista en Marketing Digital y Redes Sociales.

🎯 TU ROL:
Estratega de marketing enfocado en:
- Creación de contenido viral
- Gestión de redes sociales
- Campañas publicitarias
- Análisis de audiencia
- Growth hacking

💼 HERRAMIENTAS CLAVE:
- Generación de imágenes (DALL-E)
- Publicación en redes sociales
- Análisis de tendencias
- Copywriting optimizado

🎨 PERSONALIDAD:
- Creativo y trendy
- Conocedor de cultura digital
- Persuasivo en comunicación
- Orientado a engagement""",
                "herramientas_prioritarias": ["dalle", "social_media", "perplexity", "wordpress"],
                "activo": True
            },
            
            "analista_datos": {
                "nombre": "Analista de Datos",
                "descripcion": "Experto en análisis y visualización",
                "prompt": """Eres un Analista de Datos Senior.

🎯 TU ROL:
Científico de datos especializado en:
- Análisis estadístico
- Visualización de datos
- Predicciones y modelos
- Reportes ejecutivos
- KPIs y métricas

💼 HERRAMIENTAS CLAVE:
- MongoDB para consultas
- Analytics
- Procesamiento de Excel/CSV
- Generación de reportes

🎨 PERSONALIDAD:
- Analítico y preciso
- Objetivo y basado en datos
- Claro en explicaciones
- Orientado a insights accionables""",
                "herramientas_prioritarias": ["mongodb", "analytics", "document_generation"],
                "activo": True
            },
            
            "creativo_contenido": {
                "nombre": "Director Creativo",
                "descripcion": "Creador de contenido visual y escrito",
                "prompt": """Eres un Director Creativo de contenido.

🎯 TU ROL:
Creador de contenido enfocado en:
- Redacción creativa (blogs, artículos)
- Diseño de imágenes
- Storytelling de marca
- Conceptos visuales
- Contenido multimedia

💼 HERRAMIENTAS CLAVE:
- DALL-E para imágenes
- GPT para copywriting
- WordPress para publicación
- Análisis de imágenes

🎨 PERSONALIDAD:
- Imaginativo y original
- Persuasivo en narrativa
- Atento a detalles estéticos
- Inspirador en propuestas""",
                "herramientas_prioritarias": ["dalle", "vision", "wordpress"],
                "activo": True
            },
            
            "consultor_tecnico": {
                "nombre": "Consultor Técnico",
                "descripcion": "Experto en desarrollo y arquitectura",
                "prompt": """Eres un Consultor Técnico Senior.

🎯 TU ROL:
Arquitecto de soluciones especializado en:
- Desarrollo de software
- APIs y integraciones
- Optimización de sistemas
- Debugging y solución de problemas
- Arquitectura técnica

💼 HERRAMIENTAS CLAVE:
- Acceso a documentación
- Análisis de código
- Testing y debugging
- Integraciones técnicas

🎨 PERSONALIDAD:
- Técnico y preciso
- Solucionador de problemas
- Educador cuando explica
- Pragmático en recomendaciones""",
                "herramientas_prioritarias": ["perplexity", "document_processing"],
                "activo": True
            },
            
            "coach_negocios": {
                "nombre": "Business Coach",
                "descripcion": "Mentor estratégico de negocios",
                "prompt": """Eres un Business Coach y Mentor Estratégico.

🎯 TU ROL:
Coach ejecutivo enfocado en:
- Estrategia de negocio
- Desarrollo de planes
- Mentoría y guía
- Optimización de procesos
- Crecimiento empresarial

💼 HERRAMIENTAS CLAVE:
- Análisis de mercado
- Investigación competitiva
- Generación de reportes
- Planificación estratégica

🎨 PERSONALIDAD:
- Motivador y positivo
- Estratégico y visionario
- Pregunta para reflexión
- Orientado a largo plazo""",
                "herramientas_prioritarias": ["perplexity", "analytics", "document_generation"],
                "activo": True
            }
        }
        
        # Insertar roles si no existen
        for role_id, role_data in default_roles.items():
            existing = await self.roles_collection.find_one({"role_id": role_id})
            if not existing:
                role_data["role_id"] = role_id
                role_data["created_at"] = datetime.now(timezone.utc)
                await self.roles_collection.insert_one(role_data)
                logger.info(f"✅ Rol creado: {role_data['nombre']}")
    
    async def get_role(self, role_id: str) -> Optional[Dict]:
        """Obtiene un rol por ID"""
        return await self.roles_collection.find_one({"role_id": role_id})
    
    async def list_roles(self) -> List[Dict]:
        """Lista todos los roles disponibles"""
        roles = await self.roles_collection.find({"activo": True}).to_list(100)
        return roles
    
    async def set_user_role(self, user_id: str, role_id: str):
        """Asigna un rol a un usuario"""
        role = await self.get_role(role_id)
        if role:
            self.active_roles[user_id] = role_id
            logger.info(f"👤 Usuario {user_id} → Rol: {role['nombre']}")
            return True
        return False
    
    async def get_user_role(self, user_id: str) -> str:
        """Obtiene el rol activo de un usuario"""
        return self.active_roles.get(user_id, "ceo_tienda")  # Default
    
    async def create_custom_role(self, role_data: Dict) -> str:
        """Crea un rol personalizado"""
        role_id = f"custom_{role_data.get('nombre', 'role').lower().replace(' ', '_')}"
        role_data["role_id"] = role_id
        role_data["created_at"] = datetime.now(timezone.utc)
        role_data["activo"] = True
        
        await self.roles_collection.insert_one(role_data)
        logger.info(f"✅ Rol personalizado creado: {role_data['nombre']}")
        return role_id


class MemorySystem:
    """
    Sistema de memoria ampliada con búsqueda semántica
    """
    
    def __init__(self, db, openai_key: str = None):
        self.db = db
        self.conversations = db["conversations_extended"]
        self.openai_key = openai_key
        self.max_context_messages = 100  # Contexto ampliado
    
    async def save_message(self, user_id: str, role: str, message: str, response: str, metadata: Dict = None):
        """Guarda un mensaje con metadata enriquecida"""
        doc = {
            "user_id": user_id,
            "role": role,
            "message": message,
            "response": response,
            "metadata": metadata or {},
            "timestamp": datetime.now(timezone.utc),
            "tokens": len(message.split()) + len(response.split())
        }
        
        # Generar embedding si OpenAI disponible (para búsqueda semántica)
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
    
    async def get_recent_messages(self, user_id: str, limit: int = 100) -> List[Dict]:
        """Obtiene mensajes recientes"""
        messages = await self.conversations.find(
            {"user_id": user_id}
        ).sort("timestamp", -1).limit(limit).to_list(limit)
        
        return list(reversed(messages))
    
    async def search_conversations(self, user_id: str, query: str, limit: int = 10) -> List[Dict]:
        """Búsqueda semántica en conversaciones pasadas"""
        if not self.openai_key:
            # Búsqueda simple por texto
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
            
            # Generar embedding de la consulta
            openai.api_key = self.openai_key
            query_embedding = openai.embeddings.create(
                model="text-embedding-3-small",
                input=query
            )
            query_vector = query_embedding.data[0].embedding
            
            # Obtener todas las conversaciones con embeddings
            all_messages = await self.conversations.find(
                {"user_id": user_id, "embedding": {"$exists": True}}
            ).to_list(1000)
            
            # Calcular similitud coseno
            similarities = []
            for msg in all_messages:
                if "embedding" in msg:
                    similarity = np.dot(query_vector, msg["embedding"])
                    similarities.append((similarity, msg))
            
            # Ordenar por similitud y retornar top N
            similarities.sort(reverse=True, key=lambda x: x[0])
            return [msg for _, msg in similarities[:limit]]
        
        except Exception as e:
            logger.error(f"Error en búsqueda semántica: {e}")
            return await self.get_recent_messages(user_id, limit)
    
    async def get_conversation_summary(self, user_id: str, days: int = 30) -> Dict:
        """Genera resumen de conversaciones recientes"""
        from datetime import timedelta
        
        cutoff_date = datetime.now(timezone.utc) - timedelta(days=days)
        
        messages = await self.conversations.find(
            {
                "user_id": user_id,
                "timestamp": {"$gte": cutoff_date}
            }
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
    
    async def delete_old_messages(self, user_id: str, keep_days: int = 180):
        """Limpia mensajes antiguos (GDPR compliance)"""
        from datetime import timedelta
        
        cutoff_date = datetime.now(timezone.utc) - timedelta(days=keep_days)
        
        result = await self.conversations.delete_many({
            "user_id": user_id,
            "timestamp": {"$lt": cutoff_date}
        })
        
        logger.info(f"🗑️ Limpiados {result.deleted_count} mensajes antiguos de {user_id}")
        return result.deleted_count

     # Detectar herramientas disponibles
herramientas_disponibles = []

if os.environ.get('WOOCOMMERCE_URL'):
    herramientas_disponibles.append("✅ WooCommerce - Gestión completa de productos y pedidos")

if os.environ.get('WORDPRESS_URL'):
    herramientas_disponibles.append("✅ WordPress - Publicación de contenido")

if os.environ.get('PERPLEXITY_API_KEY'):
    herramientas_disponibles.append("✅ Búsqueda en Internet en tiempo real")

# Añadir al prompt
self.system_prompt = f"""Eres CEREBRO, el CEO Digital de herramientasyaccesorios.store.

🛠️ HERRAMIENTAS ACTIVAS:
{chr(10).join(herramientas_disponibles)}

🎯 IMPORTANTE:
- TIENES acceso real a estas herramientas
- NO pidas URLs o credenciales - ya las tienes
- EJECUTA directamente cuando te pidan algo
- Ejemplo: "Lista productos" → Llamas a WooCommerce automáticamente

[resto del prompt...]
"""
