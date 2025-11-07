# 🚀 Venice Platform v2.0

## Plataforma de Orquestación AI con Múltiples Herramientas Integradas

**Venice Platform** es un sistema modular y escalable que actúa como orquestador central entre diferentes servicios de AI, herramientas de automatización y plataformas de e-commerce, todo conectado a través de un chat inteligente.

---

## 📋 Tabla de Contenidos

- [Arquitectura](#arquitectura)
- [Instalación](#instalación)
- [Configuración](#configuración)
- [Estructura de Archivos](#estructura-de-archivos)
- [Servicios Integrados](#servicios-integrados)
- [API Endpoints](#api-endpoints)
- [Desarrollo](#desarrollo)

---

## 🏗️ Arquitectura

### Componentes Principales

```
Venice Platform
├── Venice (Orquestador Central)
│   ├── Analiza intenciones del usuario
│   ├── Selecciona agente/servicio apropiado
│   └── Ensambla y devuelve respuestas
│
├── OpenRouter (Hub AI)
│   ├── OpenAI (GPT-4, GPT-4 Vision)
│   ├── Anthropic (Claude)
│   └── Otros modelos AI comerciales
│
├── Perplexity (Búsqueda Internet)
│   └── Agente especializado en búsquedas web
│
└── Herramientas & Servicios
    ├── n8n (Automatizaciones)
    ├── WooCommerce (E-commerce)
    ├── MongoDB (Base de datos)
    ├── Telegram Bot (Mensajería)
    └── WordPress (CMS)
```

---

## 🛠️ Instalación

### Requisitos

- Node.js >= 18.0.0
- npm >= 9.0.0
- MongoDB (local o cloud)
- Cuentas activas en: OpenRouter, Perplexity

### Pasos

```bash
# 1. Clonar repositorio
git clone https://github.com/Roberzuzu/ai-agent-backend80.git
cd ai-agent-backend80/venice-platform/backend

# 2. Instalar dependencias
npm install

# 3. Configurar variables de entorno
cp config/.env.example .env
# Editar .env con tus credenciales

# 4. Iniciar servidor de desarrollo
npm run dev

# 5. Iniciar en producción
npm start
```

---

## ⚙️ Configuración

### Variables de Entorno Esenciales

Edita el archivo `.env` con tus credenciales:

```env
PORT=8080
NODE_ENV=development

# OpenRouter (OBLIGATORIO)
OPENROUTER_API_KEY=tu_api_key
MODELO_AI_PREFERIDO=openai/gpt-4

# Perplexity (OBLIGATORIO)
SERVICE_PERPLEXITY_KEY=tu_api_key

# MongoDB (OBLIGATORIO)
SERVICE_MONGODB_URI=mongodb+srv://...

# Resto de servicios (OPCIONAL)
# Ver config/.env.example para lista completa
```

---

## 📁 Estructura de Archivos


```
venice-platform/backend/
├── index.js                 # Entry point del servidor
├── package.json             # Dependencias y scripts
├── config/
│   ├── .env.example          # Plantilla de variables de entorno
│   └── services.js           # Registro dinámico de servicios
├── controllers/
│   ├── veniceController.js   # Lógica de orquestación Venice
│   └── pluginController.js   # Interfaz con plugin WordPress
├── services/
│   ├── openrouter.js         # Cliente OpenRouter AI
│   ├── perplexity.js         # Cliente Perplexity búsqueda
│   ├── n8n.js                # Integración n8n workflows
│   ├── wooCommerce.js        # API WooCommerce
│   └── mongoDB.js            # Conexión y helpers MongoDB
├── middlewares/
│   ├── auth.js               # Autenticación y validación
│   └── logging.js            # Logs y auditoría
├── routes/
│   ├── api.js                # Rutas públicas API
│   └── internal.js           # Rutas internas (health, etc)
└── utils/
    ├── agentSelector.js      # Selector de agente AI
    └── webhookHelper.js      # Helpers para webhooks
```

### Archivos Pendientes de Crear

Los siguientes archivos deben ser creados siguiendo los patrones establecidos:

**Config:**
- `config/services.js` - Gestor de servicios dinámicos

**Controllers:**
- `controllers/veniceController.js` - Orquestador principal
- `controllers/pluginController.js` - Interfaz WordPress

**Services:**
- `services/openrouter.js` - Cliente para OpenRouter
- `services/perplexity.js` - Cliente para búsquedas
- `services/n8n.js` - Automatizaciones
- `services/wooCommerce.js` - E-commerce
- `services/mongoDB.js` - Base de datos

**Middlewares:**
- `middlewares/auth.js` - Autenticación
- `middlewares/logging.js` - Logging

**Routes:**
- `routes/api.js` - Endpoints públicos
- `routes/internal.js` - Endpoints internos

**Utils:**
- `utils/agentSelector.js` - Selección inteligente de agente
- `utils/webhookHelper.js` - Gestión de webhooks

---

## 🤖 Servicios Integrados

### 1. OpenRouter (Hub AI Principal)

**Propósito:** Gateway unificado para acceder a múltiples modelos AI comerciales.

**Modelos Disponibles:**
- `openai/gpt-4` - Generación de texto avanzada
- `openai/gpt-4-vision` - Análisis de imágenes
- `anthropic/claude-3-sonnet` - Razonamiento complejo
- Otros modelos AI disponibles vía OpenRouter

**Uso:**
```javascript
const response = await openrouter.askAI({
  model: 'openai/gpt-4',
  message: 'Tu pregunta aquí'
});
```

### 2. Perplexity (Búsqueda Internet)

**Propósito:** Agente especializado en búsquedas web en tiempo real.

**Uso:**
```javascript
const results = await perplexity.searchInternet('término de búsqueda');
```

### 3. n8n (Automatizaciones)

**Propósito:** Ejecutar workflows automatizados desde Venice.

**Uso:**
```javascript
await n8n.executeFlow({
  workflowId: '12345',
  payload: { data: 'valor' }
});
```

### 4. WooCommerce

**Propósito:** Gestionar pedidos, productos, clientes desde el chat.

**Uso:**
```javascript
const orders = await wooCommerce.getOrders({ status: 'pending' });
```

### 5. MongoDB

**Propósito:** Almacenamiento de logs, usuarios, historial de conversaciones.

---

## 🔌 API Endpoints

### Públicos

**POST /api/chat**
Enviar mensaje al orquestador Venice

```json
{
  "message": "Busca información sobre AI",
  "userId": "user123"
}
```

**Respuesta:**
```json
{
  "agent": "perplexity",
  "response": "Resultados de búsqueda..."
}
```

### Internos

**GET /internal/health**
Verificar estado del servidor

```json
{
  "status": "OK",
  "timestamp": "2025-11-07T09:00:00Z"
}
```

---

## 👨‍💻 Desarrollo

### Scripts Disponibles

```bash
npm start        # Producción
npm run dev      # Desarrollo con nodemon
npm test         # Ejecutar tests
npm run lint     # Validar código
```

### Agregar Nuevo Servicio

1. Crear archivo en `/services/nuevoServicio.js`
2. Agregar variables de entorno en `.env`
3. Registrar en `config/services.js`
4. Actualizar `utils/agentSelector.js`

### Convenciones de Código

- **Nombres de archivos:** camelCase.js
- **Funciones:** async/await preferido
- **Errores:** try/catch con mensajes descriptivos
- **Comentarios:** JSDoc para funciones públicas

---

## 🛡️ Seguridad

- Todas las rutas públicas requieren autenticación vía token
- Variables sensibles NUNCA en el código (usar .env)
- Validación de entrada en todos los endpoints
- Rate limiting en producción (recomendado)

---

## 📝 Licencia

MIT License - Roberzuzu

---

## 📞 Soporte

Para dudas o problemas:
- Issues: https://github.com/Roberzuzu/ai-agent-backend80/issues
- Email: tu_email@ejemplo.com

---

¡Gracias por usar Venice Platform! 🚀
