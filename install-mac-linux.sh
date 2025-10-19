#!/bin/bash
# ====================================
# INSTALADOR AUTOMATICO - macOS/Linux
# Sistema de Dropshipping con IA
# ====================================

set -e  # Exit on error

echo ""
echo "========================================"
echo "  INSTALADOR AUTOMATICO"
echo "  Sistema de Dropshipping con IA"
echo "========================================"
echo ""

# Verificar Python
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python 3 no esta instalado"
    echo "Por favor instala Python 3.11+ desde https://www.python.org"
    exit 1
fi

# Verificar Node.js
if ! command -v node &> /dev/null; then
    echo "[ERROR] Node.js no esta instalado"
    echo "Por favor instala Node.js 18+ desde https://nodejs.org"
    exit 1
fi

# Verificar MongoDB (opcional)
if ! command -v mongod &> /dev/null; then
    echo "[ADVERTENCIA] MongoDB no detectado"
    echo "Puedes instalarlo con:"
    echo "  macOS: brew install mongodb-community"
    echo "  Ubuntu: sudo apt install mongodb"
    echo "O usar Docker (recomendado)"
fi

echo ""
echo "[1/5] Configurando variables de entorno..."
if [ ! -f .env ]; then
    if [ -f .env.example ]; then
        cp .env.example .env
        echo "[OK] Archivo .env creado desde .env.example"
        echo ""
        echo "IMPORTANTE: Edita el archivo .env con tus credenciales"
        echo "  nano .env    # o usa tu editor preferido"
        echo ""
        read -p "Presiona Enter cuando hayas editado .env..."
    else
        echo "[ERROR] No se encuentra .env.example"
        exit 1
    fi
else
    echo "[OK] Archivo .env ya existe"
fi

echo ""
echo "[2/5] Instalando dependencias del Backend..."
cd backend
python3 -m pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "[ERROR] Fallo al instalar dependencias del backend"
    exit 1
fi
echo "[OK] Backend instalado correctamente"
cd ..

echo ""
echo "[3/5] Instalando dependencias del Frontend..."
cd frontend

# Detectar si tiene yarn o npm
if command -v yarn &> /dev/null; then
    echo "Usando yarn..."
    yarn install
else
    echo "Usando npm..."
    npm install
fi

if [ $? -ne 0 ]; then
    echo "[ERROR] Fallo al instalar dependencias del frontend"
    exit 1
fi
echo "[OK] Frontend instalado correctamente"
cd ..

echo ""
echo "[4/5] Creando directorios necesarios..."
mkdir -p data/db
mkdir -p backups
mkdir -p logs
echo "[OK] Directorios creados"

echo ""
echo "[5/5] Inicializando base de datos..."
cd backend
python3 init_db.py || echo "[ADVERTENCIA] No se pudo inicializar la BD. Asegurate de que MongoDB este corriendo"
cd ..

echo ""
echo "========================================"
echo "  INSTALACION COMPLETADA!"
echo "========================================"
echo ""
echo "Para iniciar el sistema:"
echo ""
echo "  Opcion 1 - Docker (Recomendado):"
echo "  docker-compose up -d"
echo ""
echo "  Opcion 2 - Manual:"
echo "  1. Terminal 1: mongod --dbpath ./data/db"
echo "  2. Terminal 2: cd backend && python3 -m uvicorn server:app --reload"
echo "  3. Terminal 3: cd frontend && npm start"
echo ""
echo "Accede a:"
echo "  - Frontend: http://localhost:3000"
echo "  - Backend:  http://localhost:8001/api"
echo "  - Docs:     http://localhost:8001/docs"
echo ""
echo "========================================"
echo ""
