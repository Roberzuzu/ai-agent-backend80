=== AI Dropshipping Manager ===
Contributors: agenteemergent
Tags: woocommerce, dropshipping, ai, automation, pricing
Requires at least: 5.8
Tested up to: 6.4
Requires PHP: 7.4
Stable tag: 1.0.0
License: GPLv2 or later
License URI: http://www.gnu.org/licenses/gpl-2.0.html

Gestión automática de productos dropshipping con IA - Calcula precios óptimos y genera contenido profesional.

== Description ==

AI Dropshipping Manager es un plugin de WordPress que automatiza completamente la gestión de tus productos de dropshipping. Calcula precios óptimos con márgenes configurables y genera contenido profesional usando inteligencia artificial.

= Características principales =

* **Cálculo automático de precios** - Aplica márgenes del 50% para productos €1-€50, 45% para €50-€100, etc.
* **Generación de contenido IA** - Crea imágenes profesionales y videos demostrativos con FAL AI Wan 2.5
* **Procesamiento en tiempo real** - Webhooks detectan productos nuevos y los procesan automáticamente
* **Cron job de respaldo** - Revisa periódicamente productos sin precio como sistema de seguridad
* **Integración con WooCommerce** - Funciona perfectamente con tu tienda existente
* **Meta box en productos** - Botones directos en cada producto para procesamiento individual

= Cómo funciona =

1. Importas productos con SharkDropship u otra herramienta de dropshipping
2. El webhook automáticamente detecta productos nuevos sin precio
3. IA calcula el precio de venta con margen óptimo
4. El producto se actualiza automáticamente y está listo para vender

= Requisitos =

* WooCommerce 5.0 o superior
* PHP 7.4 o superior
* WordPress 5.8 o superior
* Acceso a API de procesamiento (incluido en el sistema)

== Installation ==

1. Sube el plugin a la carpeta `/wp-content/plugins/ai-dropshipping-manager/`
2. Activa el plugin a través del menú 'Plugins' en WordPress
3. Ve a "AI Dropshipping" → "Configuración" para configurar la URL de API
4. Configura los webhooks siguiendo las instrucciones en la página de configuración
5. ¡Listo! Tus productos se procesarán automáticamente

== Frequently Asked Questions ==

= ¿Necesito una cuenta de IA separada? =

No, el sistema incluye acceso a FAL AI Wan 2.5 para generación de contenido.

= ¿Funciona con SharkDropship? =

Sí, funciona perfectamente con SharkDropship y cualquier otra herramienta de importación de productos.

= ¿Puedo ajustar los márgenes de ganancia? =

Los márgenes están configurados por defecto (50% para €1-€50, 45% para €50-€100, etc.) pero puedes personalizarlos en el backend.

= ¿Qué pasa si ya tengo precios configurados? =

El sistema solo procesa productos sin precio. Los productos con precios existentes no se modifican.

= ¿Cuánto tarda en procesar un producto? =

El procesamiento de precio es instantáneo (1-5 segundos). La generación de contenido IA puede tardar 1-2 minutos.

== Screenshots ==

1. Dashboard principal con estadísticas de productos
2. Meta box en productos individuales
3. Página de configuración con webhooks
4. Lista de productos sin precio
5. Procesamiento automático en acción

== Changelog ==

= 1.0.0 =
* Lanzamiento inicial
* Cálculo automático de precios con márgenes configurables
* Generación de contenido IA con FAL AI Wan 2.5
* Integración con webhooks de WooCommerce
* Meta box en productos individuales
* Dashboard con estadísticas
* Página de configuración completa

== Upgrade Notice ==

= 1.0.0 =
Primera versión del plugin. ¡Instala y automatiza tu dropshipping!

== Support ==

Para soporte técnico, visita https://herramientasyaccesorios.store/support

== Configuración de Webhooks ==

Para habilitar el procesamiento automático en tiempo real, configura estos webhooks en WooCommerce:

**Webhook 1: Product Created**
* Nombre: Product Created - AI Processing
* Estado: Activo
* Tema: product.created
* URL: https://tu-api.com/api/webhooks/woocommerce/product-created
* Secreto: wc_webhook_secret_herramientas2024

**Webhook 2: Product Updated**
* Nombre: Product Updated - AI Processing
* Estado: Activo
* Tema: product.updated
* URL: https://tu-api.com/api/webhooks/woocommerce/product-updated
* Secreto: wc_webhook_secret_herramientas2024

Consulta la documentación completa en la página de configuración del plugin.
