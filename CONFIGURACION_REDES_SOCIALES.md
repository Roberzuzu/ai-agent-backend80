# 🔧 Configuración de Redes Sociales - Guía Completa

## ⚠️ IMPORTANTE: Los tokens proporcionados han expirado

Los tokens de acceso de Facebook/Instagram expiraron el **16 de octubre, 2025**.  
Necesitas generar **nuevos tokens** para que la integración funcione.

---

## 📱 OPCIÓN 1: Instagram + Facebook (Recomendado)

### Paso 1: Crear Facebook App

1. Ve a: https://developers.facebook.com/apps
2. Click en "Create App"
3. Selecciona tipo: **Business**
4. Nombre de la app: "Herramientas y Accesorios Social Manager"
5. Email de contacto: tu email
6. Click "Create App"

### Paso 2: Configurar Instagram Basic Display

1. En el dashboard de tu app, click en "Add Product"
2. Busca **"Instagram Basic Display"**
3. Click "Set Up"
4. En la configuración:
   - Valid OAuth Redirect URIs: `https://localhost`
   - Deauthorize URL: `https://localhost`
   - Data Deletion Request URL: `https://localhost`
5. Click "Save Changes"

### Paso 3: Configurar Instagram Graph API (Para publicar)

1. En el dashboard, añade producto **"Instagram Graph API"**
2. Ve a "Basic Settings"
3. Añade tu dominio: `herramientasyaccesorios.store`
4. Guarda cambios

### Paso 4: Obtener Access Token

**Opción A: Token de Usuario (Más fácil)**
1. Ve a: https://developers.facebook.com/tools/explorer/
2. Selecciona tu app en el dropdown
3. Click en "Get Token" → "Get User Access Token"
4. Selecciona permisos:
   - `instagram_basic`
   - `instagram_content_publish`
   - `pages_show_list`
   - `pages_read_engagement`
   - `pages_manage_posts`
5. Click "Generate Access Token"
6. **¡COPIA EL TOKEN INMEDIATAMENTE!**

**Opción B: Token de Larga Duración (60 días)**
```bash
# Usa el token de usuario de Opción A
USER_TOKEN="tu_token_de_usuario"
APP_ID="tu_app_id"
APP_SECRET="tu_app_secret"

curl "https://graph.facebook.com/v18.0/oauth/access_token?grant_type=fb_exchange_token&client_id=$APP_ID&client_secret=$APP_SECRET&fb_exchange_token=$USER_TOKEN"
```

### Paso 5: Obtener IDs de Cuenta

#### Facebook Page ID:
```bash
curl "https://graph.facebook.com/v18.0/me/accounts?access_token=TU_TOKEN"
```
Respuesta te dará el `id` de tu página

#### Instagram Business Account ID:
```bash
curl "https://graph.facebook.com/v18.0/PAGE_ID?fields=instagram_business_account&access_token=TU_TOKEN"
```

### Paso 6: Actualizar .env

Edita `/app/backend/.env`:
```bash
INSTAGRAM_ACCESS_TOKEN="tu_nuevo_token"
FACEBOOK_ACCESS_TOKEN="tu_nuevo_token"  # Usa el mismo
INSTAGRAM_BUSINESS_ACCOUNT_ID="id_de_instagram"
FACEBOOK_PAGE_ID="id_de_página"
```

### Paso 7: Reiniciar Backend
```bash
sudo supervisorctl restart backend
```

---

## ✅ OPCIÓN 2: Usar Graph API Explorer (Rápido para testing)

### Para Testing Rápido:

1. **Ve a Graph API Explorer**: https://developers.facebook.com/tools/explorer/

2. **Selecciona tu app** (o crea una)

3. **Genera token con permisos**:
   - Click "Get Token" → "Get User Access Token"
   - Selecciona: `instagram_basic`, `instagram_content_publish`, `pages_manage_posts`

4. **Prueba la conexión**:
   ```
   Endpoint: me/accounts
   Click "Submit"
   ```

5. **Copia el token y actualiza .env**

---

## 🔄 OPCIÓN 3: Usar Integración de Terceros (Más fácil pero con costo)

### Make.com (Anteriormente Integromat)
- Costo: $9/mes
- Conecta automáticamente Instagram, Facebook, TikTok, etc.
- Sin necesidad de configurar APIs manualmente

### Zapier
- Costo: $20/mes
- Similar a Make.com
- Interfaz más amigable

### Buffer / Hootsuite
- Costo: $6-15/mes
- Plataforma dedicada a social media
- APIs bien documentadas

---

## 🎯 ALTERNATIVA TEMPORAL: Publicación Manual con Links

Mientras configuras los tokens, el sistema puede:

1. **Generar el contenido con IA** ✓ (Ya funciona)
2. **Preparar el post** ✓ (Ya funciona)
3. **Darte un link para publicar manualmente**:
   - Copia el texto generado
   - Copia las imágenes
   - Publica tú mismo en Instagram/Facebook
   - Marca como "publicado" en el sistema

---

## 🛠️ SOLUCIÓN INMEDIATA: Configurar Solo lo Básico

### Para empezar YA SIN tokens de redes sociales:

**El sistema FUNCIONA sin tokens**, solo no publicará automáticamente. Puedes:

1. ✅ **Usar Growth Hacker** - Analizar tendencias
2. ✅ **Usar Content Creator** - Generar contenido con IA
3. ✅ **Usar Monetization** - Gestionar productos
4. ✅ **Usar Social Manager** - Programar posts (internamente)
5. ✅ **Usar Ad Manager** - Gestionar campañas
6. ❌ Publicación automática - Necesita tokens

**Workflow sin tokens:**
```
1. Generas contenido con IA
2. Sistema lo guarda
3. Vas a tu Instagram/Facebook
4. Copias y pegas el contenido
5. Publicas manualmente
6. Marcas como "publicado" en el sistema
```

---

## 📊 INTEGRACIÓN CON HERRAMIENTASYACCESORIOS.STORE

### Conectar con WordPress (No requiere tokens de redes sociales)

**Esto SÍ puedes configurar ahora:**

1. **Ve a tu WordPress**: https://herramientasyaccesorios.store/wp-admin

2. **Crea Application Password**:
   - Usuarios → Tu perfil
   - Scroll down a "Application Passwords"
   - Nombre: "Monetization Agent"
   - Click "Add New"
   - **COPIA EL PASSWORD** (sale una sola vez)

3. **Actualiza .env**:
   ```bash
   WORDPRESS_URL="https://herramientasyaccesorios.store"
   WORDPRESS_USER="tu_usuario_admin"
   WORDPRESS_APP_PASSWORD="xxxx xxxx xxxx xxxx"
   ```

4. **Beneficios**:
   - Productos del agente → WooCommerce automático
   - Contenido generado → Posts de blog automáticos
   - Featured products en homepage
   - Sin necesidad de redes sociales

---

## 🎯 MI RECOMENDACIÓN

### FASE 1 (Esta semana): Sin redes sociales

1. ✅ Configurar WordPress (10 minutos)
2. ✅ Poblar productos en el agente
3. ✅ Generar contenido con IA
4. ✅ Publicar contenido manualmente en redes
5. ✅ Sincronizar productos con tu tienda

### FASE 2 (Próxima semana): Con redes sociales

1. Crear Facebook App (30 min)
2. Obtener tokens válidos (15 min)
3. Configurar IDs de cuenta (10 min)
4. ¡Publicación automática funcionando!

---

## 🆘 ¿Necesitas ayuda?

**Opción 1**: Sigue esta guía paso a paso y yo te ayudo cuando tengas los tokens

**Opción 2**: Usa Make.com ($9/mes) para conexión automática sin configurar APIs

**Opción 3**: Empieza sin redes sociales, solo WordPress + generación de contenido

---

## 🚀 ¿Qué Quieres Hacer Primero?

**A) Configurar Facebook/Instagram tokens ahora** (yo te guío)  
**B) Configurar WordPress primero** (más fácil, funcional inmediato)  
**C) Empezar a usar el sistema sin integraciones** (genera contenido, gestiona productos)  
**D) Ver demostración de cómo funciona actualmente**

**¿Cuál prefieres?**
