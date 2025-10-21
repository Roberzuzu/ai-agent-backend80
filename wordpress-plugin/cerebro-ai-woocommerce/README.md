# Cerebro AI - Plugin de WordPress para WooCommerce

🧠 Asistente de Inteligencia Artificial experto en gestión de WooCommerce.

## 📋 Descripción

Cerebro AI es un plugin revolucionario para WordPress que integra inteligencia artificial avanzada directamente en tu tienda WooCommerce. Gestiona productos, crea ofertas, optimiza tu catálogo y mucho más, todo mediante comandos en lenguaje natural.

## ✨ Características Principales

### 🛍️ Gestión de Productos
- **Análisis de imágenes**: Sube una foto de producto y Cerebro AI creará automáticamente la ficha completa
- **Creación automática**: Descripción SEO optimizada, precio sugerido, categorización
- **Optimización masiva**: Mejora todo tu catálogo con un solo comando
- **Importación desde Excel/CSV**: Carga productos en masa automáticamente

### 📊 Análisis e Inteligencia
- Estadísticas en tiempo real de tu tienda
- Análisis de competencia y precios
- Identificación de tendencias de mercado
- Recomendaciones de precios óptimos

### 💰 Marketing y Ventas
- Creación de ofertas y cupones
- Generación de contenido para redes sociales
- Campañas publicitarias automatizadas
- Optimización SEO de productos

### 🎨 Contenido y Creatividad
- Generación de descripciones profesionales
- Creación de títulos atractivos
- Contenido para blogs y emails
- Análisis de keywords

## 🚀 Instalación

### Método 1: Desde el Panel de WordPress

1. Descarga el archivo `cerebro-ai-woocommerce.zip`
2. Ve a **WordPress Admin → Plugins → Añadir nuevo**
3. Click en **Subir plugin**
4. Selecciona el archivo ZIP descargado
5. Click en **Instalar ahora**
6. **Activa** el plugin

### Método 2: Instalación Manual

1. Descomprime el archivo `cerebro-ai-woocommerce.zip`
2. Sube la carpeta `cerebro-ai-woocommerce` a `/wp-content/plugins/`
3. Ve a **WordPress Admin → Plugins**
4. **Activa** Cerebro AI

## ⚙️ Configuración

### Paso 1: Configuración Inicial

1. Ve a **Cerebro AI** en el menú de WordPress
2. Configura la **URL de la API**: 
   ```
   https://api-switcher.preview.emergentagent.com/api
   ```
   (O tu URL personalizada si tienes tu propia instalación)
3. Activa el **Chat flotante**
4. Configura los permisos (recomendado: solo administradores)
5. Guarda los cambios

### Paso 2: Verificar Funcionamiento

1. Refresca cualquier página de tu sitio
2. Verás el botón flotante de Cerebro AI en la esquina
3. Click para abrir el chat
4. Prueba con: *"Dame las estadísticas de mi tienda"*

## 📖 Uso

### Chat Flotante

El chat flotante aparece automáticamente en todas las páginas para administradores:

- **Ubicación**: Esquina inferior derecha (o izquierda, configurable)
- **Disponible para**: Administradores de WooCommerce
- **Funciones**: Comandos de texto + adjuntar archivos

### Shortcode

Inserta el chat en cualquier página o entrada:

```
[cerebro_chat]
```

Ejemplo de uso:
```
<!-- En una página de WordPress -->
<h2>Asistente de IA</h2>
<p>Pregúntale a nuestro asistente sobre productos</p>
[cerebro_chat]
```

## 💬 Ejemplos de Comandos

### Productos
```
"Crea un producto llamado 'Taladro Bosch 750W' a 89 euros"
"Actualiza el precio del producto ID 123 a 120 euros"
"Optimiza todos los productos de la categoría herramientas"
"Busca productos sin stock"
```

### Análisis
```
"Dame las estadísticas de ventas del mes"
"¿Cuáles son mis productos más vendidos?"
"Analiza la competencia en taladros"
"Busca productos tendencia en bricolaje"
```

### Marketing
```
"Crea una oferta del 20% para Black Friday"
"Genera contenido para Instagram sobre herramientas"
"Optimiza el SEO de todos mis productos"
```

### Con Archivos
```
[Adjuntar imagen] "Crea un producto con esta imagen"
[Adjuntar Excel] "Importa estos productos a mi catálogo"
[Adjuntar PDF] "Extrae los productos de este catálogo"
```

## 🔧 Requisitos

- **WordPress**: 5.8 o superior
- **PHP**: 7.4 o superior
- **WooCommerce**: 5.0 o superior
- **Permisos**: Editor de WooCommerce o Administrador

## 🛡️ Seguridad

- ✅ Solo administradores pueden usar el agente (configurable)
- ✅ Validación de permisos en todas las peticiones
- ✅ Nonces de WordPress para protección CSRF
- ✅ Sanitización de todas las entradas
- ✅ Comunicación segura con la API

## 🐛 Solución de Problemas

### El chat no aparece

1. Verifica que el plugin esté **activado**
2. Comprueba que eres **administrador de WooCommerce**
3. Asegúrate de que el chat esté **habilitado** en configuración
4. Limpia la caché de WordPress

### Error de conexión con la API

1. Verifica la **URL de la API** en configuración
2. Comprueba que la URL termine en `/api`
3. Asegúrate de tener conexión a internet
4. Contacta con soporte si el problema persiste

### Los comandos no funcionan

1. Abre la **consola del navegador** (F12)
2. Busca errores en rojo
3. Verifica que WooCommerce esté activo
4. Comprueba los permisos de tu usuario

## 📞 Soporte

- 📧 Email: support@cerebroai.com
- 📚 Documentación: https://docs.cerebroai.com
- 💬 Chat: Disponible en nuestro sitio web

## 🔄 Actualizaciones

El plugin se actualiza automáticamente desde el repositorio de WordPress. Para actualizaciones manuales:

1. Descarga la última versión
2. Desactiva el plugin actual
3. Elimina la carpeta antigua
4. Sube la nueva versión
5. Reactiva el plugin

## 📝 Changelog

### Versión 1.0.0 (2025-01-21)
- ✨ Lanzamiento inicial
- 🧠 Integración con Perplexity AI
- 📸 Análisis de imágenes con GPT-4 Vision
- 📊 Gestión completa de productos WooCommerce
- 💰 Sistema de ofertas y cupones
- 🎨 Generación de contenido
- 📈 Análisis de mercado y competencia

## 📄 Licencia

GPL v2 or later

## 👨‍💻 Autor

Desarrollado por el equipo de Cerebro AI

---

**¿Te gusta Cerebro AI?** ⭐ Déjanos una valoración de 5 estrellas en WordPress.org
