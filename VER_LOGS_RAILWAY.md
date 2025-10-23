# 🔍 Cómo Ver los Logs en Railway

## URGENTE: Necesito que veas los logs

Los logs me dirán EXACTAMENTE qué está fallando.

---

## 📋 Pasos para Ver los Logs:

### 1. Ve a Railway Dashboard
```
https://railway.app/dashboard
```

### 2. Click en tu Proyecto
```
Click en el proyecto del backend
```

### 3. Click en el Servicio
```
Click en el servicio (círculo/cuadrado con el nombre)
```

### 4. Tab "Deployments"
```
Arriba verás tabs: Overview, Deployments, Metrics, etc.
Click en "Deployments"
```

### 5. Click en el Último Deployment
```
Verás una lista de deployments
El primero (arriba) es el más reciente
Click en él
```

### 6. Ver los Logs
```
Scroll hacia abajo
Verás una caja negra/gris con texto
ESO SON LOS LOGS
```

---

## 📸 Lo Que Necesito:

**Copia y pega aquí:**
- Las **últimas 30-50 líneas** de los logs
- Especialmente las líneas que tengan:
  - ❌ "Error"
  - ❌ "Failed"
  - ❌ "Exception"
  - ❌ Cualquier línea ROJA

---

## 🎯 Qué Buscar en los Logs:

### Error Común 1: MongoDB
```
Error: Connection refused
Error: Authentication failed
MongoServerError
```
**Significa:** Problema con MongoDB Atlas

### Error Común 2: Módulos
```
ModuleNotFoundError: No module named 'X'
ImportError: cannot import name
```
**Significa:** Falta instalar algo

### Error Común 3: Variables
```
KeyError: 'MONGO_URL'
Environment variable not found
```
**Significa:** Falta configurar variables

### Error Común 4: Puerto
```
Address already in use
Failed to bind to port
```
**Significa:** Problema con el puerto

---

## 💡 Tip Rápido

Si los logs dicen algo como:
```
✅ "Application startup complete"
✅ "Uvicorn running on"
✅ "Started server process"
```

Pero igual da error → El problema es con MongoDB o variables.

---

## 🆘 Copia los Logs Aquí

**Por favor:**
1. Ve a los logs (siguiendo los pasos arriba)
2. Copia las últimas 30-50 líneas
3. Pégalas aquí en el chat

Con eso te digo EXACTAMENTE qué arreglar. 🎯

---

**Tiempo estimado: 2 minutos** ⏱️
