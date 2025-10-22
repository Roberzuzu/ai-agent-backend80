<?php
/**
 * Plugin Name: AI Chat Widget - Admin Only
 * Description: Chat AI solo visible para administradores
 * Version: 1.1.0
 * Author: HerramientasyAccesorios
 */

if (!defined('ABSPATH')) exit;

// Add admin menu
add_action('admin_menu', 'ai_chat_admin_add_menu');
function ai_chat_admin_add_menu() {
    add_menu_page(
        'AI Chat Admin Settings',
        'AI Chat Admin',
        'manage_options',
        'ai-chat-admin-settings',
        'ai_chat_admin_settings_page',
        'dashicons-format-chat',
        60
    );
}

// Settings page
function ai_chat_admin_settings_page() {
    if (isset($_POST['save_chat_settings'])) {
        check_admin_referer('ai_chat_settings');
        update_option('ai_chat_backend_url', sanitize_text_field($_POST['backend_url']));
        update_option('ai_chat_frontend_url', sanitize_text_field($_POST['frontend_url']));
        update_option('ai_chat_show_widget', isset($_POST['show_widget']) ? 'yes' : 'no');
        update_option('ai_chat_admin_only', isset($_POST['admin_only']) ? 'yes' : 'no');
        echo '<div class="updated"><p>✅ Configuración guardada!</p></div>';
    }
    
    $backend_url = get_option('ai_chat_backend_url', '');
    $frontend_url = get_option('ai_chat_frontend_url', '');
    $show_widget = get_option('ai_chat_show_widget', 'no');
    $admin_only = get_option('ai_chat_admin_only', 'yes');
    ?>
    <div class="wrap">
        <h1>💬 AI Chat - Configuración Admin</h1>
        
        <div class="notice notice-info">
            <p><strong>ℹ️ Estado Actual:</strong></p>
            <ul>
                <li>Backend configurado: <?php echo !empty($backend_url) ? '<span style="color:green;">✓ Sí</span>' : '<span style="color:red;">✗ No</span>'; ?></li>
                <li>Frontend configurado: <?php echo !empty($frontend_url) ? '<span style="color:green;">✓ Sí</span>' : '<span style="color:red;">✗ No</span>'; ?></li>
                <li>Widget visible: <?php echo $show_widget === 'yes' ? '<span style="color:green;">✓ Sí</span>' : '<span style="color:red;">✗ No</span>'; ?></li>
                <li>Solo admin: <?php echo $admin_only === 'yes' ? '<span style="color:green;">✓ Sí</span>' : '<span style="color:orange;">✗ No (visible para todos)</span>'; ?></li>
            </ul>
        </div>
        
        <form method="post">
            <?php wp_nonce_field('ai_chat_settings'); ?>
            
            <table class="form-table">
                <tr>
                    <th>Backend URL</th>
                    <td>
                        <input type="url" name="backend_url" value="<?php echo esc_attr($backend_url); ?>" class="regular-text" placeholder="http://herramientasyaccesorios.store:8001" />
                        <p class="description">⚠️ <strong>IMPORTANTE:</strong> Debes desplegar el backend primero. Ver instrucciones abajo.</p>
                    </td>
                </tr>
                
                <tr>
                    <th>Frontend URL</th>
                    <td>
                        <input type="url" name="frontend_url" value="<?php echo esc_attr($frontend_url); ?>" class="regular-text" placeholder="http://herramientasyaccesorios.store:3000" />
                        <p class="description">URL del frontend React con el chat</p>
                    </td>
                </tr>
                
                <tr>
                    <th>Mostrar Widget</th>
                    <td>
                        <label>
                            <input type="checkbox" name="show_widget" <?php checked($show_widget, 'yes'); ?> />
                            Activar widget flotante de chat
                        </label>
                        <p class="description">Si no está marcado, el chat NO aparecerá</p>
                    </td>
                </tr>
                
                <tr>
                    <th>Solo Administrador</th>
                    <td>
                        <label>
                            <input type="checkbox" name="admin_only" <?php checked($admin_only, 'yes'); ?> />
                            Chat visible solo para administradores
                        </label>
                        <p class="description">✅ <strong>Recomendado:</strong> Solo tú verás el chat</p>
                    </td>
                </tr>
            </table>
            
            <p class="submit">
                <button type="submit" name="save_chat_settings" class="button button-primary button-large">💾 Guardar Configuración</button>
            </p>
        </form>
        
        <hr>
        
        <div class="notice notice-warning">
            <h3>⚠️ EL BACKEND NO ESTÁ DESPLEGADO AÚN</h3>
            <p>El chat widget solo funcionará cuando despliegues el backend standalone en tu servidor.</p>
            <p><strong>Archivos necesarios:</strong></p>
            <ul>
                <li><code>miapp-standalone-20251022-142042.zip</code> (637 KB)</li>
                <li><code>DEPLOYMENT_HERRAMIENTAS.md</code> (guía de instalación)</li>
                <li><code>install-herramientas.sh</code> (script automático)</li>
            </ul>
            <p><strong>Ubicación:</strong> <code>/app/</code> en el servidor donde trabajaste conmigo</p>
        </div>
        
        <hr>
        
        <h2>🧪 Test de Conexión</h2>
        <button type="button" id="test-backend" class="button button-secondary">🔌 Probar Backend</button>
        <button type="button" id="test-frontend" class="button button-secondary">🖥️ Probar Frontend</button>
        <div id="test-result" style="margin-top:15px;"></div>
        
        <hr>
        
        <h2>📖 Cómo Funciona</h2>
        <ol>
            <li><strong>Backend:</strong> API FastAPI que procesa las peticiones del chat</li>
            <li><strong>Frontend:</strong> Interfaz React con el chat interactivo</li>
            <li><strong>Widget:</strong> Botón flotante que abre el chat en iframe</li>
        </ol>
        
        <h3>Para que el chat funcione:</h3>
        <ol>
            <li>✅ Desplegar backend en tu servidor (puerto 8001)</li>
            <li>✅ Iniciar frontend React (puerto 3000)</li>
            <li>✅ Configurar URLs aquí arriba</li>
            <li>✅ Marcar "Mostrar Widget"</li>
            <li>✅ Guardar configuración</li>
        </ol>
        
        <script>
        jQuery(document).ready(function($) {
            $('#test-backend').click(function() {
                var backendUrl = $('input[name="backend_url"]').val();
                if (!backendUrl) {
                    alert('❌ Configura la Backend URL primero');
                    return;
                }
                
                $(this).prop('disabled', true).text('Probando...');
                $('#test-result').html('<p>⏳ Conectando con backend...</p>');
                
                $.ajax({
                    url: backendUrl + '/api/health',
                    timeout: 5000
                })
                .done(function() {
                    $('#test-result').html('<div class="updated"><p>✅ <strong>Backend conectado correctamente!</strong></p></div>');
                })
                .fail(function(jqXHR) {
                    if (jqXHR.status === 0) {
                        $('#test-result').html('<div class="error"><p>❌ <strong>No se pudo conectar.</strong><br>El backend no está corriendo o la URL es incorrecta.<br>Verifica que el backend esté desplegado en tu servidor.</p></div>');
                    } else {
                        $('#test-result').html('<div class="error"><p>❌ Error: ' + jqXHR.status + '</p></div>');
                    }
                })
                .always(function() {
                    $('#test-backend').prop('disabled', false).text('🔌 Probar Backend');
                });
            });
            
            $('#test-frontend').click(function() {
                var frontendUrl = $('input[name="frontend_url"]').val();
                if (!frontendUrl) {
                    alert('❌ Configura la Frontend URL primero');
                    return;
                }
                
                $(this).prop('disabled', true).text('Probando...');
                $('#test-result').html('<p>⏳ Conectando con frontend...</p>');
                
                $.ajax({
                    url: frontendUrl,
                    timeout: 5000
                })
                .done(function() {
                    $('#test-result').html('<div class="updated"><p>✅ <strong>Frontend accesible!</strong></p></div>');
                })
                .fail(function() {
                    $('#test-result').html('<div class="error"><p>❌ <strong>Frontend no accesible.</strong><br>Verifica que el frontend esté corriendo en tu servidor.</p></div>');
                })
                .always(function() {
                    $('#test-frontend').prop('disabled', false).text('🖥️ Probar Frontend');
                });
            });
        });
        </script>
    </div>
    <?php
}

// Widget flotante SOLO para admin
add_action('wp_footer', 'ai_chat_admin_floating_widget');
function ai_chat_admin_floating_widget() {
    // Verificar permisos de admin
    if (!current_user_can('manage_options')) {
        return;
    }
    
    // Verificar que esté activado
    if (get_option('ai_chat_show_widget') !== 'yes') {
        return;
    }
    
    $backend_url = get_option('ai_chat_backend_url', '');
    $frontend_url = get_option('ai_chat_frontend_url', '');
    
    // Si no hay URLs configuradas, mostrar mensaje
    if (empty($backend_url) || empty($frontend_url)) {
        ?>
        <div style="position:fixed;bottom:20px;right:20px;background:#ff9800;color:white;padding:15px;border-radius:10px;box-shadow:0 4px 12px rgba(0,0,0,0.3);z-index:999999;max-width:300px;">
            <strong>⚠️ AI Chat no configurado</strong>
            <p style="margin:10px 0 0 0;font-size:12px;">Ve a <strong>AI Chat Admin → Settings</strong> para configurar las URLs del backend.</p>
        </div>
        <?php
        return;
    }
    
    ?>
    <style>
    #ai-chat-admin-widget-button {
        position: fixed;
        bottom: 20px;
        right: 20px;
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
    
    #ai-chat-admin-widget-button:hover {
        transform: scale(1.1);
    }
    
    #ai-chat-admin-widget-button svg {
        width: 30px;
        height: 30px;
        fill: white;
    }
    
    #ai-chat-admin-widget-button::after {
        content: 'ADMIN';
        position: absolute;
        bottom: -20px;
        left: 50%;
        transform: translateX(-50%);
        font-size: 9px;
        color: #667eea;
        font-weight: bold;
        white-space: nowrap;
    }
    
    #ai-chat-admin-iframe {
        position: fixed;
        bottom: 90px;
        right: 20px;
        width: 420px;
        height: 650px;
        max-width: calc(100vw - 40px);
        max-height: calc(100vh - 120px);
        border: none;
        border-radius: 10px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.3);
        z-index: 999999;
        display: none;
        background: white;
    }
    
    #ai-chat-admin-close {
        position: fixed;
        bottom: 90px;
        right: 450px;
        width: 35px;
        height: 35px;
        background: #ff4444;
        border-radius: 50%;
        cursor: pointer;
        z-index: 1000000;
        display: none;
        align-items: center;
        justify-content: center;
        color: white;
        font-weight: bold;
        font-size: 20px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.3);
    }
    
    #ai-chat-admin-close:hover {
        background: #cc0000;
    }
    
    @media (max-width: 768px) {
        #ai-chat-admin-iframe {
            width: calc(100vw - 40px);
            height: calc(100vh - 120px);
            right: 20px;
        }
        
        #ai-chat-admin-close {
            right: calc(100vw - 35px);
        }
    }
    </style>
    
    <div id="ai-chat-admin-widget-button" onclick="toggleAdminAIChat()" title="Chat AI Admin">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
            <path d="M20 2H4c-1.1 0-2 .9-2 2v18l4-4h14c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zm0 14H6l-2 2V4h16v12z"/>
            <circle cx="12" cy="10" r="1.5"/>
            <circle cx="8" cy="10" r="1.5"/>
            <circle cx="16" cy="10" r="1.5"/>
        </svg>
    </div>
    
    <div id="ai-chat-admin-close" onclick="toggleAdminAIChat()" title="Cerrar chat">×</div>
    
    <iframe 
        id="ai-chat-admin-iframe"
        src="<?php echo esc_url($frontend_url); ?>"
        allow="microphone; camera"
    ></iframe>
    
    <script>
    function toggleAdminAIChat() {
        var iframe = document.getElementById('ai-chat-admin-iframe');
        var closeBtn = document.getElementById('ai-chat-admin-close');
        var button = document.getElementById('ai-chat-admin-widget-button');
        
        if (iframe.style.display === 'none' || iframe.style.display === '') {
            iframe.style.display = 'block';
            closeBtn.style.display = 'flex';
            button.style.opacity = '0.5';
        } else {
            iframe.style.display = 'none';
            closeBtn.style.display = 'none';
            button.style.opacity = '1';
        }
    }
    </script>
    <?php
}

// Notice de activación
add_action('admin_notices', 'ai_chat_admin_activation_notice');
function ai_chat_admin_activation_notice() {
    if (get_transient('ai_chat_admin_activated')) {
        ?>
        <div class="updated notice is-dismissible">
            <p><strong>💬 AI Chat Admin activado!</strong></p>
            <p>Ve a <a href="<?php echo admin_url('admin.php?page=ai-chat-admin-settings'); ?>"><strong>AI Chat Admin → Settings</strong></a> para configurar.</p>
            <p><strong>⚠️ IMPORTANTE:</strong> Necesitas desplegar el backend standalone primero.</p>
        </div>
        <?php
        delete_transient('ai_chat_admin_activated');
    }
}

add_action('activated_plugin', 'ai_chat_admin_set_activation_transient');
function ai_chat_admin_set_activation_transient($plugin) {
    if ($plugin == plugin_basename(__FILE__)) {
        set_transient('ai_chat_admin_activated', true, 60);
    }
}

// Notice si el widget está activo pero no hay URLs
add_action('admin_notices', 'ai_chat_admin_config_reminder');
function ai_chat_admin_config_reminder() {
    $screen = get_current_screen();
    if ($screen->id === 'toplevel_page_ai-chat-admin-settings') {
        return; // No mostrar en la página de settings
    }
    
    if (get_option('ai_chat_show_widget') === 'yes') {
        $backend = get_option('ai_chat_backend_url', '');
        $frontend = get_option('ai_chat_frontend_url', '');
        
        if (empty($backend) || empty($frontend)) {
            ?>
            <div class="notice notice-warning">
                <p><strong>⚠️ AI Chat:</strong> Widget activado pero URLs no configuradas. 
                <a href="<?php echo admin_url('admin.php?page=ai-chat-admin-settings'); ?>">Configurar ahora</a></p>
            </div>
            <?php
        }
    }
}
