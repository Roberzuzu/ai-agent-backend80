# 🚀 DEPLOYMENT DEFINITIVO - 100% DESDE NAVEGADOR

## ✅ SIN COMANDOS, SIN GIT, SIN COMPLICACIONES

He preparado TODO para que lo hagas desde el navegador en 5 minutos.

---

## 📋 OPCIÓN 1: RENDER (Más Fácil)

### Paso 1: Crear Cuenta en Render

1. Ve a: **https://render.com**
2. Click **"Get Started"**
3. Sign up con **GitHub** o **Email**
4. Verificar email y login

---

### Paso 2: Crear Web Service

1. Click **"New +"** (arriba derecha)
2. Click **"Web Service"**
3. En "Public Git repository" **DEJA EN BLANCO**
4. Scroll abajo y click **"Next"**

**O mejor:**

1. Click **"New +"**
2. **"Blueprint"**
3. **"Import from existing repository"**

**ESPERA** - esto también necesita Git...

---

## 🎯 MÉTODO QUE SÍ FUNCIONA: Railway con Interfaz Web

### Paso 1: Subir Código a GitHub (Manual)

Ya que el token no funciona, vamos a hacerlo manual:

1. **Ve a:** https://github.com/Roberzuzu/ai-agent-backend
2. **Click "Add file"** → **"Upload files"**
3. **En tu PC, descarga los archivos:**
   - Usa WinSCP (instalado antes)
   - Servidor: `178.16.128.200:65002`
   - Usuario: `u833032076`
   - Password: `Amparo14.14.14$`
   - Descarga carpeta `/home/u833032076/ai-agent-backend` a `C:\ai-backend`

4. **Vuelve a GitHub**
5. **Arrastra TODOS los archivos** de `C:\ai-backend` a la ventana de GitHub
6. **Commit message:** "Backend completo"
7. **Click "Commit changes"**

---

### Paso 2: Deploy en Railway

1. **Ve a:** https://railway.app/new
2. **Click "Deploy from GitHub repo"**
3. **Autoriza Railway** a acceder a GitHub
4. **Selecciona:** `Roberzuzu/ai-agent-backend`
5. **Click "Deploy"**

Railway construirá el proyecto automáticamente (3-5 min).

---

### Paso 3: Configurar Variables

1. En Railway Dashboard
2. Click en tu proyecto
3. Click en el servicio
4. Tab **"Variables"**
5. Click **"Raw Editor"**
6. **Pega ESTO:**

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

7. Click **"Add"**

---

### Paso 4: Generar Dominio

1. Settings → Networking
2. **"Generate Domain"**
3. Copiar URL: `https://ai-agent-backend-production-xxxx.up.railway.app`

---

### Paso 5: Configurar WordPress

1. **WordPress Admin → AI Chat Admin → Settings**
2. **Backend URL:** Pegar URL de Railway
3. ✅ Mostrar Widget
4. ✅ Solo Administrador
5. **Guardar**
6. **🔌 Probar Backend** → ✅ Conectado!

---

## 📝 RESUMEN VISUAL

```
1. WinSCP → Descargar archivos del servidor
                ↓
2. GitHub → Upload files (arrastrar archivos)
                ↓
3. Railway → Deploy from GitHub
                ↓
4. Railway → Configurar variables
                ↓
5. Railway → Generate Domain
                ↓
6. WordPress → Pegar URL y probar
                ↓
            ✅ FUNCIONA!
```

---

## ⏱️ TIEMPO ESTIMADO

- Paso 1 (WinSCP descarga): 2 min
- Paso 2 (Subir a GitHub): 2 min
- Paso 3 (Railway deploy): 5 min (automático)
- Paso 4 (Variables): 1 min
- Paso 5 (Dominio): 30 seg
- Paso 6 (WordPress): 30 seg

**TOTAL: ~10 minutos**

---

## 🆘 SI TIENES PROBLEMAS

**GitHub no acepta tantos archivos:**
- Sube en 2 partes (primero los .py, luego las carpetas)

**Railway no detecta FastAPI:**
- Agrega archivo `Procfile` con:
  ```
  web: uvicorn server:app --host 0.0.0.0 --port $PORT
  ```

**MongoDB no conecta:**
- Verifica en MongoDB Atlas → Network Access → IP `0.0.0.0/0` permitida

---

## ✅ ARCHIVOS PREPARADOS

En tu servidor Hostinger:
- `~/ai-agent-backend/` - Código completo
- `~/backend-render-deploy.tar.gz` - Backup comprimido

---

**¡EMPIEZA CON EL PASO 1!** 🚀
