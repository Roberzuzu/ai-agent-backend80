# 🧪 GUÍA DE PRUEBA DE CONEXIÓN WEB

## ✅ Backend Configurado y Funcionando

Tu backend está **LIVE** en:
```
https://ai-agent-backend80.onrender.com
```

---

## 🌐 OPCIÓN 1: Página de Test Interactiva (RECOMENDADA)

Necesitas tener el frontend desplegado. Si ya lo tienes:

**URL de prueba:**
```
https://tu-frontend.com/test-connection.html
```

Esta página prueba automáticamente:
- ✅ Health Check
- ✅ MongoDB Connection
- ✅ Agent Status
- ✅ GET Productos
- ✅ POST Crear Producto

---

## 🔧 OPCIÓN 2: Prueba Manual con cURL

### Test 1: Health Check
```bash
curl https://ai-agent-backend80.onrender.com/api/health
```

**Respuesta esperada:**
```json
{
  "status": "healthy",
  "database": { "status": "healthy" }
}
```

### Test 2: MongoDB Status
```bash
curl https://ai-agent-backend80.onrender.com/api/status/detailed
```

**Respuesta esperada:**
```json
{
  "services": {
    "mongodb": { "status": "connected" }
  }
}
```

### Test 3: Listar Productos
```bash
curl https://ai-agent-backend80.onrender.com/api/products
```

### Test 4: Crear Producto
```bash
curl -X POST https://ai-agent-backend80.onrender.com/api/products \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Producto Test",
    "description": "Test desde cURL",
    "price": 99.99,
    "category": "test"
  }'
```

---

## 🌍 OPCIÓN 3: Prueba desde Navegador

### Test Simple (Abre en tu navegador):

**1. Health Check:**
```
https://ai-agent-backend80.onrender.com/api/health
```

**2. Documentación Interactiva (Swagger):**
```
https://ai-agent-backend80.onrender.com/docs
```

Aquí puedes probar **TODOS** los endpoints directamente desde el navegador.

---

## 📋 OPCIÓN 4: HTML Simple de Prueba

Crea un archivo `test.html` en tu computadora con este contenido:

```html
<!DOCTYPE html>
<html>
<head>
    <title>Test Backend</title>
</head>
<body>
    <h1>Test de Conexión</h1>
    <button onclick="testBackend()">Probar Backend</button>
    <pre id="result"></pre>
    
    <script>
        async function testBackend() {
            const result = document.getElementById('result');
            result.textContent = 'Probando...';
            
            try {
                const response = await fetch('https://ai-agent-backend80.onrender.com/api/health');
                const data = await response.json();
                result.textContent = JSON.stringify(data, null, 2);
            } catch (error) {
                result.textContent = 'Error: ' + error.message;
            }
        }
    </script>
</body>
</html>
```

Abre ese archivo en tu navegador y haz click en el botón.

---

## 🚀 OPCIÓN 5: JavaScript desde Consola del Navegador

1. Abre cualquier página web
2. Presiona `F12` (abrir DevTools)
3. Ve a la pestaña **Console**
4. Pega este código:

```javascript
// Test Health Check
fetch('https://ai-agent-backend80.onrender.com/api/health')
  .then(r => r.json())
  .then(data => console.log('✅ Health:', data))
  .catch(err => console.error('❌ Error:', err));

// Test MongoDB
fetch('https://ai-agent-backend80.onrender.com/api/status/detailed')
  .then(r => r.json())
  .then(data => console.log('✅ MongoDB:', data.services.mongodb))
  .catch(err => console.error('❌ Error:', err));

// Test Products
fetch('https://ai-agent-backend80.onrender.com/api/products')
  .then(r => r.json())
  .then(data => console.log('✅ Productos:', data))
  .catch(err => console.error('❌ Error:', err));
```

---

## 📊 Endpoints Principales Disponibles

```
GET  /api/health                - Health check
GET  /api/status/detailed       - Status completo del sistema
GET  /api/agent/status          - Status del agente AI
GET  /api/products               - Listar productos
POST /api/products               - Crear producto
GET  /api/trends                 - Listar tendencias
GET  /api/social/posts           - Posts de redes sociales
GET  /api/campaigns              - Campañas
GET  /api/woocommerce/products   - Productos de WooCommerce
POST /api/wordpress/posts        - Publicar en WordPress
GET  /docs                       - Documentación Swagger
```

---

## ✅ Estado Actual del Sistema

- ✅ Servidor funcionando
- ✅ MongoDB conectado
- ✅ API REST operacional
- ✅ CORS habilitado (permite conexiones desde frontend)
- ⏳ APIs de IA pendientes de configurar
- ⏳ WooCommerce pendiente de configurar
- ⏳ WordPress pendiente de configurar

---

## 🎯 Próximos Pasos

Una vez que pruebes y confirmes que todo funciona, configuraremos:

1. **APIs de IA** (OpenRouter/OpenAI/Perplexity)
2. **WooCommerce** (Consumer Key & Secret)
3. **WordPress** (Application Password)

---

**¿Necesitas ayuda?** Avísame qué método quieres usar para probar. 🚀
