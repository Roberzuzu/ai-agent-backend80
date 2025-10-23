#!/bin/bash

echo "🔍 Verificando Configuración para Railway..."
echo ""

# Colores
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Contadores
errors=0
warnings=0

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "1. Verificando Archivos de Configuración..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Check Procfile
if [ -f "Procfile" ]; then
    echo -e "${GREEN}✓${NC} Procfile existe"
    if grep -q "cd backend" Procfile; then
        echo -e "${GREEN}✓${NC} Procfile contiene 'cd backend'"
    else
        echo -e "${RED}✗${NC} Procfile NO contiene 'cd backend'"
        errors=$((errors+1))
    fi
    if grep -q "\$PORT" Procfile; then
        echo -e "${GREEN}✓${NC} Procfile usa \$PORT"
    else
        echo -e "${RED}✗${NC} Procfile NO usa \$PORT"
        errors=$((errors+1))
    fi
else
    echo -e "${RED}✗${NC} Procfile NO existe"
    errors=$((errors+1))
fi

# Check railway.json
if [ -f "railway.json" ]; then
    echo -e "${GREEN}✓${NC} railway.json existe"
else
    echo -e "${YELLOW}⚠${NC} railway.json no existe (opcional)"
    warnings=$((warnings+1))
fi

# Check nixpacks.toml
if [ -f "nixpacks.toml" ]; then
    echo -e "${GREEN}✓${NC} nixpacks.toml existe"
else
    echo -e "${YELLOW}⚠${NC} nixpacks.toml no existe (opcional)"
    warnings=$((warnings+1))
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "2. Verificando Estructura del Backend..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Check backend directory
if [ -d "backend" ]; then
    echo -e "${GREEN}✓${NC} Directorio backend/ existe"
else
    echo -e "${RED}✗${NC} Directorio backend/ NO existe"
    errors=$((errors+1))
fi

# Check server.py
if [ -f "backend/server.py" ]; then
    echo -e "${GREEN}✓${NC} backend/server.py existe"
else
    echo -e "${RED}✗${NC} backend/server.py NO existe"
    errors=$((errors+1))
fi

# Check requirements
if [ -f "backend/requirements_standalone.txt" ]; then
    echo -e "${GREEN}✓${NC} backend/requirements_standalone.txt existe"
    echo "   Paquetes clave:"
    if grep -q "fastapi" backend/requirements_standalone.txt; then
        echo -e "   ${GREEN}✓${NC} fastapi"
    else
        echo -e "   ${RED}✗${NC} fastapi"
        errors=$((errors+1))
    fi
    if grep -q "uvicorn" backend/requirements_standalone.txt; then
        echo -e "   ${GREEN}✓${NC} uvicorn"
    else
        echo -e "   ${RED}✗${NC} uvicorn"
        errors=$((errors+1))
    fi
    if grep -q "motor" backend/requirements_standalone.txt; then
        echo -e "   ${GREEN}✓${NC} motor (MongoDB)"
    else
        echo -e "   ${RED}✗${NC} motor (MongoDB)"
        errors=$((errors+1))
    fi
else
    echo -e "${RED}✗${NC} backend/requirements_standalone.txt NO existe"
    errors=$((errors+1))
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "3. Verificando Variables de Entorno..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if [ -f "backend/.env" ]; then
    echo -e "${GREEN}✓${NC} backend/.env existe"
    echo "   Variables críticas:"
    
    # MONGO_URL
    if grep -q "MONGO_URL=" backend/.env && ! grep -q "MONGO_URL=$" backend/.env; then
        echo -e "   ${GREEN}✓${NC} MONGO_URL configurada"
    else
        echo -e "   ${YELLOW}⚠${NC} MONGO_URL no configurada o vacía"
        warnings=$((warnings+1))
    fi
    
    # DB_NAME
    if grep -q "DB_NAME=" backend/.env && ! grep -q "DB_NAME=$" backend/.env; then
        echo -e "   ${GREEN}✓${NC} DB_NAME configurada"
    else
        echo -e "   ${YELLOW}⚠${NC} DB_NAME no configurada o vacía"
        warnings=$((warnings+1))
    fi
    
    # SECRET_KEY
    if grep -q "SECRET_KEY=" backend/.env && ! grep -q "SECRET_KEY=$" backend/.env; then
        echo -e "   ${GREEN}✓${NC} SECRET_KEY configurada"
    else
        echo -e "   ${YELLOW}⚠${NC} SECRET_KEY no configurada o vacía"
        warnings=$((warnings+1))
    fi
    
    # OPENAI_API_KEY
    if grep -q "OPENAI_API_KEY=" backend/.env && ! grep -q "OPENAI_API_KEY=$" backend/.env; then
        echo -e "   ${GREEN}✓${NC} OPENAI_API_KEY configurada"
    else
        echo -e "   ${YELLOW}⚠${NC} OPENAI_API_KEY no configurada o vacía"
        warnings=$((warnings+1))
    fi
    
else
    echo -e "${YELLOW}⚠${NC} backend/.env no existe (normal en Railway, se configura en el dashboard)"
    echo "   Recuerda configurar las variables en Railway Dashboard → Variables"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "4. Verificando Estructura de Código..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Check for FastAPI app
if grep -q "app = FastAPI" backend/server.py; then
    echo -e "${GREEN}✓${NC} FastAPI app declarada correctamente"
else
    echo -e "${RED}✗${NC} FastAPI app no encontrada en server.py"
    errors=$((errors+1))
fi

# Check for /api prefix
if grep -q "prefix=\"/api\"" backend/server.py || grep -q 'prefix="/api"' backend/server.py; then
    echo -e "${GREEN}✓${NC} Router con prefijo /api configurado"
else
    echo -e "${YELLOW}⚠${NC} Router /api no encontrado (verificar manualmente)"
    warnings=$((warnings+1))
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📊 RESUMEN"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if [ $errors -eq 0 ] && [ $warnings -eq 0 ]; then
    echo -e "${GREEN}✅ ¡Todo perfecto! Listo para Railway${NC}"
    echo ""
    echo "Próximos pasos:"
    echo "1. Push a GitHub: git push origin main"
    echo "2. Ve a Railway: https://railway.app/new"
    echo "3. Deploy from GitHub repo"
    echo "4. Configura Root Directory: backend (sin /)"
    echo "5. Agrega variables de entorno"
    echo "6. ¡Listo! 🚀"
elif [ $errors -eq 0 ]; then
    echo -e "${YELLOW}⚠ Hay $warnings advertencias, pero está listo para Railway${NC}"
    echo ""
    echo "Las advertencias son menores y no bloquean el deployment."
    echo "Puedes proceder con el deployment en Railway."
else
    echo -e "${RED}❌ Hay $errors errores que deben corregirse${NC}"
    if [ $warnings -gt 0 ]; then
        echo -e "${YELLOW}⚠ Y $warnings advertencias${NC}"
    fi
    echo ""
    echo "Por favor, corrige los errores antes de deployar."
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📚 Documentación"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "• Quick Start: RAILWAY_QUICK_START.md"
echo "• Guía Completa: RAILWAY_DEPLOYMENT_GUIDE.md"
echo "• Railway Docs: https://docs.railway.app"
echo ""

exit $errors
