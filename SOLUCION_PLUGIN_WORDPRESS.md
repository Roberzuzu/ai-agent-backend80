# 🔧 SOLUCIÓN: Plugin WordPress - Error de Conexión

## ❌ Problema
El plugin mostraba: **"❌ Error de conexión. Por favor, intenta de nuevo."**

## ✅ Soluciones Aplicadas

### 1. **Backend - Endpoint Temporal Creado**
He creado un endpoint temporal `/api/agent/execute` que:
- ✅ Acepta comandos del plugin
- ✅ Guarda los comandos en MongoDB
- ✅ Responde con un mensaje informativo
- ⏳ Preparado para implementación AI completa

### 2. **Plugin - URL Actualizada**
He actualizado el plugin para conectar con tu backend:
- ❌ Antes: `https://wpmoneyhub.preview.emergentagent.com/api`
- ✅ Ahora: `https://ai-agent-backend80.onrender.com/api`

---

## 🚀 PASOS PARA ACTIVAR LA SOLUCIÓN

### **Paso 1: Espera el Deploy de Render (5 minutos)**

Render está desplegando los cambios. Espera 5 minutos y verifica:

```bash
curl -X POST "https://ai-agent-backend80.onrender.com/api/agent/execute" \
  -H "Content-Type: application/json" \
  -d '{"command":"test","user_id":"test"}'
```

**Respuesta esperada:**
```json
{
  "success": true,
  "mensaje": "✅ Comando recibido: 'test'..."
}
```

---

### **Paso 2: Actualiza el Plugin en WordPress**

#### **Opción A: Reinstalar Plugin (RECOMENDADO)**

1. **Descarga el plugin actualizado:**
   - Ubicación: `/app/wordpress-plugin/cerebro-ai-plugin-updated.zip`

2. **Desinstala el plugin viejo:**
   - WordPress Admin > Plugins > Cerebro AI > Desactivar
   - Click en "Eliminar"

3. **Instala el nuevo:**
   - WordPress Admin > Plugins > Add New > Upload Plugin
   - Sube `cerebro-ai-plugin-updated.zip`
   - Activar

4. **Verifica la configuración:**
   - WordPress Admin > Cerebro AI > Settings
   - **API URL** debe ser: `https://ai-agent-backend80.onrender.com/api`

---

#### **Opción B: Actualizar Manualmente (Solo si Opción A falla)**

1. **Edita el archivo:**
   - Vía FTP o File Manager
   - Ruta: `wp-content/plugins/cerebro-ai-woocommerce/cerebro-ai.php`

2. **Busca la línea 75:**
```php
'api_url' => 'https://wpmoneyhub.preview.emergentagent.com/api',
```

3. **Cámbiala a:**
```php
'api_url' => 'https://ai-agent-backend80.onrender.com/api',
```

4. **Guarda el archivo**

5. **Actualiza la configuración:**
   - WordPress Admin > Plugins
   - Desactiva "Cerebro AI"
   - Reactívalo (esto ejecuta el código de activación)

---

### **Paso 3: Prueba el Plugin**

1. Ve a cualquier página de WooCommerce en tu WordPress
2. Deberías ver el botón flotante de Cerebro AI (abajo a la derecha)
3. Haz click y escribe un mensaje de prueba:
   ```
   Hola, ¿estás ahí?
   ```

**Respuesta esperada:**
```
✅ Comando recibido: 'Hola, ¿estás ahí?'

⚠️ El agente AI está en configuración. Por ahora, puedo:

1. ✅ Guardar tus comandos
2. ✅ Gestionar productos (usa la API REST)
3. ✅ Ver analíticas

Pronto tendré capacidades AI completas! 🚀
```

---

## 🔍 VERIFICACIÓN MANUAL

### Test desde WordPress Admin Panel:

1. **Ve a:** WordPress Admin > Cerebro AI > Settings
2. **Verifica que API URL sea:** `https://ai-agent-backend80.onrender.com/api`
3. **Click en:** "Test Connection" (si existe el botón)

### Test desde navegador:

Abre la consola del navegador (F12) y pega:

```javascript
fetch('https://ai-agent-backend80.onrender.com/api/agent/status')
  .then(r => r.json())
  .then(data => console.log('✅ Backend:', data))
  .catch(err => console.error('❌ Error:', err));
```

---

## ⚙️ CONFIGURACIÓN DE LA BASE DE DATOS

Si el plugin sigue sin conectar después de estos pasos, actualiza manualmente la configuración en WordPress:

```sql
-- Conecta a tu base de datos MySQL de WordPress
UPDATE wp_options 
SET option_value = 'a:4:{s:7:"api_url";s:48:"https://ai-agent-backend80.onrender.com/api";s:13:"chat_position";s:12:"bottom-right";s:12:"chat_enabled";b:1;s:10:"admin_only";b:1;}' 
WHERE option_name = 'cerebro_ai_settings';
```

**⚠️ IMPORTANTE:** Reemplaza `wp_options` con el prefijo correcto de tu tabla si es diferente.

---

## 🐛 SOLUCIÓN DE PROBLEMAS

### Problema 1: "404 Not Found"
**Causa:** El backend todavía no ha desplegado la nueva versión
**Solución:** Espera 5-10 minutos más y vuelve a intentar

### Problema 2: "CORS Error"
**Causa:** El backend no permite conexiones desde tu dominio
**Solución:** Ya está configurado CORS en el backend, pero verifica que uses HTTPS en WordPress

### Problema 3: "SSL Certificate Error"
**Causa:** Render usa HTTPS, WordPress debe usar HTTPS también
**Solución:** Asegúrate que tu WordPress esté en HTTPS

### Problema 4: Plugin no aparece
**Causa:** JavaScript no se está cargando
**Solución:** 
1. Limpia caché de WordPress
2. Desactiva plugins de caché temporalmente
3. Verifica que no haya errores en consola del navegador (F12)

---

## 📊 ENDPOINTS DISPONIBLES PARA EL PLUGIN

El plugin puede usar estos endpoints:

```
✅ POST /api/agent/execute     - Enviar comandos al agente
✅ GET  /api/agent/status       - Ver estado del agente
✅ GET  /api/products           - Listar productos
✅ POST /api/products           - Crear producto
✅ GET  /api/woocommerce/products - Productos de WooCommerce
✅ POST /api/wordpress/posts    - Publicar en WordPress
```

---

## 🎯 PRÓXIMOS PASOS

Una vez que el plugin conecte correctamente, podemos:

1. **Implementar el agente AI completo** con capacidades de:
   - Análisis de imágenes de productos
   - Generación automática de descripciones
   - Optimización de precios
   - Creación de contenido para redes sociales

2. **Configurar APIs de IA:**
   - OpenRouter / OpenAI / Perplexity
   - Para generación de contenido inteligente

3. **Activar funciones avanzadas:**
   - Análisis de tendencias
   - Recomendaciones automáticas
   - Integración con redes sociales

---

## ✅ CHECKLIST

- [ ] Esperar 5 minutos para deploy de Render
- [ ] Verificar endpoint `/api/agent/execute` con curl
- [ ] Reinstalar plugin en WordPress (Opción A)
- [ ] O actualizar URL manualmente (Opción B)
- [ ] Probar chat widget en WordPress
- [ ] Confirmar que recibe respuesta del backend

---

**Última actualización:** 2025-10-28
**Versión del plugin:** 1.0.0
**Versión del backend:** 1.0.0

---

**¿Necesitas ayuda?** Una vez que Render despliegue (5 minutos), prueba el plugin y avísame si hay algún problema. 🚀
