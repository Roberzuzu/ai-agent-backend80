# 🎯 Railway - 5 Pasos Simples

## Sigue EXACTAMENTE estos pasos:

---

## PASO 1: Abrir Railway

1. Ve a: **https://railway.app/dashboard**
2. Busca tu proyecto (el que tiene el backend)
3. **Click en el servicio del backend**

---

## PASO 2: Cambiar Builder a NIXPACKS

1. Click en **"Settings"** (arriba)
2. Busca la sección que dice **"Build"**
3. Verás algo que dice **"Builder"**
4. **Si dice "Docker"**, haz click y cámbialo a **"NIXPACKS"**
5. Si ya dice **"NIXPACKS"**, déjalo así

```
Builder: [NIXPACKS ▼]  ← Debe decir esto
```

---

## PASO 3: Verificar Root Directory

1. En la misma página de **Settings**
2. Scroll hacia abajo hasta **"Service Settings"**
3. Busca **"Root Directory"**
4. **DEBE decir:** `backend` (sin la barra /)

```
Root Directory: backend
```

**Si dice `/backend` o está vacío:**
- Click en el campo
- Borra todo
- Escribe: `backend`
- Presiona Enter

---

## PASO 4: Verificar Variables

1. Click en el tab **"Variables"** (arriba)
2. **Verifica que TODAS estas variables existan:**

```
MONGO_URL              (debe empezar con mongodb+srv://)
DB_NAME                ai_agent_db
SECRET_KEY             (cualquier texto largo)
CORS_ORIGINS           *
OPENAI_API_KEY         (tu key de OpenAI)
PERPLEXITY_API_KEY     (tu key de Perplexity)
PORT                   $PORT
PYTHONUNBUFFERED       1
```

**Si falta alguna:**
- Click en **"New Variable"**
- Escribe el nombre (ejemplo: `CORS_ORIGINS`)
- Escribe el valor (ejemplo: `*`)
- Click **"Add"**

---

## PASO 5: Hacer Redeploy

1. Click en el tab **"Deployments"** (arriba)
2. Arriba a la derecha verás un botón **"Deploy"**
3. **Click en "Deploy"**
4. Espera 3-5 minutos

**Verás que empieza a hacer el build...**

---

## ✅ VERIFICAR QUE FUNCIONA

Cuando el deployment diga **"Success"** (con un ✅ verde):

1. Abre una **nueva pestaña** en tu navegador
2. Copia y pega esta URL:
   ```
   https://ai-agent-backend-production-9d42.up.railway.app/api/health
   ```
3. Presiona Enter

**Deberías ver algo como:**
```json
{
  "status": "healthy",
  "database": "connected"
}
```

### ✅ Si ves eso = ¡FUNCIONA!

### ❌ Si ves error 502:

1. Ve a Railway
2. Tab **"Deployments"**
3. Click en el último deployment
4. **Scroll hacia abajo para ver los logs**
5. **Copia las últimas 20 líneas** (las que sean rojas o tengan "Error")
6. Pégalas aquí y te ayudo

---

## 🔌 DESPUÉS: Configurar WordPress

Cuando `/api/health` funcione:

1. Ve a tu **WordPress Admin**
2. Busca **AI Chat Settings** (o como se llame tu plugin)
3. En **"Backend URL"** pon:
   ```
   https://ai-agent-backend-production-9d42.up.railway.app
   ```
   ⚠️ **SIN** `/api` al final

4. Click **"Guardar"**
5. Click **"Probar Conexión"**

### ✅ Debería decir: "Backend conectado correctamente"

---

## 🆘 Si Algo Sale Mal

**Dime:**
1. ¿En qué paso estás?
2. ¿Qué ves en la pantalla?
3. Si hay error, copia el mensaje

---

## 📋 Resumen de lo que vas a hacer:

```
1. Settings → Builder → NIXPACKS
2. Settings → Root Directory → backend
3. Variables → Verificar todas
4. Deployments → Deploy
5. Esperar 5 minutos
6. Probar /api/health
```

**Total: 5-10 minutos** ⏱️

---

**¿Listo? ¡Empieza con el PASO 1!** 🚀
