# 🎯 INSTRUCCIONES PERSONALIZADAS - HERRAMIENTAS Y ACCESORIOS

> Configuración específica para tu caso usando Render.com y herramientasyaccesorios.store

---

## ✅ LO QUE YA TIENES

- ✅ **Render.com:** Cuenta activa
  - Servicio: `srv-d3tot4muk2gs73dbhid0`
  - Dashboard: https://dashboard.render.com/web/srv-d3tot4muk2gs73dbhid0
  - Login: Bricospeed0@gmail.com / Amparo14.14.14

- ✅ **WordPress en Hostinger:**
  - URL: https://herramientasyaccesorios.store
  - Admin: https://herramientasyaccesorios.store/wp-admin
  - Usuario: agenteweb@herramientasyaccesorios.store
  - Password: j(t(xcePLL^Wt09XTXubC!pJ

- ✅ **Variables de entorno:**
  - Ya configuradas en Render: https://dashboard.render.com/web/srv-d3tot4muk2gs73dbhid0/env

---

## 🚀 PASOS RÁPIDOS PARA TI

### PASO 1: CONFIGURAR MONGODB (5 minutos)

Como prefieres MongoDB en tu servidor, sigue estos pasos:

1. **Crear cuenta en MongoDB Atlas:**
   - https://cloud.mongodb.com
   - Sign up con Google (usa Bricospeed0@gmail.com para mantener todo junto)

2. **Crear cluster gratuito M0:**
   - Región: **eu-central-1 (Frankfurt)** (más cercano a España)
   - Nombre: `cerebro-ai-cluster`

3. **Crear usuario de base de datos:**
   - Username: `cerebro_admin`
   - Password: `Amparo14.14.14` (o genera una nueva segura)
   - Role: **Atlas Admin**

4. **Permitir acceso desde cualquier IP:**
   - Security → Network Access
   - Add IP Address → **Allow Access from Anywhere** (0.0.0.0/0)

5. **Obtener connection string:**
   ```
   mongodb+srv://cerebro_admin:Amparo14.14.14@cerebro-ai-cluster.xxxxx.mongodb.net/social_media_monetization?retryWrites=true&w=majority
   ```
   
   ⚠️ **IMPORTANTE:** Reemplaza `xxxxx` con el ID real de tu cluster que aparece en Atlas.

---

### PASO 2: VERIFICAR/AÑADIR VARIABLES EN RENDER (10 minutos)

Ve a tu servicio en Render:
https://dashboard.render.com/web/srv-d3tot4muk2gs73dbhid0/env

**Variables que DEBES tener (obligatorias):**

```bash
# MONGODB (añadir la nueva)
MONGO_URL=mongodb+srv://cerebro_admin:Amparo14.14.14@cerebro-ai-cluster.xxxxx.mongodb.net/social_media_monetization?retryWrites=true&w=majority
DB_NAME=social_media_monetization

# WOOCOMMERCE (probablemente ya las tienes, si no, créalas)
WC_URL=https://herramientasyaccesorios.store/wp-json/wc/v3
WC_KEY=ck_xxxxx  # Tu Consumer Key de WooCommerce
WC_SECRET=cs_xxxxx  # Tu Consumer Secret

# WORDPRESS (ya las tienes)
WP_URL=https://herramientasyaccesorios.store/wp-json/wp/v2
WP_USER=agenteweb@herramientasyaccesorios.store
WP_PASS=j(t(xcePLL^Wt09XTXubC!pJ

# AI APIS (probablemente ya las tienes)
OPENROUTER_API_KEY=sk-or-v1-xxxxx
OPENAI_API_KEY=sk-xxxxx
PERPLEXITY_API_KEY=pplx-xxxxx

# SECURITY (probablemente ya las tienes)
SECRET_KEY=xxxxx  # Si no existe, genera una
ENVIRONMENT=production
```

**Si faltan las WooCommerce API Keys:**

1. Ve a WordPress Admin:
   - https://herramientasyaccesorios.store/wp-admin
   - Login: agenteweb@herramientasyaccesorios.store / j(t(xcePLL^Wt09XTXubC!pJ

2. Ve a:
   ```
   WooCommerce → Ajustes → Avanzado → API REST → Añadir key
   ```

3. Configura:
   - Descripción: `Cerebro AI Backend`
   - Permisos: **Lectura/Escritura**
   - Click **Generar clave API**

4. Copia las keys y añádelas a Render Environment.

---

### PASO 3: DESPLEGAR EN RENDER (5 minutos)

1. Ve a tu servicio:
   https://dashboard.render.com/web/srv-d3tot4muk2gs73dbhid0

2. En **Settings**, verifica:
   
   **Build Command:**
   ```bash
   cd backend && pip install -r requirements_standalone.txt
   ```
   
   **Start Command:**
   ```bash
   cd backend && uvicorn server:app --host 0.0.0.0 --port $PORT --workers 1
   ```
   
   **Health Check Path:**
   ```
   /api/health
   ```

3. Click **Manual Deploy** → **Deploy latest commit**

4. Espera 5-8 minutos mientras despliega.

5. Una vez que el status sea **"Live" 🟢**, copia la URL de tu servicio.
   
   Debería ser algo como:
   ```
   https://cerebro-ai-backend-XXXX.onrender.com
   ```

---

### PASO 4: PROBAR EL BACKEND (2 minutos)

Abre en tu navegador:

```
https://TU-URL.onrender.com/api/health
```

**Debe mostrar:**
```json
{
  "status": "healthy",
  "services": {
    "database": "connected",
    "ai": "available"
  }
}
```

✅ **Si ves esto, el backend funciona correctamente!**

---

### PASO 5: INSTALAR PLUGIN EN WORDPRESS (3 minutos)

1. **Descargar el plugin:**
   
   El archivo está listo en:
   ```
   /app/cerebro-ai-woocommerce.zip
   ```
   
   Descárgalo a tu computadora.

2. **Ir a WordPress:**
   - https://herramientasyaccesorios.store/wp-admin
   - Login: agenteweb@herramientasyaccesorios.store / j(t(xcePLL^Wt09XTXubC!pJ

3. **Instalar plugin:**
   - Ve a: **Plugins → Añadir nuevo**
   - Click **"Subir plugin"**
   - Selecciona `cerebro-ai-woocommerce.zip`
   - Click **"Instalar ahora"**
   - Click **"Activar plugin"**

4. **Verificar instalación:**
   - Debe aparecer **"Cerebro AI"** en el menú lateral de WordPress (con icono de cerebro 🧠)

---

### PASO 6: CONFIGURAR EL PLUGIN (2 minutos)

1. En WordPress, ve a:
   ```
   Cerebro AI → Configuración
   ```

2. **URL de la API:**
   
   Pega la URL de tu backend de Render (del Paso 3):
   ```
   https://TU-URL.onrender.com/api
   ```
   
   ⚠️ **IMPORTANTE:** NO incluir barra final, debe terminar en `/api`

3. **Opciones:**
   - ✅ Activar chat flotante
   - ✅ Solo para administradores de WooCommerce
   - Posición: `bottom-right` (esquina inferior derecha)

4. Click **"Guardar cambios"**

---

### PASO 7: PROBAR EN TU SITIO WEB (2 minutos)

1. **Abrir tu sitio web:**
   https://herramientasyaccesorios.store

2. **Buscar el botón flotante:**
   - Debe aparecer en la esquina inferior derecha
   - Icono de cerebro 🧠
   - Badge "AI"

3. **Hacer click en el botón:**
   - Se abre el chat
   - Mensaje de bienvenida de Cerebro AI

4. **Probar comando:**
   
   Escribe en el chat:
   ```
   Dame las estadísticas de mi tienda
   ```
   
   Presiona Enter o click en Enviar.

5. **Verificar respuesta:**
   - Debe aparecer indicador de "escribiendo..."
   - Respuesta en 2-10 segundos
   - Sin errores

✅ **Si todo funciona, ¡felicidades! Cerebro AI está 100% operativo.**

---

## 🧪 DIAGNÓSTICO RÁPIDO

Si algo no funciona, usa el script de diagnóstico:

```bash
bash /app/diagnostico.sh https://TU-URL.onrender.com
```

Este script verificará automáticamente:
- ✅ Conectividad
- ✅ Health check
- ✅ MongoDB conectado
- ✅ Agente AI activo (18 herramientas)
- ✅ Memoria persistente
- ✅ Tiempos de respuesta

---

## 🔧 PROBLEMAS COMUNES

### 1. "Database connection failed"

**Causa:** MongoDB no configurado o connection string incorrecto

**Solución:**
1. Verifica `MONGO_URL` en variables de Render
2. Verifica que reemplazaste la contraseña
3. Verifica que la IP 0.0.0.0/0 esté permitida en MongoDB Atlas
4. Reinicia el servicio en Render

---

### 2. "Could not connect to API" desde WordPress

**Causa:** URL incorrecta en configuración del plugin

**Solución:**
1. Ve a: Cerebro AI → Configuración en WordPress
2. Verifica que la URL sea: `https://TU-URL.onrender.com/api` (sin barra final)
3. Verifica que el backend esté "Live" en Render
4. Prueba la URL manualmente en el navegador

---

### 3. Chat no aparece en el sitio

**Causa:** Plugin no activado o no eres admin

**Solución:**
1. Verifica que el plugin esté **activado** en WordPress
2. Verifica que estás logueado como administrador
3. Verifica que "Activar chat flotante" esté marcado en configuración
4. Limpia caché de WordPress
5. Abre consola del navegador (F12) y busca errores

---

### 4. Render se duerme después de 15 minutos

**Causa:** Plan gratuito entra en "sleep" por inactividad

**Solución:**

**Opción 1 - Actualizar a plan de pago (Recomendado):**
1. Ve a tu servicio en Render
2. Click **"Upgrade"**
3. Selecciona **"Starter"** ($7/mes)
4. El servicio NUNCA se dormirá

**Opción 2 - Ping automático (gratis):**
1. Usa UptimeRobot: https://uptimerobot.com
2. Crea monitor HTTP cada 5 minutos:
   ```
   https://TU-URL.onrender.com/api/health
   ```
3. Render detecta actividad y no se duerme

⚠️ **Recomendación:** Plan Starter ($7/mes) para producción 24/7.

---

## 📋 CHECKLIST FINAL

- [ ] MongoDB Atlas creado y conectado
- [ ] Variables de entorno configuradas en Render
- [ ] Backend desplegado (status: Live)
- [ ] Health check funciona
- [ ] WooCommerce API keys configuradas
- [ ] Plugin WordPress instalado y activado
- [ ] URL de API configurada en plugin
- [ ] Chat flotante visible en el sitio
- [ ] Comando de prueba funciona correctamente

---

## 💡 RECOMENDACIONES

### Para Producción 24/7

1. **Actualizar a plan de pago en Render:**
   - Starter: $7/mes (sin sleep)
   - Suficiente para tu caso de uso

2. **Monitorear el servicio:**
   - UptimeRobot para avisos si se cae
   - Revisar logs en Render regularmente

3. **Backups:**
   - MongoDB Atlas hace backups automáticos en planes M2+ ($9/mes)
   - En plan Free (M0), exporta datos manualmente cada semana

4. **Seguridad:**
   - WordPress Application Password en lugar de contraseña principal (opcional pero recomendado)
   - Cambiar SECRET_KEY periódicamente

---

## 🎯 EJEMPLOS DE COMANDOS PARA TU TIENDA

Una vez que todo funcione, prueba estos comandos en el chat:

### Gestión de Productos
```
"Busca 10 herramientas eléctricas más vendidas en España"
"Crea un producto: Taladro Bosch 750W a 89 euros"
"Actualiza el precio del producto ID 123 a 120 euros"
"Productos sin stock"
"Optimiza los productos sin descripción"
```

### Análisis
```
"Dame las estadísticas de ventas del mes"
"¿Cuáles son mis productos más vendidos?"
"Analiza la competencia en taladros"
"Productos con bajo stock (menos de 10 unidades)"
```

### Marketing
```
"Crea una oferta del 20% para el Black Friday"
"Genera contenido para Instagram sobre herramientas"
"Optimiza el SEO de todos mis productos"
"Crea un cupón de 15% de descuento válido por 7 días"
```

---

## 🆘 SI NECESITAS AYUDA

1. **Revisa logs en Render:**
   https://dashboard.render.com/web/srv-d3tot4muk2gs73dbhid0/logs

2. **Revisa métricas:**
   https://dashboard.render.com/web/srv-d3tot4muk2gs73dbhid0/metrics

3. **Ejecuta diagnóstico:**
   ```bash
   bash /app/diagnostico.sh https://TU-URL.onrender.com
   ```

4. **Revisa documentación completa:**
   - [DEPLOYMENT_RENDER_COMPLETO.md](/app/DEPLOYMENT_RENDER_COMPLETO.md)
   - [GUIA_API_KEYS.md](/app/GUIA_API_KEYS.md)
   - [VERIFICACION_RENDER.md](/app/VERIFICACION_RENDER.md)

---

## ✅ RESUMEN

Con esta configuración, tendrás:

- ✅ **Backend funcionando 24/7 en Render.com**
- ✅ **MongoDB Atlas con memoria persistente**
- ✅ **Plugin WordPress con chat flotante**
- ✅ **18 herramientas AI integradas**
- ✅ **Claude 3.5 Sonnet como cerebro**
- ✅ **Sincronización con WooCommerce**
- ✅ **100% independiente de Emergent**

**Total inversión:**
- Infraestructura: $0-7/mes (Render + MongoDB Atlas)
- APIs de IA: $10-30/mes según uso
- **Total: $10-37/mes** para un sistema completo 24/7

---

**🎉 ¡Tu agente AI está listo para gestionar tu tienda automáticamente!**

*Configuración específica para: herramientasyaccesorios.store*  
*Fecha: Enero 2025*
