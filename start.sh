#!/bin/bash
# ====================================
# SCRIPT DE INICIO RAPIDO
# Inicia todos los servicios
# ====================================

echo "🚀 Iniciando sistema..."

# Verificar si Docker está disponible
if command -v docker-compose &> /dev/null; then
    echo "✅ Usando Docker Compose..."
    docker-compose up -d
    
    echo ""
    echo "⏳ Esperando que los servicios inicien..."
    sleep 10
    
    echo ""
    echo "✅ Sistema iniciado!"
    echo ""
    echo "📱 Accede a:"
    echo "   Frontend:  http://localhost:3000"
    echo "   Backend:   http://localhost:8001/api"
    echo "   Docs API:  http://localhost:8001/docs"
    echo "   Grafana:   http://localhost:3001 (admin/admin)"
    echo ""
    echo "📊 Ver logs:"
    echo "   docker-compose logs -f"
    echo ""
    echo "🛑 Detener:"
    echo "   docker-compose down"
    echo ""
    
else
    echo "⚠️  Docker no disponible. Iniciando manualmente..."
    echo ""
    echo "Necesitas abrir 3 terminales:"
    echo ""
    echo "Terminal 1 - MongoDB:"
    echo "  mongod --dbpath ./data/db"
    echo ""
    echo "Terminal 2 - Backend:"
    echo "  cd backend && python3 -m uvicorn server:app --reload --host 0.0.0.0 --port 8001"
    echo ""
    echo "Terminal 3 - Frontend:"
    echo "  cd frontend && npm start"
    echo ""
fi
