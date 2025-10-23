# 🔗 INTEGRACIÓN CON N8N - CEREBRO AI

## 📍 INFORMACIÓN BÁSICA

**URL Base:** `https://railway-port-config.preview.emergentagent.com`  
**Endpoint Principal:** `/api/agent/execute`  
**Método:** POST  
**Content-Type:** application/json

---

## 🚀 CONFIGURACIÓN RÁPIDA EN N8N

### Paso 1: Crear un Webhook

1. Agrega un nodo **Webhook**
2. Método: POST
3. Path: `cerebro-ai` (o el que prefieras)
4. Response Mode: "When Last Node Finishes"

**URL del Webhook resultante:**
```
https://tu-n8n-instance.com/webhook/cerebro-ai
```

---

### Paso 2: Agregar HTTP Request Node

1. Agrega un nodo **HTTP Request**
2. Conecta al nodo Webhook
3. **Configuración:**

```
Method: POST
URL: https://railway-port-config.preview.emergentagent.com/api/agent/execute
Authentication: None
Send Body: ✅ (activado)
Body Content Type: JSON
```

4. **Body Parameters:**

```json
{
  "command": "={{ $json.body.command }}",
  "user_id": "={{ $json.body.user_id || 'n8n_user' }}"
}
```

---

### Paso 3: Procesar Respuesta (Opcional)

Agrega un nodo **Code** para formatear la respuesta:

```javascript
// items[0].json contiene la respuesta de Cerebro AI

const response = items[0].json;

return [{
  json: {
    success: response.success,
    mensaje: response.mensaje,
    plan: response.plan,
    resultados: response.resultados,
    provider: response.provider || 'perplexity',
    completado: response.completado,
    timestamp: new Date().toISOString()
  }
}];
```

---

## 📋 EJEMPLOS DE WORKFLOWS

### Ejemplo 1: Comando Simple

**Input (Webhook):**
```json
{
  "command": "Dame las estadísticas del sitio",
  "user_id": "admin_n8n"
}
```

**Output (Cerebro AI):**
```json
{
  "success": true,
  "mensaje": "Voy a recopilar las estadísticas...",
  "plan": "Obtener las estadísticas generales...",
  "acciones_planificadas": 1,
  "resultados": [
    {
      "herramienta": "obtener_estadisticas",
      "resultado": {
        "productos": { "total": 29, "sin_stock": 29 },
        "ventas": { "total_ordenes": 0, "ingresos_totales": 0 }
      }
    }
  ],
  "completado": true
}
```

---

### Ejemplo 2: Workflow con Slack

```
Webhook → HTTP Request (Cerebro AI) → Slack → Respond to Webhook
```

**Nodo Slack:**
```javascript
// Message Text
Nueva respuesta de Cerebro AI:
📊 {{ $json.mensaje }}

✅ Completado: {{ $json.completado }}
🤖 Provider: {{ $json.provider }}
```

---

### Ejemplo 3: Workflow con Email

```
Schedule Trigger → HTTP Request (Cerebro AI) → Email → Done
```

**HTTP Request Body:**
```json
{
  "command": "Dame un resumen de ventas del día",
  "user_id": "daily_report"
}
```

**Email Node:**
```
Subject: Reporte Diario - Cerebro AI
Body: 
{{ $json.mensaje }}

Resultados:
{{ JSON.stringify($json.resultados, null, 2) }}
```

---

### Ejemplo 4: Multi-Comando en Secuencia

```
Webhook → Split In Batches → HTTP Request → Aggregate → Respond
```

**Input:**
```json
{
  "comandos": [
    "Dame las estadísticas",
    "¿Cuántos productos tengo?",
    "Analiza las ventas del mes"
  ]
}
```

**Split In Batches:** Divide los comandos
**HTTP Request:** Ejecuta cada comando
**Aggregate:** Combina resultados

---

## 🔧 COMANDOS ÚTILES PARA N8N

### Productos:
```json
{ "command": "¿Cuántos productos tengo?" }
{ "command": "Dame información de los productos más vendidos" }
{ "command": "Busca productos sin stock" }
```

### Estadísticas:
```json
{ "command": "Dame las estadísticas del sitio" }
{ "command": "Muéstrame las ventas del mes" }
{ "command": "¿Cuál es el ingreso total?" }
```

### Análisis:
```json
{ "command": "Analiza los precios de la competencia" }
{ "command": "Busca tendencias en herramientas eléctricas" }
{ "command": "Dame un análisis de ventas" }
```

### Marketing:
```json
{ "command": "Crea una campaña para promocionar el producto X" }
{ "command": "Genera contenido para redes sociales" }
{ "command": "Optimiza el SEO de mis productos" }
```

---

## 🎯 WORKFLOW COMPLETO - ASISTENTE DIARIO

```
┌─────────────┐
│  Schedule   │  Cada día a las 9:00 AM
│  Trigger    │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│    HTTP     │  Comando: "Dame resumen diario"
│   Request   │  URL: /api/agent/execute
└──────┬──────┘
       │
       ▼
┌─────────────┐
│    Code     │  Formatear respuesta
│             │
└──────┬──────┘
       │
       ├──────────┐
       │          │
       ▼          ▼
┌──────────┐  ┌──────────┐
│  Email   │  │  Slack   │
│  Report  │  │  Message │
└──────────┘  └──────────┘
```

**Configuración Schedule:**
- Trigger Interval: Days
- Days Between Triggers: 1
- Trigger at Hour: 9
- Trigger at Minute: 0

---

## 📊 MONITOREO Y DEBUGGING

### Ver logs en tiempo real:
```bash
tail -f /var/log/supervisor/backend.*.log | grep -E "(Perplexity|OpenAI|Error)"
```

### Verificar estado del agente:
```bash
curl https://railway-port-config.preview.emergentagent.com/api/agent/status | jq .
```

### Ver historial de un usuario:
```bash
curl "https://railway-port-config.preview.emergentagent.com/api/agent/memory/n8n_user?limit=10" | jq .
```

---

## 🔐 BUENAS PRÁCTICAS

1. **User ID:** Usa IDs únicos para cada workflow/usuario
   ```json
   {
     "user_id": "n8n_workflow_{{ $workflow.id }}_{{ $execution.id }}"
   }
   ```

2. **Error Handling:** Agrega un nodo de error
   ```
   HTTP Request → Error Trigger → Send Alert
   ```

3. **Timeout:** Configura timeout en HTTP Request (60 segundos)

4. **Retry:** Activa "Retry On Fail" en HTTP Request
   - Number of Retries: 2
   - Wait Between Tries: 5000ms

---

## 📝 PLANTILLA DE WORKFLOW (JSON)

Importa este workflow directamente en n8n:

```json
{
  "name": "Cerebro AI - Integración Básica",
  "nodes": [
    {
      "parameters": {
        "httpMethod": "POST",
        "path": "cerebro-ai",
        "responseMode": "lastNode"
      },
      "name": "Webhook",
      "type": "n8n-nodes-base.webhook",
      "position": [250, 300]
    },
    {
      "parameters": {
        "method": "POST",
        "url": "https://railway-port-config.preview.emergentagent.com/api/agent/execute",
        "jsonParameters": true,
        "options": {},
        "bodyParametersJson": "={\n  \"command\": \"{{ $json.body.command }}\",\n  \"user_id\": \"{{ $json.body.user_id || 'n8n_user' }}\"\n}"
      },
      "name": "Cerebro AI Request",
      "type": "n8n-nodes-base.httpRequest",
      "position": [450, 300]
    },
    {
      "parameters": {
        "respondWith": "json",
        "responseBody": "={{ $json }}"
      },
      "name": "Respond to Webhook",
      "type": "n8n-nodes-base.respondToWebhook",
      "position": [650, 300]
    }
  ],
  "connections": {
    "Webhook": {
      "main": [[{ "node": "Cerebro AI Request", "type": "main", "index": 0 }]]
    },
    "Cerebro AI Request": {
      "main": [[{ "node": "Respond to Webhook", "type": "main", "index": 0 }]]
    }
  }
}
```

---

## 🧪 TESTING EN N8N

1. **Activar el Webhook**
2. **Copiar la URL de testing**
3. **Hacer POST con curl:**

```bash
curl -X POST "https://tu-n8n.com/webhook-test/cerebro-ai" \
  -H "Content-Type: application/json" \
  -d '{
    "command": "Dame las estadísticas",
    "user_id": "test_n8n"
  }'
```

---

## 🆘 TROUBLESHOOTING

### Error: "Field required"
- Verifica que el body tenga `command` y `user_id`

### Error: Connection timeout
- Aumenta el timeout a 60 segundos
- Verifica que el backend esté corriendo

### Error: 500 Internal Server Error
- Revisa los logs del backend
- Verifica las API keys de Perplexity/OpenAI

---

## 📞 CONTACTO

Si necesitas ayuda:
1. Revisa los logs: `tail -f /var/log/supervisor/backend.*.log`
2. Prueba primero con curl
3. Verifica el estado: `GET /api/agent/status`

---

**Última actualización:** 2025-07-15  
**Versión:** 1.0  
**Compatible con:** n8n v1.x
