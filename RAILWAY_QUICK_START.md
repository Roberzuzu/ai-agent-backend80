# 🚀 Railway Quick Start - Configuración en 5 Minutos

## ✅ Cambios Realizados para Railway

### 1. Archivos Creados
- ✅ `railway.json` - Configuración automática de Railway
- ✅ `.railwayignore` - Optimización del deployment
- ✅ `RAILWAY_DEPLOYMENT_GUIDE.md` - Guía completa paso a paso

### 2. Archivos Actualizados
- ✅ `Procfile` - Ahora ejecuta desde el directorio `backend/`

---

## 🎯 Configuración en Railway (Paso a Paso)

### PASO 1: Deploy Inicial

1. Ve a: https://railway.app/new
2. Click **"Deploy from GitHub repo"**
3. Selecciona tu repositorio
4. Click **"Deploy"**

### PASO 2: Configurar Root Directory ⚠️ IMPORTANTE

1. Click en tu servicio
2. Tab **"Settings"**
3. Scroll a **"Service Settings"**
4. **Root Directory:**
   ```
   backend
   ```
   ⚠️ **SIN la barra inicial `/`**
   
   ```
   ❌ INCORRECTO: /backend
   ✅ CORRECTO:   backend
   ```

5. Click **"Update"** o presiona Enter

### PASO 3: Configurar Target Port

1. En **"Settings"** → scroll a **"Networking"**
2. **Target Port:**
   ```
   $PORT
   ```
   O déjalo **vacío** (Railway lo asignará automáticamente)

   ⚠️ NO uses `8000` o `8001` - Railway usa puertos dinámicos

### PASO 4: Variables de Entorno

1. Tab **"Variables"**
2. Click **"Raw Editor"**
3. Pega esto (ajusta con tus valores):

```env
MONGO_URL=mongodb+srv://usuario:password@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
DB_NAME=ai_agent_db
SECRET_KEY=tu-clave-secreta-minimo-32-caracteres
CORS_ORIGINS=*
OPENAI_API_KEY=sk-proj-tu-key
PERPLEXITY_API_KEY=pplx-tu-key
STRIPE_API_KEY=sk_test_tu-key
STRIPE_PUBLISHABLE_KEY=pk_test_tu-key
TELEGRAM_BOT_TOKEN=tu-token
TELEGRAM_CHAT_ID=tu-chat-id
WORDPRESS_URL=https://tu-sitio.com
WC_CONSUMER_KEY=ck_tu-key
WC_CONSUMER_SECRET=cs_tu-secret
FAL_API_KEY=tu-key
PORT=$PORT
PYTHONUNBUFFERED=1
```

4. Click **"Update Variables"**

### PASO 5: Generar Dominio

1. En **"Settings"** → **"Networking"**
2. Click **"Generate Domain"**
3. **Copia la URL generada**

### PASO 6: Verificar

Abre en tu navegador:
```
https://tu-url-railway.up.railway.app/api/health
```

✅ Deberías ver:
```json
{
  "status": "healthy",
  "database": "connected"
}
```

---

## 🔌 Configurar en WordPress

1. **WordPress Admin → AI Chat Settings**
2. **Backend URL:**
   ```
   https://tu-url-railway.up.railway.app
   ```
   ⚠️ **SIN** `/api` al final

3. Click **"Guardar"** y **"Probar Conexión"**

✅ Deberías ver: **"Backend conectado correctamente"**

---

## 📝 Resumen de Configuraciones Clave

| Configuración | Valor | Ubicación en Railway |
|---------------|-------|---------------------|
| Root Directory | `backend` (sin `/`) | Settings → Service Settings |
| Target Port | `$PORT` o vacío | Settings → Networking |
| Start Command | Auto-detectado del Procfile | - |
| Variables | Ver lista arriba | Variables tab |

---

## 🐛 Si algo falla

### Error: "Module not found"
✅ **Solución:** Verifica que Root Directory sea `backend` (sin `/`)

### Error: "Database connection failed"
✅ **Solución:**
1. Verifica MongoDB Atlas permite IP `0.0.0.0/0`
2. Verifica que `MONGO_URL` no tenga `<password>` literal

### Error: "CORS policy"
✅ **Solución:** Agrega variable `CORS_ORIGINS=*`

### Ver Logs
1. Railway Dashboard → tu servicio
2. Tab **"Deployments"**
3. Click en deployment activo
4. Ver logs en tiempo real

---

## 💡 Tips

1. **Railway auto-deploya** cada vez que haces push a GitHub
2. **Logs en tiempo real** disponibles en el dashboard
3. **Métricas gratuitas** (CPU, RAM, Network) en la pestaña "Metrics"
4. **$5 USD gratis/mes** en el plan Starter
5. **Dominio personalizado** disponible en Settings → Networking

---

## 🎉 ¡Todo Listo!

Con estos cambios, tu backend funcionará **perfectamente en Railway** y tu plugin de WordPress podrá conectarse sin problemas.

**Tiempo total:** 5-10 minutos

**Próximos pasos:**
- Deploy en Railway siguiendo estos pasos
- Conectar WordPress
- ¡Disfrutar de tu aplicación autónoma! 🚀

---

## 📚 Documentación Adicional

- **Guía Completa:** Ver `RAILWAY_DEPLOYMENT_GUIDE.md`
- **Railway Docs:** https://docs.railway.app
- **Support:** https://help.railway.app
