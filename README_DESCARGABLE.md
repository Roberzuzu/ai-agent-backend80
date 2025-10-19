# 🚀 Sistema Completo de Dropshipping con IA

[![Version](https://img.shields.io/badge/version-4.0.0-blue.svg)](https://github.com/tu-repo)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.11+-yellow.svg)](https://python.org)
[![Node](https://img.shields.io/badge/node-18+-green.svg)](https://nodejs.org)

> Sistema empresarial completo para dropshipping automatizado con generación de contenido IA, pagos con Stripe, programa de afiliados, analytics avanzados y más.

---

## ✨ Características Principales

### 💼 **Core del Negocio**
- ✅ **Dropshipping Automatizado** - Calcula precios, genera contenido, actualiza productos
- ✅ **Integración WooCommerce** - Gestión completa de productos y órdenes
- ✅ **Sistema de Pagos Stripe** - Productos individuales y suscripciones recurrentes
- ✅ **Programa de Afiliados** - Tracking, comisiones automáticas, dashboard

### 🎨 **Generación de Contenido IA**
- ✅ **FAL AI Wan 2.5** - Genera imágenes y videos de productos
- ✅ **Text-to-Image** - Imágenes profesionales desde descripciones
- ✅ **Text-to-Video** - Videos demostrativos automáticos (hasta 1080p)
- ✅ **Contenido para Redes Sociales** - Instagram, TikTok, Facebook

### 📊 **Analytics y Reporting**
- ✅ **Dashboard Avanzado** - Revenue, MRR, ROI por campaña
- ✅ **Gráficos Interactivos** - Chart.js con múltiples visualizaciones
- ✅ **Analytics de Afiliados** - Comisiones, clicks, conversiones
- ✅ **Métricas en Tiempo Real** - Prometheus + Grafana

### 🔒 **Seguridad Enterprise**
- ✅ **Rate Limiting Avanzado** - Protección contra abuso
- ✅ **2FA (TOTP)** - Autenticación de dos factores
- ✅ **API Key Management** - Genera, rota y gestiona keys
- ✅ **Audit Logs** - Tracking completo de acciones
- ✅ **IP Whitelisting** - Restricción de acceso admin

### 🛠️ **DevOps y Monitoring**
- ✅ **Docker Compose** - Deploy con un comando
- ✅ **CI/CD con GitHub Actions** - Tests y deploy automático
- ✅ **Health Checks** - Liveness y readiness probes
- ✅ **Sistema de Backups** - Automáticos con retención configurable
- ✅ **Logging Estructurado** - JSON logs con rotación

---

## 🎯 ¿Para Quién es Este Sistema?

✔️ **Emprendedores de eCommerce** que quieren dropshipping automatizado
✔️ **Agencies de Marketing** que necesitan generar contenido rápido
✔️ **Desarrolladores** que quieren una base sólida para proyectos SaaS
✔️ **Negocios Online** que buscan escalar con automatización

---

## 📦 Descarga e Instalación

### Opción 1: Descarga Directa (Recomendado)

1. **Descarga el proyecto completo:**
   - [Descargar ZIP](https://github.com/tu-usuario/tu-repo/archive/refs/heads/main.zip)

2. **Extrae el archivo** en tu carpeta deseada

3. **Ejecuta el instalador:**

   **Windows:**
   ```bash
   install-windows.bat
   ```

   **macOS/Linux:**
   ```bash
   chmod +x install-mac-linux.sh
   ./install-mac-linux.sh
   ```

4. **Edita el archivo `.env`** con tus credenciales

5. **Inicia el sistema:**
   ```bash
   docker-compose up -d
   ```

6. **Accede a:** http://localhost:3000

**Tiempo de instalación:** 5-10 minutos

---

### Opción 2: Con Git

```bash
git clone https://github.com/tu-usuario/tu-repo.git
cd tu-repo
chmod +x install-mac-linux.sh
./install-mac-linux.sh
docker-compose up -d
```

---

## 🚀 Inicio Rápido (3 Pasos)

### 1. Configurar Variables de Entorno

Copia `.env.example` a `.env` y configura:

```bash
# Mínimo necesario
MONGO_URL=mongodb://localhost:27017
DB_NAME=mi_tienda_db
SECRET_KEY=cambia-esto-por-algo-seguro

# Opcional - FAL AI (ya configurado)
FAL_API_KEY=tu_clave_aqui

# Opcional - Stripe
STRIPE_API_KEY=sk_test_...
STRIPE_PUBLISHABLE_KEY=pk_test_...

# Opcional - WooCommerce
WORDPRESS_URL=https://tu-tienda.com
WC_CONSUMER_KEY=ck_...
WC_CONSUMER_SECRET=cs_...
```

### 2. Iniciar Servicios

```bash
docker-compose up -d
```

### 3. Acceder

- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:8001/api
- **Docs API:** http://localhost:8001/docs
- **Grafana:** http://localhost:3001

---

## 💰 Casos de Uso

### Caso 1: Dropshipping Básico

```bash
# 1. Importa productos con SharkDropship
# 2. Procesa todos automáticamente:
curl -X POST http://localhost:8001/api/dropshipping/process-all

# El sistema calcula precios óptimos y actualiza tu tienda
```

### Caso 2: Generar Contenido IA

```bash
# Genera imagen de producto
curl -X POST http://localhost:8001/api/ai/generate-image \
-H "Content-Type: application/json" \
-d '{"prompt": "Professional hammer photo, white background"}'

# Genera video demostrativo
curl -X POST http://localhost:8001/api/ai/generate-video \
-H "Content-Type: application/json" \
-d '{"prompt": "Hammer demonstration video"}'
```

### Caso 3: Marketing en Redes Sociales

```bash
# Genera contenido para Instagram, TikTok, Facebook
curl -X POST http://localhost:8001/api/dropshipping/social-media/123 \
-H "Content-Type: application/json" \
-d '{"platforms": ["instagram", "tiktok", "facebook"]}'
```

---

## 📊 Dashboard y Analytics

El sistema incluye:

- **Dashboard Principal** con métricas clave
- **Revenue Tracking** con MRR y proyecciones
- **ROI por Campaña** publicitaria
- **Comisiones de Afiliados** en tiempo real
- **Gráficos Interactivos** con Chart.js
- **Exportación de Datos** (CSV, PDF próximamente)

Accede a: http://localhost:3000/dashboard

---

## 🎨 Generación de Contenido IA

Powered by **FAL AI Wan 2.5**, genera automáticamente:

### Imágenes
- Fotos profesionales de productos
- Banners promocionales
- Imágenes para redes sociales
- Resolución hasta 2048x2048

### Videos
- Demos de productos (5-30 segundos)
- Videos para TikTok/Instagram
- Ads para Facebook
- Resolución hasta 1080p

### Uso:
```bash
# Procesar un producto completo con contenido IA
curl -X POST http://localhost:8001/api/dropshipping/process-product/123 \
-H "Content-Type: application/json" \
-d '{"supplier_price": 25.00, "generate_content": true}'
```

---

## 💳 Sistema de Pagos

### Stripe Integration

Acepta pagos con:
- Tarjetas de crédito/débito
- Apple Pay / Google Pay
- SEPA Direct Debit
- Y más...

### Suscripciones Recurrentes

3 planes pre-configurados:
- **Basic:** €9.99/mes
- **Pro:** €29.99/mes
- **Enterprise:** €99.99/mes

### Webhooks

Procesamiento automático de:
- Pagos completados
- Suscripciones renovadas
- Pagos fallidos
- Cancelaciones

---

## 🔒 Seguridad

### Features de Seguridad

- **Rate Limiting:** Protección contra abuso y DDoS
- **2FA (TOTP):** Autenticación de dos factores con QR
- **API Keys:** Sistema completo de gestión
- **Audit Logs:** Tracking de todas las acciones
- **IP Whitelist:** Restricción de acceso admin
- **CORS:** Configuración estricta
- **Headers de Seguridad:** Helmet.js equivalent
- **Encryption:** Passwords hasheados con bcrypt

---

## 📈 Proyección de Ingresos

### Escenario Conservador (29 productos)
- Precio promedio: €50
- Margen: 50% = €25 profit/venta
- 10 ventas/día = €250 profit/día
- **€7,500/mes profit**

### Con Marketing IA (contenido optimizado)
- Conversión +30%
- 15 ventas/día = €375 profit/día
- **€11,250/mes profit**

### Con Escalado (100 productos + ads)
- 50 ventas/día = €1,250 profit/día
- **€37,500/mes profit**

---

## 🛠️ Stack Tecnológico

### Backend
- **FastAPI** - API moderna y rápida
- **Python 3.11+** - Lenguaje principal
- **MongoDB** - Base de datos NoSQL
- **Motor** - Driver async de MongoDB
- **Stripe SDK** - Procesamiento de pagos
- **FAL AI SDK** - Generación de contenido

### Frontend
- **React 18** - UI moderna
- **TailwindCSS** - Styling utility-first
- **Chart.js** - Gráficos interactivos
- **Axios** - HTTP client
- **React Router** - Navegación

### DevOps
- **Docker & Docker Compose** - Containerización
- **GitHub Actions** - CI/CD
- **Prometheus** - Métricas
- **Grafana** - Visualización
- **MongoDB Tools** - Backups

---

## 📚 Documentación

- **[INSTALACION_COMPLETA.md](INSTALACION_COMPLETA.md)** - Guía detallada de instalación
- **[GUIA_RAPIDA.md](GUIA_RAPIDA.md)** - Inicio en 10 minutos
- **[INVENTARIO_COMPLETO.md](INVENTARIO_COMPLETO.md)** - Lista de todas las features
- **[CONFIGURACION_ENV_COMPLETA.md](CONFIGURACION_ENV_COMPLETA.md)** - Variables de entorno
- **[backend/README_DATABASE.md](backend/README_DATABASE.md)** - Optimización de BD

---

## 🤝 Soporte

¿Necesitas ayuda?

- **Email:** soporte@tuapp.com
- **Discord:** [Unirse al servidor]
- **Telegram:** @tusistema
- **Documentación:** [Ver docs completos]

---

## 📝 Licencia

Este proyecto está bajo la licencia MIT. Ver [LICENSE](LICENSE) para más detalles.

---

## 🎉 Contribuir

¡Las contribuciones son bienvenidas!

1. Fork el proyecto
2. Crea tu feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push al branch (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

---

## 📊 Estadísticas del Proyecto

- **Endpoints:** 83+
- **Líneas de Código:** ~25,000+
- **Archivos:** 100+
- **Tests:** Automáticos con CI/CD
- **Uptime:** 99.9% (con monitoring)

---

## 🌟 Features Próximas

- [ ] Multi-idioma (i18n) - ES, EN, PT
- [ ] Exportar reportes PDF
- [ ] Calendario visual para scheduling
- [ ] Competitor analysis
- [ ] Sentiment analysis
- [ ] Chatbot de soporte
- [ ] Video tutorials integrados
- [ ] Marketplace de templates

---

## 💡 Hecho con

- ❤️ Pasión
- ☕ Café
- 🤖 IA (FAL AI Wan 2.5)
- 🎨 Creatividad
- 💪 Trabajo duro

---

**⭐ Si te gusta este proyecto, dale una estrella en GitHub!**

**🚀 ¡Empieza a generar ingresos hoy mismo!**
