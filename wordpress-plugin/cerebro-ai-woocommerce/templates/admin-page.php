<?php
/**
 * Template: Página de administración
 */

if (!defined('ABSPATH')) exit;

$settings = get_option('cerebro_ai_settings', array());
$api_url = $settings['api_url'] ?? '';
$chat_enabled = $settings['chat_enabled'] ?? true;
$admin_only = $settings['admin_only'] ?? true;
$chat_position = $settings['chat_position'] ?? 'bottom-right';

// Guardar configuración
if (isset($_POST['cerebro_ai_save'])) {
    check_admin_referer('cerebro_ai_settings_nonce');
    
    $new_settings = array(
        'api_url' => sanitize_text_field($_POST['api_url']),
        'chat_enabled' => isset($_POST['chat_enabled']),
        'admin_only' => isset($_POST['admin_only']),
        'chat_position' => sanitize_text_field($_POST['chat_position']),
    );
    
    update_option('cerebro_ai_settings', $new_settings);
    echo '<div class="notice notice-success"><p>✅ Configuración guardada correctamente</p></div>';
    
    $settings = $new_settings;
    $api_url = $settings['api_url'];
    $chat_enabled = $settings['chat_enabled'];
    $admin_only = $settings['admin_only'];
    $chat_position = $settings['chat_position'];
}
?>

<div class="wrap cerebro-ai-admin">
    <h1>
        <span class="dashicons dashicons-brain" style="color: #6366f1;"></span>
        Cerebro AI - Configuración
    </h1>
    
    <div class="cerebro-ai-header">
        <p class="description">
            Asistente de IA experto en WooCommerce. Gestiona productos, crea ofertas, optimiza tu tienda y mucho más.
        </p>
    </div>
    
    <div class="cerebro-ai-content">
        <div class="cerebro-ai-main">
            <form method="post" action="">
                <?php wp_nonce_field('cerebro_ai_settings_nonce'); ?>
                
                <div class="card">
                    <h2>⚙️ Configuración General</h2>
                    
                    <table class="form-table">
                        <tr>
                            <th scope="row">
                                <label for="api_url">URL de la API</label>
                            </th>
                            <td>
                                <input 
                                    type="url" 
                                    id="api_url" 
                                    name="api_url" 
                                    value="<?php echo esc_attr($api_url); ?>" 
                                    class="regular-text"
                                    required
                                />
                                <p class="description">
                                    URL base de tu API de Cerebro AI (ejemplo: https://plugin-stability.preview.emergentagent.com/api)
                                </p>
                            </td>
                        </tr>
                        
                        <tr>
                            <th scope="row">Chat flotante</th>
                            <td>
                                <label>
                                    <input 
                                        type="checkbox" 
                                        name="chat_enabled" 
                                        <?php checked($chat_enabled, true); ?>
                                    />
                                    Activar chat flotante en el sitio
                                </label>
                            </td>
                        </tr>
                        
                        <tr>
                            <th scope="row">Acceso al chat</th>
                            <td>
                                <label>
                                    <input 
                                        type="checkbox" 
                                        name="admin_only" 
                                        <?php checked($admin_only, true); ?>
                                    />
                                    Solo administradores pueden usar el chat
                                </label>
                                <p class="description">
                                    Recomendado: mantener activado para seguridad
                                </p>
                            </td>
                        </tr>
                        
                        <tr>
                            <th scope="row">
                                <label for="chat_position">Posición del chat</label>
                            </th>
                            <td>
                                <select id="chat_position" name="chat_position">
                                    <option value="bottom-right" <?php selected($chat_position, 'bottom-right'); ?>>
                                        Abajo a la derecha
                                    </option>
                                    <option value="bottom-left" <?php selected($chat_position, 'bottom-left'); ?>>
                                        Abajo a la izquierda
                                    </option>
                                </select>
                            </td>
                        </tr>
                    </table>
                </div>
                
                <p class="submit">
                    <button type="submit" name="cerebro_ai_save" class="button button-primary button-large">
                        💾 Guardar Configuración
                    </button>
                </p>
            </form>
        </div>
        
        <div class="cerebro-ai-sidebar">
            <div class="card">
                <h3>🚀 Características</h3>
                <ul class="cerebro-features">
                    <li>✅ Gestión completa de productos</li>
                    <li>✅ Análisis de imágenes con IA</li>
                    <li>✅ Optimización SEO automática</li>
                    <li>✅ Creación de ofertas y cupones</li>
                    <li>✅ Análisis de competencia</li>
                    <li>✅ Búsqueda de tendencias</li>
                    <li>✅ Generación de contenido</li>
                    <li>✅ Importación desde Excel/CSV</li>
                </ul>
            </div>
            
            <div class="card">
                <h3>📖 Uso del Shortcode</h3>
                <p>Puedes insertar el chat en cualquier página usando:</p>
                <code style="display: block; padding: 10px; background: #f0f0f0; margin: 10px 0;">
                    [cerebro_chat]
                </code>
            </div>
            
            <div class="card">
                <h3>💡 Ejemplos de Comandos</h3>
                <ul style="font-size: 13px; line-height: 1.6;">
                    <li><strong>Subir foto:</strong> Adjunta una imagen de producto</li>
                    <li><strong>Estadísticas:</strong> "Dame las ventas del mes"</li>
                    <li><strong>Optimizar:</strong> "Optimiza mi catálogo"</li>
                    <li><strong>Ofertas:</strong> "Crea una oferta flash del 20%"</li>
                    <li><strong>Tendencias:</strong> "Busca productos tendencia"</li>
                </ul>
            </div>
            
            <div class="card" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white;">
                <h3 style="color: white;">🎯 ¿Necesitas ayuda?</h3>
                <p style="color: rgba(255,255,255,0.9);">
                    Visita nuestra documentación o contacta con soporte.
                </p>
                <a href="#" class="button button-secondary" style="margin-top: 10px;">
                    📚 Ver Documentación
                </a>
            </div>
        </div>
    </div>
</div>

<style>
.cerebro-ai-admin .cerebro-ai-header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 20px;
    border-radius: 8px;
    margin: 20px 0;
}

.cerebro-ai-content {
    display: grid;
    grid-template-columns: 1fr 350px;
    gap: 20px;
    margin-top: 20px;
}

.cerebro-ai-main {
    background: white;
}

.cerebro-ai-sidebar .card {
    background: white;
    border: 1px solid #ddd;
    border-radius: 8px;
    padding: 20px;
    margin-bottom: 20px;
}

.cerebro-ai-sidebar h3 {
    margin-top: 0;
    font-size: 16px;
}

.cerebro-features {
    list-style: none;
    padding: 0;
    margin: 0;
}

.cerebro-features li {
    padding: 8px 0;
    border-bottom: 1px solid #f0f0f0;
}

.cerebro-features li:last-child {
    border-bottom: none;
}

@media (max-width: 1280px) {
    .cerebro-ai-content {
        grid-template-columns: 1fr;
    }
}
</style>
