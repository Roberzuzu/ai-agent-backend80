#!/bin/bash

# ============================================
# Script de Instalación de Dependencias
# Para Ubuntu/Debian
# ============================================

set -e

echo "===================================="
echo "  Instalando Dependencias del Sistema"
echo "===================================="

# Colores
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Verificar sudo
if [ "$EUID" -ne 0 ]; then 
    echo -e "${YELLOW}!${NC} Este script necesita permisos de sudo"
    exit 1
fi

# Actualizar sistema
echo -e "${GREEN}✓${NC} Actualizando sistema..."
apt update -y
apt upgrade -y

# Python 3.10+
echo -e "${GREEN}✓${NC} Instalando Python 3.10..."
apt install -y python3.10 python3.10-venv python3-pip

# Node.js (para frontend)
echo -e "${GREEN}✓${NC} Instalando Node.js..."
curl -fsSL https://deb.nodesource.com/setup_18.x | bash -
apt install -y nodejs

# MongoDB (opcional - puedes usar MongoDB Atlas)
read -p "¿Instalar MongoDB localmente? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${GREEN}✓${NC} Instalando MongoDB..."
    wget -qO - https://www.mongodb.org/static/pgp/server-7.0.asc | apt-key add -
    echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/7.0 multiverse" | tee /etc/apt/sources.list.d/mongodb-org-7.0.list
    apt update -y
    apt install -y mongodb-org
    
    systemctl enable mongod
    systemctl start mongod
    echo -e "${GREEN}✓${NC} MongoDB instalado y en ejecución"
fi

# Nginx (opcional)
read -p "¿Instalar Nginx? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${GREEN}✓${NC} Instalando Nginx..."
    apt install -y nginx
    systemctl enable nginx
    systemctl start nginx
    echo -e "${GREEN}✓${NC} Nginx instalado"
fi

# Git
apt install -y git curl wget

echo ""
echo "===================================="
echo -e "  ${GREEN}✓ Instalación Completa${NC}"
echo "===================================="
echo ""
echo "Versiones instaladas:"
echo "  Python:  $(python3 --version)"
echo "  Node.js: $(node --version)"
echo "  npm:     $(npm --version)"

if command -v mongod &> /dev/null; then
    echo "  MongoDB: $(mongod --version | head -n 1)"
fi

echo ""
echo "Próximos pasos:"
echo "1. Configura el archivo backend/.env"
echo "2. Ejecuta: ./start_standalone.sh"
echo ""
