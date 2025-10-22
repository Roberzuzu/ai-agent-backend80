#!/bin/bash

# ============================================
# Servidor HTTP Simple para Descargar Paquete
# ============================================

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Buscar el archivo .zip más reciente
ZIP_FILE=$(ls -t /app/miapp-standalone-*.zip 2>/dev/null | head -1)

if [ -z "$ZIP_FILE" ]; then
    echo -e "${RED}✗${NC} No se encontró paquete .zip"
    echo "Ejecuta primero: ./create_mobile_package.sh"
    exit 1
fi

echo "=========================================="
echo "  Servidor de Descarga Móvil"
echo "=========================================="
echo ""
echo -e "${GREEN}✓${NC} Archivo: $(basename $ZIP_FILE)"
echo -e "${GREEN}✓${NC} Tamaño: $(du -h $ZIP_FILE | cut -f1)"
echo ""

# Obtener IP del servidor
SERVER_IP=$(hostname -I | awk '{print $1}')

echo "=========================================="
echo "  Cómo Descargar desde tu Móvil"
echo "=========================================="
echo ""
echo "1. Asegúrate de estar en la misma red o tener acceso al servidor"
echo ""
echo "2. Abre el navegador en tu móvil y visita:"
echo ""
echo -e "   ${GREEN}http://$SERVER_IP:8080/$(basename $ZIP_FILE)${NC}"
echo ""
echo "3. O desde terminal móvil (Termux):"
echo ""
echo "   wget http://$SERVER_IP:8080/$(basename $ZIP_FILE)"
echo ""
echo "=========================================="
echo ""
echo -e "${YELLOW}⚠️  IMPORTANTE:${NC}"
echo "- Este servidor es temporal y para descarga única"
echo "- Presiona Ctrl+C cuando termines de descargar"
echo "- No dejes este servidor corriendo por seguridad"
echo ""
echo "=========================================="
echo "  Iniciando servidor..."
echo "=========================================="
echo ""

# Iniciar servidor HTTP
cd /app
python3 -m http.server 8080
