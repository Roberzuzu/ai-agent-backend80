#!/bin/bash

# ============================================
# Standalone Startup Script
# Ejecuta Backend + Telegram Bot sin Supervisor
# ============================================

set -e

echo "===================================="
echo "  Iniciando Aplicación Autónoma"
echo "===================================="

# Colores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Directorio base
BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND_DIR="$BASE_DIR/backend"
FRONTEND_DIR="$BASE_DIR/frontend"

echo -e "${GREEN}✓${NC} Directorio base: $BASE_DIR"

# Verificar Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}✗${NC} Python 3 no encontrado. Instala Python 3.10+"
    exit 1
fi

echo -e "${GREEN}✓${NC} Python encontrado: $(python3 --version)"

# Verificar MongoDB
if ! command -v mongod &> /dev/null; then
    echo -e "${YELLOW}!${NC} MongoDB no encontrado localmente. Asegúrate de tener MONGO_URL configurado en .env"
else
    echo -e "${GREEN}✓${NC} MongoDB encontrado"
fi

# Crear directorios de logs
mkdir -p "$BASE_DIR/logs"

echo ""
echo "===================================="
echo "  Instalando Dependencias"
echo "===================================="

# Backend Dependencies
cd "$BACKEND_DIR"

if [ ! -d "venv" ]; then
    echo -e "${YELLOW}!${NC} Creando entorno virtual..."
    python3 -m venv venv
fi

source venv/bin/activate

echo -e "${GREEN}✓${NC} Instalando dependencias del backend..."
pip install -q -r requirements_standalone.txt

echo ""
echo "===================================="
echo "  Configurando Variables de Entorno"
echo "===================================="

# Verificar .env
if [ ! -f "$BACKEND_DIR/.env" ]; then
    echo -e "${RED}✗${NC} Archivo .env no encontrado en $BACKEND_DIR"
    echo "Crea el archivo .env con las siguientes variables:"
    echo ""
    echo "MONGO_URL=mongodb://localhost:27017"
    echo "DB_NAME=social_media_monetization"
    echo "OPENAI_API_KEY=tu-api-key"
    echo "PERPLEXITY_API_KEY=tu-api-key"
    echo "STRIPE_API_KEY=tu-api-key"
    echo "TELEGRAM_BOT_TOKEN=tu-token"
    echo "SECRET_KEY=tu-secret-key"
    exit 1
fi

echo -e "${GREEN}✓${NC} Archivo .env encontrado"

# Load .env
export $(cat "$BACKEND_DIR/.env" | grep -v '^#' | xargs)

echo ""
echo "===================================="
echo "  Iniciando Servicios"
echo "===================================="

# Función para manejar Ctrl+C
cleanup() {
    echo ""
    echo -e "${YELLOW}!${NC} Deteniendo servicios..."
    kill $BACKEND_PID $TELEGRAM_PID 2>/dev/null
    echo -e "${GREEN}✓${NC} Servicios detenidos"
    exit 0
}

trap cleanup SIGINT SIGTERM

# Iniciar Backend
echo -e "${GREEN}✓${NC} Iniciando Backend en puerto 8001..."
cd "$BACKEND_DIR"
uvicorn server:app --host 0.0.0.0 --port 8001 --reload > "$BASE_DIR/logs/backend.log" 2>&1 &
BACKEND_PID=$!
echo -e "${GREEN}✓${NC} Backend PID: $BACKEND_PID"

# Esperar a que el backend esté listo
echo "Esperando a que el backend esté listo..."
for i in {1..30}; do
    if curl -s http://localhost:8001/api/health > /dev/null 2>&1 || \
       curl -s http://localhost:8001 > /dev/null 2>&1; then
        echo -e "${GREEN}✓${NC} Backend listo"
        break
    fi
    sleep 1
done

# Iniciar Telegram Bot
echo -e "${GREEN}✓${NC} Iniciando Telegram Bot..."
cd "$BACKEND_DIR"
python3 telegram_bot.py > "$BASE_DIR/logs/telegram.log" 2>&1 &
TELEGRAM_PID=$!
echo -e "${GREEN}✓${NC} Telegram Bot PID: $TELEGRAM_PID"

echo ""
echo "===================================="
echo -e "  ${GREEN}✓ Aplicación Iniciada${NC}"
echo "===================================="
echo ""
echo "Backend:       http://localhost:8001"
echo "API Docs:      http://localhost:8001/docs"
echo "Telegram Bot:  Activo"
echo ""
echo "Logs:"
echo "  Backend:     tail -f $BASE_DIR/logs/backend.log"
echo "  Telegram:    tail -f $BASE_DIR/logs/telegram.log"
echo ""
echo -e "${YELLOW}Presiona Ctrl+C para detener${NC}"
echo ""

# Mantener el script corriendo y mostrar logs
tail -f "$BASE_DIR/logs/backend.log" "$BASE_DIR/logs/telegram.log"
