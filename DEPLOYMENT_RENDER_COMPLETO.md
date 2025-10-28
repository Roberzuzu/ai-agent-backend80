# 🚀 DESPLIEGUE COMPLETO EN RENDER.COM - CEREBRO AI 24/7

## 📋 RESUMEN EJECUTIVO

Esta guía te permitirá desplegar Cerebro AI en Render.com para que funcione **24/7 independientemente de Emergent**.

**Tiempo estimado:** 20-30 minutos  
**Costo:** Gratuito (plan Starter) o $7/mes (plan Starter Plus recomendado)  
**Resultado:** Backend funcionando 24/7 + Plugin WordPress conectado

---

## 🎯 ARQUITECTURA FINAL

```
┌─────────────────────────────────────────────────────────────┐
│                    RENDER.COM (24/7)                        │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  Backend API (FastAPI + Uvicorn)                       │ │
│  │  URL: https://cerebro-ai-backend.onrender.com         │ │
│  │  - 18 herramientas AI                                  │ │
│  │  - Claude 3.5 Sonnet                                   │ │
│  │  - Memoria persistente                                 │ │
│  └────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                            │
                            │ HTTPS/API
                            ▼
┌─────────────────────────────────────────────────────────────┐
│              WORDPRESS (Hostinger)                          │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  Plugin: Cerebro AI WooCommerce                        │ │
│  │  - Chat widget flotante                                │ │
│  │  - Panel de administración                             │ │
│  │  - Integración WooCommerce                             │ │
│  └────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                            │
                            │ API REST
                            ▼
┌─────────────────────────────────────────────────────────────┐
│            MONGODB ATLAS (Cloud Database)                   │
│  - Memoria del agente                                       │
│  - Conversaciones                                           │
│  - Historial de acciones                                    │
└─────────────────────────────────────────────────────────────┘
```

---

## ✅ PREREQUISITOS

Antes de comenzar, necesitas:

### 1. Cuentas
- ✅ Cuenta Render.com: https://render.com (ya tienes)
- ✅ Cuenta MongoDB Atlas: https://cloud.mongodb.com (gratis)
- ✅ Acceso WordPress: herramientasyaccesorios.store ✅

### 2. API Keys (ya las tienes en Render)
- OpenRouter API Key (Claude 3.5 Sonnet)
- OpenAI API Key (Embeddings)
- Perplexity API Key (Búsquedas)
- Fal API Key (Imágenes)
- Abacus API Key (Análisis predictivo)
- WooCommerce Consumer Key + Secret
- WordPress User + Application Password

---

## 📝 PASO 1: CONFIGURAR MONGODB ATLAS (5 minutos)

### 1.1 Crear Cluster Gratuito

1. Ve a: https://cloud.mongodb.com
2. **Sign Up / Log In** con Google o Email
3. Click **"Build a Database"**
4. Selecciona **"Shared"** (Gratis para siempre)
5. Elige región: **Frankfurt (eu-central-1)** (más cercana a España)
6. Nombre del cluster: `cerebro-ai-cluster`
7. Click **"Create"**

⏱️ Espera 2-3 minutos mientras se crea el cluster.

### 1.2 Configurar Acceso

1. **Network Access:**
   - Click en **"Network Access"** en el menú lateral
   - Click **"Add IP Address"**
   - Click **"Allow Access from Anywhere"** (0.0.0.0/0)
   - Click **"Confirm"**
   
   ⚠️ Esto permite que Render.com se conecte desde cualquier IP.

2. **Database User:**
   - Click en **"Database Access"**
   - Click **"Add New Database User"**
   - Método: **Password**
   - Username: `cerebro_admin`
   - Password: Genera una contraseña segura (cópiala!)
   - Built-in Role: **"Atlas Admin"**
   - Click **"Add User"**

### 1.3 Obtener Connection String

1. Click **"Connect"** en tu cluster
2. Selecciona **"Connect your application"**
3. Driver: **Python**, Version: **3.12 or later**
4. Copia el connection string:

```
mongodb+srv://cerebro_admin:<password>@cerebro-ai-cluster.xxxxx.mongodb.net/?retryWrites=true&w=majority
```

5. **Reemplaza `<password>`** con tu contraseña
6. **Añade el nombre de la base de datos** al final:

```
mongodb+srv://cerebro_admin:TU_PASSWORD@cerebro-ai-cluster.xxxxx.mongodb.net/social_media_monetization?retryWrites=true&w=majority
```

💾 **GUARDA ESTE STRING** - lo necesitarás en Render.

---

## 🚀 PASO 2: DESPLEGAR BACKEND EN RENDER.COM (10 minutos)

### 2.1 Verificar Servicio Existente

Ya tienes un servicio en Render:
- **Service ID:** `srv-d3tot4muk2gs73dbhid0`
- **Dashboard:** https://dashboard.render.com/web/srv-d3tot4muk2gs73dbhid0

### 2.2 Configurar Variables de Entorno

1. Ve a tu servicio: https://dashboard.render.com/web/srv-d3tot4muk2gs73dbhid0
2. Click en **"Environment"** en el menú lateral
3. Verifica/añade estas variables:

#### 🔴 OBLIGATORIAS (Servidor no arranca sin ellas)

```bash
# MONGODB
MONGO_URL=mongodb+srv://cerebro_admin:TU_PASSWORD@cerebro-ai-cluster.xxxxx.mongodb.net/social_media_monetization?retryWrites=true&w=majority
DB_NAME=social_media_monetization

# AI KEYS (Claude 3.5 Sonnet)
OPENROUTER_API_KEY=sk-or-v1-xxxxx

# OpenAI (Embeddings + GPT)
OPENAI_API_KEY=sk-xxxxx

# Perplexity (Búsquedas en tiempo real)
PERPLEXITY_API_KEY=pplx-xxxxx

# WOOCOMMERCE
WC_URL=https://herramientasyaccesorios.store/wp-json/wc/v3
WC_KEY=ck_xxxxx
WC_SECRET=cs_xxxxx

# WORDPRESS
WP_URL=https://herramientasyaccesorios.store/wp-json/wp/v2
WP_USER=agenteweb@herramientasyaccesorios.store
WP_PASS=j(t(xcePLL^Wt09XTXubC!pJ

# SECURITY
SECRET_KEY=genera-una-clave-segura-aqui-min-32-caracteres-aleatorios
ENVIRONMENT=production
```

#### 🟢 OPCIONALES (Funcionalidades extra)

```bash
# Telegram Bot (Opcional)
TELEGRAM_BOT_TOKEN=7708509018:xxxxx
TELEGRAM_CHAT_ID=7202793910

# Fal AI (Generación de imágenes - Opcional)
FAL_API_KEY=xxxxx

# Abacus AI (Análisis predictivo - Opcional)
ABACUS_API_KEY=xxxxx

# Stripe (Pagos - Opcional)
STRIPE_API_KEY=sk_test_xxxxx
STRIPE_WEBHOOK_SECRET=whsec_xxxxx

# Redes Sociales (Opcional)
INSTAGRAM_TOKEN=xxxxx
FACEBOOK_TOKEN=xxxxx

# Monitoring (Opcional)
SENTRY_DSN=https://xxxxx@sentry.io/xxxxx
```

### 2.3 Configurar Build y Start Commands

1. En **"Settings"** de tu servicio
2. **Build Command:**
   ```bash
   cd backend && pip install -r requirements_standalone.txt
   ```

3. **Start Command:**
   ```bash
   cd backend && uvicorn server:app --host 0.0.0.0 --port $PORT --workers 1
   ```

4. **Health Check Path:**
   ```
   /api/health
   ```

### 2.4 Desplegar

1. Click **"Manual Deploy"** → **"Deploy latest commit"**
2. Espera 5-8 minutos mientras:
   - Se instalan las dependencias
   - Se inicia el servidor
   - Se pasan los health checks

3. **Verificar deployment:**
   - Logs deben mostrar: `Uvicorn running on http://0.0.0.0:10000`
   - Status: **"Live"** 🟢

### 2.5 Obtener URL del Backend

Tu backend estará disponible en:
```
https://cerebro-ai-backend-XXXX.onrender.com
```

O verifica en el dashboard de Render en la parte superior.

💾 **COPIA ESTA URL** - la necesitarás para el plugin WordPress.

---

## 🧪 PASO 3: PROBAR EL BACKEND (2 minutos)

### 3.1 Test de Health Check

Abre en tu navegador:
```
https://TU-URL.onrender.com/api/health
```

Debes ver:
```json
{
  "status": "healthy",
  "services": {
    "database": "connected",
    "ai": "available"
  }
}
```

### 3.2 Test del Agente AI

```bash
curl -X POST https://TU-URL.onrender.com/api/agent/status
```

Debe retornar:
```json
{
  "success": true,
  "agente_activo": true,
  "herramientas_disponibles": 18,
  "caracteristicas": {
    "memoria_persistente": true,
    "busqueda_semantica": true
  }
}
```

✅ **Si ves esto, el backend funciona correctamente!**

---

## 🔌 PASO 4: INSTALAR PLUGIN EN WORDPRESS (5 minutos)

### 4.1 Crear ZIP del Plugin

El plugin ya está preparado en:
```
/app/wordpress-plugin/cerebro-ai-woocommerce/
```

Necesitas crear un ZIP con todos los archivos.

**Estructura del ZIP:**
```
cerebro-ai-woocommerce.zip
└── cerebro-ai-woocommerce/
    ├── cerebro-ai.php
    ├── README.md
    ├── assets/
    │   ├── admin.css
    │   ├── chat.css
    │   └── chat.js
    └── templates/
        ├── admin-page.php
        ├── chat-widget.php
        └── chat-inline.php
```

### 4.2 Subir e Instalar en WordPress

1. **Accede a WordPress:**
   - URL: https://herramientasyaccesorios.store/wp-admin
   - Usuario: `agenteweb@herramientasyaccesorios.store`
   - Password: `j(t(xcePLL^Wt09XTXubC!pJ`

2. **Instalar Plugin:**
   - Ve a: **Plugins** → **Añadir nuevo**
   - Click **"Subir plugin"**
   - Selecciona `cerebro-ai-woocommerce.zip`
   - Click **"Instalar ahora"**
   - Click **"Activar plugin"**

3. **Verificar instalación:**
   - Debe aparecer **"Cerebro AI"** en el menú lateral de WordPress
   - Con icono de cerebro 🧠

---

## ⚙️ PASO 5: CONFIGURAR EL PLUGIN (3 minutos)

### 5.1 Configuración Básica

1. Ve a: **Cerebro AI** → **Configuración** en WordPress

2. **URL de la API:**
   ```
   https://TU-URL.onrender.com/api
   ```
   ⚠️ **IMPORTANTE:** NO incluir barra final

3. **Posición del Chat:**
   - Selecciona: `bottom-right` (esquina inferior derecha)

4. **Opciones:**
   - ✅ Activar chat flotante
   - ✅ Solo para administradores de WooCommerce

5. Click **"Guardar cambios"**

### 5.2 Verificar Funcionamiento

1. **Abrir cualquier página de tu sitio** (herramientasyaccesorios.store)

2. **Buscar el botón flotante:**
   - Esquina inferior derecha
   - Icono de cerebro 🧠
   - Badge "AI"

3. **Hacer click en el botón:**
   - Debe abrirse el chat
   - Mensaje de bienvenida de Cerebro AI
   - Input para escribir comandos

4. **Probar comando:**
   - Escribe: `"Dame las estadísticas de mi tienda"`
   - Click enviar o Enter
   - Debe aparecer indicador de "escribiendo..."
   - Respuesta del agente AI en 2-5 segundos

✅ **Si funciona, todo está conectado correctamente!**

---

## 🎉 PASO 6: CASOS DE USO (Ejemplos)

### 6.1 Comandos de Productos

```
"Busca 10 herramientas eléctricas tendencia"
"Crea un producto llamado Taladro Bosch 750W a 89 euros"
"Actualiza el precio del producto ID 123 a 120 euros"
"Optimiza todos los productos de la categoría herramientas"
```

### 6.2 Análisis y Estadísticas

```
"Dame las estadísticas de ventas del mes"
"¿Cuáles son mis productos más vendidos?"
"Analiza la competencia en taladros"
"Productos sin stock"
```

### 6.3 Marketing

```
"Crea una oferta del 20% para Black Friday"
"Genera contenido para Instagram sobre herramientas"
"Optimiza el SEO de todos mis productos"
"Crea una campaña publicitaria para el producto 4146"
```

### 6.4 Con Archivos

```
[Adjuntar imagen] "Crea un producto con esta imagen"
[Adjuntar Excel] "Importa estos productos"
```

---

## 🔧 SOLUCIÓN DE PROBLEMAS

### ❌ Error: "Could not connect to API"

**Causa:** URL incorrecta o backend caído

**Solución:**
1. Verifica URL en Configuración del plugin
2. Asegúrate de que termina en `/api` (sin barra final)
3. Verifica que el backend esté "Live" en Render
4. Prueba la URL directamente: `https://TU-URL.onrender.com/api/health`

---

### ❌ Error: "Database connection failed"

**Causa:** MongoDB no conectado

**Solución:**
1. Verifica `MONGO_URL` en variables de Render
2. Asegúrate de reemplazar `<password>` con tu contraseña real
3. Verifica que la IP 0.0.0.0/0 esté permitida en MongoDB Atlas
4. Revisa logs en Render para ver el error exacto

---

### ❌ Error: "AI generation failed"

**Causa:** API Keys incorrectas

**Solución:**
1. Verifica que las API keys estén configuradas en Render:
   - `OPENROUTER_API_KEY` (obligatorio)
   - `OPENAI_API_KEY` (obligatorio)
   - `PERPLEXITY_API_KEY` (obligatorio para búsquedas)
2. Revisa que tengas saldo en las cuentas
3. Verifica logs en Render: `Deploy` → `Logs`

---

### ❌ El chat no aparece en WordPress

**Causa:** Plugin no activado o usuario sin permisos

**Solución:**
1. Verifica que el plugin esté **activado**
2. Asegúrate de estar logueado como administrador
3. Limpia caché de WordPress/navegador
4. Verifica en consola del navegador (F12) si hay errores JS

---

### ❌ Render se duerme después de 15 minutos

**Causa:** Plan gratuito entra en "sleep" por inactividad

**Solución:**

**Opción 1 - Actualizar a plan de pago ($7/mes):**
1. Ve a tu servicio en Render
2. Click **"Upgrade"**
3. Selecciona **"Starter Plus"** ($7/mes)
4. El servicio NUNCA se dormirá

**Opción 2 - Ping automático (gratis pero con limitaciones):**
1. Usa un servicio como UptimeRobot: https://uptimerobot.com
2. Configura monitor HTTP(s) cada 5 minutos:
   ```
   https://TU-URL.onrender.com/api/health
   ```
3. Render detecta actividad y no se duerme

⚠️ **Recomendación:** Plan Starter Plus ($7/mes) para producción.

---

## 📊 MONITOREO Y MANTENIMIENTO

### Ver Logs del Backend

1. Render Dashboard: https://dashboard.render.com/web/srv-d3tot4muk2gs73dbhid0
2. Tab **"Logs"**
3. Verás todos los requests, errores y acciones del agente en tiempo real

### Métricas

1. Tab **"Metrics"**
2. Verás:
   - CPU usage
   - Memory usage
   - Request rate
   - Response time

### Reiniciar Servicio

Si algo falla:
1. Click **"Manual Deploy"** → **"Clear build cache & deploy"**
2. O usa el botón **"Restart Service"**

---

## 💰 COSTOS ESTIMADOS

### Render.com

| Plan | Precio | RAM | Sleep | Recomendación |
|------|--------|-----|-------|---------------|
| Free | $0 | 512MB | Después de 15 min | Solo testing |
| Starter | $7/mes | 512MB | Nunca | ✅ **Recomendado** |
| Standard | $25/mes | 2GB | Nunca | Producción alta |

### MongoDB Atlas

| Plan | Precio | Storage | Recomendación |
|------|--------|---------|---------------|
| Free (M0) | $0 | 512MB | ✅ **Suficiente para empezar** |
| M2 | $9/mes | 2GB | Producción media |
| M5 | $25/mes | 5GB | Producción alta |

### APIs de AI (Variables)

- OpenRouter: ~$0.003 por cada comando (Claude 3.5 Sonnet)
- OpenAI: ~$0.0001 por embedding (búsquedas en memoria)
- Perplexity: ~$0.005 por búsqueda en internet
- Fal AI: ~$0.05 por imagen generada

**Estimado:** $10-30/mes en APIs según uso.

---

## 🎯 RESUMEN FINAL

✅ **Backend en Render.com:** Funcionando 24/7  
✅ **MongoDB Atlas:** Base de datos persistente  
✅ **Plugin WordPress:** Instalado y conectado  
✅ **Chat Widget:** Disponible en toda la web  
✅ **18 Herramientas AI:** Listas para usar  
✅ **Memoria persistente:** RAG y búsqueda semántica  

**INDEPENDIENTE DE EMERGENT ✅**

---

## 📞 SOPORTE

Si tienes problemas:

1. **Revisa logs en Render:** https://dashboard.render.com/web/srv-d3tot4muk2gs73dbhid0/logs
2. **Verifica health check:** `https://TU-URL.onrender.com/api/health`
3. **Revisa consola de WordPress:** Panel Admin → Herramientas → Salud del sitio
4. **Revisa consola del navegador:** F12 → Console (errores JS)

---

## 🚀 PRÓXIMOS PASOS SUGERIDOS

1. **Actualizar a plan de pago en Render** ($7/mes) para evitar sleep
2. **Configurar dominio personalizado:** api.herramientasyaccesorios.store
3. **Activar HTTPS** (automático en Render)
4. **Configurar backups automáticos** en MongoDB Atlas
5. **Añadir más herramientas AI** según necesidades
6. **Integrar con más canales:** WhatsApp, Instagram, Facebook Messenger

---

**🎉 ¡Felicidades! Cerebro AI está funcionando 24/7 de forma independiente.**

Tu asistente AI está listo para gestionar tu tienda WooCommerce completamente en autopiloto.
