# 🚀 AI DROPSHIPPING MANAGER - GUÍA DE INSTALACIÓN

## 📦 PLUGIN DE WORDPRESS

**Versión:** 1.0.0  
**Autor:** Agente Monetización  
**Requisitos:** WordPress 5.8+, WooCommerce 5.0+, PHP 7.4+

---

## 📥 DESCARGAR EL PLUGIN

El archivo ZIP del plugin está disponible en:
```
/app/ai-dropshipping-manager.zip
```

**Tamaño:** 16KB  
**Archivos incluidos:** 9 archivos PHP, CSS y JS

---

## 🔧 INSTALACIÓN

### **Método 1: Desde WordPress Admin (Recomendado)**

1. **Descarga el archivo:** `ai-dropshipping-manager.zip`

2. **En WordPress:**
   - Ve a: `Plugins` → `Añadir nuevo`
   - Click en `Subir plugin`
   - Selecciona `ai-dropshipping-manager.zip`
   - Click en `Instalar ahora`
   - Click en `Activar plugin`

3. **¡Listo!** Verás "AI Dropshipping" en el menú lateral

---

### **Método 2: Por FTP/SFTP**

1. **Descomprimir el ZIP**
   ```bash
   unzip ai-dropshipping-manager.zip
   ```

2. **Subir por FTP:**
   - Conecta a tu servidor FTP
   - Navega a: `/wp-content/plugins/`
   - Sube la carpeta `wordpress-plugin` y renómbrala a `ai-dropshipping-manager`

3. **Activar en WordPress:**
   - Ve a: `Plugins`
   - Busca "AI Dropshipping Manager"
   - Click en `Activar`

---

### **Método 3: SSH/Terminal**

```bash
# Conectar a tu servidor
ssh usuario@herramientasyaccesorios.store

# Ir al directorio de plugins
cd /ruta/a/wordpress/wp-content/plugins/

# Descargar (si tienes acceso al archivo)
wget https://tu-servidor.com/ai-dropshipping-manager.zip

# Descomprimir
unzip ai-dropshipping-manager.zip

# Renombrar carpeta
mv wordpress-plugin ai-dropshipping-manager

# Ajustar permisos
chmod -R 755 ai-dropshipping-manager
chown -R www-data:www-data ai-dropshipping-manager

# Activar desde WordPress admin
```

---

## ⚙️ CONFIGURACIÓN POST-INSTALACIÓN

### **Paso 1: Configurar URL de API**

1. Ve a: `AI Dropshipping` → `Configuración`

2. **URL de API:**
   ```
   https://api-switcher.preview.emergentagent.com/api
   ```
   
3. **Opciones:**
   - ✅ Marcar: "Procesar automáticamente productos sin precio"
   - ⚠️ Opcional: "Generar imágenes y videos automáticamente" (consume recursos IA)

4. Click en **Guardar cambios**

---

### **Paso 2: Configurar Webhooks en WooCommerce**

#### **Webhook 1: Product Created**

1. Ve a: `WooCommerce` → `Ajustes` → `Avanzado` → `Webhooks`

2. Click en **Añadir webhook**

3. Configura:
   - **Nombre:** `Product Created - AI Processing`
   - **Estado:** `Activo` ✅
   - **Tema:** `product.created`
   - **URL de entrega:**
     ```
     https://api-switcher.preview.emergentagent.com/api/webhooks/woocommerce/product-created
     ```
   - **Secreto:**
     ```
     wc_webhook_secret_herramientas2024
     ```
   - **Versión API:** `WP REST API v3`

4. Click en **Guardar webhook**

---

#### **Webhook 2: Product Updated**

1. Click en **Añadir webhook** (de nuevo)

2. Configura:
   - **Nombre:** `Product Updated - AI Processing`
   - **Estado:** `Activo` ✅
   - **Tema:** `product.updated`
   - **URL de entrega:**
     ```
     https://api-switcher.preview.emergentagent.com/api/webhooks/woocommerce/product-updated
     ```
   - **Secreto:**
     ```
     wc_webhook_secret_herramientas2024
     ```

3. Click en **Guardar webhook**

---

### **Paso 3: Verificar Instalación**

1. Ve a: `AI Dropshipping` → `Dashboard`

2. Deberías ver:
   - ✅ Estadísticas de productos
   - ✅ Total de productos
   - ✅ Productos con/sin precio
   - ✅ Botón "Procesar Todos"

3. **Probar en un producto:**
   - Ve a: `Productos` → Editar cualquier producto
   - En el sidebar derecho verás: **🤖 AI Dropshipping**
   - Botones disponibles:
     - `Calcular Precio Óptimo`
     - `Generar Contenido IA`

---

## 🎯 USO DEL PLUGIN

### **Desde el Dashboard**

1. **Ver estadísticas globales:**
   - `AI Dropshipping` → `Dashboard`

2. **Procesar todos los productos sin precio:**
   - Click en `Procesar Todos los Productos`
   - Confirmar
   - Esperar 10-30 segundos
   - ✅ Productos actualizados

---

### **Desde Productos Individuales**

1. **Editar cualquier producto:**
   - `Productos` → Editar producto

2. **En el sidebar derecho:**
   - Meta box **🤖 AI Dropshipping**
   
3. **Opciones:**
   - `Calcular Precio Óptimo`: Calcula y actualiza precio (5 seg)
   - `Generar Contenido IA`: Crea imágenes/videos (1-2 min)

---

## 🔄 FLUJO AUTOMÁTICO

Una vez configurado, el sistema funciona así:

### **1. Importas producto con SharkDropship**
   → Producto sin precio en WooCommerce

### **2. Webhook detecta producto nuevo**
   → Envía notificación a API

### **3. Sistema procesa automáticamente**
   → Calcula precio con margen 50%
   → Actualiza producto en WooCommerce

### **4. Producto listo en 5 segundos** ⚡
   → Sin intervención manual

---

## 📊 CÁLCULO DE PRECIOS

El sistema aplica estos márgenes automáticamente:

| Rango de Precio | Margen | Ejemplo |
|-----------------|--------|---------|
| €1 - €50 | 50% | €30 → €45 |
| €50 - €100 | 45% | €70 → €101.50 |
| €100 - €200 | 40% | €150 → €210 |
| €200 - €500 | 30% | €300 → €390 |
| > €500 | 25% | €600 → €750 |

Todos los precios se redondean a .99 (ej: €45.50 → €45.99)

---

## 🎨 GENERACIÓN DE CONTENIDO IA

El plugin puede generar:

- ✅ **Imágenes profesionales** (1024x1024px)
- ✅ **Videos demostrativos** (5-15 segundos, hasta 1080p)
- ✅ **Descripciones optimizadas** (SEO-friendly)
- ✅ **Contenido para redes sociales** (Instagram, TikTok, Facebook)

**Nota:** La generación de contenido IA es opcional y puede tardar 1-2 minutos por producto.

---

## 🐛 SOLUCIÓN DE PROBLEMAS

### **El plugin no aparece en el menú**

1. Verificar que WooCommerce esté activado
2. Verificar permisos del usuario (debe tener rol `manage_woocommerce`)
3. Verificar que el plugin esté activado en `Plugins`

---

### **Los webhooks no funcionan**

1. **Verificar URL de API:**
   - `AI Dropshipping` → `Configuración`
   - URL debe terminar en `/api` (sin barra final)

2. **Verificar webhooks:**
   - `WooCommerce` → `Ajustes` → `Avanzado` → `Webhooks`
   - Estado debe ser `Activo` ✅
   - Verificar que las URLs sean correctas

3. **Probar webhook manualmente:**
   ```bash
   curl https://api-switcher.preview.emergentagent.com/api/webhooks/test
   ```
   Debería retornar: `{"status": "ok"}`

---

### **Error al procesar productos**

1. **Verificar conexión a API:**
   - Desde tu servidor WordPress:
   ```bash
   curl https://api-switcher.preview.emergentagent.com/api/woocommerce/products
   ```

2. **Verificar credenciales WooCommerce:**
   - Las credenciales están en el backend de la API
   - Deben coincidir con tu tienda

3. **Ver logs de errores:**
   ```bash
   tail -f /var/www/html/wp-content/debug.log
   ```

---

## 📞 SOPORTE

**Email:** agenteweb@herramientasyaccesorios.store  
**Web:** https://herramientasyaccesorios.store

---

## 📝 NOTAS IMPORTANTES

1. ⚠️ **Backup:** Haz un backup de tu base de datos antes de procesar todos los productos

2. 💰 **Precios existentes:** El sistema NO modifica productos que ya tienen precio

3. 🤖 **Contenido IA:** Es opcional y consume recursos. Úsalo solo para productos importantes

4. 🔄 **Cron Job:** Además del webhook, hay un cron job que revisa productos cada hora como respaldo

5. 🔒 **Seguridad:** El webhook usa firma HMAC SHA256 para autenticación

---

## 🎉 ¡LISTO!

Una vez instalado y configurado:

- ✅ Productos nuevos se procesan automáticamente
- ✅ Precios óptimos calculados con IA
- ✅ Sistema funciona 24/7 sin intervención
- ✅ Dashboard completo para monitoreo

**🚀 ¡Tu tienda dropshipping ahora es 100% automática!**
