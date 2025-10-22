# 🔧 Troubleshooting - Plugin WordPress

## ❌ Problema: "El plugin no se activa"

### Solución 1: Verificar Requisitos

**Requisitos mínimos:**
```
✓ WordPress 6.0+
✓ WooCommerce 7.0+ (INSTALADO Y ACTIVADO)
✓ PHP 7.4+
```

**Verificar WooCommerce:**
1. Ve a **Plugins** en WordPress
2. Busca **WooCommerce**
3. Si no está instalado:
   - **Plugins → Añadir nuevo**
   - Busca "WooCommerce"
   - Instala y activa
4. LUEGO activa AI WooCommerce Agent

---

### Solución 2: Verificar Logs de Error

**Activar WP_DEBUG:**

Edita `wp-config.php`:

```php
define('WP_DEBUG', true);
define('WP_DEBUG_LOG', true);
define('WP_DEBUG_DISPLAY', false);
@ini_set('display_errors', 0);
```

**Ver errores:**

```bash
tail -f /var/www/html/wp-content/debug.log
```

O desde WordPress:
- Descargar via FTP: `/wp-content/debug.log`

---

### Solución 3: Verificar Permisos

```bash
# Permisos correctos
cd /var/www/html/wp-content/plugins
chmod 755 ai-woocommerce-agent
chmod 644 ai-woocommerce-agent/*.php
chmod -R 755 ai-woocommerce-agent/includes
chmod -R 755 ai-woocommerce-agent/templates
chmod -R 755 ai-woocommerce-agent/assets
```

---

### Solución 4: Instalación Manual Paso a Paso

**1. Descomprimir localmente:**

```bash
unzip ai-woocommerce-agent.zip -d ai-woocommerce-agent
```

**2. Verificar estructura:**

Debe verse así:

```
ai-woocommerce-agent/
├── ai-woocommerce-agent.php  ← Archivo principal
├── readme.txt
├── includes/
│   ├── class-ai-client.php
│   ├── class-telegram-bot.php
│   └── ...
├── templates/
│   └── admin/
└── assets/
```

**3. Subir por FTP/SFTP:**

- Sube la carpeta `ai-woocommerce-agent` completa a:
  `/wp-content/plugins/`

**4. Activar desde WordPress Admin**

---

### Solución 5: Conflicto de Plugins

**Desactivar otros plugins temporalmente:**

1. Ve a **Plugins**
2. Desactiva todos excepto WooCommerce
3. Intenta activar AI WooCommerce Agent
4. Si funciona, reactiva uno por uno para encontrar conflicto

**Plugins conocidos con conflictos:**
- Algunos plugins de cache agresivos
- Plugins de seguridad muy restrictivos
- Otros plugins de AI/automation

---

### Solución 6: Verificar versión PHP

```bash
php -v
```

Debe ser 7.4 o superior.

Si es menor:

```bash
# Ubuntu/Debian
sudo apt install php8.1
sudo a2dismod php7.2
sudo a2enmod php8.1
sudo systemctl restart apache2

# O para Nginx + PHP-FPM
sudo apt install php8.1-fpm
sudo systemctl restart php8.1-fpm
```

---

### Solución 7: Reinstalación Limpia

```bash
# 1. Desactivar (desde admin o por SSH)
cd /var/www/html/wp-content/plugins
mv ai-woocommerce-agent ai-woocommerce-agent.backup

# 2. Limpiar base de datos (opcional, solo si es necesario)
# Desde phpMyAdmin o CLI:
mysql -u root -p wordpress_db

DELETE FROM wp_options WHERE option_name LIKE 'aiwca_%';
DROP TABLE IF EXISTS wp_aiwca_memory;
DROP TABLE IF EXISTS wp_aiwca_telegram_messages;

# 3. Subir nueva copia
# Descomprimir y subir de nuevo

# 4. Activar
```

---

## ⚠️ Errores Comunes y Soluciones

### Error: "Plugin generated X characters of unexpected output"

**Causa:** Espacios o BOM al inicio de archivos PHP

**Solución:**

```bash
# Buscar archivos con espacios al inicio
cd /var/www/html/wp-content/plugins/ai-woocommerce-agent
grep -r "^[[:space:]]*<?php" *.php
```

Edita cada archivo y asegura que empiece exactamente con:
```php
<?php
```

Sin espacios, sin líneas en blanco antes.

---

### Error: "Call to undefined function"

**Causa:** Clase no cargada

**Solución:**

Verifica que estos archivos existan:

```bash
cd /var/www/html/wp-content/plugins/ai-woocommerce-agent/includes
ls -la
```

Debe mostrar:
- class-ai-client.php
- class-telegram-bot.php
- class-product-processor.php
- class-agent-executor.php
- functions.php

---

### Error: "Fatal error: Cannot redeclare"

**Causa:** Plugin ya incluido o duplicado

**Solución:**

```bash
# Buscar duplicados
cd /var/www/html/wp-content/plugins
ls -d ai-*

# Eliminar duplicados
rm -rf ai-woocommerce-agent-old
```

---

### Error: "Failed to load plugin file"

**Causa:** Ruta incorrecta o estructura rota

**Solución:**

El archivo principal **DEBE** llamarse:
```
ai-woocommerce-agent.php
```

Y estar en:
```
/wp-content/plugins/ai-woocommerce-agent/ai-woocommerce-agent.php
```

---

## ✅ Verificación Post-Instalación

Una vez activado, verifica:

**1. Menú aparece:**
- [ ] "AI Agent" en menú lateral de WordPress admin

**2. Páginas cargan:**
- [ ] Dashboard
- [ ] Command Center
- [ ] Telegram Bot
- [ ] Settings

**3. Sin errores en consola:**
- F12 → Console → Sin errores rojos

**4. Botón en productos:**
- Edita cualquier producto
- Busca sección "AI Optimization"
- Botón "Process with AI Agent" debe aparecer

---

## 🐛 Debug Avanzado

### Ver queries de base de datos:

En `wp-config.php` añade:

```php
define('SAVEQUERIES', true);
```

Luego en footer de admin:

```php
global $wpdb;
print_r($wpdb->queries);
```

### Ver hooks registrados:

```php
global $wp_filter;
echo '<pre>';
print_r($wp_filter['init']);
echo '</pre>';
```

---

## 📞 Reporte de Error

Si persiste el error, proporciona:

```
1. Versión de WordPress: [6.x]
2. Versión de WooCommerce: [7.x o 8.x]
3. Versión de PHP: [7.4/8.0/8.1]
4. Contenido de debug.log: [últimas 50 líneas]
5. Otros plugins activos: [lista]
6. Mensaje de error exacto: [texto completo]
```

---

## 🔄 Versión de Emergencia (Minimalista)

Si nada funciona, usa esta versión ultra-simple:

**Crear: `/wp-content/plugins/aiwca-simple/aiwca-simple.php`**

```php
<?php
/**
 * Plugin Name: AI WooCommerce Agent (Simple)
 * Version: 1.0.0-simple
 * Requires at least: 6.0
 * Requires PHP: 7.4
 */

if (!defined('ABSPATH')) exit;

// Add admin menu
add_action('admin_menu', function() {
    add_menu_page(
        'AI Agent',
        'AI Agent',
        'manage_woocommerce',
        'aiwca-simple',
        function() {
            echo '<div class="wrap">';
            echo '<h1>AI WooCommerce Agent</h1>';
            echo '<p>Plugin activado correctamente!</p>';
            echo '<p>Configuración disponible próximamente.</p>';
            echo '</div>';
        },
        'dashicons-superhero'
    );
});

// Check WooCommerce
add_action('admin_init', function() {
    if (!class_exists('WooCommerce')) {
        deactivate_plugins(plugin_basename(__FILE__));
        add_action('admin_notices', function() {
            echo '<div class="error"><p>AI WooCommerce Agent requiere WooCommerce.</p></div>';
        });
    }
});
```

Esta versión minimalista SIEMPRE debería activar. Si ni esta activa, el problema es del servidor o WordPress.

---

## 📧 Contacto

Si después de seguir todas estas soluciones el plugin no activa, hay un problema con tu instalación de WordPress que va más allá del plugin.

Verifica:
- Hosting compatible con WordPress
- Base de datos MySQL funcional
- PHP sin modo seguro (safe_mode)
- .htaccess correcto
- Permisos de escritura en wp-content

---

**¡El plugin DEBE activar si sigues estos pasos! 🚀**
