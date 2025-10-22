#!/bin/bash

# ============================================
# Instalación Backend AI - herramientasyaccesorios.store
# Usuario: u833032076
# ============================================

echo "============================================"
echo "  Instalación Backend AI"
echo "  herramientasyaccesorios.store"
echo "============================================"
echo ""

# Colores
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Verificar que estemos en home
cd ~
echo -e "${GREEN}✓${NC} Directorio actual: $(pwd)"

# Verificar si ya existe la instalación
if [ -d "miapp-standalone-20251022-142042" ]; then
    echo -e "${YELLOW}!${NC} Instalación existente encontrada"
    read -p "¿Deseas reinstalar? (s/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Ss]$ ]]; then
        mv miapp-standalone-20251022-142042 miapp-standalone-20251022-142042.backup-$(date +%Y%m%d-%H%M%S)
        echo -e "${GREEN}✓${NC} Backup creado"
    else
        echo "Usando instalación existente"
        cd miapp-standalone-20251022-142042
    fi
fi

# Verificar si existe el ZIP
if [ ! -f "miapp-standalone-20251022-142042.zip" ]; then
    echo -e "${RED}✗${NC} No se encuentra miapp-standalone-20251022-142042.zip"
    echo ""
    echo "Por favor, sube el archivo primero:"
    echo "  scp -P 65002 /app/miapp-standalone-20251022-142042.zip u833032076@178.16.128.200:~/"
    echo ""
    exit 1
fi

# Descomprimir
echo -e "${GREEN}✓${NC} Descomprimiendo paquete..."
unzip -q miapp-standalone-20251022-142042.zip
cd miapp-standalone-20251022-142042

echo -e "${GREEN}✓${NC} Archivos descomprimidos"
echo ""

# Verificar Python
echo "Verificando Python..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version 2>&1 | cut -d' ' -f2)
    echo -e "${GREEN}✓${NC} Python: $PYTHON_VERSION"
else
    echo -e "${RED}✗${NC} Python no encontrado"
    echo "Instalando Python 3..."
    # En hosting compartido, Python suele estar disponible
fi

# Configurar backend
echo ""
echo "============================================"
echo "  Configurando Backend"
echo "============================================"
echo ""

cd backend

# Crear entorno virtual
if [ ! -d "venv" ]; then
    echo "Creando entorno virtual..."
    python3 -m venv venv || python -m venv venv
fi

# Activar entorno virtual
echo "Activando entorno virtual..."
source venv/bin/activate

# Instalar dependencias
echo "Instalando dependencias (puede tomar varios minutos)..."
pip install --upgrade pip -q
pip install -r requirements_standalone.txt -q

echo -e "${GREEN}✓${NC} Dependencias instaladas"
echo ""

# Crear .env si no existe
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}!${NC} Creando archivo .env..."
    cp .env.example .env
    
    # Generar SECRET_KEY
    SECRET_KEY=$(openssl rand -hex 32 2>/dev/null || cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 64 | head -n 1)
    sed -i "s/SECRET_KEY=.*/SECRET_KEY=$SECRET_KEY/" .env
    
    echo -e "${GREEN}✓${NC} Archivo .env creado"
else
    echo -e "${GREEN}✓${NC} Archivo .env ya existe"
fi

echo ""
echo "============================================"
echo "  IMPORTANTE: Configurar API Keys"
echo "============================================"
echo ""
echo "Edita el archivo .env con tus API keys:"
echo "  nano ~/miapp-standalone-20251022-142042/backend/.env"
echo ""
echo "Configura al menos:"
echo "  - OPENAI_API_KEY o PERPLEXITY_API_KEY"
echo "  - MONGO_URL (MongoDB Atlas gratis)"
echo "  - WC_KEY y WC_SECRET (de WooCommerce)"
echo ""
echo "Luego ejecuta el backend con:"
echo "  cd ~/miapp-standalone-20251022-142042/backend"
echo "  source venv/bin/activate"
echo "  nohup uvicorn server:app --host 0.0.0.0 --port 8001 > ../logs/backend.log 2>&1 &"
echo ""
echo "============================================"
echo ""
