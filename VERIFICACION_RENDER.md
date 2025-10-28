# ✅ LISTA DE VERIFICACIÓN - CEREBRO AI EN RENDER.COM

## 📋 CHECKLIST PRE-DEPLOYMENT

### 1. MONGODB ATLAS
- [ ] Cuenta creada en MongoDB Atlas
- [ ] Cluster gratuito creado (M0)
- [ ] Usuario de base de datos creado
- [ ] IP 0.0.0.0/0 permitida en Network Access
- [ ] Connection string copiado y contraseña reemplazada
- [ ] Nombre de base de datos añadido: `social_media_monetization`

**Connection String debe verse así:**
```
mongodb+srv://cerebro_admin:TU_PASSWORD_AQUI@cerebro-ai-cluster.xxxxx.mongodb.net/social_media_monetization?retryWrites=true&w=majority
```

---

### 2. RENDER.COM - VARIABLES DE ENTORNO

#### 🔴 OBLIGATORIAS (Servidor no arranca sin ellas)

- [ ] `MONGO_URL` - Connection string de MongoDB
- [ ] `DB_NAME` - social_media_monetization
- [ ] `OPENROUTER_API_KEY` - Para Claude 3.5 Sonnet
- [ ] `OPENAI_API_KEY` - Para embeddings y GPT
- [ ] `PERPLEXITY_API_KEY` - Para búsquedas en tiempo real
- [ ] `WC_URL` - https://herramientasyaccesorios.store/wp-json/wc/v3
- [ ] `WC_KEY` - Consumer Key de WooCommerce
- [ ] `WC_SECRET` - Consumer Secret de WooCommerce
- [ ] `WP_URL` - https://herramientasyaccesorios.store/wp-json/wp/v2
- [ ] `WP_USER` - agenteweb@herramientasyaccesorios.store
- [ ] `WP_PASS` - Application Password de WordPress
- [ ] `SECRET_KEY` - Clave secreta de 32+ caracteres
- [ ] `ENVIRONMENT` - production

#### 🟢 OPCIONALES (Funcionalidades extra)

- [ ] `TELEGRAM_BOT_TOKEN` - Para notificaciones Telegram
- [ ] `TELEGRAM_CHAT_ID` - ID del chat de Telegram
- [ ] `FAL_API_KEY` - Para generación de imágenes
- [ ] `ABACUS_API_KEY` - Para análisis predictivo
- [ ] `STRIPE_API_KEY` - Para procesar pagos
- [ ] `STRIPE_WEBHOOK_SECRET` - Para webhooks de Stripe
- [ ] `INSTAGRAM_TOKEN` - Para publicar en Instagram
- [ ] `FACEBOOK_TOKEN` - Para publicar en Facebook
- [ ] `SENTRY_DSN` - Para monitoring de errores

---

### 3. RENDER.COM - CONFIGURACIÓN DEL SERVICIO

- [ ] Build Command: `cd backend && pip install -r requirements_standalone.txt`
- [ ] Start Command: `cd backend && uvicorn server:app --host 0.0.0.0 --port $PORT --workers 1`
- [ ] Health Check Path: `/api/health`
- [ ] Auto-Deploy activado
- [ ] Region seleccionada (Frankfurt recomendado para España)

---

### 4. DEPLOYMENT

- [ ] Click en "Manual Deploy" → "Deploy latest commit"
- [ ] Esperar 5-8 minutos
- [ ] Status cambió a "Live" 🟢
- [ ] No hay errores en los logs

---

### 5. TESTS DE VERIFICACIÓN

#### Test 1: Health Check
```bash
curl https://TU-URL.onrender.com/api/health
```

**Respuesta esperada:**
```json
{
  "status": "healthy",
  "services": {
    "database": "connected",
    "ai": "available"
  }
}
```

- [ ] Health check responde correctamente

---

#### Test 2: Status del Agente
```bash
curl -X POST https://TU-URL.onrender.com/api/agent/status
```

**Respuesta esperada:**
```json
{
  "success": true,
  "agente_activo": true,
  "conversaciones_totales": 0,
  "memorias_guardadas": 0,
  "herramientas_disponibles": 18,
  "caracteristicas": {
    "memoria_persistente": true,
    "busqueda_semantica": true,
    "rag_enabled": true,
    "embeddings": true
  }
}
```

- [ ] Status del agente responde correctamente
- [ ] 18 herramientas disponibles

---

#### Test 3: Comando Simple
```bash
curl -X POST https://TU-URL.onrender.com/api/agent/execute \
  -H "Content-Type: application/json" \
  -d '{
    "command": "Dame las estadísticas del sitio",
    "user_id": "test_user"
  }'
```

**Respuesta esperada:**
```json
{
  "success": true,
  "mensaje": "Voy a obtener las estadísticas...",
  "plan": "...",
  "acciones_planificadas": 1,
  "resultados": [...],
  "completado": true
}
```

- [ ] Comando ejecutado correctamente
- [ ] Respuesta recibida en menos de 10 segundos

---

### 6. WORDPRESS - INSTALACIÓN DEL PLUGIN

- [ ] Acceso a WordPress: https://herramientasyaccesorios.store/wp-admin
- [ ] Usuario: agenteweb@herramientasyaccesorios.store
- [ ] Plugin `cerebro-ai-woocommerce.zip` descargado de `/app/`
- [ ] Plugin subido e instalado
- [ ] Plugin activado
- [ ] Menú "Cerebro AI" visible en el sidebar

---

### 7. WORDPRESS - CONFIGURACIÓN DEL PLUGIN

- [ ] URL de API configurada: `https://TU-URL.onrender.com/api`
- [ ] Chat flotante activado
- [ ] Posición: bottom-right
- [ ] Solo administradores: activado
- [ ] Cambios guardados

---

### 8. WORDPRESS - VERIFICACIÓN FRONTEND

- [ ] Botón flotante visible en esquina inferior derecha
- [ ] Click en botón abre el chat
- [ ] Mensaje de bienvenida se muestra
- [ ] Input de texto funciona

---

### 9. WORDPRESS - TEST DE COMANDO

**Comando de prueba:** "Dame las estadísticas de mi tienda"

- [ ] Comando enviado desde el chat
- [ ] Indicador de "escribiendo..." aparece
- [ ] Respuesta recibida en 2-10 segundos
- [ ] Respuesta se muestra correctamente
- [ ] Sin errores en consola del navegador (F12)

---

### 10. VERIFICACIÓN DE LOGS

#### Logs de Render
- [ ] Sin errores críticos en logs
- [ ] Requests aparecen en logs
- [ ] Respuestas 200 OK

#### Logs de WordPress
- [ ] Sin errores PHP
- [ ] Sin errores JavaScript en consola

---

## 🎯 TESTS AVANZADOS

### Test de Memoria Persistente
```bash
# Comando 1
curl -X POST https://TU-URL.onrender.com/api/agent/execute \
  -H "Content-Type: application/json" \
  -d '{
    "command": "Me llamo Pedro y soy de Madrid",
    "user_id": "test_pedro"
  }'

# Esperar 3 segundos

# Comando 2 - Debe recordar el nombre
curl -X POST https://TU-URL.onrender.com/api/agent/execute \
  -H "Content-Type: application/json" \
  -d '{
    "command": "¿Cómo me llamo?",
    "user_id": "test_pedro"
  }'
```

- [ ] El agente recuerda el nombre "Pedro"
- [ ] Memoria persistente funciona

---

### Test de Herramientas

#### Test 1: Búsqueda de Tendencias
```bash
curl -X POST https://TU-URL.onrender.com/api/agent/execute \
  -H "Content-Type: application/json" \
  -d '{
    "command": "Busca las 5 herramientas más vendidas en España",
    "user_id": "test_user"
  }'
```

- [ ] Usa herramienta `buscar_tendencias`
- [ ] Responde con productos/tendencias
- [ ] Sin errores

---

#### Test 2: Estadísticas WooCommerce
```bash
curl -X POST https://TU-URL.onrender.com/api/agent/execute \
  -H "Content-Type: application/json" \
  -d '{
    "command": "Dame las estadísticas de productos",
    "user_id": "test_user"
  }'
```

- [ ] Usa herramienta `obtener_estadisticas`
- [ ] Responde con números reales de WooCommerce
- [ ] Sin errores de conexión

---

### Test 3: Análisis de Competencia
```bash
curl -X POST https://TU-URL.onrender.com/api/agent/execute \
  -H "Content-Type: application/json" \
  -d '{
    "command": "Analiza la competencia de taladros Bosch",
    "user_id": "test_user"
  }'
```

- [ ] Usa herramienta `analizar_competencia`
- [ ] Responde con análisis detallado
- [ ] Sin errores

---

## 🔥 TESTS DE STRESS

### Test de Múltiples Requests
```bash
# Enviar 5 comandos seguidos
for i in {1..5}; do
  curl -X POST https://TU-URL.onrender.com/api/agent/execute \
    -H "Content-Type: application/json" \
    -d "{\"command\": \"Test $i\", \"user_id\": \"stress_test\"}" &
done
```

- [ ] Todos los requests responden
- [ ] No hay errores de timeout
- [ ] Servidor no se cae

---

### Test de Memoria con 10 Conversaciones
```bash
# Crear 10 conversaciones diferentes
for i in {1..10}; do
  curl -X POST https://TU-URL.onrender.com/api/agent/execute \
    -H "Content-Type: application/json" \
    -d "{\"command\": \"Mi número favorito es $i\", \"user_id\": \"user_$i\"}"
done
```

- [ ] Todas las conversaciones se guardan
- [ ] MongoDB no reporta errores
- [ ] Búsqueda semántica funciona

---

## 📊 MÉTRICAS DE PERFORMANCE

### Tiempos de Respuesta Esperados

| Operación | Tiempo Esperado | Tu Resultado |
|-----------|-----------------|--------------|
| Health Check | < 1 segundo | _____ seg |
| Comando simple | 2-5 segundos | _____ seg |
| Búsqueda de tendencias | 5-10 segundos | _____ seg |
| Análisis de competencia | 8-15 segundos | _____ seg |
| Generación de imágenes | 30-60 segundos | _____ seg |

- [ ] Todos los tiempos están dentro del rango esperado

---

### Uso de Recursos (Render Metrics)

| Recurso | Uso Esperado | Tu Resultado |
|---------|--------------|--------------|
| CPU | 20-40% en idle | _____ % |
| CPU bajo carga | 60-90% | _____ % |
| RAM | 250-400 MB | _____ MB |
| Requests/min | Variable | _____ req/min |

- [ ] Recursos dentro de límites del plan

---

## 🛡️ SEGURIDAD

### Verificaciones de Seguridad

- [ ] HTTPS activado (Render lo hace automático)
- [ ] Variables de entorno NO visibles en código
- [ ] API Keys NO expuestas en frontend
- [ ] CORS configurado correctamente
- [ ] WordPress nonce implementado
- [ ] Permisos de usuario verificados
- [ ] MongoDB usa autenticación
- [ ] Network Access de MongoDB restringido a 0.0.0.0/0

---

## 💰 MONITOREO DE COSTOS

### Render.com
- [ ] Plan actual: _______ ($0 o $7/mes)
- [ ] Plan suficiente para tráfico actual: Sí / No
- [ ] Sleep activado: Sí / No

### MongoDB Atlas
- [ ] Plan actual: Free (M0)
- [ ] Storage usado: _____ MB / 512 MB
- [ ] Connections actuales: _____

### APIs de IA
- [ ] OpenRouter uso este mes: $______
- [ ] OpenAI uso este mes: $______
- [ ] Perplexity uso este mes: $______
- [ ] Total APIs: $______

---

## 🎉 RESUMEN FINAL

### ✅ TODO FUNCIONA SI:

- [x] ✅ Backend responde en Render (status: Live)
- [x] ✅ MongoDB conectado (health check OK)
- [x] ✅ Health check retorna "healthy"
- [x] ✅ Status del agente muestra 18 herramientas
- [x] ✅ Comandos simples funcionan
- [x] ✅ Plugin WordPress instalado y activado
- [x] ✅ Chat flotante visible en el sitio
- [x] ✅ Comandos desde WordPress funcionan
- [x] ✅ Memoria persistente guarda conversaciones
- [x] ✅ Sin errores en logs de Render
- [x] ✅ Sin errores en consola de WordPress

---

## 🚨 PROBLEMAS COMUNES Y SOLUCIONES

### ❌ Backend no arranca en Render

**Síntomas:**
- Status: "Build failed" o "Deploy failed"
- Errores en logs sobre dependencias

**Solución:**
1. Verifica `requirements_standalone.txt` existe en `/app/backend/`
2. Verifica Build Command: `cd backend && pip install -r requirements_standalone.txt`
3. Click "Clear build cache & deploy"

---

### ❌ "Database connection failed"

**Síntomas:**
- Health check retorna error
- Logs muestran "Can't connect to MongoDB"

**Solución:**
1. Verifica `MONGO_URL` en variables de Render
2. Verifica que la contraseña no tenga caracteres especiales sin escapar
3. Verifica que 0.0.0.0/0 esté permitido en MongoDB Atlas
4. Prueba la connection string con `mongosh`:
   ```bash
   mongosh "mongodb+srv://cerebro_admin:PASSWORD@cluster.mongodb.net/social_media_monetization"
   ```

---

### ❌ "AI generation failed"

**Síntomas:**
- Comandos fallan con error de AI
- Logs muestran "API key invalid"

**Solución:**
1. Verifica API keys en Render Environment
2. Prueba las keys manualmente:
   ```bash
   # Test OpenRouter
   curl https://openrouter.ai/api/v1/models \
     -H "Authorization: Bearer $OPENROUTER_API_KEY"
   
   # Test OpenAI
   curl https://api.openai.com/v1/models \
     -H "Authorization: Bearer $OPENAI_API_KEY"
   ```
3. Verifica saldo en las cuentas de APIs

---

### ❌ Chat no aparece en WordPress

**Síntomas:**
- Botón flotante invisible
- Sin errores en consola

**Solución:**
1. Verifica que estás logueado como admin de WooCommerce
2. Verifica que el plugin esté activado
3. Verifica configuración: Chat activado = ✅
4. Limpia caché de WordPress
5. Abre consola (F12) y busca errores JS

---

### ❌ "Could not connect to API" desde WordPress

**Síntomas:**
- Chat se abre pero comandos fallan
- Error de conexión en el chat

**Solución:**
1. Verifica URL de API en configuración del plugin
2. URL debe ser: `https://TU-URL.onrender.com/api` (sin barra final)
3. Prueba la URL manualmente desde navegador
4. Verifica CORS en backend (ya está configurado)
5. Revisa logs de Render para ver si llegan los requests

---

## 📞 CONTACTO DE SOPORTE

Si después de todas las verificaciones algo no funciona:

1. **Revisa logs detallados:**
   - Render: https://dashboard.render.com/web/srv-d3tot4muk2gs73dbhid0/logs
   - MongoDB Atlas: Metrics → Database Access
   - WordPress: Herramientas → Salud del sitio

2. **Información a reportar:**
   - URL del backend en Render
   - Mensaje de error exacto (captura de pantalla)
   - Logs relevantes (últimas 50 líneas)
   - Variables de entorno configuradas (sin revelar valores)

---

## ✅ CHECKLIST FINAL

### Deployment Completado

- [ ] ✅ MongoDB Atlas configurado y conectado
- [ ] ✅ Backend desplegado en Render (Live)
- [ ] ✅ Todas las variables de entorno configuradas
- [ ] ✅ Health check OK
- [ ] ✅ Status del agente OK (18 herramientas)
- [ ] ✅ Plugin WordPress instalado y activado
- [ ] ✅ Chat flotante funcionando
- [ ] ✅ Comandos ejecutándose correctamente
- [ ] ✅ Memoria persistente guardando conversaciones
- [ ] ✅ Sin errores en logs

### Listo para Producción

- [ ] ✅ Plan de pago en Render configurado ($7/mes) para evitar sleep
- [ ] ✅ Backups de MongoDB Atlas configurados
- [ ] ✅ Monitoring activado (opcional: Sentry)
- [ ] ✅ Dominio personalizado configurado (opcional)
- [ ] ✅ SSL/HTTPS activado (automático en Render)

---

**🎉 ¡FELICIDADES! Cerebro AI está funcionando 24/7 independientemente de Emergent.**

Fecha de deployment: _____________  
URL del backend: _____________  
Status: ✅ OPERACIONAL
