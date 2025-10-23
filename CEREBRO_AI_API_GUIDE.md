# 🧠 CEREBRO AI - Guía Completa de APIs

## 📍 URL BASE
```
https://railway-port-config.preview.emergentagent.com
```

---

## 🔗 ENDPOINTS DISPONIBLES

### 1️⃣ **POST /api/agent/execute** - Ejecutar Comando con IA
**Descripción:** Envía un comando en lenguaje natural, el agente lo interpreta, ejecuta herramientas automáticamente y responde.

**URL Completa:**
```
https://railway-port-config.preview.emergentagent.com/api/agent/execute
```

**Método:** POST  
**Content-Type:** application/json

**Body (JSON):**
```json
{
  "command": "Dame las estadísticas del sitio",
  "user_id": "usuario_wordpress_123"
}
```

**Ejemplo con curl:**
```bash
curl -X POST https://railway-port-config.preview.emergentagent.com/api/agent/execute \
  -H "Content-Type: application/json" \
  -d '{
    "command": "Dame las estadísticas del sitio",
    "user_id": "admin_wordpress"
  }'
```

**Respuesta Exitosa (200):**
```json
{
  "success": true,
  "mensaje": "He obtenido las estadísticas del sitio",
  "plan": {
    "plan": "Obtener estadísticas generales...",
    "acciones": [
      {
        "herramienta": "obtener_estadisticas",
        "parametros": {"tipo": "general"},
        "orden": 1
      }
    ],
    "respuesta_usuario": "Aquí están las estadísticas..."
  },
  "resultados": [
    {
      "herramienta": "obtener_estadisticas",
      "resultado": {
        "productos": 150,
        "ventas_mes": 45,
        "ingresos": 12500
      }
    }
  ],
  "provider": "perplexity"
}
```

---

### 2️⃣ **POST /api/agent/chat** - Chat Conversacional
**Descripción:** Chat sin auto-ejecución. Solo conversa y sugiere acciones.

**URL Completa:**
```
https://railway-port-config.preview.emergentagent.com/api/agent/chat
```

**Método:** POST  
**Content-Type:** application/json

**Body (JSON):**
```json
{
  "message": "¿Qué herramientas tienes disponibles?",
  "user_id": "usuario_wordpress_123"
}
```

**Ejemplo con curl:**
```bash
curl -X POST https://railway-port-config.preview.emergentagent.com/api/agent/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "¿Qué puedes hacer por mí?",
    "user_id": "admin_wordpress"
  }'
```

**Respuesta Exitosa (200):**
```json
{
  "success": true,
  "respuesta": "Puedo ayudarte con múltiples tareas...",
  "acciones_sugeridas": [
    {
      "herramienta": "obtener_estadisticas",
      "descripcion": "Ver estadísticas del sitio"
    }
  ],
  "provider": "perplexity"
}
```

---

### 3️⃣ **GET /api/agent/status** - Estado del Agente
**Descripción:** Verifica que el agente está activo y obtiene información sobre las herramientas disponibles.

**URL Completa:**
```
https://railway-port-config.preview.emergentagent.com/api/agent/status
```

**Método:** GET

**Ejemplo con curl:**
```bash
curl https://railway-port-config.preview.emergentagent.com/api/agent/status
```

**Respuesta Exitosa (200):**
```json
{
  "success": true,
  "agente_activo": true,
  "modelo": "Perplexity Pro (sonar-pro)",
  "herramientas_disponibles": 22,
  "categorias": {
    "productos": 7,
    "analisis": 7,
    "marketing": 4,
    "creatividad": 1,
    "integraciones": 3
  },
  "caracteristicas": {
    "memoria_persistente": true,
    "rag_enabled": true,
    "fallback_openai": true
  }
}
```

---

### 4️⃣ **GET /api/agent/memory/{user_id}** - Obtener Historial
**Descripción:** Recupera el historial de conversaciones de un usuario.

**URL Completa:**
```
https://railway-port-config.preview.emergentagent.com/api/agent/memory/{user_id}?limit=10
```

**Método:** GET  
**Parámetros de Query:**
- `limit` (opcional): Número de memorias a recuperar (default: 10)

**Ejemplo con curl:**
```bash
curl "https://railway-port-config.preview.emergentagent.com/api/agent/memory/admin_wordpress?limit=5"
```

**Respuesta Exitosa (200):**
```json
{
  "success": true,
  "user_id": "admin_wordpress",
  "count": 5,
  "memories": [
    {
      "command": "Dame las estadísticas",
      "response": "Aquí están las estadísticas...",
      "timestamp": "2025-07-15T10:30:00Z"
    }
  ]
}
```

---

### 5️⃣ **POST /api/agent/search-memory** - Búsqueda Semántica
**Descripción:** Busca memorias relevantes usando IA y embeddings.

**URL Completa:**
```
https://railway-port-config.preview.emergentagent.com/api/agent/search-memory
```

**Método:** POST  
**Content-Type:** application/json

**Body (JSON):**
```json
{
  "user_id": "admin_wordpress",
  "query": "estadísticas de ventas",
  "limit": 5
}
```

**Ejemplo con curl:**
```bash
curl -X POST https://railway-port-config.preview.emergentagent.com/api/agent/search-memory \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "admin_wordpress",
    "query": "estadísticas",
    "limit": 3
  }'
```

---

## 🔧 INTEGRACIÓN CON N8N

### Configuración en n8n:

1. **Nodo HTTP Request**
2. **Configuración:**
   - Method: POST
   - URL: `https://railway-port-config.preview.emergentagent.com/api/agent/execute`
   - Authentication: None
   - Body Content Type: JSON

3. **Body (JSON):**
```json
{
  "command": "{{ $json.comando }}",
  "user_id": "n8n_workflow_{{ $workflow.id }}"
}
```

### Ejemplo de Workflow n8n:

```
Webhook → HTTP Request (Cerebro AI) → Code → Send Response
```

**Paso 1 - Webhook:** Recibe el comando
```json
{
  "comando": "Dame estadísticas de productos"
}
```

**Paso 2 - HTTP Request:**
- URL: `https://railway-port-config.preview.emergentagent.com/api/agent/execute`
- Method: POST
- Body:
```json
{
  "command": "{{ $json.comando }}",
  "user_id": "n8n_user"
}
```

**Paso 3 - Code:** Procesa la respuesta
```javascript
return [{
  json: {
    respuesta: $input.item.json.mensaje,
    resultados: $input.item.json.resultados,
    proveedor: $input.item.json.provider
  }
}];
```

---

## 📊 COMANDOS DE EJEMPLO

### Productos:
```
"Dame información sobre los productos"
"Busca productos de la categoría herramientas"
"¿Cuántos productos tengo en stock?"
```

### Estadísticas:
```
"Dame las estadísticas del sitio"
"Muéstrame las ventas del mes"
"¿Cuál es el ingreso total?"
```

### Análisis:
```
"Analiza los precios de la competencia"
"Busca tendencias en herramientas eléctricas"
"¿Qué productos están de moda?"
```

### Marketing:
```
"Crea una campaña para el producto X"
"Genera contenido para redes sociales"
"Optimiza el SEO del producto Y"
```

---

## 🧪 SCRIPT DE PRUEBA RÁPIDO

Guarda esto como `test_cerebro_api.sh`:

```bash
#!/bin/bash

BASE_URL="https://railway-port-config.preview.emergentagent.com"

echo "🧪 Testing Cerebro AI APIs..."
echo ""

# Test 1: Status
echo "1️⃣ GET /api/agent/status"
curl -s "$BASE_URL/api/agent/status" | jq .
echo ""

# Test 2: Execute command
echo "2️⃣ POST /api/agent/execute"
curl -s -X POST "$BASE_URL/api/agent/execute" \
  -H "Content-Type: application/json" \
  -d '{"command": "Dame las estadísticas", "user_id": "test_user"}' | jq .
echo ""

# Test 3: Chat
echo "3️⃣ POST /api/agent/chat"
curl -s -X POST "$BASE_URL/api/agent/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "Hola, ¿qué puedes hacer?", "user_id": "test_user"}' | jq .
echo ""

echo "✅ Tests completados"
```

**Para ejecutar:**
```bash
chmod +x test_cerebro_api.sh
./test_cerebro_api.sh
```

---

## 🔐 SEGURIDAD (A IMPLEMENTAR)

Por ahora las APIs están abiertas. Para producción se recomienda:
- Sistema de API Keys
- Rate limiting
- Autenticación JWT
- CORS configurado

---

## 📞 SOPORTE

Si tienes problemas:
1. Verifica que el backend esté corriendo
2. Revisa los logs: `tail -f /var/log/supervisor/backend.*.log`
3. Prueba con curl primero antes de integrar

---

**Última actualización:** 2025-07-15  
**Versión:** 1.0  
**Cerebro AI:** Perplexity (primario) + OpenAI (backup)
