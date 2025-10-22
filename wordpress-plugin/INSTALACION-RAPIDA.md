# 🚀 GUÍA DE INSTALACIÓN RÁPIDA - Cerebro AI WordPress Plugin

## ⚡ Instalación en 5 minutos

### Paso 1: Descarga el Plugin
📦 Archivo: `cerebro-ai-woocommerce.zip` (16 KB)
📍 Ubicación: `/app/wordpress-plugin/cerebro-ai-woocommerce.zip`

### Paso 2: Instalar en WordPress

**Opción A - Desde el Panel de WordPress:**
1. Ve a: `WordPress Admin → Plugins → Añadir nuevo`
2. Click en `Subir plugin`
3. Selecciona `cerebro-ai-woocommerce.zip`
4. Click en `Instalar ahora`
5. Click en `Activar`

**Opción B - Por FTP:**
1. Descomprime el ZIP
2. Sube la carpeta `cerebro-ai-woocommerce` a `/wp-content/plugins/`
3. Activa el plugin desde WordPress Admin

### Paso 3: Configuración (2 minutos)

1. Ve a: `WordPress Admin → Cerebro AI`
2. Configura:
   ```
   URL de la API: https://plugin-stability.preview.emergentagent.com/api
   ✅ Chat flotante: Activado
   ✅ Solo administradores: Activado
   Posición: Abajo a la derecha
   ```
3. Click en `💾 Guardar Configuración`

### Paso 4: ¡Pruébalo!

1. Refresca cualquier página de tu WordPress
2. Verás el botón flotante 🧠 en la esquina
3. Click para abrir el chat
4. Prueba: `"Dame las estadísticas de mi tienda"`

---

## 🎯 CASOS DE USO INMEDIATOS

### 1. Crear Producto desde Foto
```
1. Click en botón 📎 (clip)
2. Selecciona foto del producto
3. Click Enviar
→ Cerebro AI analiza la imagen y crea el producto automáticamente
```

### 2. Optimizar Catálogo
```
Escribe: "Optimiza todos mis productos para mejorar las ventas"
→ Revisa y mejora descripciones, precios y SEO
```

### 3. Crear Oferta Flash
```
Escribe: "Crea una oferta del 20% para los 10 productos más vendidos"
→ Genera cupón y contenido promocional
```

### 4. Importar desde Excel
```
1. Adjunta tu archivo Excel con productos
2. Escribe: "Importa estos productos a WooCommerce"
→ Crea todos los productos automáticamente
```

---

## 🔧 CONFIGURACIÓN AVANZADA

### Cambiar la URL de la API

Si tienes tu propia instalación de Cerebro AI:

1. Ve a `Cerebro AI → Configuración`
2. Cambia la URL a tu dominio:
   ```
   https://tu-dominio.com/api
   ```
3. Asegúrate de que termine en `/api`

### Usar el Shortcode

Para insertar el chat en páginas específicas:

```
[cerebro_chat]
```

Ejemplo en página "Soporte":
```html
<h2>¿Necesitas ayuda?</h2>
<p>Pregúntale a nuestro asistente de IA</p>
[cerebro_chat]
```

### Permitir a Más Usuarios

Por defecto, solo administradores pueden usar el chat. Para cambiar:

1. Edita `cerebro-ai.php`
2. Busca línea 62:
   ```php
   if (current_user_can('manage_woocommerce')) {
   ```
3. Cambia a:
   ```php
   if (current_user_can('edit_posts')) { // Editores y superiores
   // o
   if (is_user_logged_in()) { // Todos los usuarios registrados
   ```

---

## 📱 CONECTAR CON N8N

### Webhook en N8N

1. Crea un nodo HTTP Request en n8n
2. Configura:
   ```
   URL: https://plugin-stability.preview.emergentagent.com/api/agent/execute
   Method: POST
   Body:
   {
     "command": "{{ $json.comando }}",
     "user_id": "n8n_wordpress"
   }
   ```

### Automatizar Acciones

Ejemplo - Notificar en Slack cuando se crea un producto:

```
WordPress Webhook → Cerebro AI → Slack Notification
```

---

## ❓ SOLUCIÓN DE PROBLEMAS

### El chat no aparece
✅ **Solución**:
1. Verifica que seas administrador de WooCommerce
2. Ve a `Cerebro AI → Configuración`
3. Asegúrate de que "Chat flotante" está activado
4. Limpia caché (Ctrl+F5)

### Error "No se puede conectar con la API"
✅ **Solución**:
1. Verifica la URL de la API en configuración
2. Comprueba que termina en `/api`
3. Prueba directamente: `https://tu-url.com/api/agent/status`

### Los comandos no responden
✅ **Solución**:
1. Abre consola del navegador (F12)
2. Busca errores en rojo
3. Verifica que WooCommerce esté instalado y activo

---

## 📞 SOPORTE Y AYUDA

- 📖 **Documentación completa**: Ver `README.md`
- 💬 **Chat de soporte**: Disponible en el plugin
- 📧 **Email**: support@cerebroai.com

---

## 🎉 ¡LISTO!

Ya tienes Cerebro AI funcionando en tu WordPress. Ahora puedes:

✅ Gestionar productos con IA
✅ Crear ofertas automáticamente
✅ Analizar tu competencia
✅ Optimizar tu catálogo
✅ Generar contenido
✅ Y mucho más...

**¿Necesitas más ayuda?** Abre el chat y pregunta: *"¿Qué puedes hacer por mí?"*
