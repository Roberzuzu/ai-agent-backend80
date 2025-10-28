# ⚡ CEREBRO AI - Pruebas Rápidas con curl

## ✅ URLs LISTAS PARA COPIAR Y PEGAR

### 1. Ver Estado del Agente
```bash
curl https://wpmoneyhub.preview.emergentagent.com/api/agent/status
```

### 2. Ejecutar Comando - Estadísticas
```bash
curl -X POST https://wpmoneyhub.preview.emergentagent.com/api/agent/execute \
  -H "Content-Type: application/json" \
  -d '{
    "command": "Dame las estadísticas del sitio",
    "user_id": "mi_usuario"
  }'
```

### 3. Ejecutar Comando - Productos
```bash
curl -X POST https://wpmoneyhub.preview.emergentagent.com/api/agent/execute \
  -H "Content-Type: application/json" \
  -d '{
    "command": "¿Cuántos productos tengo?",
    "user_id": "mi_usuario"
  }'
```

### 4. Ejecutar Comando - Análisis
```bash
curl -X POST https://wpmoneyhub.preview.emergentagent.com/api/agent/execute \
  -H "Content-Type: application/json" \
  -d '{
    "command": "Analiza las tendencias de productos",
    "user_id": "mi_usuario"
  }'
```

### 5. Ver Historial
```bash
curl "https://wpmoneyhub.preview.emergentagent.com/api/agent/memory/mi_usuario?limit=5"
```

### 6. Búsqueda Semántica
```bash
curl -X POST https://wpmoneyhub.preview.emergentagent.com/api/agent/search-memory \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "mi_usuario",
    "query": "estadísticas",
    "limit": 3
  }'
```

---

## 📦 COLECCIÓN POSTMAN/THUNDER CLIENT

### Importar esta colección:

```json
{
  "info": {
    "name": "Cerebro AI",
    "description": "APIs del sistema Cerebro AI con Perplexity + OpenAI",
    "version": "1.0.0"
  },
  "item": [
    {
      "name": "Agent Status",
      "request": {
        "method": "GET",
        "header": [],
        "url": {
          "raw": "https://wpmoneyhub.preview.emergentagent.com/api/agent/status",
          "protocol": "https",
          "host": ["api-switcher", "preview", "emergentagent", "com"],
          "path": ["api", "agent", "status"]
        }
      }
    },
    {
      "name": "Execute Command - Estadísticas",
      "request": {
        "method": "POST",
        "header": [
          {
            "key": "Content-Type",
            "value": "application/json"
          }
        ],
        "body": {
          "mode": "raw",
          "raw": "{\n  \"command\": \"Dame las estadísticas del sitio\",\n  \"user_id\": \"postman_user\"\n}"
        },
        "url": {
          "raw": "https://wpmoneyhub.preview.emergentagent.com/api/agent/execute",
          "protocol": "https",
          "host": ["api-switcher", "preview", "emergentagent", "com"],
          "path": ["api", "agent", "execute"]
        }
      }
    },
    {
      "name": "Execute Command - Productos",
      "request": {
        "method": "POST",
        "header": [
          {
            "key": "Content-Type",
            "value": "application/json"
          }
        ],
        "body": {
          "mode": "raw",
          "raw": "{\n  \"command\": \"¿Cuántos productos tengo?\",\n  \"user_id\": \"postman_user\"\n}"
        },
        "url": {
          "raw": "https://wpmoneyhub.preview.emergentagent.com/api/agent/execute",
          "protocol": "https",
          "host": ["api-switcher", "preview", "emergentagent", "com"],
          "path": ["api", "agent", "execute"]
        }
      }
    },
    {
      "name": "Get Memory",
      "request": {
        "method": "GET",
        "header": [],
        "url": {
          "raw": "https://wpmoneyhub.preview.emergentagent.com/api/agent/memory/postman_user?limit=5",
          "protocol": "https",
          "host": ["api-switcher", "preview", "emergentagent", "com"],
          "path": ["api", "agent", "memory", "postman_user"],
          "query": [
            {
              "key": "limit",
              "value": "5"
            }
          ]
        }
      }
    },
    {
      "name": "Search Memory",
      "request": {
        "method": "POST",
        "header": [
          {
            "key": "Content-Type",
            "value": "application/json"
          }
        ],
        "body": {
          "mode": "raw",
          "raw": "{\n  \"user_id\": \"postman_user\",\n  \"query\": \"estadísticas\",\n  \"limit\": 3\n}"
        },
        "url": {
          "raw": "https://wpmoneyhub.preview.emergentagent.com/api/agent/search-memory",
          "protocol": "https",
          "host": ["api-switcher", "preview", "emergentagent", "com"],
          "path": ["api", "agent", "search-memory"]
        }
      }
    }
  ]
}
```

---

## 🎯 COMANDOS MÁS ÚTILES

### Productos
```bash
# Ver productos
curl -X POST https://wpmoneyhub.preview.emergentagent.com/api/agent/execute \
  -H "Content-Type: application/json" \
  -d '{"command": "Muéstrame todos los productos", "user_id": "test"}'

# Buscar productos
curl -X POST https://wpmoneyhub.preview.emergentagent.com/api/agent/execute \
  -H "Content-Type: application/json" \
  -d '{"command": "Busca productos de herramientas", "user_id": "test"}'

# Productos sin stock
curl -X POST https://wpmoneyhub.preview.emergentagent.com/api/agent/execute \
  -H "Content-Type: application/json" \
  -d '{"command": "¿Qué productos están sin stock?", "user_id": "test"}'
```

### Estadísticas y Análisis
```bash
# Estadísticas generales
curl -X POST https://wpmoneyhub.preview.emergentagent.com/api/agent/execute \
  -H "Content-Type: application/json" \
  -d '{"command": "Dame las estadísticas completas", "user_id": "test"}'

# Ventas del mes
curl -X POST https://wpmoneyhub.preview.emergentagent.com/api/agent/execute \
  -H "Content-Type: application/json" \
  -d '{"command": "¿Cuántas ventas tuve este mes?", "user_id": "test"}'

# Análisis de tendencias
curl -X POST https://wpmoneyhub.preview.emergentagent.com/api/agent/execute \
  -H "Content-Type: application/json" \
  -d '{"command": "Analiza las tendencias de mercado", "user_id": "test"}'
```

### Marketing
```bash
# Crear campaña
curl -X POST https://wpmoneyhub.preview.emergentagent.com/api/agent/execute \
  -H "Content-Type: application/json" \
  -d '{"command": "Crea una campaña para promocionar herramientas", "user_id": "test"}'

# Generar contenido
curl -X POST https://wpmoneyhub.preview.emergentagent.com/api/agent/execute \
  -H "Content-Type: application/json" \
  -d '{"command": "Genera contenido para redes sociales", "user_id": "test"}'
```

---

## 🔥 PYTHON SCRIPT DE PRUEBA

```python
#!/usr/bin/env python3
import requests
import json

BASE_URL = "https://wpmoneyhub.preview.emergentagent.com"

def test_cerebro_ai():
    print("=" * 60)
    print("🧠 PRUEBA CEREBRO AI")
    print("=" * 60)
    
    # Test 1: Status
    print("\n1️⃣ Estado del Agente:")
    response = requests.get(f"{BASE_URL}/api/agent/status")
    print(json.dumps(response.json(), indent=2))
    
    # Test 2: Execute
    print("\n2️⃣ Ejecutar Comando:")
    response = requests.post(
        f"{BASE_URL}/api/agent/execute",
        json={
            "command": "Dame las estadísticas",
            "user_id": "python_test"
        }
    )
    print(json.dumps(response.json(), indent=2))
    
    # Test 3: Memory
    print("\n3️⃣ Ver Historial:")
    response = requests.get(f"{BASE_URL}/api/agent/memory/python_test?limit=2")
    print(json.dumps(response.json(), indent=2))
    
    print("\n" + "=" * 60)
    print("✅ Pruebas completadas")

if __name__ == "__main__":
    test_cerebro_ai()
```

Guarda como `test_api.py` y ejecuta:
```bash
python3 test_api.py
```

---

## 🌐 JAVASCRIPT/NODE.JS

```javascript
const axios = require('axios');

const BASE_URL = 'https://wpmoneyhub.preview.emergentagent.com';

async function testCerebroAI() {
  console.log('🧠 Probando Cerebro AI...\n');
  
  try {
    // Test 1: Status
    const status = await axios.get(`${BASE_URL}/api/agent/status`);
    console.log('✅ Estado:', status.data);
    
    // Test 2: Execute
    const execute = await axios.post(`${BASE_URL}/api/agent/execute`, {
      command: 'Dame las estadísticas',
      user_id: 'node_test'
    });
    console.log('✅ Resultado:', execute.data);
    
    // Test 3: Memory
    const memory = await axios.get(`${BASE_URL}/api/agent/memory/node_test?limit=2`);
    console.log('✅ Historial:', memory.data);
    
  } catch (error) {
    console.error('❌ Error:', error.message);
  }
}

testCerebroAI();
```

---

## 📱 EJEMPLO PHP (WordPress)

```php
<?php
$base_url = 'https://wpmoneyhub.preview.emergentagent.com';

// Ejecutar comando
function cerebro_execute($command, $user_id) {
    global $base_url;
    
    $response = wp_remote_post($base_url . '/api/agent/execute', [
        'headers' => ['Content-Type' => 'application/json'],
        'body' => json_encode([
            'command' => $command,
            'user_id' => $user_id
        ]),
        'timeout' => 60
    ]);
    
    if (is_wp_error($response)) {
        return ['error' => $response->get_error_message()];
    }
    
    return json_decode(wp_remote_retrieve_body($response), true);
}

// Uso
$result = cerebro_execute('Dame las estadísticas', 'wp_user_123');
echo json_encode($result, JSON_PRETTY_PRINT);
?>
```

---

## ⏱️ RESPUESTAS TÍPICAS

- **GET /api/agent/status**: ~100-200ms
- **POST /api/agent/execute**: ~2-5 segundos (depende de Perplexity)
- **GET /api/agent/memory**: ~100-300ms
- **POST /api/agent/search-memory**: ~500-1000ms (embeddings)

---

## 📊 ESTRUCTURA DE RESPUESTA EXITOSA

```json
{
  "success": true,
  "mensaje": "Texto de respuesta para el usuario",
  "plan": "Descripción del plan ejecutado",
  "acciones_planificadas": 1,
  "resultados": [
    {
      "herramienta": "nombre_herramienta",
      "resultado": { /* datos específicos */ }
    }
  ],
  "completado": true,
  "provider": "perplexity"
}
```

---

**¡LISTO PARA USAR!** 🚀
