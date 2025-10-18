# 🔧 CONFIGURACIÓN DE VARIABLES DE ENTORNO - GUÍA COMPLETA

## ✅ ESTADO: CONFIGURADO

---

## 📝 VARIABLES CONFIGURADAS

### **1. TRUSTED_IPS** ✅
**Qué hace:** IPs que bypasean completamente el rate limiting.
**Valor configurado:** `127.0.0.1,34.16.56.64`
- `127.0.0.1` - Localhost (acceso local)
- `34.16.56.64` - Tu IP actual

**Uso:**
- Si tu IP cambia, actualiza este valor
- Para agregar más IPs: `TRUSTED_IPS="127.0.0.1,34.16.56.64,otra.ip.aqui"`

---

### **2. ADMIN_WHITELIST_IPS** ✅
**Qué hace:** Solo estas IPs pueden acceder a endpoints administrativos.
**Valor configurado:** `127.0.0.1,34.16.56.64`

**Endpoints protegidos:**
- `/api/admin/*` - Funciones de administración
- `/api/database/*` - Gestión de base de datos
- `/api/audit-logs/*` - Logs de auditoría
- `/api/api-keys/*` - Gestión de API keys

**Seguridad:**
- Si intentas acceder desde otra IP → Error 403 Forbidden
- Para agregar más IPs: `ADMIN_WHITELIST_IPS="127.0.0.1,34.16.56.64,ip.admin.aqui"`

---

### **3. ENVIRONMENT** ✅
**Qué hace:** Define el entorno de ejecución.
**Valor configurado:** `development`

**Opciones:**
- `development` - Desarrollo local (logs verbose, headers permisivos)
- `staging` - Ambiente de pruebas
- `production` - Producción (seguridad máxima, logs mínimos)

**Cambiar a producción:**
```bash
ENVIRONMENT="production"
```

---

### **4. LOG_LEVEL** ✅
**Qué hace:** Controla qué nivel de logs se guardan.
**Valor configurado:** `INFO`

**Opciones (de menos a más verbose):**
- `CRITICAL` - Solo errores críticos
- `ERROR` - Errores
- `WARNING` - Advertencias
- `INFO` - Información general (recomendado)
- `DEBUG` - Debugging detallado

---

### **5. APP_VERSION** ✅
**Qué hace:** Versión de la app para tracking.
**Valor configurado:** `1.0.0`

**Uso:**
- Útil para Sentry (error tracking)
- Tracking de deploys
- Changelog

---

## ⚠️ VARIABLES OPCIONALES (NO CONFIGURADAS)

### **6. SENTRY_DSN** ❌ (Opcional pero recomendado)
**Qué hace:** Error tracking automático con Sentry.

**Cómo obtener:**
1. Ve a https://sentry.io
2. Crea una cuenta gratuita
3. Crea un nuevo proyecto → Selecciona "Python" → "FastAPI"
4. Copia el DSN que aparece
5. Agrégalo al .env:

```bash
SENTRY_DSN="https://abc123def456@o123456.ingest.sentry.io/7891011"
```

**Beneficios:**
- Captura automática de errores
- Stack traces completos
- Notificaciones de errores
- Performance monitoring
- 5,000 eventos/mes gratis

---

### **7. GRAFANA_USER y GRAFANA_PASSWORD** ✅
**Qué hace:** Credenciales para Grafana (dashboard de métricas).
**Valores configurados:** `admin` / `admin`

**⚠️ IMPORTANTE:** Cambiar en producción:
```bash
GRAFANA_USER="tu_usuario"
GRAFANA_PASSWORD="contraseña_segura_aqui"
```

**Acceso:**
- URL: http://localhost:3001
- User: admin
- Password: admin

---

## 🚀 VERIFICAR CONFIGURACIÓN

### **Test 1: Health Check**
```bash
curl http://localhost:8001/api/health/liveness
```
**Esperado:** `{"status":"alive"}`

### **Test 2: Acceso Admin (desde tu IP)**
```bash
curl http://localhost:8001/api/database/info
```
**Esperado:** JSON con info de base de datos

### **Test 3: Rate Limiting (tu IP está whitelisted)**
```bash
# Hacer 100 requests rápidos
for i in {1..100}; do curl -s http://localhost:8001/api/health/liveness > /dev/null; done
echo "Requests completados sin rate limit"
```
**Esperado:** Ningún error 429

---

## 📋 CHECKLIST DE CONFIGURACIÓN

- [x] TRUSTED_IPS configurado con tu IP
- [x] ADMIN_WHITELIST_IPS configurado con tu IP
- [x] ENVIRONMENT configurado (development)
- [x] LOG_LEVEL configurado (INFO)
- [x] APP_VERSION configurado
- [x] Backend reiniciado con nuevas variables
- [ ] SENTRY_DSN configurado (opcional)
- [ ] GRAFANA_PASSWORD cambiado (si usas Grafana)

---

## 🔄 CÓMO ACTUALIZAR TU IP

Si tu IP cambia (reinicio del servidor, nueva red, etc.):

### Opción 1: Automático (Script)
```bash
# Crear script para actualizar IP
cat > /app/backend/scripts/update_ip.sh << 'EOF'
#!/bin/bash
NEW_IP=$(curl -s ifconfig.me)
sed -i "s/TRUSTED_IPS=.*/TRUSTED_IPS=\"127.0.0.1,$NEW_IP\"/" /app/backend/.env
sed -i "s/ADMIN_WHITELIST_IPS=.*/ADMIN_WHITELIST_IPS=\"127.0.0.1,$NEW_IP\"/" /app/backend/.env
echo "IP actualizada a: $NEW_IP"
sudo supervisorctl restart backend
EOF

chmod +x /app/backend/scripts/update_ip.sh
```

Ejecutar:
```bash
/app/backend/scripts/update_ip.sh
```

### Opción 2: Manual
1. Obtener nueva IP: `curl ifconfig.me`
2. Editar `/app/backend/.env`
3. Actualizar `TRUSTED_IPS` y `ADMIN_WHITELIST_IPS`
4. Reiniciar: `sudo supervisorctl restart backend`

---

## 🛡️ CONFIGURACIÓN DE PRODUCCIÓN RECOMENDADA

Cuando vayas a producción, actualiza estos valores:

```bash
# Producción
ENVIRONMENT="production"
LOG_LEVEL="WARNING"  # Menos verbose
CORS_ORIGINS="https://tu-dominio.com"  # Solo tu dominio
GRAFANA_PASSWORD="contraseña_segura_random"

# IPs específicas (NO usar wildcards)
TRUSTED_IPS="127.0.0.1,ip.loadbalancer.aqui"
ADMIN_WHITELIST_IPS="ip.admin.oficina.aqui,ip.vpn.aqui"

# Sentry (MUY recomendado en producción)
SENTRY_DSN="https://tu-dsn@sentry.io/proyecto"
```

---

## 📞 SOLUCIÓN DE PROBLEMAS

### **Error 403 al acceder a /api/database/info**
**Causa:** Tu IP no está en ADMIN_WHITELIST_IPS
**Solución:**
1. Verifica tu IP: `curl ifconfig.me`
2. Agrégala a ADMIN_WHITELIST_IPS
3. Reinicia backend

### **Rate limit 429 aunque tu IP está en TRUSTED_IPS**
**Causa:** Backend no cargó las nuevas variables
**Solución:**
```bash
sudo supervisorctl restart backend
```

### **Backend no inicia después de cambiar .env**
**Causa:** Sintaxis incorrecta en .env
**Solución:**
1. Ver logs: `tail -n 50 /var/log/supervisor/backend.err.log`
2. Verificar no hay comillas mal cerradas
3. Verificar no hay espacios extras

---

## 🎉 RESUMEN

✅ **CONFIGURADO:**
- Tu IP está whitelisted para admin
- Rate limiting bypaseado para tu IP
- Logging configurado en INFO
- Variables de entorno listas

⚠️ **OPCIONAL:**
- Configurar Sentry DSN para error tracking
- Cambiar password de Grafana

🚀 **PRÓXIMO PASO:**
- Testear funcionalidades
- O configurar features adicionales
