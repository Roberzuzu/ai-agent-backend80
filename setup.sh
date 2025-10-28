#!/bin/bash

# ============================================
# SCRIPT DE SETUP AUTOMATIZADO - CEREBRO AI
# ============================================
# Este script prepara todo lo necesario para el deployment
# ============================================

set -e  # Salir si hay error

echo "============================================"
echo "🧠 CEREBRO AI - SETUP AUTOMATIZADO"
echo "============================================"
echo ""

# Colores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_step() {
    echo -e "${BLUE}▶ $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${YELLOW}ℹ️  $1${NC}"
}

# ============================================
# PASO 1: VERIFICAR ARCHIVOS NECESARIOS
# ============================================
print_step "Verificando archivos necesarios..."

if [ ! -f "/app/cerebro-ai-woocommerce.zip" ]; then
    print_error "Plugin WordPress no encontrado"
    exit 1
fi

if [ ! -f "/app/backend/server.py" ]; then
    print_error "Backend no encontrado"
    exit 1
fi

if [ ! -f "/app/backend/requirements_standalone.txt" ]; then
    print_error "Requirements no encontrado"
    exit 1
fi

print_success "Todos los archivos necesarios están presentes"
echo ""

# ============================================
# PASO 2: GENERAR VARIABLES DE ENTORNO
# ============================================
print_step "Generando template de variables de entorno..."

cat > /app/.env.template << 'EOF'
# ============================================
# VARIABLES DE ENTORNO - RENDER.COM
# ============================================
# Copia estas variables a Render.com Environment
# https://dashboard.render.com/web/srv-d3tot4muk2gs73dbhid0/env
# ============================================

# ============================================
# MONGODB (OBLIGATORIO)
# ============================================
# Obtener de MongoDB Atlas después de crear cluster
# Formato: mongodb+srv://usuario:password@cluster.mongodb.net/database
MONGO_URL=mongodb+srv://cerebro_admin:TU_PASSWORD@cerebro-ai-cluster.xxxxx.mongodb.net/social_media_monetization?retryWrites=true&w=majority
DB_NAME=social_media_monetization

# ============================================
# AI APIs (OBLIGATORIO)
# ============================================
# OpenRouter - Claude 3.5 Sonnet
# Obtener en: https://openrouter.ai/keys
OPENROUTER_API_KEY=sk-or-v1-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# OpenAI - Embeddings y GPT
# Obtener en: https://platform.openai.com/api-keys
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# Perplexity - Búsquedas en tiempo real
# Obtener en: https://www.perplexity.ai/settings/api
PERPLEXITY_API_KEY=pplx-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# ============================================
# WOOCOMMERCE (OBLIGATORIO)
# ============================================
# Obtener en: WooCommerce → Ajustes → Avanzado → API REST
WC_URL=https://herramientasyaccesorios.store/wp-json/wc/v3
WC_KEY=ck_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
WC_SECRET=cs_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# ============================================
# WORDPRESS (OBLIGATORIO)
# ============================================
WP_URL=https://herramientasyaccesorios.store/wp-json/wp/v2
WP_USER=agenteweb@herramientasyaccesorios.store
WP_PASS=j(t(xcePLL^Wt09XTXubC!pJ

# ============================================
# SECURITY (OBLIGATORIO)
# ============================================
# Generar con: openssl rand -hex 32
SECRET_KEY=GENERAR_CLAVE_SEGURA_DE_32_CARACTERES_MINIMO
ENVIRONMENT=production

# ============================================
# TELEGRAM (OPCIONAL)
# ============================================
TELEGRAM_BOT_TOKEN=
TELEGRAM_CHAT_ID=

# ============================================
# OTRAS APIs (OPCIONAL)
# ============================================
FAL_API_KEY=
ABACUS_API_KEY=
STRIPE_API_KEY=
STRIPE_WEBHOOK_SECRET=
INSTAGRAM_TOKEN=
FACEBOOK_TOKEN=
SENTRY_DSN=
EOF

print_success "Template de variables creado: /app/.env.template"
echo ""

# ============================================
# PASO 3: GENERAR SECRET KEY
# ============================================
print_step "Generando SECRET_KEY..."

if command -v openssl &> /dev/null; then
    SECRET_KEY=$(openssl rand -hex 32)
else
    SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_hex(32))")
fi

print_success "SECRET_KEY generada: $SECRET_KEY"
echo ""

# ============================================
# PASO 4: CREAR ARCHIVO DE INSTRUCCIONES
# ============================================
print_step "Creando instrucciones de deployment..."

cat > /app/DEPLOYMENT_STEPS.txt << EOF
============================================
🚀 PASOS PARA DEPLOYMENT EN RENDER.COM
============================================

IMPORTANTE: Sigue estos pasos EN ORDEN

============================================
PASO 1: MONGODB ATLAS (5 minutos)
============================================

1. Abrir: https://cloud.mongodb.com
   - Sign up con Google (usa Bricospeed0@gmail.com)

2. Crear Cluster:
   - Click "Build a Database"
   - Seleccionar "Shared" (M0 Free)
   - Provider: AWS
   - Region: eu-central-1 (Frankfurt)
   - Nombre: cerebro-ai-cluster
   - Click "Create"

3. Network Access:
   - Security → Network Access
   - Add IP Address
   - "Allow Access from Anywhere" (0.0.0.0/0)
   - Confirm

4. Database User:
   - Security → Database Access
   - Add New Database User
   - Username: cerebro_admin
   - Password: Amparo14.14.14 (o genera una segura)
   - Role: Atlas Admin
   - Add User

5. Obtener Connection String:
   - Click "Connect" en el cluster
   - "Connect your application"
   - Copiar string:
   
   mongodb+srv://cerebro_admin:Amparo14.14.14@cerebro-ai-cluster.XXXXX.mongodb.net/social_media_monetization?retryWrites=true&w=majority
   
   ⚠️ Reemplazar XXXXX con el ID real de tu cluster

============================================
PASO 2: RENDER.COM (10 minutos)
============================================

1. Abrir: https://dashboard.render.com/web/srv-d3tot4muk2gs73dbhid0/env
   - Login: Bricospeed0@gmail.com / Amparo14.14.14

2. Click "Add Environment Variable" para cada una:

   MONGO_URL = [Tu connection string de MongoDB Atlas]
   DB_NAME = social_media_monetization
   OPENROUTER_API_KEY = [Ver en https://dashboard.render.com/web/srv-d3tot4muk2gs73dbhid0/env]
   OPENAI_API_KEY = [Ver en https://dashboard.render.com/web/srv-d3tot4muk2gs73dbhid0/env]
   PERPLEXITY_API_KEY = [Ver en https://dashboard.render.com/web/srv-d3tot4muk2gs73dbhid0/env]
   WC_URL = https://herramientasyaccesorios.store/wp-json/wc/v3
   WC_KEY = [Crear en WooCommerce o ver en Render si ya existe]
   WC_SECRET = [Crear en WooCommerce o ver en Render si ya existe]
   WP_URL = https://herramientasyaccesorios.store/wp-json/wp/v2
   WP_USER = agenteweb@herramientasyaccesorios.store
   WP_PASS = j(t(xcePLL^Wt09XTXubC!pJ
   SECRET_KEY = $SECRET_KEY
   ENVIRONMENT = production

3. Verificar Build Settings:
   - Settings → Build & Deploy
   - Build Command: cd backend && pip install -r requirements_standalone.txt
   - Start Command: cd backend && uvicorn server:app --host 0.0.0.0 --port \$PORT --workers 1

4. Verificar Health Check:
   - Settings → Health & Alerts
   - Health Check Path: /api/health

5. Deploy:
   - Click "Manual Deploy" → "Deploy latest commit"
   - Esperar 5-8 minutos
   - Status debe cambiar a "Live" 🟢

6. Copiar URL del servicio:
   - Aparece en la parte superior del dashboard
   - Ejemplo: https://cerebro-ai-backend-XXXX.onrender.com

============================================
PASO 3: VERIFICAR BACKEND (2 minutos)
============================================

1. Abrir en navegador:
   https://[TU-URL].onrender.com/api/health

2. Debe mostrar:
   {"status":"healthy","services":{"database":"connected","ai":"available"}}

3. Si no funciona:
   - Ver logs: https://dashboard.render.com/web/srv-d3tot4muk2gs73dbhid0/logs
   - Verificar variables de entorno
   - Verificar MongoDB connection string

============================================
PASO 4: WOOCOMMERCE API KEYS (3 minutos)
============================================

Solo si NO tienes las keys ya en Render:

1. WordPress Admin:
   https://herramientasyaccesorios.store/wp-admin
   Login: agenteweb@herramientasyaccesorios.store / j(t(xcePLL^Wt09XTXubC!pJ

2. Ir a:
   WooCommerce → Ajustes → Avanzado → API REST

3. Click "Añadir key":
   - Descripción: Cerebro AI Backend
   - Permisos: Lectura/Escritura
   - Generar

4. Copiar:
   - Consumer Key (ck_...)
   - Consumer Secret (cs_...)

5. Añadir a Render Environment

============================================
PASO 5: INSTALAR PLUGIN WORDPRESS (3 minutos)
============================================

1. Descargar:
   /app/cerebro-ai-woocommerce.zip

2. WordPress Admin:
   https://herramientasyaccesorios.store/wp-admin
   Login: agenteweb@herramientasyaccesorios.store / j(t(xcePLL^Wt09XTXubC!pJ

3. Ir a:
   Plugins → Añadir nuevo → Subir plugin

4. Seleccionar: cerebro-ai-woocommerce.zip

5. Click: Instalar ahora → Activar

6. Verificar:
   - Debe aparecer "Cerebro AI" en menú lateral

============================================
PASO 6: CONFIGURAR PLUGIN (2 minutos)
============================================

1. En WordPress:
   Cerebro AI → Configuración

2. URL de API:
   https://[TU-URL-RENDER].onrender.com/api
   
   ⚠️ Sin barra final, debe terminar en /api

3. Opciones:
   ✅ Activar chat flotante
   ✅ Solo para administradores
   Posición: bottom-right

4. Guardar cambios

============================================
PASO 7: PROBAR (2 minutos)
============================================

1. Abrir: https://herramientasyaccesorios.store

2. Buscar botón flotante (esquina inferior derecha)

3. Click para abrir chat

4. Escribir: "Dame las estadísticas de mi tienda"

5. Debe responder en 2-10 segundos

============================================
✅ DEPLOYMENT COMPLETADO
============================================

Si todo funciona:
- ✅ Backend en Render: Live 24/7
- ✅ MongoDB: Conectado
- ✅ Plugin WordPress: Instalado
- ✅ Chat: Funcionando

Siguiente paso:
- Actualizar a plan Starter en Render (\$7/mes) para evitar sleep

============================================
EOF

print_success "Instrucciones creadas: /app/DEPLOYMENT_STEPS.txt"
echo ""

# ============================================
# PASO 5: VERIFICAR BACKEND
# ============================================
print_step "Verificando configuración del backend..."

if [ -f "/app/backend/server.py" ]; then
    # Verificar que server.py tiene las importaciones correctas
    if grep -q "from motor.motor_asyncio import AsyncIOMotorClient" /app/backend/server.py; then
        print_success "MongoDB configurado en server.py"
    else
        print_error "MongoDB no configurado correctamente"
    fi
    
    if grep -q "from llm_client import" /app/backend/server.py; then
        print_success "LLM client configurado"
    else
        print_error "LLM client no configurado"
    fi
fi

echo ""

# ============================================
# PASO 6: VERIFICAR PLUGIN
# ============================================
print_step "Verificando plugin WordPress..."

if [ -f "/app/cerebro-ai-woocommerce.zip" ]; then
    SIZE=$(ls -lh /app/cerebro-ai-woocommerce.zip | awk '{print $5}')
    print_success "Plugin WordPress listo: $SIZE"
else
    print_error "Plugin no encontrado"
fi

echo ""

# ============================================
# RESUMEN FINAL
# ============================================
echo "============================================"
echo "📋 RESUMEN"
echo "============================================"
echo ""

print_success "✅ Archivos preparados:"
echo "  • /app/.env.template - Template de variables"
echo "  • /app/DEPLOYMENT_STEPS.txt - Instrucciones paso a paso"
echo "  • /app/cerebro-ai-woocommerce.zip - Plugin WordPress (16K)"
echo "  • /app/diagnostico.sh - Script de verificación"
echo ""

print_info "SECRET_KEY generada:"
echo "  $SECRET_KEY"
echo ""

print_info "📖 SIGUIENTE PASO:"
echo ""
echo "  1. Leer: cat /app/DEPLOYMENT_STEPS.txt"
echo ""
echo "  2. O seguir guía detallada: /app/INSTRUCCIONES_TU_CASO.md"
echo ""

print_info "🧪 Después de deployment, ejecutar:"
echo "  bash /app/diagnostico.sh https://TU-URL.onrender.com"
echo ""

echo "============================================"
print_success "✅ SETUP COMPLETADO"
echo "============================================"
echo ""
