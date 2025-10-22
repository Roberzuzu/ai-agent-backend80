#!/bin/bash

# ============================================
# Script de Instalación Automática
# Backend AI Standalone para herramientasyaccesorios.store
# ============================================

set -e

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo "============================================"
echo "  Instalación Backend AI Standalone"
echo "  herramientasyaccesorios.store"
echo "============================================"
echo ""

# Verificar que estamos en el directorio correcto
if [ ! -f "backend/server.py" ]; then
    echo -e "${RED}✗${NC} Error: Ejecuta este script desde el directorio del proyecto"
    echo "  cd ~/miapp-standalone-*"
    echo "  ./install-herramientas.sh"
    exit 1
fi

PROJECT_DIR=$(pwd)
echo -e "${GREEN}✓${NC} Directorio del proyecto: $PROJECT_DIR"

# ============================================
# 1. Verificar Dependencias del Sistema
# ============================================

echo ""
echo "1. Verificando dependencias del sistema..."

if ! command -v python3 &> /dev/null; then
    echo -e "${RED}✗${NC} Python 3 no encontrado"
    echo "  Instalando Python 3.10..."
    sudo apt update
    sudo apt install -y python3.10 python3.10-venv python3-pip
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
echo -e "${GREEN}✓${NC} Python: $(python3 --version)"

if ! command -v node &> /dev/null; then
    echo -e "${YELLOW}!${NC} Node.js no encontrado. Instalando..."
    curl -fsSL https://deb.nodesource.com/setup_18.x | sudo bash -
    sudo apt install -y nodejs
fi

echo -e "${GREEN}✓${NC} Node.js: $(node --version)"
echo -e "${GREEN}✓${NC} npm: $(npm --version)"

# ============================================
# 2. Configurar Backend
# ============================================

echo ""
echo "2. Configurando Backend..."

cd "$PROJECT_DIR/backend"

# Crear .env si no existe
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}!${NC} Creando archivo .env..."
    cp .env.example .env
    
    # Generar SECRET_KEY
    SECRET_KEY=$(openssl rand -hex 32)
    sed -i "s/SECRET_KEY=.*/SECRET_KEY=$SECRET_KEY/" .env
    
    echo -e "${GREEN}✓${NC} Archivo .env creado"
    echo -e "${YELLOW}⚠${NC} IMPORTANTE: Edita backend/.env y configura tus API keys"
else
    echo -e "${GREEN}✓${NC} Archivo .env ya existe"
fi

# Crear entorno virtual
if [ ! -d "venv" ]; then
    echo "Creando entorno virtual..."
    python3 -m venv venv
fi

echo "Activando entorno virtual..."
source venv/bin/activate

# Instalar dependencias
echo "Instalando dependencias Python (puede tomar unos minutos)..."
pip install -q --upgrade pip
pip install -q -r requirements_standalone.txt

echo -e "${GREEN}✓${NC} Dependencias Python instaladas"

# ============================================
# 3. Configurar Frontend
# ============================================

echo ""
echo "3. Configurando Frontend..."

cd "$PROJECT_DIR/frontend"

# Crear .env si no existe
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}!${NC} Creando frontend/.env..."
    echo "REACT_APP_BACKEND_URL=http://localhost:8001/api" > .env
    echo -e "${GREEN}✓${NC} Frontend .env creado"
fi

# Instalar dependencias (opcional, comentado para ahorrar tiempo)
# echo "Instalando dependencias Node.js..."
# npm install --legacy-peer-deps

echo -e "${GREEN}✓${NC} Frontend configurado"

# ============================================
# 4. Crear Servicios Systemd
# ============================================

echo ""
echo "4. Configurando servicios systemd..."

# Backend service
sudo tee /etc/systemd/system/herramientas-backend.service > /dev/null <<EOF
[Unit]
Description=Herramientas AI Backend
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$PROJECT_DIR/backend
Environment="PATH=$PROJECT_DIR/backend/venv/bin"
ExecStart=$PROJECT_DIR/backend/venv/bin/uvicorn server:app --host 0.0.0.0 --port 8001
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

echo -e "${GREEN}✓${NC} Servicio backend creado"

# Telegram bot service
sudo tee /etc/systemd/system/herramientas-telegram.service > /dev/null <<EOF
[Unit]
Description=Herramientas Telegram Bot
After=network.target herramientas-backend.service

[Service]
Type=simple
User=$USER
WorkingDirectory=$PROJECT_DIR/backend
Environment="PATH=$PROJECT_DIR/backend/venv/bin"
ExecStart=$PROJECT_DIR/backend/venv/bin/python telegram_bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

echo -e "${GREEN}✓${NC} Servicio telegram bot creado"

# Recargar systemd
sudo systemctl daemon-reload

echo -e "${GREEN}✓${NC} Servicios systemd configurados"

# ============================================
# 5. Mostrar Instrucciones
# ============================================

echo ""
echo "============================================"
echo -e "  ${GREEN}✓ Instalación Completada${NC}"
echo "============================================"
echo ""
echo "📝 PRÓXIMOS PASOS:"
echo ""
echo "1. Configurar API Keys:"
echo "   nano $PROJECT_DIR/backend/.env"
echo ""
echo "   Configura al menos:"
echo "   - OPENAI_API_KEY o PERPLEXITY_API_KEY"
echo "   - MONGO_URL (MongoDB Atlas o local)"
echo "   - WC_KEY y WC_SECRET (de WooCommerce)"
echo ""
echo "2. Iniciar servicios:"
echo "   sudo systemctl start herramientas-backend"
echo "   sudo systemctl start herramientas-telegram"
echo ""
echo "3. Habilitar arranque automático:"
echo "   sudo systemctl enable herramientas-backend"
echo "   sudo systemctl enable herramientas-telegram"
echo ""
echo "4. Ver logs:"
echo "   sudo journalctl -u herramientas-backend -f"
echo ""
echo "5. Probar backend:"
echo "   http://herramientasyaccesorios.store:8001/docs"
echo ""
echo "============================================"
echo ""
echo "📖 Documentación completa:"
echo "   cat $PROJECT_DIR/DEPLOYMENT.md"
echo ""
echo "🆘 Soporte:"
echo "   - Ver logs: sudo journalctl -u herramientas-backend -n 50"
echo "   - Reiniciar: sudo systemctl restart herramientas-backend"
echo ""
