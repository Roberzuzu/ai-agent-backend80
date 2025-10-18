#!/usr/bin/env python3
"""
Script to create test notifications for demonstration
"""
import asyncio
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime, timezone, timedelta
import uuid

# MongoDB connection
mongo_url = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ.get('DB_NAME', 'social_media_agent')]

async def create_test_notifications():
    """Create test notifications"""
    
    test_user_email = "test@example.com"
    
    notifications = [
        {
            "id": str(uuid.uuid4()),
            "user_email": test_user_email,
            "type": "payment",
            "title": "💰 Pago Recibido",
            "message": "Has recibido un pago de $199.99 por la compra de Sierra Circular Makita.",
            "link": "/revenue",
            "icon": "payment",
            "is_read": False,
            "is_archived": False,
            "metadata": {"amount": 199.99, "product": "Sierra Circular"},
            "created_at": (datetime.now(timezone.utc) - timedelta(hours=2)).isoformat(),
            "read_at": None
        },
        {
            "id": str(uuid.uuid4()),
            "user_email": test_user_email,
            "type": "affiliate",
            "title": "🤝 Nueva Comisión Ganada",
            "message": "Has ganado $12.50 en comisiones por una venta referida.",
            "link": "/affiliate-dashboard",
            "icon": "affiliate",
            "is_read": False,
            "is_archived": False,
            "metadata": {"commission": 12.50},
            "created_at": (datetime.now(timezone.utc) - timedelta(hours=5)).isoformat(),
            "read_at": None
        },
        {
            "id": str(uuid.uuid4()),
            "user_email": test_user_email,
            "type": "subscription",
            "title": "⭐ Nueva Suscripción",
            "message": "Un nuevo usuario se ha suscrito al plan Pro ($29.99/mes).",
            "link": "/subscriptions",
            "icon": "subscription",
            "is_read": True,
            "is_archived": False,
            "metadata": {"plan": "pro", "amount": 29.99},
            "created_at": (datetime.now(timezone.utc) - timedelta(days=1)).isoformat(),
            "read_at": (datetime.now(timezone.utc) - timedelta(hours=12)).isoformat()
        },
        {
            "id": str(uuid.uuid4()),
            "user_email": test_user_email,
            "type": "campaign",
            "title": "📢 Campaña Completada",
            "message": "Tu campaña 'Black Friday Sale' ha finalizado con 15,234 impresiones y 342 conversiones.",
            "link": "/campaigns",
            "icon": "campaign",
            "is_read": False,
            "is_archived": False,
            "metadata": {"campaign": "Black Friday", "impressions": 15234, "conversions": 342},
            "created_at": (datetime.now(timezone.utc) - timedelta(hours=8)).isoformat(),
            "read_at": None
        },
        {
            "id": str(uuid.uuid4()),
            "user_email": test_user_email,
            "type": "product",
            "title": "🛍️ Producto Destacado",
            "message": "El producto 'Taladro Inalámbrico' ha sido marcado como destacado.",
            "link": "/products",
            "icon": "product",
            "is_read": True,
            "is_archived": False,
            "metadata": {"product": "Taladro Inalámbrico"},
            "created_at": (datetime.now(timezone.utc) - timedelta(days=2)).isoformat(),
            "read_at": (datetime.now(timezone.utc) - timedelta(days=1)).isoformat()
        },
        {
            "id": str(uuid.uuid4()),
            "user_email": test_user_email,
            "type": "system",
            "title": "🔔 Actualización del Sistema",
            "message": "Nueva función disponible: Dashboard Analytics con gráficos interactivos.",
            "link": "/dashboard-enhanced",
            "icon": "system",
            "is_read": False,
            "is_archived": False,
            "metadata": {"feature": "dashboard-analytics"},
            "created_at": (datetime.now(timezone.utc) - timedelta(minutes=30)).isoformat(),
            "read_at": None
        },
        {
            "id": str(uuid.uuid4()),
            "user_email": test_user_email,
            "type": "success",
            "title": "✅ Sincronización Exitosa",
            "message": "Tus productos se han sincronizado correctamente con WordPress.",
            "link": "/products",
            "icon": "success",
            "is_read": False,
            "is_archived": False,
            "metadata": {"synced": 12},
            "created_at": (datetime.now(timezone.utc) - timedelta(hours=1)).isoformat(),
            "read_at": None
        },
        {
            "id": str(uuid.uuid4()),
            "user_email": test_user_email,
            "type": "warning",
            "title": "⚠️ Bajo Inventario",
            "message": "El producto 'Martillo Profesional' tiene solo 5 unidades en stock.",
            "link": "/products",
            "icon": "warning",
            "is_read": False,
            "is_archived": False,
            "metadata": {"product": "Martillo", "stock": 5},
            "created_at": (datetime.now(timezone.utc) - timedelta(hours=3)).isoformat(),
            "read_at": None
        }
    ]
    
    # Clear existing test notifications
    await db.notifications.delete_many({"user_email": test_user_email})
    
    # Insert new notifications
    if notifications:
        await db.notifications.insert_many(notifications)
    
    print(f"✅ Created {len(notifications)} test notifications for {test_user_email}")
    print(f"Unread: {sum(1 for n in notifications if not n['is_read'])}")
    print(f"Read: {sum(1 for n in notifications if n['is_read'])}")

if __name__ == "__main__":
    asyncio.run(create_test_notifications())
