# 🔑 GUÍA RÁPIDA: OBTENER API KEYS NECESARIAS

## 📋 ÍNDICE

1. [WooCommerce API Keys](#woocommerce-api-keys)
2. [WordPress Application Password](#wordpress-application-password)
3. [OpenRouter (Claude 3.5 Sonnet)](#openrouter-claude-35-sonnet)
4. [OpenAI](#openai)
5. [Perplexity AI](#perplexity-ai)
6. [MongoDB Atlas](#mongodb-atlas)
7. [Opcionales](#opcionales-fal-abacus-stripe-telegram)

---

## 1. WOOCOMMERCE API KEYS

### Ubicación
WordPress Admin → WooCommerce → Ajustes → Avanzado → API REST

### Pasos

1. **Acceder a WooCommerce:**
   - URL: https://herramientasyaccesorios.store/wp-admin
   - Usuario: `agenteweb@herramientasyaccesorios.store`
   - Password: `j(t(xcePLL^Wt09XTXubC!pJ`

2. **Ir a API Settings:**
   ```
   WooCommerce → Ajustes → Avanzado → API REST
   ```

3. **Añadir Key:**
   - Click **"Añadir key"** o **"Add key"**

4. **Configurar:**
   - **Descripción:** `Cerebro AI Backend`
   - **Usuario:** Selecciona tu usuario admin
   - **Permisos:** **Lectura/Escritura** (Read/Write)
   - Click **"Generar clave API"**

5. **Copiar Credenciales:**
   
   ⚠️ **IMPORTANTE:** Solo se muestran UNA VEZ. Cópialas ahora.

   ```
   Consumer Key:    ck_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   Consumer Secret: cs_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   ```

6. **Añadir a Render:**
   ```bash
   WC_URL=https://herramientasyaccesorios.store/wp-json/wc/v3
   WC_KEY=ck_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   WC_SECRET=cs_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   ```

---

## 2. WORDPRESS APPLICATION PASSWORD

### ¿Por qué Application Password?

WordPress recomienda usar Application Passwords en lugar de la contraseña principal para mayor seguridad.

### Pasos

1. **Ir a Perfil de Usuario:**
   ```
   WordPress Admin → Usuarios → Perfil
   ```
   O directamente:
   ```
   https://herramientasyaccesorios.store/wp-admin/profile.php
   ```

2. **Scroll hasta "Application Passwords":**
   - Sección al final de la página

3. **Crear Nueva:**
   - **Nombre:** `Cerebro AI Backend`
   - Click **"Añadir nueva contraseña de aplicación"**

4. **Copiar la Contraseña:**
   
   Aparecerá algo como:
   ```
   xxxx xxxx xxxx xxxx xxxx xxxx
   ```

   ⚠️ **IMPORTANTE:** Copia SIN espacios:
   ```
   xxxxxxxxxxxxxxxxxxxxxxxx
   ```

5. **Añadir a Render:**
   ```bash
   WP_URL=https://herramientasyaccesorios.store/wp-json/wp/v2
   WP_USER=agenteweb@herramientasyaccesorios.store
   WP_PASS=xxxxxxxxxxxxxxxxxxxxxxxx
   ```

### Alternativa: Usar Contraseña Actual

Si no puedes crear Application Password, usa tu contraseña actual:
```bash
WP_PASS=j(t(xcePLL^Wt09XTXubC!pJ
```

⚠️ **Menos seguro** pero funciona igual.

---

## 3. OPENROUTER (CLAUDE 3.5 SONNET)

### ¿Qué es?
OpenRouter permite acceder a múltiples modelos de IA (Claude, GPT, etc.) con una sola API key.

### Crear Cuenta

1. **Ir a:** https://openrouter.ai/
2. Click **"Sign In"** → **"Sign up"**
3. Registrarse con Google o Email

### Obtener API Key

1. **Dashboard:** https://openrouter.ai/keys
2. Click **"Create Key"**
3. **Nombre:** `Cerebro AI Production`
4. **Créditos iniciales:** $1 gratis para probar
5. Copiar la key:
   ```
   sk-or-v1-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   ```

### Añadir Saldo (Recomendado)

1. **Credits:** https://openrouter.ai/credits
2. **Añadir:** $10 USD (suficiente para ~3,000 comandos)
3. Métodos: Tarjeta o crypto

### Costos (Claude 3.5 Sonnet)

| Modelo | Costo Input | Costo Output | Comando típico |
|--------|-------------|--------------|----------------|
| Claude 3.5 Sonnet | $3/M tokens | $15/M tokens | ~$0.003 |

**Estimado:** $0.003 por comando → 333 comandos por $1

### Añadir a Render

```bash
OPENROUTER_API_KEY=sk-or-v1-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

---

## 4. OPENAI

### ¿Para qué?
- Embeddings (búsqueda semántica en memoria)
- GPT como backup
- Análisis de imágenes

### Crear Cuenta

1. **Ir a:** https://platform.openai.com/signup
2. Registrarse con Email o Google
3. Verificar email

### Obtener API Key

1. **Dashboard:** https://platform.openai.com/api-keys
2. Click **"Create new secret key"**
3. **Nombre:** `Cerebro AI Production`
4. Copiar la key:
   ```
   sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   ```

### Añadir Saldo

1. **Billing:** https://platform.openai.com/account/billing
2. **Add payment method:** Tarjeta de crédito
3. **Añadir créditos:** $5-10 USD inicial

### Costos

| Servicio | Modelo | Costo | Uso en Cerebro |
|----------|--------|-------|----------------|
| Embeddings | text-embedding-ada-002 | $0.0001/1K tokens | $0.0001 por búsqueda |
| GPT-4 | gpt-4 | $0.03/1K tokens | Opcional |
| GPT-4o | gpt-4o | $0.005/1K tokens | Backup |

**Estimado:** $0.0001 por búsqueda en memoria → 10,000 búsquedas por $1

### Añadir a Render

```bash
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

---

## 5. PERPLEXITY AI

### ¿Para qué?
Búsquedas en tiempo real en internet (tendencias, precios, competencia)

### Crear Cuenta

1. **Ir a:** https://www.perplexity.ai/
2. Click **"Sign In"** → **"Sign up"**
3. Registrarse con Google o Email

### Obtener API Key

1. **Settings:** https://www.perplexity.ai/settings/api
2. Click **"Generate API Key"**
3. **Nombre:** `Cerebro AI`
4. Copiar la key:
   ```
   pplx-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   ```

### Créditos

- **Gratis:** $5 de crédito inicial
- **De pago:** $20/mes por 5M tokens
- **Pay as you go:** $0.001 por búsqueda

### Costos

| Modelo | Costo | Uso típico |
|--------|-------|------------|
| Sonar Small | $0.0005/request | Búsquedas simples |
| Sonar Medium | $0.002/request | Búsquedas complejas |
| Sonar Large | $0.005/request | Análisis profundo |

**Estimado:** $0.002 por búsqueda → 500 búsquedas por $1

### Añadir a Render

```bash
PERPLEXITY_API_KEY=pplx-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

---

## 6. MONGODB ATLAS

### ¿Para qué?
Base de datos para memoria del agente, conversaciones, historial.

### Crear Cuenta

1. **Ir a:** https://cloud.mongodb.com
2. Click **"Try Free"**
3. Registrarse con Google o Email

### Crear Cluster Gratuito

1. **Seleccionar Plan:** **M0 Free** (512MB, gratis para siempre)
2. **Provider:** AWS
3. **Region:** **eu-central-1 (Frankfurt)** (más cercana a España)
4. **Cluster Name:** `cerebro-ai-cluster`
5. Click **"Create"**

⏱️ Espera 2-3 minutos.

### Configurar Acceso

#### Network Access (Permitir todas las IPs)

1. **Security → Network Access**
2. Click **"Add IP Address"**
3. Click **"Allow Access from Anywhere"**
4. IP Address: `0.0.0.0/0`
5. Click **"Confirm"**

#### Database User

1. **Security → Database Access**
2. Click **"Add New Database User"**
3. **Authentication Method:** Password
4. **Username:** `cerebro_admin`
5. **Password:** Genera una fuerte (guárdala!)
6. **Database User Privileges:** **Atlas Admin**
7. Click **"Add User"**

### Obtener Connection String

1. Click **"Connect"** en tu cluster
2. **Connect your application**
3. Driver: **Python**, Version: **3.12 or later**
4. Copiar string:
   ```
   mongodb+srv://cerebro_admin:<password>@cerebro-ai-cluster.xxxxx.mongodb.net/?retryWrites=true&w=majority
   ```

5. **Reemplazar:**
   - `<password>` → Tu contraseña real
   - Añadir DB name al final: `/social_media_monetization`

**String final:**
```
mongodb+srv://cerebro_admin:TU_PASSWORD@cerebro-ai-cluster.xxxxx.mongodb.net/social_media_monetization?retryWrites=true&w=majority
```

### Añadir a Render

```bash
MONGO_URL=mongodb+srv://cerebro_admin:TU_PASSWORD@cerebro-ai-cluster.xxxxx.mongodb.net/social_media_monetization?retryWrites=true&w=majority
DB_NAME=social_media_monetization
```

---

## 7. OPCIONALES (FAL, ABACUS, STRIPE, TELEGRAM)

### FAL.AI (Generación de Imágenes)

**Solo si necesitas generar imágenes con IA.**

1. **Ir a:** https://fal.ai/
2. Sign up con GitHub o Google
3. **Dashboard:** https://fal.ai/dashboard/keys
4. Click **"Create Key"**
5. Copiar key: `fal_xxxxxxxxxxxxxxxx`
6. Añadir créditos: $5-10

**Añadir a Render:**
```bash
FAL_API_KEY=fal_xxxxxxxxxxxxxxxx
```

**Costos:** ~$0.05 por imagen HD

---

### ABACUS.AI (Análisis Predictivo)

**Solo si necesitas análisis predictivo avanzado.**

1. **Ir a:** https://abacus.ai/
2. Sign up (tiene plan gratuito)
3. **API Keys:** https://abacus.ai/app/profile/apikey
4. Click **"Generate API Key"**
5. Copiar key

**Añadir a Render:**
```bash
ABACUS_API_KEY=xxxxx
```

---

### STRIPE (Pagos)

**Solo si vas a procesar pagos.**

1. **Ir a:** https://stripe.com
2. Sign up
3. **Dashboard:** https://dashboard.stripe.com/test/apikeys
4. Modo: **Test** (para pruebas) o **Live** (producción)
5. Copiar:
   - **Secret Key:** `sk_test_xxxxx` o `sk_live_xxxxx`
   - **Webhook Secret:** `whsec_xxxxx` (si usas webhooks)

**Añadir a Render:**
```bash
STRIPE_API_KEY=sk_test_xxxxx
STRIPE_WEBHOOK_SECRET=whsec_xxxxx
```

---

### TELEGRAM BOT (Notificaciones)

**Solo si quieres notificaciones por Telegram.**

1. **Abrir Telegram**
2. Buscar: `@BotFather`
3. Comando: `/newbot`
4. Nombre: `Cerebro AI Notificaciones`
5. Username: `cerebro_ai_notif_bot` (debe terminar en _bot)
6. Copiar token: `7708509018:AAFxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

**Obtener Chat ID:**
1. Envía un mensaje a tu bot
2. Abre: `https://api.telegram.org/bot<TOKEN>/getUpdates`
3. Busca `"chat":{"id":7202793910}`
4. Ese es tu Chat ID

**Añadir a Render:**
```bash
TELEGRAM_BOT_TOKEN=7708509018:AAFxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TELEGRAM_CHAT_ID=7202793910
```

---

## 📋 RESUMEN: VARIABLES OBLIGATORIAS PARA RENDER

```bash
# ============================================
# VARIABLES OBLIGATORIAS
# ============================================

# MONGODB
MONGO_URL=mongodb+srv://cerebro_admin:PASSWORD@cerebro-ai-cluster.xxxxx.mongodb.net/social_media_monetization?retryWrites=true&w=majority
DB_NAME=social_media_monetization

# AI KEYS
OPENROUTER_API_KEY=sk-or-v1-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
PERPLEXITY_API_KEY=pplx-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# WOOCOMMERCE
WC_URL=https://herramientasyaccesorios.store/wp-json/wc/v3
WC_KEY=ck_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
WC_SECRET=cs_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# WORDPRESS
WP_URL=https://herramientasyaccesorios.store/wp-json/wp/v2
WP_USER=agenteweb@herramientasyaccesorios.store
WP_PASS=xxxxxxxxxxxxxxxxxxxxxxxx

# SECURITY
SECRET_KEY=genera-clave-aleatoria-de-32-caracteres-minimo-para-seguridad
ENVIRONMENT=production
```

---

## 💰 COSTOS ESTIMADOS MENSUALES

### Infraestructura
- **Render.com:** $0 (Free) o $7 (Starter - Recomendado)
- **MongoDB Atlas:** $0 (M0 Free - 512MB)

### APIs de IA (Variable según uso)

| Servicio | Costo por uso | 100 comandos/día | 1000 comandos/día |
|----------|---------------|------------------|-------------------|
| OpenRouter (Claude) | $0.003/comando | ~$9/mes | ~$90/mes |
| OpenAI (Embeddings) | $0.0001/búsqueda | ~$0.30/mes | ~$3/mes |
| Perplexity (Búsquedas) | $0.002/búsqueda | ~$6/mes | ~$60/mes |
| **TOTAL APIs** | - | **~$15/mes** | **~$150/mes** |

### Total Estimado

| Escenario | Comandos/día | Costo mensual |
|-----------|--------------|---------------|
| 🟢 Bajo uso | 10-50 | $7-15 |
| 🟡 Uso medio | 50-200 | $15-40 |
| 🔴 Alto uso | 200-1000 | $40-150 |

---

## ✅ CHECKLIST DE API KEYS

Una vez tengas todas las keys, verifica:

- [ ] `MONGO_URL` - MongoDB Atlas connection string
- [ ] `OPENROUTER_API_KEY` - Claude 3.5 Sonnet
- [ ] `OPENAI_API_KEY` - Embeddings y GPT
- [ ] `PERPLEXITY_API_KEY` - Búsquedas en tiempo real
- [ ] `WC_KEY` y `WC_SECRET` - WooCommerce API
- [ ] `WP_USER` y `WP_PASS` - WordPress credentials
- [ ] `SECRET_KEY` - Clave de seguridad generada

### Generar SECRET_KEY

Puedes usar este comando en tu terminal:

```bash
# En Linux/Mac
openssl rand -hex 32

# O en Python
python3 -c "import secrets; print(secrets.token_hex(32))"
```

Resultado:
```
f4e9c3a8b7d6f1e2a5c8d7b9f3e6a1c4d8e2f5a9b3c7d1e6f2a8c4d7e1b5f9a3
```

---

## 🆘 PROBLEMAS COMUNES

### ❌ "Invalid API Key"

**Causa:** Key incorrecta o sin saldo

**Solución:**
1. Verifica que copiaste la key completa (sin espacios)
2. Verifica saldo en el dashboard del servicio
3. Genera una nueva key si es necesario

---

### ❌ "MongoDB connection failed"

**Causa:** Connection string incorrecto o red bloqueada

**Solución:**
1. Verifica que reemplazaste `<password>` con tu contraseña real
2. Verifica que 0.0.0.0/0 esté permitido en Network Access
3. Prueba el string con `mongosh`:
   ```bash
   mongosh "tu-connection-string"
   ```

---

### ❌ "WooCommerce API error"

**Causa:** Keys incorrectas o permisos insuficientes

**Solución:**
1. Verifica que los permisos sean "Lectura/Escritura"
2. Verifica que WC_URL termine en `/wc/v3`
3. Prueba manualmente:
   ```bash
   curl https://herramientasyaccesorios.store/wp-json/wc/v3/products \
     -u "ck_xxx:cs_xxx"
   ```

---

**✅ Con todas estas keys, Cerebro AI estará completamente funcional 24/7 en Render.com**
