# 🔍 GUÍA DE DIAGNÓSTICO PARA RENDER.COM

## ✅ STATUS ACTUAL DEL DESPLIEGUE

Tu backend está **LIVE** y funcionando en:
- URL: https://ai-agent-backend80.onrender.com
- Health Check: `/api/health` ✅ (200 OK)
- Swagger UI: `/docs` ✅ (Accesible)

## 🎯 ENDPOINTS DE DIAGNÓSTICO NUEVOS

Ahora tienes estos endpoints para verificar el estado del sistema:

### 1. Status Simple (Sin DB)
```bash
curl https://ai-agent-backend80.onrender.com/api/status/simple
```
**Qué hace:** Verifica que el servidor esté vivo sin depender de MongoDB

### 2. Status Detallado (Con tests de servicios)
```bash
curl https://ai-agent-backend80.onrender.com/api/status/detailed
```
**Qué hace:** 
- Prueba conexión MongoDB
- Verifica todas las API keys configuradas
- Muestra estado de integraciones (WooCommerce, WordPress, Stripe, Telegram)

### 3. Agent Status (Mejorado)
```bash
curl https://ai-agent-backend80.onrender.com/api/agent/status
```
**Qué hace:** 
- Cuenta conversaciones y memorias en MongoDB
- Muestra capacidades del agente
- Manejo robusto de errores si MongoDB falla

### 4. AI Health Check
```bash
curl https://ai-agent-backend80.onrender.com/api/ai/health
```
**Qué hace:** Verifica que todas las APIs de IA estén configuradas

## 🔧 PASOS PARA PROBAR DESPUÉS DEL NUEVO DEPLOY

### Paso 1: Espera 2-3 minutos después del deploy
Render necesita tiempo para:
- Construir la imagen Docker
- Descargar dependencias
- Iniciar el servidor

### Paso 2: Verifica el status simple
```bash
curl https://ai-agent-backend80.onrender.com/api/status/simple
```

**Respuesta esperada:**
```json
{
  "status": "live",
  "message": "Backend funcionando correctamente",
  "service": "Super Cerebro AI Backend",
  "version": "1.0.0",
  "endpoints_available": true,
  "environment": {
    "mongo_configured": true,
    "openrouter_configured": true,
    "openai_configured": true,
    "stripe_configured": true,
    "wc_configured": true
  }
}
```

### Paso 3: Verifica el status detallado
```bash
curl https://ai-agent-backend80.onrender.com/api/status/detailed
```

**Qué revisar:**
- `services.mongodb.status` debe ser `"connected"`
- `services.ai_apis` debe mostrar APIs configuradas
- `services.integrations` debe mostrar integraciones configuradas

### Paso 4: Verifica el agent status
```bash
curl https://ai-agent-backend80.onrender.com/api/agent/status
```

**Qué revisar:**
- `success` debe ser `true`
- `database_connected` debe ser `true`
- `agente_activo` debe ser `true`

## 📋 CHECKLIST DE VARIABLES DE ENTORNO EN RENDER

Asegúrate de tener configuradas estas variables en Render:

### OBLIGATORIAS:
- [ ] `MONGO_URL` - URL de MongoDB Atlas
- [ ] `DB_NAME` - Nombre de la base de datos (default: social_media_monetization)
- [ ] `SECRET_KEY` - Clave secreta para JWT (auto-generada por Render)

### RECOMENDADAS (AI):
- [ ] `OPENROUTER_API_KEY` - Para Claude 3.5 Sonnet
- [ ] `OPENAI_API_KEY` - Para GPT-4 y embeddings
- [ ] `PERPLEXITY_API_KEY` - Para búsquedas en tiempo real
- [ ] `FAL_API_KEY` - Para generación de imágenes

### OPCIONALES (Integraciones):
- [ ] `WC_URL` - URL de WooCommerce
- [ ] `WC_KEY` - Consumer Key de WooCommerce
- [ ] `WC_SECRET` - Consumer Secret de WooCommerce
- [ ] `WP_URL` - URL de WordPress
- [ ] `WP_USER` - Usuario de WordPress
- [ ] `WP_PASS` - Application Password de WordPress
- [ ] `STRIPE_API_KEY` - Para pagos
- [ ] `STRIPE_WEBHOOK_SECRET` - Para webhooks de Stripe
- [ ] `TELEGRAM_BOT_TOKEN` - Para notificaciones Telegram
- [ ] `TELEGRAM_CHAT_ID` - ID del chat de Telegram

## 🐛 CÓMO VER LOS LOGS EN RENDER

1. Ve a tu servicio en Render Dashboard
2. Click en "Logs" en el menú lateral
3. Busca estos mensajes en el log:

```
🚀 SUPER CEREBRO AI - STARTING UP
📋 ENVIRONMENT CONFIGURATION:
   - MongoDB: ✅ Configured
   - OpenRouter API: ✅ Configured
   [...]
✅ SUPER CEREBRO AI - READY TO SERVE
```

### Logs importantes a revisar:

#### ✅ Startup exitoso:
```
INFO - 🚀 SUPER CEREBRO AI - STARTING UP
INFO - ✅ MongoDB connection successful!
INFO - ✅ Database migrations complete
INFO - ✅ SUPER CEREBRO AI - READY TO SERVE
```

#### ❌ Errores comunes:

**Error 1: MongoDB no conecta**
```
ERROR - ❌ MongoDB connection failed: ...
```
**Solución:** Verifica que `MONGO_URL` esté correcta y que tu IP esté en la whitelist de MongoDB Atlas

**Error 2: Variables de entorno faltantes**
```
ERROR - Environment variable not found: ...
```
**Solución:** Añade la variable en Render Dashboard > Environment

**Error 3: Puerto incorrecto**
```
ERROR - Port already in use
```
**Solución:** Render asigna el puerto automáticamente vía variable `$PORT`

## 🔄 FORZAR NUEVO DEPLOY EN RENDER

Si necesitas forzar un nuevo despliegue:

### Opción 1: Desde el Dashboard
1. Ve a tu servicio en Render
2. Click en "Manual Deploy" 
3. Selecciona "Clear build cache & deploy"

### Opción 2: Desde Git (Recomendado)
1. Haz un commit vacío:
```bash
git commit --allow-empty -m "Force Render redeploy"
git push
```

### Opción 3: Webhook
Usa el webhook de deploy desde Render Dashboard

## 📊 MONITOREO CONTINUO

### Health Check Automático
Render hace health checks cada 30 segundos en:
- `/api/health`

Si este endpoint falla 5 veces consecutivas, Render reinicia el servicio automáticamente.

### Verificar uptime
```bash
# Cada 30 segundos, verificar status
watch -n 30 'curl -s https://ai-agent-backend80.onrender.com/api/status/simple | jq'
```

## 🆘 SOLUCIÓN DE PROBLEMAS COMUNES

### Problema: 404 en todos los endpoints
**Causa:** El servidor no está cargando las rutas correctamente
**Solución:** 
1. Verifica los logs de startup
2. Asegúrate que `app.include_router(api_router)` esté en server.py
3. Fuerza un redeploy limpio

### Problema: 500 Internal Server Error
**Causa:** Error en el código o configuración
**Solución:**
1. Revisa los logs en Render para ver el error exacto
2. Verifica que todas las variables obligatorias estén configuradas
3. Prueba el endpoint `/api/status/detailed` para más información

### Problema: Timeout en requests
**Causa:** El servidor está sobrecargado o el proceso es muy largo
**Solución:**
1. Considera upgradeear el plan de Render (más RAM/CPU)
2. Optimiza las queries a MongoDB
3. Implementa caching donde sea posible

### Problema: MongoDB connection timeout
**Causa:** IP no está en whitelist o credenciales incorrectas
**Solución:**
1. En MongoDB Atlas, ve a Network Access
2. Añade `0.0.0.0/0` para permitir todas las IPs (o IP de Render)
3. Verifica usuario/contraseña en la connection string

## ✨ MEJORAS IMPLEMENTADAS

### 1. Logging Mejorado
- ✅ Startup detallado con configuración de environment
- ✅ Test de conexión MongoDB en startup
- ✅ Lista de rutas disponibles en logs
- ✅ Mejor manejo de errores con stack traces

### 2. Endpoints de Diagnóstico
- ✅ `/api/status/simple` - Status sin dependencias
- ✅ `/api/status/detailed` - Status con tests de servicios
- ✅ `/api/agent/status` - Mejorado con mejor error handling

### 3. Robustez
- ✅ El servidor no falla si MongoDB no está disponible
- ✅ Los endpoints de status funcionan independientemente
- ✅ Mejor logging de errores para debugging

## 📞 PRÓXIMOS PASOS

1. **Espera 2-3 minutos** para que Render complete el deploy
2. **Prueba** `/api/status/simple` para confirmar que está live
3. **Verifica** los logs en Render Dashboard
4. **Prueba** `/api/status/detailed` para ver estado de servicios
5. **Reporta** cualquier error que veas en los logs

---

**Última actualización:** 2025-10-28
**Versión:** 1.0.0
