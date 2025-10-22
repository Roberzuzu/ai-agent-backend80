# AI Dropshipping Manager - Super Powered v2.0

Plugin de WordPress con **SUPER PODERES AI** para gestión automática de productos de dropshipping.

## 🚀 Características Principales

### ✨ PROCESAMIENTO COMPLETO AI
Un solo click para procesar productos con todas las funcionalidades AI:
- **Descripción SEO Profesional** - OpenRouter (Claude 3.5 Sonnet)
- **Análisis de Mercado en Tiempo Real** - Perplexity
- **Precio Óptimo Calculado** - Abacus AI
- **Generación de Imágenes** - Fal AI (Flux) + OpenAI DALL-E
- **Contenido para Redes Sociales** - Instagram, Facebook, Twitter
- **Campañas de Email Marketing** - Asuntos, contenido HTML, segmentación

### 📝 A) GENERACIÓN DE CONTENIDO
- ✅ Descripciones profesionales optimizadas para SEO
- ✅ Meta títulos y descripciones automáticas
- ✅ Keywords relevantes para posicionamiento
- ✅ Blogs y artículos sobre productos
- ✅ Contenido multilenguaje (ES/EN)

### 🖼️ B) GENERACIÓN DE IMÁGENES
- ✅ Imágenes realistas de productos con IA
- ✅ Banners promocionales automáticos
- ✅ Infografías de características
- ✅ Múltiples variaciones de imágenes
- ✅ Upload automático a WordPress Media Library

### 📊 C) ANÁLISIS DE MERCADO
- ✅ Investigación de competencia en tiempo real
- ✅ Análisis de precios óptimos
- ✅ Tendencias de búsqueda y keywords
- ✅ Predicciones de demanda
- ✅ Sugerencias de pricing strategy

### 🤖 D) AUTOMATIZACIÓN COMPLETA
- ✅ Procesamiento batch de múltiples productos
- ✅ Cola de trabajos con prioridades
- ✅ Generación de posts para redes sociales
- ✅ Templates de email marketing
- ✅ Dashboard avanzado con estadísticas

## 📦 Instalación

### Requisitos Previos
- WordPress 5.8 o superior
- WooCommerce 5.0 o superior
- PHP 7.4 o superior
- Backend FastAPI corriendo (incluido en el proyecto)

### Pasos de Instalación

1. **Subir Plugin a WordPress**
   - Comprimir la carpeta `wordpress-plugin` en un archivo ZIP
   - Ir a WordPress Admin → Plugins → Añadir Nuevo
   - Click en "Subir Plugin" → Seleccionar el archivo ZIP
   - Click en "Instalar Ahora"
   - Activar el plugin

2. **Configurar Backend API**
   - Ir a AI Dropshipping → Configuración
   - Configurar URL del backend FastAPI
   - Por defecto: `https://plugin-stability.preview.emergentagent.com/api`

3. **Verificar Conexión**
   - El plugin verificará automáticamente que todas las APIs AI estén disponibles
   - Verás un indicador de estado en el dashboard

## 🎯 Uso del Plugin

### En la Edición de Productos

Cuando edites un producto en WooCommerce, verás un nuevo meta box "🤖 AI Dropshipping" con los siguientes botones:

1. **🚀 PROCESAMIENTO COMPLETO AI**
   - Ejecuta todas las funcionalidades en un solo click
   - Genera descripción SEO + imágenes + precio óptimo + contenido social
   - Proceso tarda 2-3 minutos

2. **📝 Descripción SEO**
   - Genera descripción profesional optimizada
   - Incluye meta tags y keywords
   - Proceso tarda ~30 segundos

3. **🖼️ Generar Imágenes**
   - Crea 2 imágenes profesionales del producto
   - Las descarga y aplica automáticamente
   - Proceso tarda 1-2 minutos

4. **💰 Precio Óptimo**
   - Calcula precio basado en análisis de mercado
   - Aplica automáticamente al producto
   - Proceso tarda ~10 segundos

5. **📊 Análisis de Mercado**
   - Investiga competencia y tendencias
   - Muestra rangos de precios y keywords
   - Proceso tarda ~30 segundos

6. **📱 Contenido Social**
   - Genera posts para Instagram, Facebook, Twitter
   - Incluye hashtags y mejores horarios
   - Proceso tarda ~20 segundos

### En el Dashboard

- **Vista de productos sin precio**: Procesa múltiples productos de una vez
- **Estadísticas de uso**: Ve cuántos productos has procesado
- **Historial de generaciones AI**: Revisa el contenido generado

## 🔧 Configuración Avanzada

### API Keys

El backend ya tiene configuradas todas las APIs:
- ✅ OpenRouter (Claude 3.5 Sonnet)
- ✅ Perplexity (Búsqueda en tiempo real)
- ✅ OpenAI (GPT-4 + DALL-E 3)
- ✅ Fal AI (Flux Wan 2.5)
- ✅ Abacus AI (Análisis predictivo)

### Personalización

Puedes modificar el comportamiento editando los archivos:
- `includes/class-ai-client.php` - Cliente API
- `admin/dashboard.php` - Dashboard
- `assets/js/admin.js` - Interacciones JavaScript

## 📚 APIs Utilizadas

### OpenRouter
- **Modelo**: anthropic/claude-3.5-sonnet
- **Uso**: Generación de contenido premium, descripciones SEO
- **Ventaja**: Mejor calidad de texto, entendimiento contextual

### Perplexity
- **Modelo**: llama-3.1-sonar-large-128k-online
- **Uso**: Investigación de mercado en tiempo real
- **Ventaja**: Búsqueda web actualizada, datos actuales

### OpenAI
- **Modelos**: GPT-4 Turbo + DALL-E 3
- **Uso**: Texto alternativo y generación de imágenes
- **Ventaja**: Alta calidad, confiable

### Fal AI
- **Modelo**: flux/dev (Wan 2.5)
- **Uso**: Generación principal de imágenes
- **Ventaja**: Imágenes ultra realistas, rápido

### Abacus AI
- **Uso**: Análisis predictivo de precios y demanda
- **Ventaja**: Predicciones basadas en datos de mercado

## 🎨 Ejemplos de Uso

### Ejemplo 1: Producto Nuevo
```
1. Crear producto en WooCommerce con solo el nombre
2. Click en "🚀 PROCESAMIENTO COMPLETO AI"
3. Esperar 2-3 minutos
4. El producto ahora tiene:
   - Descripción SEO completa
   - 2 imágenes profesionales
   - Precio óptimo calculado
   - Meta tags configurados
   - Keywords relevantes
```

### Ejemplo 2: Mejorar Producto Existente
```
1. Abrir producto en edición
2. Click en "🖼️ Generar Imágenes"
3. Esperar 1-2 minutos
4. Las nuevas imágenes AI se aplican automáticamente
```

### Ejemplo 3: Análisis de Mercado
```
1. Abrir producto en edición
2. Click en "📊 Análisis de Mercado"
3. Ver resultados de:
   - Rango de precios competitivos
   - Tendencias actuales
   - Keywords recomendadas
```

## ⚠️ Notas Importantes

1. **Tiempos de Procesamiento**
   - Descripción: ~30 segundos
   - Imágenes: 1-2 minutos
   - Procesamiento completo: 2-3 minutos
   - No cerrar la página durante el procesamiento

2. **Límites de Uso**
   - Las APIs tienen límites de uso según el plan
   - Evita procesar demasiados productos simultáneamente
   - Usa "Procesamiento Completo" solo cuando sea necesario

3. **Calidad de Resultados**
   - Mejores resultados con nombres de productos descriptivos
   - Categorías bien definidas mejoran el análisis
   - Revisa el contenido generado antes de publicar

## 🐛 Solución de Problemas

### El plugin no se conecta al backend
- Verificar que el backend FastAPI esté corriendo
- Verificar la URL en Configuración
- Revisar que el puerto 8001 esté accesible

### Las imágenes no se generan
- Verificar que el producto tenga un nombre descriptivo
- Verificar que haya espacio en la media library
- Revisar permisos de escritura en WordPress

### El procesamiento tarda mucho
- Normal para "Procesamiento Completo" (2-3 minutos)
- Si tarda más de 5 minutos, recargar la página
- Verificar logs del backend para errores

## 📞 Soporte

Para soporte técnico:
- Revisar logs en: `/var/log/supervisor/backend.err.log`
- Dashboard de FastAPI: `http://localhost:8001/docs`
- Health check API: `http://localhost:8001/api/ai/health`

## 📄 Licencia

GPL v2 or later

## 👨‍💻 Autor

Agente Monetización
- Web: https://emergentagent.com
- Email: support@emergentagent.com

---

**Versión**: 2.0.0  
**Última actualización**: Octubre 2024  
**Compatible con**: WordPress 5.8+, WooCommerce 5.0+
