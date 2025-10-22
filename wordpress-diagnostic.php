<?php
/**
 * WordPress Diagnostic Script
 * Sube este archivo a la raíz de tu WordPress y ábrelo en el navegador
 */

// Cargar WordPress
require_once('wp-load.php');

?>
<!DOCTYPE html>
<html>
<head>
    <title>WordPress Diagnostic</title>
    <style>
        body { font-family: Arial; padding: 20px; }
        .ok { color: green; }
        .error { color: red; }
        .warning { color: orange; }
        pre { background: #f5f5f5; padding: 10px; overflow-x: auto; }
        .section { margin: 20px 0; border: 1px solid #ddd; padding: 15px; }
    </style>
</head>
<body>
    <h1>🔍 WordPress Diagnostic Report</h1>
    
    <div class="section">
        <h2>1. Información del Sistema</h2>
        <ul>
            <li>WordPress Version: <strong><?php echo get_bloginfo('version'); ?></strong></li>
            <li>PHP Version: <strong><?php echo phpversion(); ?></strong> 
                <?php echo version_compare(phpversion(), '7.4', '>=') ? '<span class="ok">✓</span>' : '<span class="error">✗ Necesitas 7.4+</span>'; ?>
            </li>
            <li>MySQL Version: <strong><?php global $wpdb; echo $wpdb->db_version(); ?></strong></li>
            <li>WP_DEBUG: <strong><?php echo WP_DEBUG ? 'Activado' : 'Desactivado'; ?></strong></li>
        </ul>
    </div>
    
    <div class="section">
        <h2>2. WooCommerce</h2>
        <?php if (class_exists('WooCommerce')): ?>
            <p class="ok">✓ WooCommerce está INSTALADO y ACTIVO</p>
            <ul>
                <li>Versión: <strong><?php echo WC()->version; ?></strong></li>
            </ul>
        <?php else: ?>
            <p class="error">✗ WooCommerce NO está instalado o activado</p>
            <p><strong>SOLUCIÓN:</strong> Instala y activa WooCommerce antes del plugin AI Agent</p>
        <?php endif; ?>
    </div>
    
    <div class="section">
        <h2>3. Plugin AI WooCommerce Agent</h2>
        <?php
        $plugin_file = 'ai-woocommerce-agent/ai-woocommerce-agent.php';
        $plugin_path = WP_PLUGIN_DIR . '/' . $plugin_file;
        
        if (file_exists($plugin_path)):
        ?>
            <p class="ok">✓ Archivo del plugin encontrado</p>
            <ul>
                <li>Ruta: <code><?php echo $plugin_path; ?></code></li>
                <li>Permisos: <code><?php echo substr(sprintf('%o', fileperms($plugin_path)), -4); ?></code></li>
                <li>Tamaño: <code><?php echo filesize($plugin_path); ?> bytes</code></li>
            </ul>
            
            <?php if (is_plugin_active($plugin_file)): ?>
                <p class="ok">✓ Plugin ACTIVADO</p>
            <?php else: ?>
                <p class="warning">⚠ Plugin instalado pero NO activado</p>
            <?php endif; ?>
            
        <?php else: ?>
            <p class="error">✗ Archivo del plugin NO encontrado</p>
            <p>Esperado en: <code><?php echo $plugin_path; ?></code></p>
        <?php endif; ?>
    </div>
    
    <div class="section">
        <h2>4. Errores en debug.log</h2>
        <?php
        $log_file = WP_CONTENT_DIR . '/debug.log';
        if (file_exists($log_file)):
            $log_content = file($log_file);
            $last_50 = array_slice($log_content, -50);
            echo '<p>Últimas 50 líneas del log:</p>';
            echo '<pre>' . esc_html(implode('', $last_50)) . '</pre>';
        else:
            echo '<p class="warning">⚠ No existe debug.log (activa WP_DEBUG en wp-config.php)</p>';
        endif;
        ?>
    </div>
    
    <div class="section">
        <h2>5. Plugins Activos</h2>
        <ul>
        <?php
        $active_plugins = get_option('active_plugins');
        foreach ($active_plugins as $plugin):
            $plugin_data = get_plugin_data(WP_PLUGIN_DIR . '/' . $plugin);
            echo '<li><strong>' . esc_html($plugin_data['Name']) . '</strong> v' . esc_html($plugin_data['Version']) . '</li>';
        endforeach;
        ?>
        </ul>
    </div>
    
    <div class="section">
        <h2>6. Permisos de Archivos</h2>
        <?php
        $dirs_to_check = array(
            WP_PLUGIN_DIR,
            WP_CONTENT_DIR,
            WP_PLUGIN_DIR . '/ai-woocommerce-agent'
        );
        
        foreach ($dirs_to_check as $dir):
            if (file_exists($dir)):
                $perms = substr(sprintf('%o', fileperms($dir)), -4);
                $writable = is_writable($dir) ? '<span class="ok">✓ Escribible</span>' : '<span class="error">✗ No escribible</span>';
                echo "<p><code>$dir</code> - Permisos: <code>$perms</code> $writable</p>";
            else:
                echo "<p class="error">✗ No existe: <code>$dir</code></p>";
            endif;
        endforeach;
        ?>
    </div>
    
    <div class="section">
        <h2>7. Memoria y Límites PHP</h2>
        <ul>
            <li>memory_limit: <strong><?php echo ini_get('memory_limit'); ?></strong></li>
            <li>max_execution_time: <strong><?php echo ini_get('max_execution_time'); ?>s</strong></li>
            <li>upload_max_filesize: <strong><?php echo ini_get('upload_max_filesize'); ?></strong></li>
            <li>post_max_size: <strong><?php echo ini_get('post_max_size'); ?></strong></li>
        </ul>
    </div>
    
    <div class="section">
        <h2>📋 Resumen</h2>
        <?php
        $issues = array();
        
        if (version_compare(phpversion(), '7.4', '<')) {
            $issues[] = 'PHP debe ser 7.4 o superior';
        }
        
        if (!class_exists('WooCommerce')) {
            $issues[] = 'WooCommerce no está activado';
        }
        
        if (!file_exists($plugin_path)) {
            $issues[] = 'Plugin no está correctamente subido';
        }
        
        if (empty($issues)):
        ?>
            <p class="ok"><strong>✓ Todo parece correcto</strong></p>
            <p>Si el plugin aún no se activa, descarga la versión minimalista.</p>
        <?php else: ?>
            <p class="error"><strong>✗ Problemas encontrados:</strong></p>
            <ul>
            <?php foreach ($issues as $issue): ?>
                <li><?php echo $issue; ?></li>
            <?php endforeach; ?>
            </ul>
        <?php endif; ?>
    </div>
    
    <p style="margin-top: 40px; color: #666;">
        <small>Generado: <?php echo date('Y-m-d H:i:s'); ?></small>
    </p>
</body>
</html>
