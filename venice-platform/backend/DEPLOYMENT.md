# 🚀 Guía de Deployment - Las Herramientas de Cerebro

## Despliegue en Render.com + MongoDB Atlas

Esta guía te ayudará a desplegar **Las Herramientas de Cerebro** en Render.com con MongoDB Atlas como base de datos.

---

## 📝 Requisitos Previos

- Cuenta en [Render.com](https://render.com) (gratis)
- Cuenta en [MongoDB Atlas](https://www.mongodb.com/cloud/atlas) (gratis)
- Repositorio GitHub con el código
- API Keys de:
  - OpenRouter
  - Perplexity
  - n8n (opcional)
  - WooCommerce (opcional)
  - Telegram Bot (opcional)

---

## 📊 Paso 1: Configurar MongoDB Atlas

### 1.1 Crear Cluster

1. Ve a [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
2. Crea una cuenta o inicia sesión
3. Click en **"Build a Database"**
4. Selecciona **FREE tier** (M0 Sandbox)
5. Elige la región más cercana (recomendado: Frankfurt para EU)
6. Nombre del cluster: `las-herramientas-cerebro`
7. Click en **"Create"**

### 1.2 Configurar Acceso a la Base de Datos

1. Ve a **Database Access** en el menú lateral
2. Click en **"Add New Database User"**
3. Crea usuario:
   - Username: `cerebro_admin`
   - Password: Genera una contraseña segura (guárdala)
   - Database User Privileges: **Read and write to any database**
4. Click en **"Add User"**

### 1.3 Whitelist de IPs

1. Ve a **Network Access** en el menú lateral
2. Click en **"Add IP Address"**
3. Selecciona **"Allow Access from Anywhere"** (0.0.0.0/0)
   - Esto es necesario para que Render pueda conectarse
4. Click en **"Confirm"**

### 1.4 Obtener Connection String

1. Ve a **Database** > **Connect**
2. Selecciona **"Connect your application"**
3. Copia el connection string:
   ```
   mongodb+srv://cerebro_admin:<password>@las-herramientas-cerebro.xxxxx.mongodb.net/?retryWrites=true&w=majority
   ```
4. **Reemplaza `<password>` con tu contraseña real**
5. Guárdalo para el siguiente paso

---

## 🌐 Paso 2: Desplegar en Render.com

### 2.1 Conectar Repositorio GitHub

1. Ve a [Render.com](https://render.com)
2. Crea una cuenta o inicia sesión
3. Click en **"New +"** > **"Blueprint"**
4. Conecta tu cuenta de GitHub si aún no lo has hecho
5. Selecciona el repositorio: `Roberzuzu/ai-agent-backend80`
6. Render detectará automáticamente el archivo `render.yaml`

### 2.2 Configurar Variables de Entorno

Render te pedirá configurar las variables de entorno. Completa con tus valores reales:

```bash
# Obligatorias
API_AUTH_TOKEN=tu_token_secreto_personalizado
OPENROUTER_API_KEY=sk-or-v1-xxxxxxxxxxxxx
SERVICE_PERPLEXITY_KEY=pplx-xxxxxxxxxxxxx
SERVICE_MONGODB_URI=mongodb+srv://cerebro_admin:tu_password@las-herramientas-cerebro.xxxxx.mongodb.net/cerebro?retryWrites=true&w=majority

# Opcionales (si las tienes)
SERVICE_N8N_URL=https://n8n.tudominio.com
SERVICE_N8N_API_KEY=tu_n8n_api_key
SERVICE_WOO_URL=https://herramientasyaccesorios.store
SERVICE_WOO_CONSUMER_KEY=ck_xxxxxxxxxxxxx
SERVICE_WOO_CONSUMER_SECRET=cs_xxxxxxxxxxxxx
TELEGRAM_BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
JWT_SECRET=un_secreto_muy_seguro_y_aleatorio_minimo_32_caracteres
```

### 2.3 Deploy

1. Click en **"Apply"** o **"Create Web Service"**
2. Render comenzará a construir y desplegar tu aplicación
3. El proceso tomará 5-10 minutos
4. Una vez completado, obtendrás una URL tipo:
   ```
   https://las-herramientas-de-cerebro.onrender.com
   ```

---

## ✅ Paso 3: Verificar Deployment

### 3.1 Health Check

Visita tu URL de Render + `/internal/health`:

```
https://las-herramientas-de-cerebro.onrender.com/internal/health
```

Deberías ver una respuesta JSON:
```json
{
  "status": "OK",
  "timestamp": "2025-11-07T09:00:00.000Z"
}
```

### 3.2 Probar API de Chat

Puedes hacer una petición POST a `/api/chat`:

```bash
curl -X POST https://las-herramientas-de-cerebro.onrender.com/api/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: tu_token_secreto_personalizado" \
  -d '{
    "message": "Hola, ¿qué puedes hacer?",
    "userId": "test-user"
  }'
```

---

## 🔧 Paso 4: Configurar Auto-Deploy

Render ya tiene configurado auto-deploy desde GitHub. Cada vez que hagas push a la rama `main`, se redesplegará automáticamente.

Para desactivarlo:
1. Ve a tu servicio en Render
2. Settings > Build & Deploy
3. Desactiva "Auto-Deploy"

---

## 🐛 Troubleshooting

### Problema: "Service Unavailable"

**Solución:**
- Verifica que todas las variables de entorno estén configuradas
- Revisa los logs en Render Dashboard
- Asegúrate de que MongoDB URI sea correcto

### Problema: "Cannot connect to MongoDB"

**Solución:**
- Verifica que la IP 0.0.0.0/0 esté en la whitelist de MongoDB Atlas
- Confirma que la contraseña en el connection string sea correcta
- Asegúrate de que el nombre de la base de datos esté en el URI

### Problema: "401 Unauthorized"

**Solución:**
- Verifica que el header `Authorization` contenga el valor correcto de `API_AUTH_TOKEN`

---

## 📊 Monitoreo

### Logs en Tiempo Real

1. Ve a tu servicio en Render Dashboard
2. Click en "Logs"
3. Verás todos los logs del servidor en tiempo real

### Métricas

1. Render proporciona métricas básicas:
   - CPU usage
   - Memory usage
   - Request count
   - Response times

---

## 🚀 Próximos Pasos

1. **Dominio Personalizado**: Conecta tu propio dominio en Render Settings
2. **SSL/TLS**: Render proporciona HTTPS automáticamente
3. **Escalar**: Actualiza a un plan paid para mejor rendimiento
4. **Backups**: Configura backups automáticos en MongoDB Atlas
5. **Monitoring**: Integra servicios como Sentry o LogRocket

---

## 📞 Soporte

- **Render Docs**: https://render.com/docs
- **MongoDB Atlas Docs**: https://docs.atlas.mongodb.com/
- **Issues GitHub**: https://github.com/Roberzuzu/ai-agent-backend80/issues

---

¡Tu plataforma **Las Herramientas de Cerebro** está lista para usar! 🎉
