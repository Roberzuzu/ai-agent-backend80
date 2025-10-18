# 🔔 Configuración de Webhooks de Stripe

## Guía Completa de Implementación

### 📋 Resumen
Este sistema de webhooks maneja automáticamente eventos de Stripe con logging completo, reintentos y verificación de firma.

---

## 🚀 Paso 1: Configurar Webhook en Stripe Dashboard

### A. Ir al Dashboard de Stripe
1. Accede a: https://dashboard.stripe.com/webhooks
2. Click en "Add endpoint" o "Agregar endpoint"

### B. Configurar el Endpoint
```
URL del Endpoint: https://tu-dominio.com/api/webhook/stripe
```

**Para desarrollo local con Stripe CLI:**
```bash
stripe listen --forward-to localhost:8001/api/webhook/stripe
```

### C. Seleccionar Eventos
Marca los siguientes eventos:

**Checkout:**
- ✓ `checkout.session.completed`
- ✓ `checkout.session.expired`

**Payment Intents:**
- ✓ `payment_intent.succeeded`
- ✓ `payment_intent.payment_failed`

**Subscriptions:**
- ✓ `customer.subscription.created`
- ✓ `customer.subscription.updated`
- ✓ `customer.subscription.deleted`

**Invoices:**
- ✓ `invoice.payment_succeeded`
- ✓ `invoice.payment_failed`

### D. Obtener Webhook Secret
1. Después de crear el endpoint, verás un **Signing secret**
2. Copia el secret (empieza con `whsec_...`)
3. Agrégalo a tu archivo `.env`:

```bash
STRIPE_WEBHOOK_SECRET="whsec_tu_secret_aqui"
```

---

## 🧪 Paso 2: Testing de Webhooks

### Opción 1: Stripe CLI (Recomendado para Desarrollo)

1. **Instalar Stripe CLI:**
```bash
# macOS
brew install stripe/stripe-cli/stripe

# Linux
wget https://github.com/stripe/stripe-cli/releases/download/v1.19.5/stripe_1.19.5_linux_x86_64.tar.gz
tar -xvf stripe_1.19.5_linux_x86_64.tar.gz
sudo mv stripe /usr/local/bin/

# Windows
scoop install stripe
```

2. **Login:**
```bash
stripe login
```

3. **Forward webhooks al servidor local:**
```bash
stripe listen --forward-to localhost:8001/api/webhook/stripe
```

4. **Trigger eventos de prueba:**
```bash
# Test checkout completado
stripe trigger checkout.session.completed

# Test pago exitoso
stripe trigger payment_intent.succeeded

# Test suscripción creada
stripe trigger customer.subscription.created

# Test pago fallido
stripe trigger payment_intent.payment_failed
```

### Opción 2: Desde Stripe Dashboard

1. Ve a: https://dashboard.stripe.com/webhooks
2. Click en tu webhook endpoint
3. Click en "Send test webhook"
4. Selecciona el tipo de evento
5. Click en "Send test webhook"

---

## 📊 Paso 3: Monitorear Webhooks

### Ver Logs de Webhooks
```bash
GET /api/webhooks/logs?status=failed&limit=50
```

Respuesta:
```json
[
  {
    "id": "uuid",
    "event_id": "evt_xxx",
    "event_type": "checkout.session.completed",
    "status": "processed",
    "retry_count": 0,
    "created_at": "2025-01-01T10:00:00Z",
    "processed_at": "2025-01-01T10:00:01Z"
  }
]
```

### Ver Estadísticas
```bash
GET /api/webhooks/stats
```

Respuesta:
```json
{
  "total_webhooks": 150,
  "by_status": {
    "processed": 145,
    "failed": 5
  },
  "by_type": {
    "checkout.session.completed": 100,
    "payment_intent.succeeded": 50
  },
  "success_rate": 96.67,
  "failed_count": 5
}
```

---

## 🔄 Paso 4: Reintentar Webhooks Fallidos

### Reintentar Manualmente
```bash
POST /api/webhooks/{event_id}/retry
```

Respuesta:
```json
{
  "message": "Webhook retried successfully",
  "retry_count": 2
}
```

---

## 📝 Eventos Soportados

| Evento | Descripción | Acción |
|--------|-------------|--------|
| `checkout.session.completed` | Checkout completado | Actualiza transacción a "paid" |
| `payment_intent.succeeded` | Pago exitoso | Log de confirmación |
| `payment_intent.payment_failed` | Pago fallido | Log de error |
| `customer.subscription.created` | Suscripción creada | Crea registro en DB |
| `customer.subscription.updated` | Suscripción actualizada | Actualiza status |
| `customer.subscription.deleted` | Suscripción cancelada | Marca como cancelled |
| `invoice.payment_succeeded` | Invoice pagado | Log de pago |
| `invoice.payment_failed` | Invoice fallido | Log de error |

---

## 🔐 Seguridad

### Verificación de Firma
El sistema verifica automáticamente la firma de Stripe:

```python
# El endpoint valida que el webhook venga de Stripe
stripe.Webhook.construct_event(body, sig_header, webhook_secret)
```

### Protección contra Duplicados
El sistema detecta y ignora eventos duplicados automáticamente usando `event_id`.

---

## 🚨 Troubleshooting

### Webhook no se recibe

**Problema:** Los webhooks no llegan al servidor

**Solución:**
1. Verifica que la URL esté accesible públicamente
2. Asegúrate que no hay firewall bloqueando
3. Revisa los logs de Stripe Dashboard → Webhooks → Recent events

### Firma inválida

**Problema:** Error "Invalid signature"

**Solución:**
1. Verifica que `STRIPE_WEBHOOK_SECRET` sea correcto
2. Asegúrate de usar el secret del endpoint correcto (test vs live)
3. No modifiques el body del request antes de verificar

### Eventos no se procesan

**Problema:** Webhooks recibidos pero no procesados

**Solución:**
1. Revisa logs: `GET /api/webhooks/logs?status=failed`
2. Ver el error en el campo `error_message`
3. Reintentar: `POST /api/webhooks/{event_id}/retry`

---

## 📊 Logging Detallado

El sistema registra cada paso:

```
📨 Processing webhook: checkout.session.completed (ID: evt_xxx)
✓ Webhook signature verified for event: evt_xxx
💳 Checkout completed: cs_xxx - Status: paid
✓ Transaction updated for session cs_xxx
✅ Successfully processed webhook: checkout.session.completed
```

Símbolos:
- ✓ Éxito
- ⚠️ Advertencia
- ❌ Error
- 📨 Recibido
- 💳 Procesando pago
- 🔔 Suscripción
- 📄 Invoice

---

## 🔧 Configuración Avanzada

### Auto-retry Fallidos (Próximamente)
```python
# Configurar retry automático cada 1 hora por 24 horas
AUTO_RETRY_ENABLED = True
AUTO_RETRY_INTERVAL = 3600  # 1 hora
AUTO_RETRY_MAX_ATTEMPTS = 24
```

### Notificaciones de Errores
```python
# Enviar email cuando webhook falla
WEBHOOK_ERROR_EMAIL = "admin@tu-dominio.com"
```

---

## 📚 Recursos

- [Stripe Webhooks Documentation](https://stripe.com/docs/webhooks)
- [Stripe CLI Documentation](https://stripe.com/docs/stripe-cli)
- [Testing Webhooks](https://stripe.com/docs/webhooks/test)
- [Webhook Best Practices](https://stripe.com/docs/webhooks/best-practices)

---

## ✅ Checklist de Implementación

- [ ] Webhook endpoint configurado en Stripe Dashboard
- [ ] `STRIPE_WEBHOOK_SECRET` agregado al `.env`
- [ ] Backend reiniciado después de agregar secret
- [ ] Testing con Stripe CLI funciona
- [ ] Verificación de firma funciona
- [ ] Eventos se procesan correctamente
- [ ] Logs se registran en la base de datos
- [ ] Dashboard de monitoring configurado

---

## 🎉 ¡Todo Listo!

Tu sistema de webhooks de Stripe está completamente configurado y listo para producción. 

Para verificar que todo funciona:

```bash
# 1. Trigger un test
stripe trigger checkout.session.completed

# 2. Ver logs
curl http://localhost:8001/api/webhooks/logs | jq

# 3. Ver stats
curl http://localhost:8001/api/webhooks/stats | jq
```

Si tienes algún problema, revisa los logs del servidor:
```bash
tail -f /var/log/supervisor/backend.err.log | grep webhook
```
