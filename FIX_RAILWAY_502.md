# 🔧 Solución Error 502 en Railway

## 🚨 Problema Detectado

Tu backend en Railway está dando **Error 502** - "Application failed to respond"

URL: `https://ai-agent-backend-production-9d42.up.railway.app`

---

## 🔍 PASO 1: Ver los Logs en Railway (MUY IMPORTANTE)

Los logs te dirán exactamente qué está fallando.

### Cómo ver los logs:

1. Ve a: https://railway.app/dashboard
2. Click en tu proyecto
3. Click en el servicio del backend
4. Tab **"Deployments"**
5. Click en el deployment activo (el que tiene el ícono verde o rojo)
6. **VER LOS LOGS** (scroll hacia abajo)

### Busca estos errores comunes:

```
❌ "ModuleNotFoundError: No module named 'X'"
   → Falta instalar una librería

❌ "Connection refused" o "MongoDB error"
   → Problema con MongoDB Atlas

❌ "ImportError"
   → Problema con las dependencias

❌ "Address already in use"
   → Problema con el puerto

❌ "KeyError: 'MONGO_URL'"
   → Falta variable de entorno
```

**📋 COPIA EL ERROR QUE VES EN LOS LOGS** y compártelo para ayudarte mejor.

---

## ✅ PASO 2: Verificar Configuración en Railway

### A) Root Directory

1. En tu servicio → **Settings**
2. Busca **"Root Directory"**
3. **DEBE SER:**
   ```
   backend
   ```
   (sin la barra `/` al inicio)

   Si dice `/backend`, **cámbialo a `backend`**

### B) Variables de Entorno

1. Tab **"Variables"**
2. **Verifica que TODAS estas variables estén configuradas:**

```env
✅ MONGO_URL (debe empezar con mongodb+srv://)
✅ DB_NAME
✅ SECRET_KEY
✅ OPENAI_API_KEY
✅ PERPLEXITY_API_KEY
✅ PORT=$PORT
✅ PYTHONUNBUFFERED=1
✅ CORS_ORIGINS=*
```

**Si falta alguna, agrégala.**

### C) Build Command

1. En **Settings** → busca **"Build Command"**
2. Debe estar **vacío** o tener:
   ```
   pip install -r requirements_standalone.txt
   ```

### D) Start Command

1. En **Settings** → busca **"Start Command"**
2. Debe estar **vacío** o tener:
   ```
   uvicorn server:app --host 0.0.0.0 --port $PORT
   ```

---

## 🔧 PASO 3: Soluciones Comunes

### Problema 1: MongoDB no conecta

**Síntoma:** Logs muestran "Connection refused" o "Authentication failed"

**Solución:**

1. Ve a MongoDB Atlas: https://cloud.mongodb.com
2. **Network Access** → Verifica que `0.0.0.0/0` esté permitida
3. **Database Access** → Verifica que el usuario tenga permisos
4. **Verifica MONGO_URL:**
   ```
   mongodb+srv://USUARIO:PASSWORD@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
   ```
   - Asegúrate que `<password>` esté reemplazado con tu contraseña real
   - Sin espacios
   - Sin `<` ni `>`

### Problema 2: Módulos no encontrados

**Síntoma:** Logs muestran "ModuleNotFoundError"

**Solución:**

1. Verifica que `Root Directory` sea `backend` (sin `/`)
2. Verifica que `requirements_standalone.txt` esté en la carpeta `backend/`
3. En Railway, haz un **Redeploy:**
   - Click en **"Deployments"**
   - Arriba a la derecha: **"Deploy"** o **"Redeploy"**

### Problema 3: Puerto incorrecto

**Síntoma:** Logs muestran "Address already in use" o "Failed to bind"

**Solución:**

1. En Variables, verifica que `PORT=$PORT` esté configurado
2. En Start Command, asegúrate que diga `--port $PORT` (no `--port 8001`)

### Problema 4: Variables de entorno faltantes

**Síntoma:** Logs muestran "KeyError" o "Environment variable not found"

**Solución:**

Agrega TODAS estas variables en Railway → Variables:

```env
MONGO_URL=mongodb+srv://usuario:password@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
DB_NAME=ai_agent_db
SECRET_KEY=09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7
CORS_ORIGINS=*
OPENAI_API_KEY=sk-proj-tu-key-de-openai
PERPLEXITY_API_KEY=pplx-tu-key-de-perplexity
STRIPE_API_KEY=sk_test_tu-stripe-key
STRIPE_PUBLISHABLE_KEY=pk_test_tu-stripe-key
TELEGRAM_BOT_TOKEN=tu-telegram-token
TELEGRAM_CHAT_ID=tu-chat-id
WORDPRESS_URL=https://tu-sitio-wordpress.com
WC_CONSUMER_KEY=ck_tu-woocommerce-key
WC_CONSUMER_SECRET=cs_tu-woocommerce-secret
FAL_API_KEY=tu-fal-key
PORT=$PORT
PYTHONUNBUFFERED=1
```

---

## 🔄 PASO 4: Forzar Redeploy

Después de hacer cambios:

1. En Railway → Tu servicio
2. Tab **"Deployments"**
3. Click en **"Deploy"** (arriba a la derecha)
4. O haz push a GitHub y Railway auto-deploye

Espera 3-5 minutos a que termine el build.

---

## ✅ PASO 5: Verificar que Funciona

Una vez que el deployment esté **"Success"** (verde):

### Test 1: Health Check
```
https://ai-agent-backend-production-9d42.up.railway.app/api/health
```

**Debe responder:**
```json
{
  "status": "healthy",
  "database": "connected"
}
```

### Test 2: Agent Status
```
https://ai-agent-backend-production-9d42.up.railway.app/api/agent/status
```

**Debe responder:**
```json
{
  "success": true,
  "agente_activo": true
}
```

---

## 🔌 PASO 6: Configurar WordPress

Una vez que el backend funcione:

1. **WordPress Admin → AI Chat Settings** (o tu plugin)
2. **Backend URL:**
   ```
   https://ai-agent-backend-production-9d42.up.railway.app
   ```
   ⚠️ **IMPORTANTE:** SIN `/api` al final

3. **Guardar Configuración**
4. **Probar Conexión**

---

## 📋 Checklist de Verificación

Marca cada item:

- [ ] Root Directory: `backend` (sin `/`)
- [ ] Variable `PORT=$PORT` configurada
- [ ] Variable `MONGO_URL` configurada correctamente
- [ ] Variable `DB_NAME` configurada
- [ ] Variable `SECRET_KEY` configurada
- [ ] Variable `OPENAI_API_KEY` configurada
- [ ] Variable `CORS_ORIGINS=*` configurada
- [ ] MongoDB Atlas permite IP `0.0.0.0/0`
- [ ] Logs no muestran errores
- [ ] Deployment status es "Success" (verde)
- [ ] `/api/health` responde correctamente
- [ ] WordPress configurado con URL correcta (sin `/api`)

---

## 🆘 Si Sigue Sin Funcionar

**Por favor comparte:**

1. **Logs completos de Railway** (copia y pega los últimos 50 líneas)
2. **Variables de entorno** que tienes configuradas (sin mostrar las keys completas)
3. **Configuración de Root Directory** (screenshot o texto)
4. **Error específico** que ves en los logs

Con esta información podré ayudarte a solucionar el problema específico.

---

## 💡 Tip: Deployment Limpio

Si después de todo sigue fallando, intenta un deployment limpio:

1. **Elimina el servicio actual en Railway**
2. **Crea uno nuevo:**
   - Deploy from GitHub repo
   - Configura Root Directory: `backend`
   - Agrega TODAS las variables de entorno
   - Deploy

A veces un deployment limpio soluciona problemas de caché o configuración corrupta.

---

## 📞 Próximo Paso

**Por favor:**
1. Ve a los logs en Railway
2. Copia el error que ves
3. Compártelo aquí

Con el error específico podré darte la solución exacta. 🎯
