# 🚨 Railway Troubleshooting - Error 502

## Tu Backend NO Está Respondiendo

URL: `https://ai-agent-backend-production-9d42.up.railway.app`
Status: ❌ **Error 502 - Application failed to respond**

---

## 🎯 Solución Rápida (3 pasos)

### PASO 1: Ver los Logs en Railway 🔍

Es **CRÍTICO** ver qué error específico está dando.

**Cómo:**
```
1. Ve a: https://railway.app/dashboard
2. Click en tu proyecto
3. Click en el servicio backend
4. Tab "Deployments"
5. Click en el deployment (el círculo verde/rojo)
6. Scroll hacia abajo para VER LOS LOGS
```

**Busca líneas rojas con "Error", "Failed", "Exception"**

---

### PASO 2: Verificar Root Directory ⚠️

**SUPER IMPORTANTE** - Esta es la causa #1 de errores 502.

```
Settings → Service Settings → Root Directory
```

**DEBE SER:**
```
backend
```

**NO DEBE SER:**
```
/backend  ❌
```

Si tiene la barra `/`, quítala y haz redeploy.

---

### PASO 3: Verificar Variables de Entorno

```
Tab "Variables" → Verifica que estén TODAS:
```

**Variables CRÍTICAS (mínimo):**
```env
MONGO_URL=mongodb+srv://...    (debe empezar con mongodb+srv://)
DB_NAME=ai_agent_db
SECRET_KEY=cualquier-string-de-32-caracteres
PORT=$PORT
PYTHONUNBUFFERED=1
CORS_ORIGINS=*
```

**Si falta alguna, agrégala y redeploy.**

---

## 🔧 Errores Comunes y Soluciones

### Error 1: Root Directory Incorrecto
```
❌ Root Directory: /backend
✅ Root Directory: backend
```

### Error 2: MONGO_URL Incorrecta
```
❌ mongodb+srv://usuario:<password>@...
✅ mongodb+srv://usuario:tu-contraseña-real@...
```
(Reemplaza `<password>` con tu contraseña real, sin `<` ni `>`)

### Error 3: MongoDB no permite Railway
```
Solución:
1. MongoDB Atlas → Network Access
2. Add IP Address → Allow Access from Anywhere (0.0.0.0/0)
3. Confirm
```

### Error 4: Puerto Incorrecto
```
Variables debe tener:
PORT=$PORT    (no PORT=8001)

Start Command debe ser:
uvicorn server:app --host 0.0.0.0 --port $PORT
```

---

## 📋 Checklist Rápido

Verifica cada punto:

- [ ] Root Directory = `backend` (sin `/`)
- [ ] `PORT=$PORT` en Variables
- [ ] `MONGO_URL` configurada (sin `<password>`)
- [ ] MongoDB Atlas permite `0.0.0.0/0`
- [ ] Deployment status = "Success" (verde)
- [ ] Revisaste los logs (no hay errores rojos)

---

## 🔄 Cómo Hacer Redeploy

Después de hacer cambios:

```
1. Railway Dashboard → Tu servicio
2. Tab "Deployments"
3. Click "Deploy" (arriba a la derecha)
4. Espera 3-5 minutos
```

---

## ✅ Test Final

Cuando el deployment esté "Success", abre en tu navegador:

```
https://ai-agent-backend-production-9d42.up.railway.app/api/health
```

**✅ Debe mostrar:**
```json
{
  "status": "healthy",
  "database": "connected",
  "timestamp": "..."
}
```

**❌ Si sigue dando 502:**
Comparte los logs de Railway para ayudarte mejor.

---

## 🔌 Configurar WordPress (cuando funcione)

Una vez que `/api/health` responda OK:

**WordPress → Settings → Backend URL:**
```
https://ai-agent-backend-production-9d42.up.railway.app
```

⚠️ **SIN `/api` al final**

---

## 🆘 Necesito los Logs

Por favor comparte:

1. **Logs de Railway** (últimas 30-50 líneas)
2. **Screenshot de Root Directory** en Settings
3. **Lista de Variables** que tienes (sin mostrar las keys completas)

Con esto podré darte la solución exacta. 🎯

---

**Archivo de referencia completo:** `FIX_RAILWAY_502.md`
