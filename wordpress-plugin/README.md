# AI WooCommerce Agent - WordPress Plugin

## 🚀 Descripción

Plugin de WordPress que integra un agente AI potente para WooCommerce con Perplexity, OpenAI, bot de Telegram y 22+ herramientas integradas.

## ✨ Características Principales

- 🤖 **Agente AI con Perplexity y OpenAI**
- 📝 **Optimización automática de productos**
- 📱 **Bot de Telegram integrado**
- 🗣️ **Comandos en lenguaje natural**
- 📊 **Análisis y reportes inteligentes**
- 🔧 **22+ herramientas integradas**
- 🧠 **Sistema de memoria con RAG**
- ⚡ **Workflows automatizados**

## 💻 Requisitos

- WordPress 6.0+
- WooCommerce 7.0+
- PHP 7.4+
- Al menos una API key (Perplexity u OpenAI)

## 📦 Instalación

### Opción 1: Desde ZIP

1. Descarga `ai-woocommerce-agent.zip`
2. Ve a **Plugins > Añadir nuevo > Subir plugin**
3. Selecciona el archivo ZIP
4. Haz clic en "Instalar ahora"
5. Activa el plugin

### Opción 2: Manual

1. Descomprime el archivo
2. Sube la carpeta `ai-woocommerce-agent` a `/wp-content/plugins/`
3. Activa el plugin desde el menú Plugins

## ⚙️ Configuración

### 1. Obtener API Keys

**Perplexity (Recomendado):**
- Visita: https://perplexity.ai
- Crea una cuenta
- Genera tu API key

**OpenAI (Alternativa):**
- Visita: https://platform.openai.com
- Crea una cuenta
- Genera tu API key

**Telegram Bot (Opcional):**
- Abre Telegram
- Busca @BotFather
- Envía `/newbot`
- Sigue las instrucciones
- Guarda el token

### 2. Configurar Plugin

1. Ve a **AI Agent > Settings**
2. Ingresa tus API keys:
   - Perplexity API Key (recomendado)
   - OpenAI API Key (backup)
   - Telegram Bot Token (opcional)
   - Telegram Chat ID (opcional)
3. Selecciona tu proveedor AI preferido
4. Habilita funciones automáticas si lo deseas
5. Guarda los cambios
6. Haz clic en "Test Connection" para verificar

## 📚 Uso

### Dashboard

- Ve a **AI Agent > Dashboard**
- Ver estadísticas en tiempo real
- Acciones rápidas
- Actividad reciente

### Command Center

- Ve a **AI Agent > Command Center**
- Escribe comandos en lenguaje natural:
  - "Muéstrame productos sin precio"
  - "Optimiza el producto 123"
  - "Busca tendencias de herramientas"
  - "Analiza la competencia"

### Procesar Productos

**Opción 1: Desde edición de producto**
1. Edita cualquier producto
2. Busca "AI Optimization"
3. Clic en "Process with AI Agent"
4. Espera a que el AI optimice:
   - Descripción SEO
   - Precio óptimo
   - Imágenes (si configurado)

**Opción 2: Desde Telegram**
1. Envía: `/procesar 123` (reemplaza 123 con ID del producto)
2. O en lenguaje natural: "Optimiza el producto de taladro"

**Opción 3: Procesamiento automático**
1. Ve a Settings
2. Activa "Auto-optimize Products"
3. Todos los productos nuevos se procesaran automáticamente

### Telegram Bot

**Configurar:**
1. Ve a **AI Agent > Telegram Bot**
2. Copia la Webhook URL
3. Configura el webhook en Telegram:
   ```
   https://api.telegram.org/bot<TOKEN>/setWebhook?url=<WEBHOOK_URL>
   ```

**Comandos disponibles:**
- `/procesar [ID]` - Procesar producto
- `/ayuda` - Ver ayuda
- Lenguaje natural: "Muéstrame ventas de hoy"

## 🔧 Herramientas Disponibles

### Gestión de Productos
- Obtener lista de productos
- Procesar producto con AI
- Actualizar producto
- Buscar productos
- Optimizar descripciones
- Calcular precios óptimos
- Generar imágenes con AI

### Análisis
- Estadísticas del sitio
- Análisis de ventas
- Reportes de rendimiento
- Búsqueda de tendencias
- Análisis de competencia
- Investigación de mercado

### Automatización
- Procesamiento automático
- Workflows personalizados
- Notificaciones de Telegram
- Tareas programadas

## 💰 Costos de APIs

### Perplexity (Recomendado)
- Modelo: sonar-pro
- Costo: ~$0.001 por 1K tokens
- Acceso a web en tiempo real
- Ideal para investigación de mercado

### OpenAI
- Modelo: GPT-4o
- Costo: ~$2.50 por 1M tokens entrada
- Excelente para generación de texto
- Backup automático si Perplexity falla

### Telegram
- **Gratis**

### Estimado Mensual
- Uso ligero (10-20 productos/día): $5-10 USD
- Uso medio (50-100 productos/día): $20-40 USD
- Uso intensivo (200+ productos/día): $50-100 USD

## 🔗 Integración con Backend Standalone

Este plugin es compatible con el backend FastAPI standalone:

1. Despliega el backend standalone en tu servidor
2. En plugin settings, ingresa la Backend URL
3. El plugin usará el backend si está disponible
4. De lo contrario, usará APIs directas

## ⚠️ Problemas Comunes

### "Backend offline"
- Verifica que el Backend URL sea correcto
- O deja el campo vacío para usar APIs directas

### "API key invalid"
- Verifica que copiaste la key completa
- Sin espacios al inicio o final
- Verifica que la key no haya expirado

### "Telegram Bot not responding"
- Verifica el Bot Token
- Configura el webhook correctamente
- Verifica que el Chat ID sea correcto

### "Product not optimized"
- Verifica que tengas al menos una API key configurada
- Revisa los logs en Settings
- Intenta con otro proveedor AI

## 📝 Logs y Debug

Activar debug en WordPress:

```php
// En wp-config.php
define('WP_DEBUG', true);
define('WP_DEBUG_LOG', true);
```

Logs estarán en: `/wp-content/debug.log`

## 🔒 Privacidad y Seguridad

- Las API keys se guardan encriptadas en la base de datos
- Los datos de productos se envían a servicios externos (Perplexity/OpenAI)
- Cumple con GDPR (si configuras correctamente)
- Las imágenes generadas son almacenadas localmente

## 🌐 Idiomas Soportados

- 🇪🇸 Español (completo)
- 🇬🇧 English (complete)

## 💬 Soporte

- **Documentación**: Incluida en el plugin
- **Issues**: Crea un issue en GitHub
- **Email**: tu-email@dominio.com

## 🚀 Roadmap

### v1.1.0 (Próximamente)
- [ ] Integración con más proveedores AI
- [ ] Generación de imágenes con Fal AI
- [ ] Batch processing de productos
- [ ] Dashboard avanzado con gráficas
- [ ] Integración con WhatsApp

### v1.2.0
- [ ] Marketplace de herramientas
- [ ] Workflows visuales
- [ ] Integración con Google Analytics
- [ ] A/B testing automatizado

## 📝 Licencia

GPL v2 or later

## 👥 Créditos

- Desarrollado por: Tu Nombre
- Basado en: AI WooCommerce Agent Standalone
- Powered by: Perplexity AI, OpenAI, Telegram

---

**¡Disfruta de tu agente AI para WooCommerce! 🎉**
