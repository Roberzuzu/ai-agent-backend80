#!/bin/bash

# ============================================
# SCRIPT DE DIAGNÓSTICO - CEREBRO AI EN RENDER
# ============================================
# Este script verifica que todo esté funcionando correctamente
# Uso: bash diagnostico.sh https://TU-URL.onrender.com
# ============================================

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # Sin color

# Función para imprimir con color
print_status() {
    local status=$1
    local message=$2
    
    if [ "$status" == "OK" ]; then
        echo -e "${GREEN}✅ $message${NC}"
    elif [ "$status" == "FAIL" ]; then
        echo -e "${RED}❌ $message${NC}"
    elif [ "$status" == "WARN" ]; then
        echo -e "${YELLOW}⚠️  $message${NC}"
    elif [ "$status" == "INFO" ]; then
        echo -e "${BLUE}ℹ️  $message${NC}"
    fi
}

# Verificar argumento
if [ -z "$1" ]; then
    print_status "FAIL" "Debes proporcionar la URL del backend"
    echo ""
    echo "Uso:"
    echo "  bash diagnostico.sh https://cerebro-ai-backend.onrender.com"
    echo ""
    exit 1
fi

BACKEND_URL=$1

# Eliminar barra final si existe
BACKEND_URL=$(echo "$BACKEND_URL" | sed 's:/*$::')

echo ""
echo "============================================"
echo "🧠 CEREBRO AI - DIAGNÓSTICO COMPLETO"
echo "============================================"
echo ""
print_status "INFO" "Backend URL: $BACKEND_URL"
echo ""

# ============================================
# TEST 1: CONECTIVIDAD BÁSICA
# ============================================
echo "🔍 Test 1: Conectividad Básica"
echo "--------------------------------------------"

if curl -s --head "$BACKEND_URL" | head -n 1 | grep "HTTP" > /dev/null; then
    print_status "OK" "Backend responde a requests HTTP"
else
    print_status "FAIL" "Backend no responde - Verifica que esté en estado 'Live' en Render"
    exit 1
fi

# ============================================
# TEST 2: HEALTH CHECK
# ============================================
echo ""
echo "🏥 Test 2: Health Check"
echo "--------------------------------------------"

HEALTH_RESPONSE=$(curl -s "${BACKEND_URL}/api/health")

if [ -z "$HEALTH_RESPONSE" ]; then
    print_status "FAIL" "Endpoint /api/health no responde"
    print_status "INFO" "Verifica que el servidor esté arrancado correctamente"
    exit 1
fi

# Verificar status
if echo "$HEALTH_RESPONSE" | grep -q '"status":"healthy"' || echo "$HEALTH_RESPONSE" | grep -q '"status": "healthy"'; then
    print_status "OK" "Status: healthy"
else
    print_status "FAIL" "Status no es healthy"
    echo "Respuesta: $HEALTH_RESPONSE"
fi

# Verificar database
if echo "$HEALTH_RESPONSE" | grep -q '"database":"connected"' || echo "$HEALTH_RESPONSE" | grep -q '"database": "connected"'; then
    print_status "OK" "Database: connected"
else
    print_status "FAIL" "Database no conectada - Verifica MONGO_URL en variables de Render"
fi

# ============================================
# TEST 3: STATUS DEL AGENTE
# ============================================
echo ""
echo "🤖 Test 3: Status del Agente AI"
echo "--------------------------------------------"

AGENT_STATUS=$(curl -s -X POST "${BACKEND_URL}/api/agent/status" \
    -H "Content-Type: application/json")

if [ -z "$AGENT_STATUS" ]; then
    print_status "FAIL" "Endpoint /api/agent/status no responde"
    exit 1
fi

# Verificar success
if echo "$AGENT_STATUS" | grep -q '"success":true' || echo "$AGENT_STATUS" | grep -q '"success": true'; then
    print_status "OK" "Agente AI activo"
else
    print_status "FAIL" "Agente AI no está activo"
    echo "Respuesta: $AGENT_STATUS"
    exit 1
fi

# Verificar herramientas
TOOLS_COUNT=$(echo "$AGENT_STATUS" | grep -o '"herramientas_disponibles":[0-9]*' | grep -o '[0-9]*' | head -1)

if [ -z "$TOOLS_COUNT" ]; then
    TOOLS_COUNT=$(echo "$AGENT_STATUS" | grep -o '"herramientas_disponibles": [0-9]*' | grep -o '[0-9]*' | head -1)
fi

if [ "$TOOLS_COUNT" -eq 18 ]; then
    print_status "OK" "Herramientas disponibles: 18/18"
else
    print_status "WARN" "Herramientas disponibles: $TOOLS_COUNT/18"
fi

# Verificar memoria persistente
if echo "$AGENT_STATUS" | grep -q '"memoria_persistente":true' || echo "$AGENT_STATUS" | grep -q '"memoria_persistente": true'; then
    print_status "OK" "Memoria persistente: activada"
else
    print_status "WARN" "Memoria persistente: no activada"
fi

# Verificar RAG
if echo "$AGENT_STATUS" | grep -q '"rag_enabled":true' || echo "$AGENT_STATUS" | grep -q '"rag_enabled": true'; then
    print_status "OK" "RAG (búsqueda semántica): activado"
else
    print_status "WARN" "RAG: no activado"
fi

# ============================================
# TEST 4: COMANDO DE PRUEBA
# ============================================
echo ""
echo "💬 Test 4: Ejecución de Comando"
echo "--------------------------------------------"

print_status "INFO" "Enviando comando de prueba..."

COMMAND_RESPONSE=$(curl -s -X POST "${BACKEND_URL}/api/agent/execute" \
    -H "Content-Type: application/json" \
    -d '{"command":"Test de diagnóstico","user_id":"diagnostic_test"}' \
    --max-time 30)

if [ -z "$COMMAND_RESPONSE" ]; then
    print_status "FAIL" "No se recibió respuesta del comando"
    print_status "INFO" "El servidor puede estar procesando lentamente"
else
    if echo "$COMMAND_RESPONSE" | grep -q '"success":true' || echo "$COMMAND_RESPONSE" | grep -q '"success": true'; then
        print_status "OK" "Comando ejecutado correctamente"
    else
        print_status "FAIL" "Comando falló"
        echo "Respuesta: $COMMAND_RESPONSE"
    fi
fi

# ============================================
# TEST 5: TIEMPOS DE RESPUESTA
# ============================================
echo ""
echo "⏱️  Test 5: Tiempos de Respuesta"
echo "--------------------------------------------"

# Health Check
START=$(date +%s%N)
curl -s "${BACKEND_URL}/api/health" > /dev/null
END=$(date +%s%N)
HEALTH_TIME=$(( ($END - $START) / 1000000 ))

if [ $HEALTH_TIME -lt 1000 ]; then
    print_status "OK" "Health check: ${HEALTH_TIME}ms (excelente)"
elif [ $HEALTH_TIME -lt 3000 ]; then
    print_status "OK" "Health check: ${HEALTH_TIME}ms (bueno)"
else
    print_status "WARN" "Health check: ${HEALTH_TIME}ms (lento)"
fi

# Agent Status
START=$(date +%s%N)
curl -s -X POST "${BACKEND_URL}/api/agent/status" \
    -H "Content-Type: application/json" > /dev/null
END=$(date +%s%N)
AGENT_TIME=$(( ($END - $START) / 1000000 ))

if [ $AGENT_TIME -lt 2000 ]; then
    print_status "OK" "Agent status: ${AGENT_TIME}ms (excelente)"
elif [ $AGENT_TIME -lt 5000 ]; then
    print_status "OK" "Agent status: ${AGENT_TIME}ms (bueno)"
else
    print_status "WARN" "Agent status: ${AGENT_TIME}ms (lento)"
fi

# ============================================
# TEST 6: VERIFICAR VARIABLES DE ENTORNO
# ============================================
echo ""
echo "🔐 Test 6: Verificación de Configuración"
echo "--------------------------------------------"

print_status "INFO" "Verificando configuración del servidor..."

# Intentar endpoint que puede revelar si faltan configs
CONFIG_CHECK=$(curl -s "${BACKEND_URL}/api/health" 2>&1)

if echo "$CONFIG_CHECK" | grep -q "database.*connected"; then
    print_status "OK" "MongoDB configurado correctamente"
else
    print_status "WARN" "Posible problema con MongoDB - Verifica MONGO_URL"
fi

# ============================================
# TEST 7: CORS Y HEADERS
# ============================================
echo ""
echo "🌐 Test 7: CORS y Headers de Seguridad"
echo "--------------------------------------------"

HEADERS=$(curl -s -I "${BACKEND_URL}/api/health")

if echo "$HEADERS" | grep -qi "access-control-allow-origin"; then
    print_status "OK" "CORS configurado"
else
    print_status "WARN" "CORS puede no estar configurado"
fi

if echo "$HEADERS" | grep -qi "content-type.*json"; then
    print_status "OK" "Content-Type JSON configurado"
fi

# ============================================
# TEST 8: HTTPS
# ============================================
echo ""
echo "🔒 Test 8: Seguridad HTTPS"
echo "--------------------------------------------"

if echo "$BACKEND_URL" | grep -q "https://"; then
    print_status "OK" "HTTPS activado (Render lo hace automáticamente)"
else
    print_status "WARN" "No estás usando HTTPS - Cambia a https://"
fi

# ============================================
# RESUMEN FINAL
# ============================================
echo ""
echo "============================================"
echo "📊 RESUMEN DE DIAGNÓSTICO"
echo "============================================"
echo ""

# Contar tests pasados
TESTS_PASSED=0
TESTS_TOTAL=8

# Evaluar cada test (simplificado)
echo "$HEALTH_RESPONSE" | grep -q '"status":"healthy"' && ((TESTS_PASSED++))
echo "$AGENT_STATUS" | grep -q '"success":true' && ((TESTS_PASSED++))
[ "$TOOLS_COUNT" -eq 18 ] && ((TESTS_PASSED++))

PERCENTAGE=$(( TESTS_PASSED * 100 / TESTS_TOTAL ))

if [ $PERCENTAGE -ge 80 ]; then
    print_status "OK" "Sistema funcionando correctamente: ${PERCENTAGE}%"
    echo ""
    print_status "INFO" "Tu backend está listo para producción ✅"
elif [ $PERCENTAGE -ge 50 ]; then
    print_status "WARN" "Sistema funcionando parcialmente: ${PERCENTAGE}%"
    echo ""
    print_status "INFO" "Revisa las advertencias arriba"
else
    print_status "FAIL" "Sistema con problemas críticos: ${PERCENTAGE}%"
    echo ""
    print_status "INFO" "Revisa los errores arriba y las variables de entorno en Render"
fi

echo ""
echo "============================================"
echo "🔗 ENLACES ÚTILES"
echo "============================================"
echo ""
echo "• Logs de Render:"
echo "  https://dashboard.render.com/web/srv-d3tot4muk2gs73dbhid0/logs"
echo ""
echo "• Variables de entorno:"
echo "  https://dashboard.render.com/web/srv-d3tot4muk2gs73dbhid0/env"
echo ""
echo "• Métricas:"
echo "  https://dashboard.render.com/web/srv-d3tot4muk2gs73dbhid0/metrics"
echo ""
echo "• MongoDB Atlas:"
echo "  https://cloud.mongodb.com"
echo ""

# ============================================
# RECOMENDACIONES
# ============================================
echo "============================================"
echo "💡 RECOMENDACIONES"
echo "============================================"
echo ""

# Plan de Render
print_status "INFO" "Plan actual de Render:"
echo "  • Si ves 'Sleep después de 15 min' → Actualiza a Starter (\$7/mes)"
echo "  • Si necesitas más recursos → Actualiza a Standard (\$25/mes)"
echo ""

# Monitoring
print_status "INFO" "Monitoring:"
echo "  • Configura UptimeRobot para ping cada 5 min (evita sleep en plan gratis)"
echo "  • Revisa logs regularmente para detectar errores"
echo "  • Configura Sentry para tracking de errores (opcional)"
echo ""

# Backups
print_status "INFO" "Backups:"
echo "  • MongoDB Atlas hace backups automáticos en plan M2+"
echo "  • En plan Free (M0), considera exportar datos manualmente"
echo ""

echo "============================================"
echo "✅ DIAGNÓSTICO COMPLETADO"
echo "============================================"
echo ""
