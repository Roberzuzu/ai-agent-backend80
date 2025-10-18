# 🔔 Sistema de Notificaciones - Guía Completa

## ✨ Características Implementadas

### 1. **Notificaciones In-App** 📱

**Bell Icon en Navegación:**
- Badge con contador animado de notificaciones sin leer
- Muestra "9+" cuando hay más de 9 notificaciones
- Actualización automática cada 30 segundos

**Dropdown Panel:**
- Últimas 10 notificaciones
- Indicador visual de no leídas (punto azul)
- Tiempo relativo (Hace 2h, Hace 1d)
- Botones de acción (marcar leída, eliminar)
- Link directo al centro de notificaciones

### 2. **Centro de Notificaciones** 🎯

**Funcionalidades:**
- Vista completa de todas las notificaciones
- Filtros: Todas / Sin leer / Leídas
- Búsqueda en tiempo real
- Marcar todas como leídas
- Eliminar todas (con confirmación)
- Navegación a recursos relacionados
- Cards con colores por tipo

**Tipos de Notificaciones:**
- 💰 **Pagos**: Transacciones, reembolsos
- 🤝 **Afiliados**: Comisiones, conversiones
- 📢 **Campañas**: Rendimiento, alertas
- 🛍️ **Productos**: Ventas, actualizaciones
- ⭐ **Suscripciones**: Nuevos suscriptores, renovaciones
- 🔔 **Sistema**: Actualizaciones, mantenimiento
- ✅ **Éxito**: Operaciones completadas
- ⚠️ **Advertencia**: Alertas importantes
- ❌ **Error**: Problemas críticos
- ℹ️ **Info**: Información general

### 3. **Preferencias de Notificaciones** ⚙️

**Configuración Global:**
- Email Notifications (activar/desactivar)
- Push Notifications (próximamente)

**Preferencias por Tipo:**
Puedes activar/desactivar notificaciones para:
- Pagos y Transacciones
- Programa de Afiliados
- Campañas Publicitarias
- Productos y Ventas
- Suscripciones
- Sistema y Actualizaciones

**Email Digest:**
- **Nunca**: No recibir resúmenes
- **Diario**: Resumen diario de notificaciones
- **Semanal**: Resumen semanal
- **Mensual**: Resumen mensual

## 🚀 Cómo Usar

### Ver Notificaciones

1. **Desde el Bell Icon:**
   - Click en el ícono de campana en la navegación
   - Ver últimas 10 notificaciones
   - Marcar como leída o eliminar

2. **Centro de Notificaciones:**
   - Click en "Ver todas las notificaciones" en el dropdown
   - O navega a `/notifications`
   - Usa filtros y búsqueda para encontrar notificaciones específicas

### Gestionar Notificaciones

**Marcar como Leída:**
- Click en el ícono ✅ en la notificación
- O click en "Marcar todas" para marcar todas

**Eliminar:**
- Click en el ícono 🗑️ en la notificación
- O click en "Eliminar todas" (con confirmación)

**Navegar a Recurso:**
- Click en la notificación para ir al recurso relacionado
- Automáticamente se marca como leída

### Configurar Preferencias

1. Navega a `/notifications/preferences`
2. Activa/desactiva tipos de notificaciones
3. Configura email digest
4. Click en "Guardar Cambios"

## 🛠️ Para Desarrolladores

### Backend API

#### Crear Notificación (Sistema/Admin)

```python
POST /api/notifications
{
  "user_email": "user@example.com",
  "type": "payment",
  "title": "Pago Recibido",
  "message": "Tu pago de $100 ha sido procesado",
  "link": "/revenue",
  "icon": "payment",
  "metadata": {"amount": 100}
}
```

#### Listar Notificaciones

```python
GET /api/notifications?user_email=user@example.com&unread_only=false&limit=50
```

#### Contador de No Leídas

```python
GET /api/notifications/count?user_email=user@example.com
```

#### Marcar como Leída

```python
PATCH /api/notifications/{notification_id}/read
```

#### Marcar Todas como Leídas

```python
PATCH /api/notifications/read-all?user_email=user@example.com
```

#### Eliminar Notificación

```python
DELETE /api/notifications/{notification_id}
```

#### Obtener Preferencias

```python
GET /api/notifications/preferences?user_email=user@example.com
```

#### Actualizar Preferencias

```python
PATCH /api/notifications/preferences?user_email=user@example.com
{
  "email_notifications": true,
  "notify_payments": true,
  "notify_affiliates": false,
  "email_digest": "daily"
}
```

### Crear Notificación Desde Código

```python
from backend.server import create_notification_internal

# Dentro de una función async
await create_notification_internal(
    user_email="user@example.com",
    notification_type="payment",
    title="💰 Pago Recibido",
    message="Tu pago ha sido procesado exitosamente",
    link="/revenue",
    icon="payment",
    metadata={"amount": 100, "transaction_id": "txn_123"}
)
```

### Frontend - Componentes

#### NotificationBell
Usado en navegación principal:

```jsx
import NotificationBell from './components/NotificationBell';

// En tu componente de navegación
<NotificationBell />
```

#### NotificationsPage
Ruta: `/notifications`

#### NotificationPreferencesPage
Ruta: `/notifications/preferences`

### Polling Automático

El bell icon actualiza el contador cada 30 segundos automáticamente:

```javascript
useEffect(() => {
  if (user) {
    loadUnreadCount();
    const interval = setInterval(loadUnreadCount, 30000);
    return () => clearInterval(interval);
  }
}, [user]);
```

## 📋 Eventos que Disparan Notificaciones

### Actualmente Implementados

1. **Pago Exitoso**
   - Se dispara cuando un pago es completado
   - Notifica al usuario que realizó el pago
   - Incluye monto y link a ingresos

2. **Comisión de Afiliado**
   - Se dispara cuando se genera una comisión
   - Notifica al afiliado que ganó la comisión
   - Incluye monto y link al dashboard de afiliado

### Próximamente

- Nueva suscripción
- Renovación de suscripción
- Cancelación de suscripción
- Campaña completada
- Producto destacado
- Bajo inventario
- Carrito abandonado recuperado
- Test A/B completado

## 🧪 Testing

### Crear Notificaciones de Prueba

```bash
cd /app
python3 create_test_notifications.py
```

Esto crea 8 notificaciones de ejemplo con diferentes tipos.

### Verificar Contador

```bash
curl http://localhost:8001/api/notifications/count?user_email=test@example.com
```

### Listar Notificaciones

```bash
curl http://localhost:8001/api/notifications?user_email=test@example.com&limit=10
```

## 🎨 Personalización

### Agregar Nuevo Tipo de Notificación

1. **Backend** - Agregar en `create_notification_internal`:
```python
type_map = {
    "payment": prefs.get('notify_payments', True),
    "your_new_type": prefs.get('notify_your_new_type', True),
    # ...
}
```

2. **Frontend** - Agregar ícono en `getNotificationIcon`:
```javascript
const iconMap = {
  payment: '💰',
  your_new_type: '🎉',
  // ...
};
```

3. **Preferencias** - Agregar toggle:
```python
# En NotificationPreferences model
notify_your_new_type: bool = True
```

### Cambiar Frecuencia de Polling

En `NotificationBell.js`:
```javascript
const interval = setInterval(loadUnreadCount, 30000); // 30 segundos
// Cambiar a 60000 para 1 minuto, etc.
```

## 📊 Estructura de Datos

### Notification Document

```json
{
  "id": "uuid",
  "user_email": "user@example.com",
  "type": "payment",
  "title": "Pago Recibido",
  "message": "Tu pago de $100 ha sido procesado",
  "link": "/revenue",
  "icon": "payment",
  "is_read": false,
  "is_archived": false,
  "metadata": {
    "amount": 100,
    "transaction_id": "txn_123"
  },
  "created_at": "2025-10-18T12:00:00Z",
  "read_at": null
}
```

### NotificationPreferences Document

```json
{
  "id": "uuid",
  "user_email": "user@example.com",
  "email_notifications": true,
  "push_notifications": false,
  "notify_payments": true,
  "notify_affiliates": true,
  "notify_campaigns": true,
  "notify_products": true,
  "notify_subscriptions": true,
  "notify_system": true,
  "email_digest": "daily",
  "created_at": "2025-10-18T12:00:00Z",
  "updated_at": "2025-10-18T12:00:00Z"
}
```

## 🔮 Próximas Mejoras

1. **Email Notifications**
   - Integración con SendGrid/AWS SES
   - Templates HTML personalizados
   - Email digest implementation

2. **Push Notifications**
   - Service Worker para web push
   - FCM para notificaciones móviles

3. **Real-time Updates**
   - WebSockets en lugar de polling
   - Notificaciones instantáneas

4. **Advanced Features**
   - Notificaciones programadas
   - Notificaciones recurrentes
   - Notificaciones basadas en eventos complejos
   - Analytics de notificaciones

---

**¿Preguntas o problemas?**  
Revisa los logs del backend o contacta al equipo de desarrollo.
