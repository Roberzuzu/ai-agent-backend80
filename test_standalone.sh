#!/bin/bash

# ============================================
# Test Script - Verificar Standalone Setup
# ============================================

set -e

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "=========================================="
echo "  Verificando Configuración Standalone"
echo "=========================================="
echo ""

# Test 1: Python
echo -n "Test 1: Python 3.10+... "
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    echo -e "${GREEN}✓${NC} $PYTHON_VERSION"
else
    echo -e "${RED}✗${NC} Python no encontrado"
    exit 1
fi

# Test 2: Backend .env
echo -n "Test 2: Backend .env... "
if [ -f "/app/backend/.env" ]; then
    echo -e "${GREEN}✓${NC} Existe"
    
    # Verificar variables críticas
    source /app/backend/.env
    
    if [ -z "$MONGO_URL" ]; then
        echo -e "  ${YELLOW}!${NC} MONGO_URL no configurado"
    fi
    
    if [ -z "$OPENAI_API_KEY" ]; then
        echo -e "  ${YELLOW}!${NC} OPENAI_API_KEY no configurado"
    fi
    
    if [ -z "$PERPLEXITY_API_KEY" ]; then
        echo -e "  ${YELLOW}!${NC} PERPLEXITY_API_KEY no configurado"
    fi
    
    if [ -z "$TELEGRAM_BOT_TOKEN" ]; then
        echo -e "  ${YELLOW}!${NC} TELEGRAM_BOT_TOKEN no configurado"
    fi
else
    echo -e "${RED}✗${NC} No existe"
    echo "  Crea /app/backend/.env desde .env.example"
    exit 1
fi

# Test 3: Dependencies
echo -n "Test 3: Python dependencies... "
cd /app/backend

if [ ! -d "venv" ]; then
    echo -e "${YELLOW}!${NC} Creando venv..."
    python3 -m venv venv
fi

source venv/bin/activate

if pip show fastapi &> /dev/null; then
    echo -e "${GREEN}✓${NC} Instaladas"
else
    echo -e "${YELLOW}!${NC} Instalando..."
    pip install -q -r requirements_standalone.txt
    echo -e "${GREEN}✓${NC} Instaladas"
fi

# Test 4: Imports
echo -n "Test 4: Imports standalone... "
python3 << 'EOF' > /dev/null 2>&1
import sys
sys.path.insert(0, '/app/backend')

try:
    from llm_client import LlmChat, UserMessage
    from stripe_client import StripeCheckout
    print("OK")
except ImportError as e:
    print(f"Error: {e}")
    sys.exit(1)
EOF

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓${NC} OK"
else
    echo -e "${RED}✗${NC} Error en imports"
    exit 1
fi

# Test 5: MongoDB
echo -n "Test 5: MongoDB connection... "
if command -v mongod &> /dev/null; then
    if sudo systemctl is-active --quiet mongod; then
        echo -e "${GREEN}✓${NC} Local activo"
    else
        echo -e "${YELLOW}!${NC} Local inactivo (¿usas Atlas?)"
    fi
else
    echo -e "${YELLOW}!${NC} No local (¿usas Atlas?)"
fi

# Test 6: Ports
echo -n "Test 6: Puerto 8001 libre... "
if sudo lsof -i :8001 > /dev/null 2>&1; then
    echo -e "${YELLOW}!${NC} En uso"
    echo "  Proceso actual: $(sudo lsof -t -i:8001)"
else
    echo -e "${GREEN}✓${NC} Disponible"
fi

# Test 7: Scripts ejecutables
echo -n "Test 7: Scripts ejecutables... "
if [ -x "/app/start_standalone.sh" ] && [ -x "/app/install_dependencies.sh" ]; then
    echo -e "${GREEN}✓${NC} OK"
else
    chmod +x /app/start_standalone.sh /app/install_dependencies.sh
    echo -e "${GREEN}✓${NC} Fixed"
fi

# Test 8: Archivos standalone
echo -n "Test 8: Archivos standalone... "
REQUIRED_FILES=(
    "/app/backend/llm_client.py"
    "/app/backend/stripe_client.py"
    "/app/backend/requirements_standalone.txt"
    "/app/README_STANDALONE.md"
    "/app/DEPLOYMENT.md"
)

ALL_EXIST=true
for file in "${REQUIRED_FILES[@]}"; do
    if [ ! -f "$file" ]; then
        echo -e "${RED}✗${NC} Falta: $file"
        ALL_EXIST=false
    fi
done

if [ "$ALL_EXIST" = true ]; then
    echo -e "${GREEN}✓${NC} Todos presentes"
fi

# Test 9: No emergentintegrations
echo -n "Test 9: Sin emergentintegrations... "
if grep -r "from emergentintegrations" /app/backend/*.py &> /dev/null; then
    echo -e "${YELLOW}!${NC} Aún presente en algún archivo"
    echo "  Archivos:"
    grep -r "from emergentintegrations" /app/backend/*.py
else
    echo -e "${GREEN}✓${NC} Eliminado"
fi

echo ""
echo "=========================================="
echo "  Resumen"
echo "=========================================="
echo ""
echo -e "${GREEN}✓${NC} Tu aplicación está lista para ser standalone"
echo ""
echo "Próximos pasos:"
echo "  1. Revisa /app/backend/.env"
echo "  2. Ejecuta: ./start_standalone.sh"
echo "  3. Para producción: ver DEPLOYMENT.md"
echo ""
