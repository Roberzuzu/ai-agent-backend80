# 🚀 DEPLOYMENT FINAL - Backend Listo para Railway

## ✅ TODO CONFIGURADO Y LISTO

✅ Backend completo con todas las API keys  
✅ MongoDB Atlas configurado correctamente  
✅ Connection string: `mongodb+srv://bricospeed0_db_user:7uCqmOCzZsKBT3Uk@cluster0.5uxiix8.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0`  
✅ Archivos optimizados para Railway  

---

## 📦 ARCHIVO LISTO PARA DEPLOYAR

**Ubicación:** `/app/railway-backend-ready.zip` (145 KB)

Este archivo contiene:
- Backend completo
- `.env` con TODAS tus configuraciones
- `railway.json` - Configuración de Railway
- `Procfile` - Comando de inicio
- `runtime.txt` - Python 3.11

---

## 🚀 OPCIÓN 1: Deploy con Railway CLI (5 minutos)

### Paso 1: Instalar Railway CLI

**En tu computadora (Mac/Linux):**
```bash
curl -fsSL https://railway.app/install.sh | sh
```

**Windows (PowerShell como Admin):**
```powershell
iwr https://railway.app/install.ps1 | iex
```

### Paso 2: Login

```bash
railway login
```

Se abrirá el navegador para autenticarte.

### Paso 3: Descargar y Preparar

```bash
# Crear carpeta
mkdir ~/ai-backend-railway
cd ~/ai-backend-railway

# Descargar desde tu servidor Hostinger
scp -P 65002 u833032076@178.16.128.200:~/ai-agent-backend/* .
```

Password: `Amparo14.14.14$`

### Paso 4: Deploy

```bash
cd ~/ai-backend-railway

# Iniciar proyecto
railway init
# Nombre: ai-agent-backend

# Deploy
railway up
```

¡Eso es todo! Railway desplegará automáticamente.

### Paso 5: Configurar Variables de Entorno

**Desde el Dashboard Web (más fácil):**

1. Ir a: https://railway.app/dashboard
2. Click en tu proyecto `ai-agent-backend`
3. Click en el servicio
4. Tab **"Variables"**
5. Click **"Raw Editor"**
6. **Copiar y pegar esto:**

```env
MONGO_URL=mongodb+srv://bricospeed0_db_user:7uCqmOCzZsKBT3Uk@cluster0.5uxiix8.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0
DB_NAME=ai_agent_db
SECRET_KEY=09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7
CORS_ORIGINS=*
OPENAI_API_KEY=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
PERPLEXITY_API_KEY=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
EMERGENT_LLM_KEY=sk-emergent-d235664E2F5205d9e1
STRIPE_API_KEY=sk_test_51RLguuEIV37qlnK9Fm2mejxSRsSVtfLWRjDbLwTwuZ6vL2XNkjQ0FPWQMhq6LNqbOQ5qsJbhuGzA2tvrCjHf1mmT00AXLet9SG
STRIPE_PUBLISHABLE_KEY=pk_test_51RLguuEIV37qlnK9dfwvGn6IN08Fv1tSKRXtrVv1bwEdiLNU4yQ1KzVOn1Jl0QgyAe96l4S6npdTFE9Bni9jDOI500i9CXuLfQ
TELEGRAM_BOT_TOKEN=7708509018:AAErAOblRAlC587j1QB4k19PAfDgoiZ3kWk
TELEGRAM_CHAT_ID=7202793910
WORDPRESS_URL=https://herramientasyaccesorios.store
WORDPRESS_USER=Agente web
WORDPRESS_PASSWORD=RWWLW1eVi8whOS5OsUosb5AU
WC_CONSUMER_KEY=ck_4f50637d85ec404fff441fceb7b113b5050431ea
WC_CONSUMER_SECRET=cs_e59ef18ea20d80ffdf835803ad2fdd834a4ba19f
FAL_API_KEY=railway-port-config:228b46f927a226c270ece128bfeb95db
GOOGLE_ANALYTICS_MEASUREMENT_ID=G-EMQDLMQ0S3
SERP_API_KEY=fa16ee7d9d905d20ed8d2ecbde2c44af34a95c018a5714b7b1cc37db63d1c270
APIFY_API_KEY=FzCveZoIKVje1CSxA
ENVIRONMENT=production
LOG_LEVEL=INFO
PORT=$PORT
PYTHONUNBUFFERED=1
```

7. Click **"Update Variables"**

### Paso 6: Generar Dominio Público

```bash
railway domain
```

O desde el dashboard:
- Settings → Networking → Generate Domain

Te dará una URL como: `https://ai-agent-backend-production-xxxx.up.railway.app`

### Paso 7: Verificar

```bash
curl https://TU-URL/api/health
```

Debería responder:
```json
{"status":"healthy", ...}
```

---

## 🚀 OPCIÓN 2: Deploy desde GitHub

### Paso 1: Crear Repositorio GitHub

1. Ir a: https://github.com/new
2. Nombre: `ai-agent-backend`
3. **Private** ✅
4. Create repository

### Paso 2: Subir Código

```bash
cd ~/ai-backend-railway

git init
git add .
git commit -m "Backend AI Agent - Ready for production"
git branch -M main
git remote add origin https://github.com/TU-USUARIO/ai-agent-backend.git
git push -u origin main
```

### Paso 3: Deploy en Railway

1. Ir a: https://railway.app/new
2. Click **"Deploy from GitHub repo"**
3. Conectar GitHub
4. Seleccionar `ai-agent-backend`
5. Railway detectará FastAPI automáticamente
6. Click **"Deploy"**

### Paso 4: Variables (igual que antes)

Copiar y pegar las variables en: Variables → Raw Editor

---

## 🔌 CONFIGURAR WORDPRESS

Una vez desplegado (2-5 minutos):

### 1. Obtener URL de Railway

En el dashboard verás tu URL: `https://ai-agent-backend-production-xxxx.up.railway.app`

### 2. Configurar Plugin WordPress

**WordPress Admin → AI Chat Admin → Settings**

```
Backend URL: https://TU-URL-DE-RAILWAY
```

Ejemplo completo:
```
Backend URL: https://ai-agent-backend-production-abcd.up.railway.app
```

✅ **Marcar:** Mostrar Widget  
✅ **Marcar:** Solo Administrador

### 3. Probar Conexión

Click en **"🔌 Probar Backend"**

Debería mostrar: **✅ Backend conectado correctamente!**

---

## 📊 VERIFICAR FUNCIONAMIENTO

### Ver Logs en Railway

**Desde CLI:**
```bash
railway logs
```

**Desde Dashboard:**
Click en tu servicio → Tab "Deployments" → Click en el deployment actual → Ver logs

### Probar Endpoints

```bash
# Health check
curl https://TU-URL/api/health

# Status del agente AI
curl https://TU-URL/api/agent/status

# WordPress status
curl https://TU-URL/api/wordpress/status
```

---

## 💰 COSTOS

### Railway
- **$5 USD gratis** al mes para nuevos usuarios
- Después: ~$5-10 USD/mes (pay-as-you-go)
- **Sin tarjeta de crédito para empezar**

### MongoDB Atlas
- **Gratis permanente** (M0 - 512 MB)

### APIs (según uso)
- OpenAI: ~$5-10 USD/mes
- Perplexity: ~$5-10 USD/mes
- Otros: Gratis o muy bajo costo

**Total estimado: $15-30 USD/mes**

---

## ❓ TROUBLESHOOTING

### "Module not found" en Railway

Ver logs:
```bash
railway logs
```

Si falta algún módulo, agregarlo a `requirements.txt`

### Puerto incorrecto

Railway asigna `$PORT` automáticamente. Verificar que el comando de inicio use:
```bash
uvicorn server:app --host 0.0.0.0 --port $PORT
```

### MongoDB no conecta

Verificar que:
1. La IP `0.0.0.0/0` esté permitida en MongoDB Atlas Network Access
2. El connection string en las variables sea correcto
3. El usuario tenga permisos de lectura/escritura

### Ver logs en tiempo real

```bash
railway logs --follow
```

---

## 📝 RESUMEN EJECUTIVO

**LO QUE ESTÁ LISTO:**
✅ Backend completo con 22 herramientas AI  
✅ Todas las API keys configuradas  
✅ MongoDB Atlas funcionando  
✅ Archivos optimizados para Railway  

**LO QUE DEBES HACER:**
1. Instalar Railway CLI (1 min)
2. Login con `railway login` (30 seg)
3. Descargar backend desde servidor (1 min)
4. Deploy con `railway init` y `railway up` (2 min)
5. Copiar variables de entorno en dashboard (1 min)
6. Generar dominio público (30 seg)
7. Configurar URL en WordPress (30 seg)

**TIEMPO TOTAL: ~10 minutos**

---

## 🆘 SI NECESITAS AYUDA

1. Ver logs: `railway logs`
2. Documentación Railway: https://docs.railway.app
3. Support Railway: https://railway.app/discord

---

## 🎯 SIGUIENTE PASO

**EJECUTA ESTOS COMANDOS:**

```bash
# Instalar Railway
curl -fsSL https://railway.app/install.sh | sh

# Login
railway login

# Descargar backend
mkdir ~/ai-backend-railway
cd ~/ai-backend-railway
scp -P 65002 -r u833032076@178.16.128.200:~/ai-agent-backend/* .

# Deploy
railway init
railway up
```

**¡En 10 minutos tu backend estará funcionando 24/7!** 🚀
