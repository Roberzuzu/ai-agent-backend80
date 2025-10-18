# 🔧 Configuración de WordPress - Paso a Paso

## ⚠️ IMPORTANTE: Necesitas crear un Application Password

La contraseña normal de WordPress **NO funciona** con la API REST.  
Necesitas crear un **Application Password** específico para la API.

---

## 📋 Pasos para Configurar (5 minutos)

### Paso 1: Accede a tu WordPress

1. Ve a: https://herramientasyaccesorios.store/wp-admin
2. Usuario: `Agente monetización`
3. Contraseña: `34*#1IYm1$s5fOukVRR$V@lI`
4. Inicia sesión

### Paso 2: Crea el Application Password

1. En el panel de WordPress, ve a:
   **Usuarios → Perfil**
   
   O directamente:
   https://herramientasyaccesorios.store/wp-admin/profile.php

2. Scroll down hasta encontrar la sección:
   **"Application Passwords"** o **"Contraseñas de aplicación"**

3. En el campo "New Application Password Name":
   Escribe: `Monetization Agent API`

4. Click en **"Add New Application Password"** o **"Añadir nueva"**

5. **¡IMPORTANTE!** WordPress te mostrará una contraseña como:
   ```
   xxxx xxxx xxxx xxxx xxxx xxxx
   ```
   
   **COPIA ESTA CONTRASEÑA INMEDIATAMENTE**
   
   (Solo se muestra una vez, si la pierdes tendrás que crear otra)

### Paso 3: Pégame la Application Password

Una vez que tengas la contraseña, simplemente pégala aquí y yo la configuraré.

Formato esperado:
```
xxxx xxxx xxxx xxxx xxxx xxxx
```

O sin espacios también funciona:
```
xxxxxxxxxxxxxxxxxxxxxxxx
```

---

## 🎯 ¿Qué pasará después?

Una vez configurada la Application Password, el agente podrá:

1. ✅ **Sincronizar productos automáticamente**
   - Productos del agente → WooCommerce
   - Con precios, descripciones, imágenes
   - Códigos de descuento incluidos

2. ✅ **Publicar contenido generado**
   - Contenido de IA → Posts de blog
   - Automáticamente categorizado
   - Con keywords como tags

3. ✅ **Actualizar productos**
   - Cambios de precio sincronizados
   - Nuevos descuentos aplicados
   - Productos destacados marcados

4. ✅ **Gestión bidireccional**
   - Ver productos de WooCommerce desde el agente
   - Editar desde cualquier lugar
   - Sincronización completa

---

## 🔍 Verificación

Una vez configurado, probaré:

```bash
# Test 1: Verificar conexión
curl http://localhost:8001/api/wordpress/status

# Test 2: Ver productos de WooCommerce
curl http://localhost:8001/api/wordpress/products

# Test 3: Sincronizar un producto
curl -X POST http://localhost:8001/api/wordpress/sync-product/PRODUCT_ID
```

---

## ❓ Problemas Comunes

**"No veo la sección Application Passwords"**
- Requiere WordPress 5.6+
- Debe ser HTTPS (tu sitio lo tiene ✓)
- Verifica que estés en tu perfil de usuario

**"Me dice que no tengo permisos"**
- Necesitas ser Administrador
- Usuario actual: "Agente monetización" debe tener rol de Admin

**"La contraseña no funciona"**
- Asegúrate de copiar la Application Password completa
- Puede tener espacios (quítalos o déjalos, ambos funcionan)
- NO uses la contraseña normal de login

---

## 🚀 Una vez configurado...

Podrás ver en el agente:

1. **Products Page**: Botón "Sync to WordPress"
2. **Content Page**: Botón "Publish to Blog"
3. **Dashboard**: Estado de sincronización
4. **Todas las acciones automáticas funcionando**

---

## 💡 Alternativa Rápida (Si tienes problemas)

Si no puedes acceder a Application Passwords, puedes:

1. **Usar un plugin**: 
   - Instala "Application Passwords" plugin
   - Actívalo
   - Crea la contraseña desde ahí

2. **Verificar HTTPS**:
   - La API REST solo funciona con HTTPS
   - Tu sitio: https://herramientasyaccesorios.store ✓

---

**¿Listo? Pega aquí tu Application Password y seguimos! 🎯**
