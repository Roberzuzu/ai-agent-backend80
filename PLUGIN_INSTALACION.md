# 🚀 Plugin AI Dropshipping Manager - Instalación Actualizada

## ✅ API Actualizada

La API del plugin ha sido actualizada a:
```
https://backend-connect-21.preview.emergentagent.com/api
```

## 📦 Información del Plugin

**Versión:** 1.1.0  
**Nombre:** AI Dropshipping Manager  
**Descripción:** Gestión automática de productos dropshipping con IA

### Cambios en v1.1.0
- ✅ API URL actualizada a: `https://backend-connect-21.preview.emergentagent.com/api`
- ✅ Conexión configurada automáticamente al instalar
- ✅ Compatible con WooCommerce 5.0+
- ✅ Procesamiento automático de precios con margen del 50%
- ✅ Generación de contenido e imágenes con IA

---

## 📥 Método 1: Descargar e Instalar Manualmente

### Paso 1: Descargar el Plugin

Opción A - Desde el navegador:
```
https://backend-connect-21.preview.emergentagent.com/api/wordpress/plugin/download
```

Opción B - Desde la terminal:
```bash
curl -o ai-dropshipping-manager.zip \
  https://backend-connect-21.preview.emergentagent.com/api/wordpress/plugin/download
```

### Paso 2: Instalar en WordPress

1. Ve a tu WordPress Admin: https://herramientasyaccesorios.store/wp-admin
2. Navega a: **Plugins → Añadir nuevo**
3. Click en: **Subir plugin**
4. Selecciona el archivo `ai-dropshipping-manager.zip`
5. Click en: **Instalar ahora**
6. Click en: **Activar plugin**

### Paso 3: Verificar Configuración

1. Ve a: **AI Dropshipping → Configuración**
2. Verifica que la URL de API sea:
   ```
   https://backend-connect-21.preview.emergentagent.com/api
   ```
3. Guarda los cambios si es necesario

---

## ⚡ Método 2: Instalación Directa (Requiere FTP/SSH)

Si tienes acceso SSH o FTP a tu servidor WordPress:

```bash
# Conectar a tu servidor
cd /path/to/wordpress/wp-content/plugins/

# Descargar y descomprimir
wget https://backend-connect-21.preview.emergentagent.com/api/wordpress/plugin/download \
  -O ai-dropshipping-manager.zip

unzip ai-dropshipping-manager.zip -d ai-dropshipping-manager/

# Establecer permisos correctos
chown -R www-data:www-data ai-dropshipping-manager/
chmod -R 755 ai-dropshipping-manager/

# Eliminar zip
rm ai-dropshipping-manager.zip
```

Luego activa el plugin desde WordPress Admin.

---

## 🎯 ¿Qué hace el Plugin?

### 1. **Cálculo Automático de Precios**
- Aplica margen del 50% sobre precio de proveedor
- Calcula precio de venta óptimo
- Actualiza automáticamente en WooCommerce

### 2. **Generación de Contenido IA**
- Genera descripciones profesionales
- Crea imágenes de productos con IA
- Genera videos promocionales (próximamente)

### 3. **Procesamiento Masivo**
- Procesa todos los productos sin precio
- Actualización automática vía webhooks
- Dashboard con estadísticas en tiempo real

### 4. **Integración Completa**
- Sincronización bidireccional con WooCommerce
- API REST completa
- Webhooks para actualizaciones automáticas

---

## 🔧 Configuración Avanzada

### Webhooks de WooCommerce

Para habilitar el procesamiento automático en tiempo real:

1. Ve a: **WooCommerce → Ajustes → Avanzado → Webhooks**

2. Crea webhook "Product Created":
   - **Nombre:** Product Created - AI Processing
   - **Estado:** Activo
   - **Tema:** product.created
   - **URL de entrega:** 
     ```
     https://backend-connect-21.preview.emergentagent.com/api/webhooks/woocommerce/product-created
     ```
   - **Secreto:** `wc_webhook_secret_herramientas2024`

3. Crea webhook "Product Updated":
   - **Nombre:** Product Updated - AI Processing
   - **Estado:** Activo
   - **Tema:** product.updated
   - **URL de entrega:** 
     ```
     https://backend-connect-21.preview.emergentagent.com/api/webhooks/woocommerce/product-updated
     ```
   - **Secreto:** `wc_webhook_secret_herramientas2024`

---

## 🎮 Cómo Usar el Plugin

### Opción 1: Procesar un producto individual

1. Ve a: **Productos → Todos los productos**
2. Edita cualquier producto
3. En el lateral derecho, verás el box **"🤖 AI Dropshipping"**
4. Click en: **"Calcular Precio Óptimo"** para actualizar precio
5. Click en: **"Generar Contenido IA"** para crear imágenes/descripción

### Opción 2: Procesamiento masivo

1. Ve a: **AI Dropshipping → Dashboard**
2. Click en: **"Procesar Todos los Productos Sin Precio"**
3. El sistema procesará automáticamente todos los productos

---

## 📊 Dashboard del Plugin

El dashboard muestra:

- ✅ Total de productos en WooCommerce
- ✅ Productos sin precio configurado
- ✅ Productos procesados por IA
- ✅ Estadísticas de ingresos estimados
- ✅ Gráficos de performance

---

## 🔍 Verificar que funciona

### Test 1: Verificar conexión API

```bash
curl https://backend-connect-21.preview.emergentagent.com/api/
```

Debería responder con información de la API.

### Test 2: Verificar plugin en WordPress

1. Ve a: **Plugins → Plugins instalados**
2. Busca: **AI Dropshipping Manager**
3. Estado debe ser: **Activado**

### Test 3: Procesar un producto de prueba

1. Crea un producto de prueba sin precio
2. En el editor del producto, verás el box AI Dropshipping
3. Click en "Calcular Precio Óptimo"
4. Verifica que se actualice el precio automáticamente

---

## ❓ Preguntas Frecuentes

### ¿El plugin es gratuito?
Sí, el plugin es totalmente gratuito. Solo necesitas tener WooCommerce instalado.

### ¿Necesito configurar la API manualmente?
No, el plugin v1.1.0 ya viene configurado con la API correcta.

### ¿Qué pasa si cambio la URL de la API?
Puedes cambiarla en: **AI Dropshipping → Configuración → URL de API**

### ¿Los precios se actualizan automáticamente?
Sí, si configuras los webhooks de WooCommerce. Si no, puedes procesarlos manualmente desde el dashboard.

### ¿Genera imágenes reales con IA?
Sí, utiliza modelos de IA avanzados para generar imágenes profesionales de productos.

---

## 🆘 Soporte y Problemas

### Si el plugin no aparece después de instalarlo:
1. Verifica que el archivo ZIP se descargó completamente
2. Asegúrate de que WooCommerce esté instalado y activado
3. Revisa los permisos de archivos en el servidor

### Si dice "API no disponible":
1. Verifica tu conexión a internet
2. Comprueba que la URL sea: `https://backend-connect-21.preview.emergentagent.com/api`
3. Prueba acceder a la URL directamente desde el navegador

### Si no procesa los productos:
1. Ve a: **AI Dropshipping → Configuración**
2. Verifica que "Procesamiento automático" esté activado
3. Revisa los logs del servidor para errores

---

## 📝 Notas Importantes

- ✅ Requiere WordPress 5.8+
- ✅ Requiere WooCommerce 5.0+
- ✅ Requiere PHP 7.4+
- ✅ La generación de imágenes consume recursos de IA
- ✅ Se recomienda usar en productos importantes primero

---

## 🎉 ¡Todo Listo!

Tu plugin AI Dropshipping Manager está actualizado y listo para usar con la nueva API.

**URL de descarga:**  
https://backend-connect-21.preview.emergentagent.com/api/wordpress/plugin/download

**Versión:** 1.1.0  
**Última actualización:** Octubre 2025
