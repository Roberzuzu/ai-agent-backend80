# ⚙️ Configuración Correcta de Railway - Guía Visual

## 🎯 El problema: Railway está usando Docker en lugar de Nixpacks

---

## ✅ CONFIGURACIÓN CORRECTA (Paso a Paso)

### 1️⃣ Builder (MUY IMPORTANTE)

```
Railway Dashboard → Tu Servicio → Settings → Build

┌─────────────────────────────────────┐
│ Build                                │
├─────────────────────────────────────┤
│ Builder: [NIXPACKS ▼]              │  ← DEBE SER NIXPACKS
│                                      │
│ ❌ NO: Docker                       │
│ ❌ NO: Docker Compose               │
│ ✅ SÍ: NIXPACKS                     │
└─────────────────────────────────────┘
```

**Si dice "Docker" → Cámbialo a "NIXPACKS"**

---

### 2️⃣ Root Directory

```
Settings → Service Settings

┌─────────────────────────────────────┐
│ Root Directory                       │
├─────────────────────────────────────┤
│ backend                              │  ← SIN la barra /
└─────────────────────────────────────┘

✅ CORRECTO:   backend
❌ INCORRECTO: /backend
❌ INCORRECTO: ./backend
❌ INCORRECTO: (vacío)
```

---

### 3️⃣ Build Command

```
Settings → Build

┌─────────────────────────────────────┐
│ Build Command (Optional)             │
├─────────────────────────────────────┤
│ pip install --no-cache-dir \       │
│   -r requirements_standalone.txt    │
└─────────────────────────────────────┘

O déjalo vacío (Railway lo detecta automáticamente)
```

---

### 4️⃣ Start Command

```
Settings → Deploy

┌─────────────────────────────────────┐
│ Start Command (Optional)             │
├─────────────────────────────────────┤
│ uvicorn server:app --host \         │
│   0.0.0.0 --port $PORT              │
└─────────────────────────────────────┘

O déjalo vacío (Railway usa el Procfile)
```

---

### 5️⃣ Variables de Entorno (CRÍTICO)

```
Tab "Variables"

┌─────────────────────────────────────┐
│ Variables                            │
├─────────────────────────────────────┤
│ MONGO_URL          mongodb+srv://... │
│ DB_NAME            ai_agent_db       │
│ SECRET_KEY         tu-secret-key     │
│ CORS_ORIGINS       *                 │
│ OPENAI_API_KEY     sk-proj-...       │
│ PERPLEXITY_API_KEY pplx-...          │
│ PORT               $PORT             │
│ PYTHONUNBUFFERED   1                 │
└─────────────────────────────────────┘

Todas estas variables SON OBLIGATORIAS
```

---

### 6️⃣ Networking

```
Settings → Networking

┌─────────────────────────────────────┐
│ Domains                              │
├─────────────────────────────────────┤
│ [Generate Domain]  ← Click aquí     │
│                                      │
│ ai-agent-backend-production-        │
│ 9d42.up.railway.app                 │
└─────────────────────────────────────┘
```

---

## 🔄 Después de Configurar

### 1. Redeploy

```
Tab "Deployments" → Click "Deploy" (arriba derecha)
```

### 2. Ver Logs

```
Tab "Deployments" → Click en el deployment activo
```

**Deberías ver:**
```
✅ Using Nixpacks
✅ Installing Python 3.10
✅ Installing requirements...
✅ Starting uvicorn...
✅ Application startup complete
```

**NO deberías ver:**
```
❌ docker-compose
❌ docker build
❌ Dockerfile not found
```

---

## ✅ Verificar que Funciona

### Test en Navegador:

```
https://ai-agent-backend-production-9d42.up.railway.app/api/health
```

**Respuesta esperada:**
```json
{
  "status": "healthy",
  "database": "connected",
  "timestamp": "..."
}
```

---

## 🆘 Troubleshooting Rápido

### Problema: Sigue usando Docker

```
Solución:
1. Settings → Builder
2. Cambiar manualmente a NIXPACKS
3. Guardar
4. Redeploy
```

### Problema: "Module not found"

```
Solución:
1. Verificar Root Directory = backend (sin /)
2. Verificar que requirements_standalone.txt esté en backend/
3. Redeploy
```

### Problema: "Connection refused" (MongoDB)

```
Solución:
1. Verificar MONGO_URL en Variables
2. MongoDB Atlas → Network Access → 0.0.0.0/0
3. Verificar usuario y password en MONGO_URL
```

### Problema: Variables no se aplican

```
Solución:
1. Tab Variables → Editar
2. Click "Update Variables"
3. Esperar 5 segundos
4. Redeploy manualmente
```

---

## 📋 Resumen de Configuración Ideal

```
┌─────────────────────────────────────────────┐
│ RAILWAY CONFIGURATION                       │
├─────────────────────────────────────────────┤
│ Builder:         NIXPACKS                   │
│ Root Directory:  backend                    │
│ Build Command:   (auto-detect or custom)    │
│ Start Command:   (auto-detect from Procfile)│
│ Variables:       8+ variables configuradas  │
│ Domain:          Generado                   │
│ Status:          Success ✅                 │
└─────────────────────────────────────────────┘
```

---

## 🎯 Configuración WordPress (Cuando funcione)

```
WordPress Admin → AI Chat Settings

┌─────────────────────────────────────────────┐
│ Backend URL                                 │
├─────────────────────────────────────────────┤
│ https://ai-agent-backend-production-       │
│ 9d42.up.railway.app                        │
│                                             │
│ ⚠️  SIN /api al final                      │
└─────────────────────────────────────────────┘

[Guardar Configuración] [Probar Conexión]

✅ Backend conectado correctamente
```

---

## 📝 Notas Importantes

1. **Builder DEBE ser NIXPACKS** - Es el más importante
2. **Root Directory DEBE ser `backend`** (sin `/`)
3. **Variables DEBEN estar todas configuradas**
4. **MongoDB Atlas DEBE permitir `0.0.0.0/0`**
5. **Cada cambio requiere REDEPLOY**

---

## 🔗 Archivos de Referencia

- Guía Completa: `RAILWAY_DEPLOYMENT_GUIDE.md`
- Quick Start: `RAILWAY_QUICK_START.md`
- Fix Error 502: `FIX_RAILWAY_502.md`
- Fix Docker Error: `FIX_DOCKER_COMPOSE_ERROR.md`

---

**Si tienes dudas, comparte screenshots de cada sección de Settings** 📸
