# 🧠 CEREBRO AI - DEPLOYMENT EN RENDER.COM (STANDALONE 24/7)

> Sistema de Inteligencia Artificial independiente de Emergent, funcionando 24/7 en Render.com

---

## 📋 ¿QUÉ HAY EN ESTE REPOSITORIO?

Este es el ecosistema completo de **Cerebro AI**, un agente inteligente basado en Claude 3.5 Sonnet con 18 herramientas integradas para gestionar tu tienda WooCommerce de forma autónoma.

### ✨ Características

- **🤖 Agente AI Autónomo:** Claude 3.5 Sonnet interpreta comandos en lenguaje natural
- **🧠 Memoria Persistente:** RAG con búsqueda semántica en MongoDB
- **🛠️ 18 Herramientas Integradas:** Gestión de productos, análisis, marketing, creatividad
- **💬 Chat Widget:** Interfaz de chat integrada en WordPress
- **🔄 Sincronización WordPress/WooCommerce:** Gestión completa de la tienda
- **📊 Análisis en Tiempo Real:** Perplexity AI para búsquedas de tendencias
- **🎨 Generación de Contenido:** Imágenes, descripciones, campañas
- **🔐 Seguro:** JWT, 2FA, rate limiting, audit logs
- **☁️ Standalone:** 100% independiente de Emergent

---

## 🗂️ ESTRUCTURA DEL PROYECTO

```
/app/
├── 📁 backend/                       # Backend FastAPI
│   ├── server.py                     # Servidor principal (18K líneas)
│   ├── ai_agent.py                   # Agente inteligente con Claude
│   ├── requirements_standalone.txt   # Dependencias sin Emergent
│   ├── llm_client.py                # Cliente LLM
│   ├── woocommerce_client.py        # Integración WooCommerce
│   ├── wordpress_integration.py     # Integración WordPress
│   ├── stripe_client.py             # Pagos con Stripe
│   ├── telegram_bot.py              # Bot de Telegram
│   └── security/                    # Sistema de seguridad
│
├── 📁 wordpress-plugin/              # Plugin WordPress
│   └── cerebro-ai-woocommerce/      # Plugin completo
│       ├── cerebro-ai.php           # Plugin principal
│       ├── assets/                  # CSS y JS
│       │   ├── admin.css
│       │   ├── chat.css
│       │   └── chat.js
│       └── templates/               # Templates PHP
│           ├── admin-page.php
│           ├── chat-widget.php
│           └── chat-inline.php
│
├── 📄 render.yaml                   # Configuración para Render.com ⭐
├── 📄 railway.toml                  # Config Railway (alternativa)
├── 📄 nixpacks.toml                 # Build config
├── 📄 Procfile                      # Start command
│
├── 📖 DEPLOYMENT_RENDER_COMPLETO.md # Guía completa de deployment ⭐
├── 📖 GUIA_API_KEYS.md             # Cómo obtener todas las API keys ⭐
├── 📖 VERIFICACION_RENDER.md       # Checklist de verificación ⭐
├── 📖 CEREBRO_AI_SISTEMA_COMPLETO.md # Documentación técnica del sistema
│
├── 🔧 diagnostico.sh               # Script de diagnóstico automatizado ⭐
├── 📦 cerebro-ai-woocommerce.zip   # Plugin WordPress listo para instalar ⭐
│
└── 📁 tests/                       # Tests automatizados
```

---

## 🚀 QUICK START (5 PASOS)

### 1️⃣ MONGODB ATLAS (5 min)

```bash
# 1. Crear cuenta en MongoDB Atlas
https://cloud.mongodb.com

# 2. Crear cluster gratuito M0 (Frankfurt)
# 3. Crear usuario: cerebro_admin
# 4. Permitir IP: 0.0.0.0/0
# 5. Copiar connection string
```

**Connection string:**
```
mongodb+srv://cerebro_admin:PASSWORD@cerebro-ai-cluster.xxxxx.mongodb.net/social_media_monetization
```

📖 **Guía detallada:** [GUIA_API_KEYS.md](GUIA_API_KEYS.md#6-mongodb-atlas)

---

### 2️⃣ OBTENER API KEYS (10 min)

Necesitas estas keys:

- ✅ **OpenRouter:** Claude 3.5 Sonnet
- ✅ **OpenAI:** Embeddings y GPT
- ✅ **Perplexity:** Búsquedas en tiempo real
- ✅ **WooCommerce:** Consumer Key + Secret
- ✅ **WordPress:** User + Application Password

📖 **Guía detallada:** [GUIA_API_KEYS.md](GUIA_API_KEYS.md)

---

### 3️⃣ DESPLEGAR EN RENDER.COM (5 min)

```bash
# 1. Login en Render
https://dashboard.render.com

# 2. Ir a tu servicio existente
https://dashboard.render.com/web/srv-d3tot4muk2gs73dbhid0

# 3. Configurar variables de entorno (Environment)
MONGO_URL=mongodb+srv://...
OPENROUTER_API_KEY=sk-or-v1-...
OPENAI_API_KEY=sk-...
PERPLEXITY_API_KEY=pplx-...
WC_URL=https://herramientasyaccesorios.store/wp-json/wc/v3
WC_KEY=ck_...
WC_SECRET=cs_...
WP_URL=https://herramientasyaccesorios.store/wp-json/wp/v2
WP_USER=agenteweb@herramientasyaccesorios.store
WP_PASS=...
SECRET_KEY=genera-clave-segura-32-caracteres
ENVIRONMENT=production

# 4. Manual Deploy → Deploy latest commit
# 5. Esperar 5-8 minutos
```

**Tu backend estará en:**
```
https://cerebro-ai-backend-XXXX.onrender.com
```

📖 **Guía detallada:** [DEPLOYMENT_RENDER_COMPLETO.md](DEPLOYMENT_RENDER_COMPLETO.md)

---

### 4️⃣ INSTALAR PLUGIN EN WORDPRESS (3 min)

```bash
# 1. Descargar plugin
/app/cerebro-ai-woocommerce.zip

# 2. WordPress Admin → Plugins → Añadir nuevo → Subir plugin
https://herramientasyaccesorios.store/wp-admin/plugin-install.php

# 3. Seleccionar ZIP e instalar
# 4. Activar plugin
```

📖 **Guía detallada:** [DEPLOYMENT_RENDER_COMPLETO.md](DEPLOYMENT_RENDER_COMPLETO.md#-paso-4-instalar-plugin-en-wordpress-5-minutos)

---

### 5️⃣ CONFIGURAR Y PROBAR (2 min)

```bash
# 1. WordPress → Cerebro AI → Configuración
URL de API: https://cerebro-ai-backend-XXXX.onrender.com/api

# 2. Guardar cambios

# 3. Ir a cualquier página de tu sitio
# 4. Verás el botón flotante de Cerebro AI (esquina inferior derecha)

# 5. Click y probar comando:
"Dame las estadísticas de mi tienda"
```

---

## 🧪 VERIFICAR DEPLOYMENT

### Opción 1: Script Automatizado (Recomendado)

```bash
bash /app/diagnostico.sh https://cerebro-ai-backend-XXXX.onrender.com
```

Este script verifica:
- ✅ Conectividad
- ✅ Health check
- ✅ Status del agente (18 herramientas)
- ✅ Memoria persistente
- ✅ Ejecución de comandos
- ✅ Tiempos de respuesta
- ✅ CORS y seguridad

---

### Opción 2: Tests Manuales

```bash
# Test 1: Health Check
curl https://TU-URL.onrender.com/api/health

# Debe retornar:
# {"status":"healthy","services":{"database":"connected","ai":"available"}}

# Test 2: Status del Agente
curl -X POST https://TU-URL.onrender.com/api/agent/status

# Debe retornar:
# {"success":true,"herramientas_disponibles":18,...}

# Test 3: Comando de Prueba
curl -X POST https://TU-URL.onrender.com/api/agent/execute \
  -H "Content-Type: application/json" \
  -d '{"command":"Hola","user_id":"test"}'
```

📖 **Checklist completo:** [VERIFICACION_RENDER.md](VERIFICACION_RENDER.md)

---

## 📖 DOCUMENTACIÓN COMPLETA

### 🎯 Para Despliegue

| Documento | Descripción | Tiempo |
|-----------|-------------|--------|
| **[DEPLOYMENT_RENDER_COMPLETO.md](DEPLOYMENT_RENDER_COMPLETO.md)** | Guía paso a paso completa | 30 min |
| **[GUIA_API_KEYS.md](GUIA_API_KEYS.md)** | Cómo obtener todas las API keys | 15 min |
| **[VERIFICACION_RENDER.md](VERIFICACION_RENDER.md)** | Checklist de verificación completo | 10 min |

### 🛠️ Para Uso y Mantenimiento

| Documento | Descripción |
|-----------|-------------|
| **[CEREBRO_AI_SISTEMA_COMPLETO.md](CEREBRO_AI_SISTEMA_COMPLETO.md)** | Documentación técnica completa del sistema |
| **[INSTALACION_PLUGIN.md](INSTALACION_PLUGIN.md)** | Instalación del plugin WordPress |
| **[API_EXAMPLES.md](API_EXAMPLES.md)** | Ejemplos de uso de la API |

---

## 💬 CASOS DE USO

### Comandos de Productos

```
"Busca 10 herramientas eléctricas tendencia"
"Crea un producto llamado Taladro Bosch 750W a 89 euros"
"Actualiza el precio del producto ID 123 a 120 euros"
"Optimiza todos los productos sin descripción"
```

### Análisis y Estadísticas

```
"Dame las estadísticas de ventas del mes"
"¿Cuáles son mis productos más vendidos?"
"Analiza la competencia en taladros Bosch"
"Productos sin stock"
```

### Marketing

```
"Crea una oferta del 20% para Black Friday"
"Genera contenido para Instagram sobre herramientas"
"Optimiza el SEO de todos mis productos"
"Crea una campaña publicitaria para el producto 4146"
```

### Con Archivos

```
[Adjuntar imagen] "Crea un producto con esta imagen"
[Adjuntar Excel] "Importa estos productos"
[Adjuntar PDF] "Extrae productos de este catálogo"
```

---

## 🛠️ HERRAMIENTAS INTEGRADAS (18)

### Productos (7)
1. `procesar_producto` - Procesa productos con AI
2. `crear_producto` - Crea nuevos productos
3. `actualizar_producto` - Actualiza productos
4. `eliminar_producto` - Elimina productos
5. `obtener_productos` - Lista productos
6. `buscar_productos` - Búsqueda avanzada
7. `gestionar_inventario` - Gestión masiva

### Análisis (5)
8. `buscar_tendencias` - Tendencias con Perplexity
9. `analizar_precios` - Precios óptimos con Abacus
10. `analizar_competencia` - Análisis competitivo
11. `obtener_estadisticas` - Métricas del sitio
12. `analizar_ventas` - Reportes de ventas

### Marketing (3)
13. `crear_campana` - Campañas publicitarias
14. `crear_descuento` - Cupones y promociones
15. `generar_contenido` - Blogs, emails, posts

### Creatividad (1)
16. `generar_imagenes` - Imágenes con Fal AI

### Integraciones (2)
17. `sincronizar_wordpress` - Sync con WordPress
18. `optimizar_seo` - Optimización SEO

---

## 🔧 TROUBLESHOOTING

### Backend no arranca

```bash
# Verificar logs en Render
https://dashboard.render.com/web/srv-d3tot4muk2gs73dbhid0/logs

# Buscar errores tipo:
# - "ModuleNotFoundError" → Dependencia faltante
# - "Connection refused" → MongoDB no conectado
# - "Invalid API key" → Verificar variables de entorno
```

### Database connection failed

```bash
# 1. Verificar MONGO_URL en Render
# 2. Probar connection string:
mongosh "tu-connection-string"

# 3. Verificar Network Access en MongoDB Atlas
# 4. Verificar usuario y contraseña
```

### Chat no aparece en WordPress

```bash
# 1. Verificar que estás logueado como admin
# 2. Verificar plugin activado: Plugins → Cerebro AI
# 3. Verificar configuración: Cerebro AI → Configuración
# 4. Limpiar caché de WordPress
# 5. Abrir consola del navegador (F12) y buscar errores
```

### Comandos no funcionan

```bash
# 1. Verificar URL de API en configuración del plugin
#    Debe ser: https://TU-URL.onrender.com/api (sin barra final)

# 2. Probar endpoint manualmente:
curl https://TU-URL.onrender.com/api/health

# 3. Verificar logs de Render para ver si llegan requests

# 4. Verificar API keys en variables de entorno
```

📖 **Solución detallada:** [VERIFICACION_RENDER.md](VERIFICACION_RENDER.md#-problemas-comunes-y-soluciones)

---

## 💰 COSTOS ESTIMADOS

### Infraestructura (Fijo)

| Servicio | Plan | Costo |
|----------|------|-------|
| Render.com | Free | $0/mes |
| Render.com | Starter | $7/mes ✅ |
| MongoDB Atlas | M0 Free | $0/mes ✅ |

### APIs de IA (Variable según uso)

| Servicio | Costo por uso | 100 comandos/día |
|----------|---------------|------------------|
| OpenRouter (Claude) | $0.003/comando | ~$9/mes |
| OpenAI (Embeddings) | $0.0001/búsqueda | ~$0.30/mes |
| Perplexity (Búsquedas) | $0.002/búsqueda | ~$6/mes |
| **TOTAL** | - | **~$15/mes** |

### Total Estimado

- **🟢 Bajo uso (10-50 comandos/día):** $7-15/mes
- **🟡 Uso medio (50-200 comandos/día):** $15-40/mes
- **🔴 Alto uso (200-1000 comandos/día):** $40-150/mes

---

## ⚡ PERFORMANCE

### Tiempos de Respuesta

| Operación | Tiempo Esperado |
|-----------|-----------------|
| Health Check | < 1 segundo |
| Comando simple | 2-5 segundos |
| Búsqueda de tendencias | 5-10 segundos |
| Análisis de competencia | 8-15 segundos |
| Generación de imágenes | 30-60 segundos |

### Uso de Recursos (Render Starter)

| Recurso | Uso Típico |
|---------|------------|
| CPU | 20-40% en idle |
| RAM | 250-400 MB |
| Requests/min | Variable |

---

## 🔒 SEGURIDAD

### Implementado

- ✅ **HTTPS:** Automático en Render
- ✅ **JWT Authentication:** Tokens seguros
- ✅ **Rate Limiting:** Protección contra abuse
- ✅ **CORS:** Configurado correctamente
- ✅ **API Key Management:** Keys en variables de entorno
- ✅ **Input Validation:** Pydantic models
- ✅ **2FA:** Autenticación de dos factores (opcional)
- ✅ **Audit Logs:** Registro de todas las acciones
- ✅ **WordPress Nonces:** Protección CSRF

---

## 🆘 SOPORTE

### Logs y Monitoring

- **Logs de Render:** https://dashboard.render.com/web/srv-d3tot4muk2gs73dbhid0/logs
- **Métricas:** https://dashboard.render.com/web/srv-d3tot4muk2gs73dbhid0/metrics
- **MongoDB Atlas:** https://cloud.mongodb.com

### Recursos

- **Documentación completa:** Ver archivos `.md` en este repo
- **Script de diagnóstico:** `bash diagnostico.sh`
- **Tests automatizados:** `/app/tests/`

---

## 📊 STATUS DEL PROYECTO

- ✅ Backend completamente funcional
- ✅ 18 herramientas integradas
- ✅ Memoria persistente con RAG
- ✅ Plugin WordPress listo para producción
- ✅ Documentación completa
- ✅ Scripts de verificación automatizados
- ✅ Standalone (sin dependencias de Emergent)

---

## 🎯 PRÓXIMOS PASOS SUGERIDOS

1. **Actualizar a plan de pago en Render** ($7/mes) para evitar sleep
2. **Configurar dominio personalizado** (api.herramientasyaccesorios.store)
3. **Activar monitoring** (UptimeRobot o Sentry)
4. **Configurar backups automáticos** en MongoDB Atlas
5. **Añadir más herramientas** según necesidades
6. **Integrar más canales** (WhatsApp, Instagram, FB Messenger)

---

## 🎉 ¡LISTO!

Con esta configuración, **Cerebro AI** funcionará 24/7 de forma completamente independiente de Emergent, gestionando tu tienda WooCommerce de forma autónoma.

### Quick Links

- 🚀 [Guía de Deployment Completa](DEPLOYMENT_RENDER_COMPLETO.md)
- 🔑 [Obtener API Keys](GUIA_API_KEYS.md)
- ✅ [Checklist de Verificación](VERIFICACION_RENDER.md)
- 🧪 [Script de Diagnóstico](diagnostico.sh)
- 📦 [Plugin WordPress](cerebro-ai-woocommerce.zip)

---

**Desarrollado con ❤️ para funcionar 24/7 en Render.com**

*Última actualización: Enero 2025*
