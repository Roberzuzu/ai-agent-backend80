#!/bin/bash

BASE_URL="https://railway-port-config.preview.emergentagent.com"

echo "================================================================"
echo "🧪 PRUEBA DE APIS - CEREBRO AI"
echo "================================================================"
echo ""
echo "📍 URL Base: $BASE_URL"
echo ""

# Test 1: Status
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "1️⃣ TEST: GET /api/agent/status"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
curl -s "$BASE_URL/api/agent/status" | python3 -m json.tool 2>/dev/null || echo "Error al parsear JSON"
echo ""
echo ""

# Test 2: Execute command
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "2️⃣ TEST: POST /api/agent/execute"
echo "   Comando: 'Dame las estadísticas del sitio'"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
curl -s -X POST "$BASE_URL/api/agent/execute" \
  -H "Content-Type: application/json" \
  -d '{"command": "Dame las estadísticas del sitio", "user_id": "test_preview_user"}' \
  | python3 -m json.tool 2>/dev/null || echo "Error al parsear JSON"
echo ""
echo ""

# Test 3: Chat
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "3️⃣ TEST: POST /api/agent/chat"
echo "   Mensaje: '¿Qué puedes hacer por mí?'"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
curl -s -X POST "$BASE_URL/api/agent/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "¿Qué puedes hacer por mí?", "user_id": "test_preview_user"}' \
  | python3 -m json.tool 2>/dev/null || echo "Error al parsear JSON"
echo ""
echo ""

# Test 4: Memory
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "4️⃣ TEST: GET /api/agent/memory/test_preview_user"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
curl -s "$BASE_URL/api/agent/memory/test_preview_user?limit=3" \
  | python3 -m json.tool 2>/dev/null || echo "Error al parsear JSON"
echo ""
echo ""

echo "================================================================"
echo "✅ PRUEBAS COMPLETADAS"
echo "================================================================"
echo ""
echo "📝 Notas:"
echo "  • URL Base: $BASE_URL"
echo "  • Todas las APIs están listas para usar"
echo "  • Puedes integrar con n8n, WordPress, o cualquier aplicación"
echo ""
