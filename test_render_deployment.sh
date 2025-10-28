#!/bin/bash

# Script de prueba para verificar todos los endpoints del backend en Render
# Uso: ./test_render_deployment.sh

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# URL del backend en Render
BACKEND_URL="https://ai-agent-backend80.onrender.com"

echo ""
echo "=========================================="
echo "🔍 PRUEBA DE ENDPOINTS - RENDER DEPLOY"
echo "=========================================="
echo "Backend URL: $BACKEND_URL"
echo ""

# Función para probar endpoint
test_endpoint() {
    local method=$1
    local endpoint=$2
    local description=$3
    
    echo -n "Testing $method $endpoint ... "
    
    response=$(curl -s -w "\n%{http_code}" -X $method "$BACKEND_URL$endpoint" -H "Content-Type: application/json")
    http_code=$(echo "$response" | tail -n 1)
    body=$(echo "$response" | head -n -1)
    
    if [ "$http_code" = "200" ]; then
        echo -e "${GREEN}✅ OK${NC} (HTTP $http_code)"
        if [ ! -z "$body" ]; then
            echo "$body" | jq '.' 2>/dev/null || echo "$body"
        fi
    elif [ "$http_code" = "404" ]; then
        echo -e "${RED}❌ NOT FOUND${NC} (HTTP $http_code)"
    elif [ "$http_code" = "500" ]; then
        echo -e "${RED}❌ SERVER ERROR${NC} (HTTP $http_code)"
        echo "$body"
    else
        echo -e "${YELLOW}⚠️  UNEXPECTED${NC} (HTTP $http_code)"
        echo "$body"
    fi
    echo ""
}

# Test 1: Root endpoint
echo -e "${BLUE}📋 Test 1: Root Endpoint${NC}"
test_endpoint "GET" "/" "Root service info"

# Test 2: Health check (original)
echo -e "${BLUE}📋 Test 2: Health Check (Original)${NC}"
test_endpoint "GET" "/api/health" "Health check endpoint"

# Test 3: Status Simple (NEW)
echo -e "${BLUE}📋 Test 3: Status Simple (NEW)${NC}"
test_endpoint "GET" "/api/status/simple" "Simple status without DB"

# Test 4: Status Detailed (NEW)
echo -e "${BLUE}📋 Test 4: Status Detailed (NEW)${NC}"
test_endpoint "GET" "/api/status/detailed" "Detailed status with service tests"

# Test 5: Agent Status (IMPROVED)
echo -e "${BLUE}📋 Test 5: Agent Status (IMPROVED)${NC}"
test_endpoint "GET" "/api/agent/status" "Agent status with MongoDB"

# Test 6: AI Health Check
echo -e "${BLUE}📋 Test 6: AI Health Check${NC}"
test_endpoint "GET" "/api/ai/health" "AI APIs configuration"

# Test 7: Products endpoint
echo -e "${BLUE}📋 Test 7: Products Endpoint${NC}"
test_endpoint "GET" "/api/products" "Get all products"

# Test 8: Trends endpoint
echo -e "${BLUE}📋 Test 8: Trends Endpoint${NC}"
test_endpoint "GET" "/api/trends" "Get all trends"

# Test 9: OpenAPI docs
echo -e "${BLUE}📋 Test 9: Swagger Documentation${NC}"
echo -n "Testing GET /docs ... "
response=$(curl -s -w "%{http_code}" "$BACKEND_URL/docs" -o /dev/null)
if [ "$response" = "200" ]; then
    echo -e "${GREEN}✅ OK${NC} (HTTP $response)"
    echo "Swagger UI is accessible at: $BACKEND_URL/docs"
else
    echo -e "${RED}❌ FAILED${NC} (HTTP $response)"
fi
echo ""

# Test 10: OpenAPI JSON
echo -e "${BLUE}📋 Test 10: OpenAPI Specification${NC}"
test_endpoint "GET" "/openapi.json" "OpenAPI spec"

echo ""
echo "=========================================="
echo "📊 RESUMEN DE PRUEBAS"
echo "=========================================="
echo ""
echo "Si ves endpoints con 404, puede ser que:"
echo "1. El router no está incluido correctamente"
echo "2. El servidor necesita reiniciarse"
echo "3. Las rutas tienen un prefijo diferente"
echo ""
echo "Si ves 500 errors, revisa los logs en Render:"
echo "   Dashboard > Tu servicio > Logs"
echo ""
echo "Para más información, consulta:"
echo "   /app/DIAGNOSTIC_RENDER.md"
echo ""
