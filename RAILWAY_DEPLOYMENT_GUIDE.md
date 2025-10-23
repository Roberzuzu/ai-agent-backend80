# 🚀 Guía Completa de Deployment en Railway

## 📋 Requisitos Previos

1. Cuenta en Railway: https://railway.app
2. Cuenta en GitHub (el código ya debe estar en tu repositorio)
3. Cuenta en MongoDB Atlas (gratis): https://www.mongodb.com/cloud/atlas

---

## 🎯 PASO 1: Preparar MongoDB Atlas (5 minutos)

### 1.1 Crear Cluster (si no lo tienes)

1. Ve a: https://cloud.mongodb.com
2. Click **"Create"** → **"Shared"** (gratis)
3. Selecciona región más cercana
4. Click **"Create Cluster"**

### 1.2 Configurar Acceso a la Red

1. En el menú lateral: **Network Access**
2. Click **"Add IP Address"**
3. Click **"Allow Access from Anywhere"** (0.0.0.0/0)
4. Click **"Confirm"**

### 1.3 Crear Usuario de Base de Datos

1. En el menú lateral: **Database Access**
2. Click **"Add New Database User"**
3. Método: **Password**
4. Username: `backend_user`
5. Password: **Genera una segura** (guárdala)
6. Rol: **Atlas Admin** o **Read and write to any database**
7. Click **"Add User"**

### 1.4 Obtener Connection String

1. En **Database** → Click **"Connect"**
2. **"Connect your application"**
3. Copia la URL que se ve así:
   ```
   mongodb+srv://backend_user:<password>@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
   ```
4. **IMPORTANTE:** Reemplaza `<password>` con tu contraseña real

---

## 🚂 PASO 2: Deploy del Backend en Railway (10 minutos)

### 2.1 Crear Nuevo Proyecto

1. Ve a: https://railway.app/new
2. Click **"Deploy from GitHub repo"**
3. Si es tu primera vez:
   - Click **"Configure GitHub App"**
   - Selecciona tu repositorio
   - Click **"Install & Authorize"**
4. Selecciona tu repositorio (ejemplo: `Roberzuzu/ai-agent-backend`)

### 2.2 Configurar el Servicio del Backend

Una vez creado el proyecto:

1. Click en el servicio que se creó
2. Ve a la pestaña **"Settings"**

#### A) Root Directory (MUY IMPORTANTE)

1. Scroll hasta **"Service Settings"**
2. Busca **"Root Directory"**
3. **Cambia de `/backend` a `backend`** (sin barra inicial /)
4. Click **"Update"** o presiona Enter

```
❌ INCORRECTO: /backend
✅ CORRECTO:   backend
```

#### B) Build Command (si es necesario)

Si Railway no detecta automáticamente:

1. En **"Build"** → **"Build Command"**
2. Agrega:
   ```
   pip install -r requirements_standalone.txt
   ```

#### C) Start Command

1. En **"Deploy"** → **"Start Command"**
2. Agrega:
   ```
   uvicorn server:app --host 0.0.0.0 --port $PORT
   ```

#### D) Variables de Entorno

1. Ve a la pestaña **"Variables"**
2. Click **"New Variable"** o **"Raw Editor"**
3. **Copia y pega estas variables** (ajusta con tus valores):

```env
# MongoDB
MONGO_URL=mongodb+srv://tu-usuario:tu-password@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
DB_NAME=ai_agent_db

# Security
SECRET_KEY=genera-una-clave-secreta-aqui-minimo-32-caracteres

# CORS (permite todas las conexiones)
CORS_ORIGINS=*

# OpenAI
OPENAI_API_KEY=sk-proj-tu-api-key-de-openai

# Perplexity
PERPLEXITY_API_KEY=pplx-tu-api-key-de-perplexity

# Stripe (si usas pagos)
STRIPE_API_KEY=sk_test_tu-stripe-secret-key
STRIPE_PUBLISHABLE_KEY=pk_test_tu-stripe-publishable-key

# Telegram Bot (si lo usas)
TELEGRAM_BOT_TOKEN=tu-telegram-bot-token
TELEGRAM_CHAT_ID=tu-telegram-chat-id

# WordPress/WooCommerce
WORDPRESS_URL=https://tu-sitio-wordpress.com
WC_CONSUMER_KEY=ck_tu-consumer-key
WC_CONSUMER_SECRET=cs_tu-consumer-secret

# FAL AI (para generación de imágenes)
FAL_API_KEY=tu-fal-api-key

# Railway (automático)
PORT=$PORT
PYTHONUNBUFFERED=1
```

4. Click **"Add"** o **"Save"**

### 2.3 Generar Dominio Público

1. En **"Settings"** → scroll a **"Networking"**
2. Click **"Generate Domain"**
3. Railway te dará una URL como:
   ```
   https://ai-agent-backend-production-xxxx.up.railway.app
   ```
4. **¡COPIA ESTA URL!** La necesitarás para WordPress y el frontend

### 2.4 Verificar Deployment

1. Ve a la pestaña **"Deployments"**
2. Espera a que el build termine (3-5 minutos)
3. El estado debe ser: **"Success"** con un ✅

#### Probar el Backend

Abre en tu navegador:
```
https://tu-url-de-railway.up.railway.app/api/health
```

**Deberías ver:**
```json
{
  "status": "healthy",
  "database": "connected",
  "timestamp": "2025-01-22T..."
}
```

✅ **Si ves esto, tu backend está funcionando!**

---

## 🎨 PASO 3: Deploy del Frontend en Railway (10 minutos)

### 3.1 Crear Nuevo Servicio

1. En el mismo proyecto de Railway, click **"+ New"**
2. **"Empty Service"**
3. Dale un nombre: `frontend`

### 3.2 Conectar el Repositorio

1. En **"Settings"** del servicio frontend
2. **"Source"** → **"Connect Repo"**
3. Selecciona tu repositorio
4. **Root Directory:** `frontend` (sin barra inicial)

### 3.3 Configurar Build

#### A) Build Command

```bash
npm install && npm run build
```

#### B) Start Command

```bash
npx serve -s build -l $PORT
```

#### C) Variables de Entorno

En la pestaña **"Variables"**:

```env
# Backend URL (usa la URL del backend de Railway)
REACT_APP_BACKEND_URL=https://tu-backend-railway.up.railway.app/api

# Node
NODE_ENV=production
PORT=$PORT
```

### 3.4 Instalar `serve` (si es necesario)

Asegúrate que tu `package.json` tenga:

```json
{
  "dependencies": {
    "serve": "^14.2.0"
  }
}
```

Si no está, agrégalo manualmente en el repositorio.

### 3.5 Generar Dominio

1. En **"Settings"** → **"Networking"**
2. **"Generate Domain"**
3. Copia la URL del frontend

---

## 🔌 PASO 4: Configurar WordPress (5 minutos)

### 4.1 Actualizar URL del Backend

1. Ve a tu **WordPress Admin**
2. **AI Chat Admin → Settings** (o donde esté tu plugin)
3. **Backend URL:** Pega la URL del backend de Railway:
   ```
   https://tu-backend-railway.up.railway.app
   ```
   **SIN** `/api` al final
4. **Guardar Configuración**

### 4.2 Probar Conexión

1. Click en **"Probar Conexión"** o **"Test Backend"**
2. Deberías ver: ✅ **Backend conectado correctamente**

### 4.3 Configurar Webhooks (si usas WooCommerce)

1. **WooCommerce → Settings → Advanced → Webhooks**
2. **Add webhook:**
   - **Name:** Product Created
   - **Topic:** Product created
   - **Delivery URL:**
     ```
     https://tu-backend-railway.up.railway.app/api/webhooks/woocommerce/product-created
     ```
   - **Secret:** (opcional)
   - **Status:** Active

3. Repetir para otros eventos:
   - Product updated: `/api/webhooks/woocommerce/product-updated`
   - Order created: `/api/webhooks/woocommerce/order-created`

---

## ✅ PASO 5: Verificación Final

### 5.1 Endpoints del Backend

Prueba estos URLs en tu navegador:

```
✅ https://tu-backend.up.railway.app/api/health
✅ https://tu-backend.up.railway.app/api/agent/status
✅ https://tu-backend.up.railway.app/api/wordpress/status
```

### 5.2 Frontend

```
✅ https://tu-frontend.up.railway.app
```

### 5.3 Desde WordPress

1. Ve a tu sitio WordPress
2. El plugin debe poder:
   - Ver productos
   - Crear órdenes
   - Usar el agente AI
   - Mostrar el chat

---

## 🐛 Troubleshooting

### Backend no inicia

**Ver logs:**
1. Railway → Tu servicio backend
2. Tab **"Deployments"**
3. Click en el deployment activo
4. Ver logs en tiempo real

**Errores comunes:**

❌ **Error: "Module not found"**
- Solución: Verifica que `requirements_standalone.txt` esté en `backend/`

❌ **Error: "Connection refused" (MongoDB)**
- Solución: Verifica que la IP `0.0.0.0/0` esté permitida en MongoDB Atlas
- Verifica que la contraseña en `MONGO_URL` sea correcta (sin `<` `>`)

❌ **Error: "Port already in use"**
- Solución: No pasa en Railway, pero verifica que uses `$PORT` no `8001`

### Frontend no conecta al Backend

❌ **Error: CORS**
- Solución: En variables del backend, asegúrate que `CORS_ORIGINS=*`

❌ **Error: "Failed to fetch"**
- Solución: Verifica que `REACT_APP_BACKEND_URL` tenga `/api` al final
- Verifica que el backend esté funcionando

### WordPress no conecta

❌ **Error: "Backend no responde"**
- Solución: Verifica que la URL en WordPress NO tenga `/api` al final
- Prueba la URL manualmente: `https://tu-backend.up.railway.app/api/health`

---

## 📊 Monitoreo

### Ver Logs en Tiempo Real

```bash
# Desde Railway Dashboard
1. Click en tu servicio
2. Tab "Deployments"
3. Click en deployment activo
4. Ver logs
```

### Ver Métricas

```bash
# Railway Dashboard
1. Click en tu servicio
2. Tab "Metrics"
3. Ver CPU, Memoria, Network
```

---

## 💰 Costos

### Railway
- **$5 USD gratis/mes** (starter plan)
- Después: ~$5-10 USD/mes dependiendo del uso

### MongoDB Atlas
- **Gratis permanente** (512 MB storage)
- Upgrade: ~$9 USD/mes (10GB)

### APIs Externas
- OpenAI: ~$5-20 USD/mes (según uso)
- Perplexity: Gratis hasta cierto límite
- Stripe: Solo comisiones por transacción (2.9% + $0.30)

**Total estimado: $10-30 USD/mes**

---

## 🔄 Actualizar el Código

Cuando hagas cambios en tu repositorio:

1. **Push a GitHub:**
   ```bash
   git add .
   git commit -m "Update"
   git push origin main
   ```

2. **Railway auto-deploya:**
   - Railway detecta el push
   - Hace build automáticamente
   - Deploy en 3-5 minutos

3. **Si necesitas redeploy manual:**
   - Railway Dashboard → Deployments
   - Click en "Deploy" (arriba a la derecha)

---

## 📝 Resumen de Configuración

### ✅ Checklist Final

- [ ] MongoDB Atlas configurado con IP 0.0.0.0/0
- [ ] Usuario de DB creado y connection string guardada
- [ ] Backend deployado en Railway
- [ ] Root Directory del backend: `backend` (sin `/`)
- [ ] Variables de entorno configuradas en backend
- [ ] Dominio generado para backend
- [ ] Endpoint `/api/health` funciona
- [ ] Frontend deployado en Railway (opcional)
- [ ] WordPress configurado con URL del backend
- [ ] Conexión entre WordPress y backend probada
- [ ] Webhooks de WooCommerce configurados (si aplica)

---

## 🆘 Soporte

### Railway
- Docs: https://docs.railway.app
- Discord: https://discord.gg/railway

### MongoDB
- Docs: https://docs.mongodb.com/atlas/
- Support: https://support.mongodb.com

---

## 🎉 ¡Listo!

Tu aplicación ahora está funcionando 24/7 de manera **totalmente autónoma**:

✅ Backend en Railway conectado a MongoDB Atlas
✅ Frontend en Railway (opcional)
✅ WordPress conectado al backend
✅ Sin dependencias de Emergent
✅ 100% bajo tu control

**Tiempo total de setup: 30-40 minutos**

**¡A disfrutar de tu aplicación autónoma!** 🚀
