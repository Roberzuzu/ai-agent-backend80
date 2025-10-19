# 🧠 CEREBRO AI - Sistema Inteligente Completo

## 📋 RESUMEN EJECUTIVO

Se ha implementado exitosamente un sistema de agente inteligente basado en **Claude 3.5 Sonnet** con memoria persistente y búsqueda semántica (RAG) que puede interpretar comandos en lenguaje natural y ejecutar acciones automáticamente.

---

## ✨ CARACTERÍSTICAS PRINCIPALES

### 1. **Agente Inteligente (Claude 3.5 Sonnet)**
- ✅ Interpreta comandos en lenguaje natural
- ✅ Decide qué herramientas usar automáticamente
- ✅ Ejecuta múltiples acciones en secuencia
- ✅ Genera planes de ejecución estructurados

### 2. **Sistema de Memoria Avanzado**
- ✅ **Memoria Persistente**: Guarda TODO el historial en MongoDB
- ✅ **Búsqueda Semántica**: Usa embeddings de OpenAI
- ✅ **RAG (Retrieval-Augmented Generation)**: Recupera contexto relevante
- ✅ **Embeddings Vectoriales**: Similaridad de coseno para búsqueda

### 3. **18 Herramientas Integradas**

#### **PRODUCTOS (7 herramientas)**
1. `procesar_producto(product_id)` - Procesa productos con AI
2. `crear_producto(datos)` - Crea nuevos productos
3. `actualizar_producto(product_id, datos)` - Actualiza productos
4. `eliminar_producto(product_id)` - Elimina productos
5. `obtener_productos(filtros)` - Lista productos
6. `buscar_productos(query, filtros)` - Búsqueda avanzada
7. `gestionar_inventario(operacion, datos)` - Gestión masiva de stock/precios

#### **ANÁLISIS E INTELIGENCIA (5 herramientas)**
8. `buscar_tendencias(categoria, pais)` - Tendencias con Perplexity
9. `analizar_precios(producto, categoria)` - Precios óptimos con Abacus AI
10. `analizar_competencia(producto, categoria)` - Análisis competitivo
11. `obtener_estadisticas(tipo)` - Métricas del sitio
12. `analizar_ventas(periodo, filtros)` - Reportes de ventas

#### **MARKETING (3 herramientas)**
13. `crear_campana(tipo, producto_id, presupuesto)` - Campañas publicitarias
14. `crear_descuento(tipo, valor, productos)` - Cupones y promociones
15. `generar_contenido(tipo, tema)` - Blogs, emails, posts

#### **CREATIVIDAD (1 herramienta)**
16. `generar_imagenes(descripcion, cantidad)` - Imágenes con Fal AI

#### **INTEGRACIONES (2 herramientas)**
17. `sincronizar_wordpress(accion, datos)` - Sync con WordPress
18. `optimizar_seo(producto_id)` - Optimización SEO

---

## 🔌 ENDPOINTS API

### **1. Endpoint Principal - Ejecutar Comando**
```bash
POST /api/agent/execute
```

**Request:**
```json
{
  "command": "Busca 10 herramientas eléctricas tendencia",
  "user_id": "telegram_7202793910"
}
```

**Response:**
```json
{
  "success": true,
  "mensaje": "Voy a buscar las 10 herramientas eléctricas más vendidas...",
  "plan": "Buscar tendencias de herramientas eléctricas en España",
  "acciones_planificadas": 1,
  "resultados": [
    {
      "herramienta": "buscar_tendencias",
      "resultado": {
        "success": true,
        "resultado": "...",
        "citations": []
      }
    }
  ],
  "completado": true
}
```

### **2. Chat Conversacional**
```bash
POST /api/agent/chat
```
Solo piensa, NO ejecuta automáticamente. Útil para confirmar antes de actuar.

### **3. Estado del Agente**
```bash
GET /api/agent/status
```

**Response:**
```json
{
  "success": true,
  "agente_activo": true,
  "conversaciones_totales": 0,
  "memorias_guardadas": 0,
  "herramientas_disponibles": 18,
  "caracteristicas": {
    "memoria_persistente": true,
    "busqueda_semantica": true,
    "rag_enabled": true,
    "embeddings": true
  }
}
```

### **4. Gestión de Memoria**

#### Obtener Memoria de Usuario
```bash
GET /api/agent/memory/{user_id}?limit=20
```

#### Obtener Historial de Conversaciones
```bash
GET /api/agent/conversations/{user_id}?limit=50
```

#### Buscar en Memoria (Semántica)
```bash
POST /api/agent/search-memory
{
  "command": "productos sin stock",
  "user_id": "user123"
}
```

#### Eliminar Memoria
```bash
DELETE /api/agent/memory/{user_id}
```

---

## 💾 ESTRUCTURA DE BASE DE DATOS

### **Colección: `conversations`**
```javascript
{
  "_id": ObjectId,
  "user_id": "telegram_7202793910",
  "command": "Busca 10 herramientas eléctricas tendencia",
  "response": "Aquí están las 10 herramientas...",
  "plan": {
    "plan": "...",
    "acciones": [...]
  },
  "timestamp": ISODate("2025-01-15T10:30:00Z")
}
```

### **Colección: `agent_memory`**
```javascript
{
  "_id": ObjectId,
  "user_id": "telegram_7202793910",
  "command": "Busca 10 herramientas eléctricas tendencia",
  "response": "Aquí están las 10 herramientas...",
  "plan": {...},
  "embedding": [0.123, -0.456, ...], // Vector de 1536 dimensiones
  "timestamp": ISODate("2025-01-15T10:30:00Z")
}
```

---

## 🤖 INTEGRACIÓN CON TELEGRAM

### **Bot Actualizado** (`telegram_bot.py`)

El bot funciona como **mensajero puro**:

1. **Recibe mensaje de Telegram**
2. **Envía a `/api/agent/execute`**
3. **Espera respuesta**
4. **Muestra resultado al usuario**

**Comandos soportados:**
```
/procesar [ID] - Procesar producto específico
/ayuda - Mostrar ayuda
/start - Iniciar bot

O cualquier texto en lenguaje natural:
- "Busca 10 herramientas eléctricas tendencia"
- "Analiza la competencia de sierras"
- "Crea una campaña para el producto 4146"
- "Muéstrame las estadísticas del sitio"
```

---

## 🔐 CONFIGURACIÓN REQUERIDA

### **Variables de Entorno (.env)**
```env
# MongoDB
MONGO_URL=mongodb://localhost:27017
DB_NAME=social_media_monetization

# AI APIs
OPENROUTER_API_KEY=sk-or-...     # Claude 3.5 Sonnet
OPENAI_API_KEY=sk-...            # Embeddings + GPT
PERPLEXITY_API_KEY=pplx-...      # Búsquedas en tiempo real
FAL_API_KEY=...                  # Generación de imágenes
ABACUS_API_KEY=...               # Análisis predictivo

# Telegram
TELEGRAM_BOT_TOKEN=7708509018:...
TELEGRAM_CHAT_ID=7202793910

# WooCommerce
WC_URL=https://herramientasyaccesorios.store/wp-json/wc/v3
WC_KEY=ck_...
WC_SECRET=cs_...

# WordPress
WP_URL=https://herramientasyaccesorios.store/wp-json/wp/v2
WP_USER=agenteweb@...
WP_PASS=...
```

---

## 📊 FLUJO DE TRABAJO COMPLETO

```
┌─────────────────┐
│  USUARIO        │
│  (Telegram)     │
└────────┬────────┘
         │
         │ "Busca 10 herramientas eléctricas tendencia"
         ▼
┌─────────────────┐
│  Bot Telegram   │
│  (Mensajero)    │
└────────┬────────┘
         │
         │ POST /api/agent/execute
         ▼
┌─────────────────┐
│  AIAgent        │
│  (Cerebro)      │
└────────┬────────┘
         │
         │ 1. Buscar memorias relevantes (RAG)
         │ 2. Obtener historial reciente
         ▼
┌─────────────────┐
│  Claude 3.5     │
│  Sonnet         │
└────────┬────────┘
         │
         │ Plan: {
         │   "herramienta": "buscar_tendencias",
         │   "parametros": {...}
         │ }
         ▼
┌─────────────────┐
│  Ejecutar       │
│  Herramientas   │
└────────┬────────┘
         │
         │ → Perplexity API
         │ → WooCommerce API
         │ → Fal AI
         │ → Abacus AI
         ▼
┌─────────────────┐
│  Guardar en     │
│  Memoria        │
│  (MongoDB)      │
└────────┬────────┘
         │
         │ Resultado + Memoria
         ▼
┌─────────────────┐
│  Bot Telegram   │
│  (Respuesta)    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  USUARIO        │
│  (Ve resultado) │
└─────────────────┘
```

---

## 🎯 CASOS DE USO

### **1. Búsqueda de Tendencias**
```
Usuario: "Busca las 10 herramientas más vendidas en España"

Agente:
1. Usa buscar_tendencias con Perplexity
2. Obtiene productos tendencia
3. Guarda en memoria para referencias futuras
4. Responde con lista detallada
```

### **2. Procesamiento de Producto**
```
Usuario: "Procesa el producto 4146 con AI"

Agente:
1. Usa procesar_producto
2. Genera descripción SEO con Claude
3. Calcula precio óptimo con Abacus AI
4. Crea 2 imágenes con Fal AI
5. Actualiza todo en WooCommerce
```

### **3. Análisis de Ventas**
```
Usuario: "Dame las estadísticas del último mes"

Agente:
1. Usa obtener_estadisticas
2. Usa analizar_ventas con periodo="mes"
3. Combina datos
4. Responde con resumen ejecutivo
```

### **4. Gestión de Inventario**
```
Usuario: "Actualiza el stock de los productos 100, 101, 102 a 50 unidades"

Agente:
1. Interpreta la intención
2. Usa gestionar_inventario con operacion="actualizar_stock"
3. Actualiza en WooCommerce
4. Confirma cambios
```

---

## 📈 VENTAJAS DEL SISTEMA

### **✅ CENTRALIZACIÓN**
- Todo en una sola aplicación
- Un solo endpoint `/api/agent/execute`
- APIs ya integradas y funcionando

### **✅ INTELIGENCIA**
- Claude 3.5 Sonnet toma decisiones
- No necesitas programar cada comando
- Lenguaje natural = facilidad de uso

### **✅ ESCALABILIDAD**
- Fácil agregar nuevas herramientas
- Multi-canal (Telegram hoy, WhatsApp mañana)
- Sistema de memoria que aprende

### **✅ MEMORIA PERSISTENTE**
- Recuerda conversaciones anteriores
- Búsqueda semántica con RAG
- Contexto relevante automático

---

## 🔧 MANTENIMIENTO

### **Agregar Nueva Herramienta**

1. Agregar descripción en `tools_description` en `ai_agent.py`
2. Agregar case en `execute_action()`
3. Implementar método `_nombre_herramienta()`
4. Actualizar contador de herramientas

### **Monitoreo**

```bash
# Ver conversaciones
curl http://localhost:8001/api/agent/status

# Ver memoria de usuario
curl http://localhost:8001/api/agent/memory/telegram_7202793910

# Buscar en memoria
curl -X POST http://localhost:8001/api/agent/search-memory \
  -d '{"command":"productos", "user_id":"user123"}'
```

### **Logs**
```bash
# Backend
tail -f /var/log/supervisor/backend.out.log

# Telegram Bot
tail -f /var/log/telegram_bot.log
```

---

## 🎉 RESULTADO FINAL

✅ **Sistema completo funcionando**
✅ **18 herramientas integradas**
✅ **Memoria persistente con RAG**
✅ **Bot de Telegram como mensajero**
✅ **Claude 3.5 Sonnet como cerebro**
✅ **APIs funcionando correctamente**

---

## 📞 PRUEBA RÁPIDA

```bash
# 1. Verificar estado
curl http://localhost:8001/api/agent/status

# 2. Ejecutar comando
curl -X POST http://localhost:8001/api/agent/execute \
  -H "Content-Type: application/json" \
  -d '{
    "command": "Dame las estadísticas del sitio",
    "user_id": "test_user"
  }'

# 3. Ver memoria guardada
curl http://localhost:8001/api/agent/memory/test_user
```

---

## 🚀 PRÓXIMOS PASOS SUGERIDOS

1. **Frontend Web**: Panel de control para visualizar conversaciones
2. **Multi-Canal**: WhatsApp, Instagram, Facebook Messenger
3. **Herramientas Adicionales**: Email, SMS, Notificaciones Push
4. **Analytics**: Dashboard de uso del agente
5. **A/B Testing**: Experimentar con diferentes modelos
6. **Fine-tuning**: Entrenar modelo personalizado con tus datos

---

**Sistema desarrollado e implementado completamente** ✅
**Fecha:** Enero 2025
**Tecnologías:** FastAPI, MongoDB, Claude 3.5 Sonnet, OpenAI Embeddings, RAG
