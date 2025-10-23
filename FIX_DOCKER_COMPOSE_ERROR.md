# 🔧 Solución: Error "docker-compose: not found"

## 🚨 Problema

Railway está intentando ejecutar `docker-compose`, pero Railway **NO usa Docker Compose**. Este error ocurre cuando Railway detecta un archivo `docker-compose.yml` y lo ejecuta por error.

Error: `start.sh: 12: docker-compose: not found`

---

## ✅ Solución Aplicada

He actualizado los archivos de configuración para que Railway **ignore los archivos de Docker** y use el método correcto (Nixpacks + Procfile).

### Archivos Actualizados:

1. **`.railwayignore`** - Ahora ignora `docker-compose.yml` y `Dockerfile`
2. **`nixpacks.toml`** - Configuración mejorada para Nixpacks
3. **`.railway-ignore-docker`** - Marcador para Railway

---

## 🚀 Cómo Arreglarlo en Railway

### Opción 1: Configuración Manual (Recomendado)

1. **Ve a Railway Dashboard**
2. **Tu servicio → Settings**
3. **Builder → Cambiar a NIXPACKS**
   ```
   Builder: NIXPACKS (no Docker)
   ```

4. **Root Directory:**
   ```
   backend
   ```
   (sin `/` al inicio)

5. **Build Command** (en Settings):
   ```
   pip install --no-cache-dir -r requirements_standalone.txt
   ```

6. **Start Command** (en Settings):
   ```
   uvicorn server:app --host 0.0.0.0 --port $PORT
   ```

7. **Variables de Entorno** - Agrega estas:
   ```env
   MONGO_URL=mongodb+srv://tu-usuario:password@cluster0.xxxxx.mongodb.net/
   DB_NAME=ai_agent_db
   SECRET_KEY=tu-secret-key-de-32-caracteres
   CORS_ORIGINS=*
   OPENAI_API_KEY=sk-proj-tu-key
   PERPLEXITY_API_KEY=pplx-tu-key
   PORT=$PORT
   PYTHONUNBUFFERED=1
   ```

8. **Redeploy:**
   - Tab "Deployments"
   - Click "Deploy" (arriba a la derecha)

---

### Opción 2: Deploy Limpio (Si sigue fallando)

Si la configuración manual no funciona, haz un deploy limpio:

1. **Elimina el servicio actual:**
   - Railway Dashboard
   - Tu servicio → Settings → scroll abajo
   - "Delete Service"

2. **Crea un nuevo servicio:**
   - Click "+ New"
   - "Deploy from GitHub repo"
   - Selecciona tu repositorio
   - **IMPORTANTE:** Cuando pregunte "Which directory?", selecciona `backend`

3. **Configura inmediatamente:**
   - Builder: NIXPACKS
   - Root Directory: `backend`
   - Agrega variables de entorno
   - Generate Domain

4. **Wait for deployment** (3-5 minutos)

---

## ✅ Verificación

Una vez que el deployment esté "Success":

### Test 1: Verificar que use Nixpacks

En los logs de Railway deberías ver:
```
Using Nixpacks
Installing Python 3.10
Installing requirements...
uvicorn server:app...
```

**NO deberías ver:**
```
❌ docker-compose
❌ docker build
❌ Dockerfile
```

### Test 2: Health Check

Abre en tu navegador:
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

---

## 📋 Checklist de Configuración Correcta

- [ ] Builder = NIXPACKS (no Docker)
- [ ] Root Directory = `backend` (sin `/`)
- [ ] Start Command = `uvicorn server:app --host 0.0.0.0 --port $PORT`
- [ ] Variables de entorno configuradas
- [ ] Logs muestran "Using Nixpacks" (no Docker)
- [ ] Deployment status = "Success"
- [ ] `/api/health` responde correctamente

---

## 🐛 Si Sigue Fallando

### Ver qué builder está usando:

En los logs de Railway, las primeras líneas dirán:
```
Using Nixpacks    ✅ CORRECTO
```

O:
```
Using Docker      ❌ INCORRECTO
```

### Forzar Nixpacks:

Si Railway sigue usando Docker:

1. **Settings → Builder**
2. **Selecciona manualmente: NIXPACKS**
3. **Guarda**
4. **Redeploy**

---

## 📚 Por Qué Ocurre Este Error

Railway detecta automáticamente qué builder usar:

1. **Si encuentra `Dockerfile`** → Usa Docker
2. **Si encuentra `docker-compose.yml`** → Usa Docker Compose
3. **Si encuentra `Procfile` o `nixpacks.toml`** → Usa Nixpacks

Tu proyecto tiene **ambos** (Docker y Nixpacks), por eso Railway se confunde.

**Solución:** Decirle explícitamente a Railway que use Nixpacks, no Docker.

---

## ✅ Archivos de Configuración Railway

Tu proyecto ahora tiene:

```
✅ Procfile                    - Comando de inicio
✅ nixpacks.toml               - Configuración de Nixpacks
✅ railway.json                - Configuración Railway
✅ .railwayignore              - Ignora archivos innecesarios
✅ backend/requirements_standalone.txt  - Dependencias
```

**Railway debe usar ESTOS archivos, NO `docker-compose.yml`**

---

## 🆘 Necesitas Ayuda

Comparte:

1. **Screenshot de Settings → Builder** (qué builder está seleccionado)
2. **Primeras 20 líneas de los logs** (para ver si dice "Using Docker" o "Using Nixpacks")
3. **Screenshot de Settings → Root Directory**

Con esto podré darte la solución exacta. 🎯

---

## 🎯 Resumen

**El problema:** Railway está usando Docker en lugar de Nixpacks

**La solución:** Configurar Railway para usar Nixpacks

**Archivos actualizados:** `.railwayignore`, `nixpacks.toml`

**Próximo paso:** Configurar manualmente el builder en Railway Settings
