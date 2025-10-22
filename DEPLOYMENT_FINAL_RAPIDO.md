# 🚀 DEPLOYMENT RÁPIDO - 3 PASOS (5 MINUTOS)

## ✅ TODO ESTÁ LISTO

El código está preparado y listo para subir a GitHub.

---

## 📋 PASO 1: SUBIR A GITHUB (2 minutos)

### Opción A: Desde tu computadora con ZIP

1. **Descargar ZIP del backend:**
   ```bash
   scp -P 65002 u833032076@178.16.128.200:~/ai-agent-backend.zip ~/
   ```
   Password: `Amparo14.14.14$`

2. **O usa el archivo:** `/app/backend-para-github.zip`

3. **Ve a tu repo:** https://github.com/Roberzuzu/ai-agent-backend

4. **Subir archivos:**
   - Click "Add file" → "Upload files"
   - Arrastra el contenido del ZIP (descomprímelo primero)
   - O click "choose your files"
   - Commit: "Backend AI Agent completo"
   - Click "Commit changes"

### Opción B: Desde terminal (más rápido)

```bash
# Descargar
mkdir ~/ai-backend && cd ~/ai-backend
scp -P 65002 -r u833032076@178.16.128.200:~/ai-agent-backend/* .

# Subir a GitHub
git init
git add .
git commit -m "Backend AI Agent"
git branch -M main
git remote add origin https://github.com/Roberzuzu/ai-agent-backend.git

# Autenticar y push
git push -u origin main
```

**Cuando pida credenciales:**
- Username: `Roberzuzu`
- Password: Tu token de GitHub

---

## 📋 PASO 2: DEPLOY EN RAILWAY (2 minutos)

1. **Ve a:** https://railway.app/new

2. **Click "Deploy from GitHub repo"**

3. **Autoriza Railway** si no lo has hecho:
   - Click "Configure GitHub App"
   - Seleccionar "All repositories" o solo `ai-agent-backend`
   - Install & Authorize

4. **Selecciona:** `Roberzuzu/ai-agent-backend`

5. **Click "Deploy"**

Railway empezará a construir (tarda 2-5 minutos).

---

## 📋 PASO 3: CONFIGURAR VARIABLES (1 minuto)

Mientras se despliega:

1. **En Railway Dashboard:**
   - Click en tu proyecto
   - Click en el servicio
   - Tab **"Variables"**
   - Click **"Raw Editor"**

2. **Pega TODAS estas variables:**

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
FAL_API_KEY=5b756394-7beb-4a8b-bda2-dd53dc9a374f:228b46f927a226c270ece128bfeb95db
PORT=$PORT
PYTHONUNBUFFERED=1
```

3. **Click "Add" o "Save"**

El servicio se reiniciará automáticamente.

---

## 🌐 OBTENER URL Y CONFIGURAR WORDPRESS

### 1. Generar Dominio en Railway

- En tu servicio → Tab **"Settings"**
- Sección **"Networking"**
- Click **"Generate Domain"**

URL ejemplo: `https://ai-agent-backend-production-abc123.up.railway.app`

### 2. Probar el Backend

Abre en navegador:
```
https://TU-URL/api/health
```

Debería mostrar:
```json
{"status":"healthy", ...}
```

### 3. Configurar en WordPress

1. **WordPress Admin → AI Chat Admin → Settings**

2. **Backend URL:**
   ```
   https://TU-URL-DE-RAILWAY
   ```

3. ✅ **Marcar:** Mostrar Widget

4. ✅ **Marcar:** Solo Administrador

5. **Click "Guardar Configuración"**

6. **Click "🔌 Probar Backend"**

**Resultado esperado:** ✅ Backend conectado correctamente!

---

## ✅ VERIFICACIÓN FINAL

```bash
# Health check
curl https://TU-URL/api/health

# Agent status
curl https://TU-URL/api/agent/status

# WordPress connection
curl https://TU-URL/api/wordpress/status
```

Todos deberían responder con `success: true`

---

## 💰 COSTOS

- **Railway:** $5 USD gratis/mes
- **MongoDB Atlas:** Gratis permanente
- **APIs:** ~$15-20 USD/mes

**Total: ~$20-25 USD/mes**

---

## 🎯 RESUMEN

1. ✅ Subir código a GitHub (2 min)
2. ✅ Deploy en Railway desde GitHub (2 min)
3. ✅ Configurar variables de entorno (1 min)
4. ✅ Generar dominio y configurar WordPress (1 min)

**TIEMPO TOTAL: 5-10 MINUTOS**

---

## 📁 ARCHIVOS DISPONIBLES

- `/app/backend-para-github.zip` - Backend listo para subir
- `~/ai-agent-backend/` en tu servidor - Backend completo con .env

---

## ❓ SI ALGO FALLA

### Railway no detecta FastAPI

Agregar archivo `Procfile` en la raíz:
```
web: uvicorn server:app --host 0.0.0.0 --port $PORT
```

### MongoDB no conecta

Verificar en MongoDB Atlas:
- Network Access → IP `0.0.0.0/0` permitida
- Database Access → Usuario tiene permisos

### Ver logs en Railway

Dashboard → Click en deployment → Ver logs en tiempo real

---

**¡TODO LISTO PARA DEPLOYAR EN 5 MINUTOS!** 🚀
