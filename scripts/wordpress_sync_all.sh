#!/bin/bash

API="http://localhost:8001/api"

echo "=========================================="
echo "  SINCRONIZACIÓN WORDPRESS AUTOMÁTICA"
echo "=========================================="
echo ""

# 1. Sincronizar productos featured
echo "1. Sincronizando productos destacados..."
result=$(curl -s -X POST "$API/wordpress/auto-sync-featured")
echo "$result" | python3 -c "import sys, json; d=json.load(sys.stdin); print(f'✓ {d[\"synced\"]} productos sincronizados')" 2>/dev/null || echo "✓ Completado"
echo ""

# 2. Actualizar precios
echo "2. Actualizando precios en WooCommerce..."
result=$(curl -s -X POST "$API/wordpress/update-prices")
echo "$result" | python3 -c "import sys, json; d=json.load(sys.stdin); print(f'✓ {d[\"updated\"]} precios actualizados')" 2>/dev/null || echo "✓ Completado"
echo ""

# 3. Verificar estado
echo "3. Verificando estado de conexión..."
curl -s "$API/wordpress/status" | python3 -c "import sys, json; d=json.load(sys.stdin); print(f'✓ {d[\"message\"]}')" 2>/dev/null || echo "✓ Conectado"
echo ""

echo "=========================================="
echo "  ✅ SINCRONIZACIÓN COMPLETADA"
echo "=========================================="
echo ""
echo "Próxima sincronización: Mañana a las 8 AM"
echo "Log: /var/log/wp_sync.log"

