<?php
/**
 * Plugin Name: AI Chat Widget Integration
 * Description: Integra el chat AI en tu sitio WordPress
 * Version: 1.0.0
 * Author: HerramientasyAccesorios
 */

if (!defined('ABSPATH')) exit;

// Settings
define('AI_CHAT_BACKEND_URL', get_option('ai_chat_backend_url', 'http://localhost:8001'));
define('AI_CHAT_FRONTEND_URL', get_option('ai_chat_frontend_url', 'http://localhost:3000'));

// Add admin menu
add_action('admin_menu', 'ai_chat_add_menu');
function ai_chat_add_menu() {
    add_menu_page(
        'AI Chat Settings',
        'AI Chat',
        'manage_options',
        'ai-chat-settings',
        'ai_chat_settings_page',
        'dashicons-format-chat',
        60
    );
}

// Settings page
function ai_chat_settings_page() {
    if (isset($_POST['save_chat_settings'])) {
        update_option('ai_chat_backend_url', sanitize_text_field($_POST['backend_url']));
        update_option('ai_chat_frontend_url', sanitize_text_field($_POST['frontend_url']));
        update_option('ai_chat_position', sanitize_text_field($_POST['chat_position']));
        update_option('ai_chat_show_on_all_pages', isset($_POST['show_on_all_pages']) ? 'yes' : 'no');
        echo '<div class="updated"><p>Configuración guardada!</p></div>';
    }
    
    $backend_url = get_option('ai_chat_backend_url', 'http://localhost:8001');
    $frontend_url = get_option('ai_chat_frontend_url', 'http://localhost:3000');
    $position = get_option('ai_chat_position', 'bottom-right');
    $show_all = get_option('ai_chat_show_on_all_pages', 'no');
    ?>
    <div class="wrap">
        <h1>💬 Configuración AI Chat</h1>
        
        <form method="post">
            <table class="form-table">
                <tr>
                    <th>Backend URL</th>
                    <td>
                        <input type="url" name="backend_url" value="<?php echo esc_attr($backend_url); ?>" class="regular-text" />
                        <p class="description">URL del backend standalone (ej: http://herramientasyaccesorios.store:8001)</p>
                    </td>
                </tr>
                
                <tr>
                    <th>Frontend URL</th>
                    <td>
                        <input type="url" name="frontend_url" value="<?php echo esc_attr($frontend_url); ?>" class="regular-text" />
                        <p class="description">URL del frontend React (ej: http://herramientasyaccesorios.store:3000)</p>
                    </td>
                </tr>
                
                <tr>
                    <th>Posición del Chat</th>
                    <td>
                        <select name="chat_position">
                            <option value="bottom-right" <?php selected($position, 'bottom-right'); ?>>Abajo Derecha</option>
                            <option value="bottom-left" <?php selected($position, 'bottom-left'); ?>>Abajo Izquierda</option>
                            <option value="top-right" <?php selected($position, 'top-right'); ?>>Arriba Derecha</option>
                            <option value="top-left" <?php selected($position, 'top-left'); ?>>Arriba Izquierda</option>
                        </select>
                    </td>
                </tr>
                
                <tr>
                    <th>Mostrar en todas las páginas</th>
                    <td>
                        <input type="checkbox" name="show_on_all_pages" <?php checked($show_all, 'yes'); ?> />
                        <p class="description">Mostrar widget flotante en todo el sitio</p>
                    </td>
                </tr>
            </table>
            
            <p class="submit">
                <button type="submit" name="save_chat_settings" class="button button-primary">Guardar Configuración</button>
            </p>
        </form>
        
        <hr>
        
        <h2>📝 Cómo Usar</h2>
        
        <h3>Opción 1: Widget Flotante (Recomendado)</h3>
        <p>Activa "Mostrar en todas las páginas" arriba y aparecerá un botón flotante en todo tu sitio.</p>
        
        <h3>Opción 2: Shortcode en Página Específica</h3>
        <p>Usa este shortcode en cualquier página o post:</p>
        <code>[ai_chat]</code>
        <p>Para mostrar chat completo en tamaño completo:</p>
        <code>[ai_chat fullscreen="true"]</code>
        
        <h3>Opción 3: Código PHP en Tema</h3>
        <p>Añade esto en tu tema donde quieras el chat:</p>
        <code>&lt;?php echo do_shortcode('[ai_chat]'); ?&gt;</code>
        
        <hr>
        
        <h2>🧪 Test de Conexión</h2>
        <button type="button" id="test-backend" class="button">Probar Backend</button>
        <div id="test-result"></div>
        
        <script>
        jQuery(document).ready(function($) {
            $('#test-backend').click(function() {
                $(this).prop('disabled', true).text('Probando...');
                $('#test-result').html('<p>Conectando...</p>');
                
                $.get('<?php echo esc_js($backend_url); ?>/api/health')
                    .done(function() {
                        $('#test-result').html('<div class="updated"><p>✅ Backend conectado correctamente!</p></div>');
                    })
                    .fail(function() {
                        $('#test-result').html('<div class="error"><p>❌ No se pudo conectar al backend. Verifica la URL.</p></div>');
                    })
                    .always(function() {
                        $('#test-backend').prop('disabled', false).text('Probar Backend');
                    });
            });
        });
        </script>
    </div>
    <?php
}

// Shortcode [ai_chat]
add_shortcode('ai_chat', 'ai_chat_shortcode');
function ai_chat_shortcode($atts) {
    $atts = shortcode_atts(array(
        'fullscreen' => 'false',
        'height' => '600px',
    ), $atts);
    
    $backend_url = get_option('ai_chat_backend_url', 'http://localhost:8001');
    $frontend_url = get_option('ai_chat_frontend_url', 'http://localhost:3000');
    
    $fullscreen = $atts['fullscreen'] === 'true';
    $height = $fullscreen ? '100vh' : esc_attr($atts['height']);
    
    ob_start();
    ?>
    <div class="ai-chat-container" style="<?php echo $fullscreen ? 'position:fixed;top:0;left:0;width:100%;height:100vh;z-index:999999;' : ''; ?>">
        <iframe 
            src="<?php echo esc_url($frontend_url); ?>" 
            style="width:100%;height:<?php echo $height; ?>;border:none;border-radius:<?php echo $fullscreen ? '0' : '10px'; ?>;"
            frameborder="0"
            allow="microphone; camera"
        ></iframe>
    </div>
    <?php
    return ob_get_clean();
}

// Widget flotante
add_action('wp_footer', 'ai_chat_floating_widget');
function ai_chat_floating_widget() {
    if (get_option('ai_chat_show_on_all_pages') !== 'yes') {
        return;
    }
    
    $frontend_url = get_option('ai_chat_frontend_url', 'http://localhost:3000');
    $position = get_option('ai_chat_position', 'bottom-right');
    
    // Parse position
    $pos_parts = explode('-', $position);
    $vertical = $pos_parts[0]; // top or bottom
    $horizontal = $pos_parts[1]; // left or right
    ?>
    <style>
    #ai-chat-widget-button {
        position: fixed;
        <?php echo $vertical; ?>: 20px;
        <?php echo $horizontal; ?>: 20px;
        width: 60px;
        height: 60px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 50%;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        cursor: pointer;
        z-index: 999998;
        display: flex;
        align-items: center;
        justify-content: center;
        transition: transform 0.3s ease;
    }
    
    #ai-chat-widget-button:hover {
        transform: scale(1.1);
    }
    
    #ai-chat-widget-button svg {
        width: 30px;
        height: 30px;
        fill: white;
    }
    
    #ai-chat-widget-iframe {
        position: fixed;
        <?php echo $vertical; ?>: 90px;
        <?php echo $horizontal; ?>: 20px;
        width: 400px;
        height: 600px;
        max-width: calc(100vw - 40px);
        max-height: calc(100vh - 120px);
        border: none;
        border-radius: 10px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.3);
        z-index: 999999;
        display: none;
    }
    
    #ai-chat-widget-close {
        position: fixed;
        <?php echo $vertical; ?>: 90px;
        <?php echo $horizontal; ?>: 430px;
        width: 30px;
        height: 30px;
        background: #ff4444;
        border-radius: 50%;
        cursor: pointer;
        z-index: 1000000;
        display: none;
        align-items: center;
        justify-content: center;
        color: white;
        font-weight: bold;
    }
    
    @media (max-width: 768px) {
        #ai-chat-widget-iframe {
            width: calc(100vw - 40px);
            height: calc(100vh - 120px);
        }
        
        #ai-chat-widget-close {
            <?php echo $horizontal; ?>: calc(100vw - 30px);
        }
    }
    </style>
    
    <div id="ai-chat-widget-button" onclick="toggleAIChat()">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
            <path d="M20 2H4c-1.1 0-2 .9-2 2v18l4-4h14c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zm0 14H6l-2 2V4h16v12z"/>
        </svg>
    </div>
    
    <div id="ai-chat-widget-close" onclick="toggleAIChat()">×</div>
    
    <iframe 
        id="ai-chat-widget-iframe"
        src="<?php echo esc_url($frontend_url); ?>"
        allow="microphone; camera"
    ></iframe>
    
    <script>
    function toggleAIChat() {
        var iframe = document.getElementById('ai-chat-widget-iframe');
        var closeBtn = document.getElementById('ai-chat-widget-close');
        var button = document.getElementById('ai-chat-widget-button');
        
        if (iframe.style.display === 'none' || iframe.style.display === '') {
            iframe.style.display = 'block';
            closeBtn.style.display = 'flex';
            button.style.display = 'none';
        } else {
            iframe.style.display = 'none';
            closeBtn.style.display = 'none';
            button.style.display = 'flex';
        }
    }
    </script>
    <?php
}

// Success notice
add_action('admin_notices', 'ai_chat_activation_notice');
function ai_chat_activation_notice() {
    if (get_transient('ai_chat_activated')) {
        ?>
        <div class="updated notice is-dismissible">
            <p><strong>💬 AI Chat Widget activado!</strong> Configúralo en <a href="<?php echo admin_url('admin.php?page=ai-chat-settings'); ?>">AI Chat → Settings</a></p>
        </div>
        <?php
        delete_transient('ai_chat_activated');
    }
}

add_action('activated_plugin', 'ai_chat_set_activation_transient');
function ai_chat_set_activation_transient($plugin) {
    if ($plugin == plugin_basename(__FILE__)) {
        set_transient('ai_chat_activated', true, 30);
    }
}
