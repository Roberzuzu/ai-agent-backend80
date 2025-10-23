# ✅ CÓDIGO EN GITHUB - DEPLOY EN 3 MINUTOS

## 🎉 ¡EL CÓDIGO YA ESTÁ EN GITHUB!

**Repositorio:** https://github.com/Roberzuzu/ai-agent-backend

---

## 🚀 PASO 1: DEPLOY EN RAILWAY (2 minutos)

1. **Ve a:** https://railway.app/new

2. **Click:** "Deploy from GitHub repo"

3. **Autoriza Railway** si no lo has hecho:
   - Click "Configure GitHub App"
   - Seleccionar "All repositories" o solo `ai-agent-backend`
   - Install & Authorize

4. **Selecciona:** `Roberzuzu/ai-agent-backend`

5. **Click "Deploy"**

Railway detectará FastAPI automáticamente y empezará el build (3-5 minutos).

---

## 🚀 PASO 2: CONFIGURAR VARIABLES (1 minuto)

Mientras se despliega:

1. En Railway, **click en tu proyecto**
2. **Click en el servicio** (aparece el nombre del repo)
3. Tab **"Variables"**
4. Click **"New Variable"** o **"Raw Editor"**
5. **Copia y pega TODO esto:**

```
MONGO_URL=mongodb+srv://bricospeed0_db_user:7uCqmOCzZsKBT3Uk@cluster0.5uxiix8.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0
DB_NAME=ai_agent_db
SECRET_KEY=09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7
CORS_ORIGINS=*
OPENAI_API_KEY=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
PERPLEXITY_API_KEY=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
STRIPE_API_KEY=sk_test_51RLguuEIV37qlnK9Fm2mejxSRsSVtfLWRjDbLwTwuZ6vL2XNkjQ0FPWQMhq6LNqbOQ5qsJbhuGzA2tvrCjHf1mmT00AXLet9SG
TELEGRAM_BOT_TOKEN=7708509018:AAErAOblRAlC587j1QB4k19PAfDgoiZ3kWk
TELEGRAM_CHAT_ID=7202793910
WORDPRESS_URL=https://herramientasyaccesorios.store
WC_CONSUMER_KEY=ck_4f50637d85ec404fff441fceb7b113b5050431ea
WC_CONSUMER_SECRET=cs_e59ef18ea20d80ffdf835803ad2fdd834a4ba19f
FAL_API_KEY=railway-port-config:228b46f927a226c270ece128bfeb95db
PORT=$PORT
PYTHONUNBUFFERED=1
```

6. Click **"Add"** o **"Update Variables"**

El servicio se reiniciará automáticamente con las nuevas variables.

---

## 🌐 PASO 3: OBTENER URL (30 segundos)

1. En tu servicio en Railway
2. Tab **"Settings"**
3. Scroll a **"Networking"**
4. Click **"Generate Domain"**

Te dará una URL como:
```
https://ai-agent-backend-production-xxxx.up.railway.app
```

**¡COPIA ESTA URL!**

---

## ✅ PASO 4: VERIFICAR QUE FUNCIONA (30 segundos)

**Abre en tu navegador:**
```
https://TU-URL-DE-RAILWAY/api/health
```

**Deberías ver algo como:**
```json
{
  "status": "healthy",
  "timestamp": "2025-10-22T...",
  "checks": {
    "database": {"status": "healthy"},
    "stripe": {"status": "healthy"},
    "openai": {"status": "healthy"}
  }
}
```

**Si ves esto, ¡FUNCIONA!** ✅

---

## 🔌 PASO 5: CONFIGURAR WORDPRESS (30 segundos)

1. **WordPress Admin → AI Chat Admin → Settings**

2. **Backend URL:** Pega la URL de Railway
   ```
   https://ai-agent-backend-production-xxxx.up.railway.app
   ```

3. **Marcar:**
   - ✅ Mostrar Widget
   - ✅ Solo Administrador

4. **Click "Guardar Configuración"**

5. **Click "🔌 Probar Backend"**

**Resultado esperado:**
```
✅ Backend conectado correctamente!
```

---

## 🎊 ¡LISTO!

**Tu backend está funcionando 24/7 en Railway conectado a:**
- ✅ MongoDB Atlas
- ✅ WordPress/WooCommerce
- ✅ OpenAI + Perplexity
- ✅ Stripe, Telegram, FAL AI
- ✅ 22 herramientas AI activas

---

## 📊 VERIFICACIÓN COMPLETA

Prueba estos endpoints en tu navegador:

```
https://TU-URL/api/health
https://TU-URL/api/agent/status
https://TU-URL/api/wordpress/status
```

Todos deberían responder con `status: "healthy"` o `status: "ready"`

---

## ⏱️ TIEMPO TOTAL

1. Deploy Railway: 3-5 min (automático)
2. Variables: 1 min
3. Generar dominio: 30 seg
4. Verificar: 30 seg
5. WordPress: 30 seg

**TOTAL: 5-7 MINUTOS**

---

## 🆘 SI ALGO FALLA

### Railway no encuentra el repo
- Refresh la página
- Click "Configure GitHub App" y autoriza de nuevo

### Build falla
- Ve a "Deployments" → Click en el deployment → Ver logs
- Busca el error específico

### MongoDB no conecta
- Verifica en MongoDB Atlas:
  - Network Access → IP `0.0.0.0/0` permitida
  - Database Access → Usuario tiene permisos

### Ver logs en Railway
- Click en tu servicio
- Tab "Deployments"
- Click en el deployment activo
- Ver logs en tiempo real

---

## 💰 COSTOS

- **Railway:** $5 USD gratis/mes
- **MongoDB Atlas:** Gratis permanente
- **APIs:** ~$15-20 USD/mes según uso

**Total primer mes: $0 USD (todo gratis)**
**Total después: ~$20-30 USD/mes**

---

## 🎯 PRÓXIMO PASO

**¡EMPIEZA AHORA!**

1. Ve a: https://railway.app/new
2. Deploy from GitHub repo
3. Selecciona: Roberzuzu/ai-agent-backend
4. Deploy!

**¡En 5 minutos tendrás todo funcionando!** 🚀
