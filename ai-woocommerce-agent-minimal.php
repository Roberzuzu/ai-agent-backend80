<?php
/**
 * Plugin Name: AI WooCommerce Agent
 * Plugin URI: https://herramientasyaccesorios.store
 * Description: Agente AI para WooCommerce con Perplexity, OpenAI y Telegram
 * Version: 1.0.1
 * Author: HerramientasyAccesorios
 * Requires at least: 6.0
 * Tested up to: 6.4
 * Requires PHP: 7.4
 * WC requires at least: 7.0
 * WC tested up to: 8.5
 * License: GPL v2 or later
 */

// Exit if accessed directly
if (!defined('ABSPATH')) {
    exit;
}

// Define constants
define('AIWCA_VERSION', '1.0.1');
define('AIWCA_FILE', __FILE__);
define('AIWCA_PATH', plugin_dir_path(__FILE__));
define('AIWCA_URL', plugin_dir_url(__FILE__));

// Activation hook
register_activation_hook(__FILE__, 'aiwca_activate');
function aiwca_activate() {
    // Check WooCommerce
    if (!class_exists('WooCommerce')) {
        deactivate_plugins(plugin_basename(__FILE__));
        wp_die('Este plugin requiere WooCommerce. <a href="' . admin_url('plugins.php') . '">Volver</a>');
    }
    
    // Set default options
    add_option('aiwca_version', AIWCA_VERSION);
    add_option('aiwca_openai_api_key', '');
    add_option('aiwca_perplexity_api_key', '');
    add_option('aiwca_ai_provider', 'perplexity');
    
    flush_rewrite_rules();
}

// Deactivation hook
register_deactivation_hook(__FILE__, 'aiwca_deactivate');
function aiwca_deactivate() {
    flush_rewrite_rules();
}

// Check WooCommerce on admin init
add_action('admin_init', 'aiwca_check_woocommerce');
function aiwca_check_woocommerce() {
    if (!class_exists('WooCommerce')) {
        add_action('admin_notices', function() {
            echo '<div class="error"><p><strong>AI WooCommerce Agent</strong> requiere que WooCommerce esté instalado y activado.</p></div>';
        });
        deactivate_plugins(plugin_basename(__FILE__));
        if (isset($_GET['activate'])) {
            unset($_GET['activate']);
        }
    }
}

// Add admin menu
add_action('admin_menu', 'aiwca_add_menu');
function aiwca_add_menu() {
    add_menu_page(
        'AI WooCommerce Agent',
        'AI Agent',
        'manage_woocommerce',
        'ai-woocommerce-agent',
        'aiwca_dashboard_page',
        'dashicons-superhero',
        56
    );
    
    add_submenu_page(
        'ai-woocommerce-agent',
        'Settings',
        'Settings',
        'manage_options',
        'ai-woocommerce-agent-settings',
        'aiwca_settings_page'
    );
}

// Dashboard page
function aiwca_dashboard_page() {
    ?>
    <div class="wrap">
        <h1>🤖 AI WooCommerce Agent</h1>
        <div class="card" style="max-width: 800px;">
            <h2>✅ Plugin Activado Correctamente</h2>
            <p>El plugin está funcionando. Ahora configura tus API keys en Settings.</p>
            
            <h3>📊 Estadísticas</h3>
            <ul>
                <li>Total Productos: <strong><?php echo wp_count_posts('product')->publish; ?></strong></li>
                <li>Versión Plugin: <strong><?php echo AIWCA_VERSION; ?></strong></li>
                <li>WooCommerce: <strong>✓ Activo</strong></li>
            </ul>
            
            <h3>🚀 Próximos Pasos</h3>
            <ol>
                <li>Ve a <a href="<?php echo admin_url('admin.php?page=ai-woocommerce-agent-settings'); ?>">Settings</a></li>
                <li>Configura tu API key (Perplexity u OpenAI)</li>
                <li>Procesa tus productos con AI</li>
            </ol>
        </div>
    </div>
    <?php
}

// Settings page
function aiwca_settings_page() {
    // Save settings
    if (isset($_POST['aiwca_save'])) {
        check_admin_referer('aiwca_settings');
        update_option('aiwca_openai_api_key', sanitize_text_field($_POST['openai_key']));
        update_option('aiwca_perplexity_api_key', sanitize_text_field($_POST['perplexity_key']));
        update_option('aiwca_ai_provider', sanitize_text_field($_POST['ai_provider']));
        echo '<div class="updated"><p>Configuración guardada.</p></div>';
    }
    
    $openai_key = get_option('aiwca_openai_api_key', '');
    $perplexity_key = get_option('aiwca_perplexity_api_key', '');
    $provider = get_option('aiwca_ai_provider', 'perplexity');
    ?>
    <div class="wrap">
        <h1>⚙️ AI Agent - Configuración</h1>
        
        <form method="post">
            <?php wp_nonce_field('aiwca_settings'); ?>
            
            <table class="form-table">
                <tr>
                    <th scope="row">Proveedor AI</th>
                    <td>
                        <select name="ai_provider">
                            <option value="perplexity" <?php selected($provider, 'perplexity'); ?>>Perplexity (Recomendado)</option>
                            <option value="openai" <?php selected($provider, 'openai'); ?>>OpenAI</option>
                        </select>
                    </td>
                </tr>
                
                <tr>
                    <th scope="row">Perplexity API Key</th>
                    <td>
                        <input type="password" name="perplexity_key" value="<?php echo esc_attr($perplexity_key); ?>" class="regular-text" />
                        <p class="description">Obtén tu key en <a href="https://perplexity.ai" target="_blank">perplexity.ai</a></p>
                    </td>
                </tr>
                
                <tr>
                    <th scope="row">OpenAI API Key</th>
                    <td>
                        <input type="password" name="openai_key" value="<?php echo esc_attr($openai_key); ?>" class="regular-text" />
                        <p class="description">Obtén tu key en <a href="https://platform.openai.com" target="_blank">platform.openai.com</a></p>
                    </td>
                </tr>
            </table>
            
            <p class="submit">
                <button type="submit" name="aiwca_save" class="button button-primary">Guardar Configuración</button>
            </p>
        </form>
        
        <hr>
        
        <h2>🧪 Test de Conexión</h2>
        <button type="button" id="test-ai" class="button">Probar Conexión AI</button>
        <div id="test-result" style="margin-top: 10px;"></div>
        
        <script>
        jQuery(document).ready(function($) {
            $('#test-ai').click(function() {
                $(this).prop('disabled', true).text('Probando...');
                $('#test-result').html('<p>⏳ Conectando con AI...</p>');
                
                $.post(ajaxurl, {
                    action: 'aiwca_test_connection',
                    nonce: '<?php echo wp_create_nonce('aiwca_test'); ?>'
                }, function(response) {
                    if (response.success) {
                        $('#test-result').html('<div class="updated"><p>✅ ' + response.data + '</p></div>');
                    } else {
                        $('#test-result').html('<div class="error"><p>❌ ' + response.data + '</p></div>');
                    }
                    $('#test-ai').prop('disabled', false).text('Probar Conexión AI');
                });
            });
        });
        </script>
    </div>
    <?php
}

// AJAX test connection
add_action('wp_ajax_aiwca_test_connection', 'aiwca_ajax_test_connection');
function aiwca_ajax_test_connection() {
    check_ajax_referer('aiwca_test', 'nonce');
    
    $provider = get_option('aiwca_ai_provider', 'perplexity');
    $key = $provider === 'perplexity' ? get_option('aiwca_perplexity_api_key') : get_option('aiwca_openai_api_key');
    
    if (empty($key)) {
        wp_send_json_error('No has configurado ninguna API key');
    }
    
    // Test API
    $url = $provider === 'perplexity' ? 'https://api.perplexity.ai/chat/completions' : 'https://api.openai.com/v1/chat/completions';
    
    $response = wp_remote_post($url, array(
        'headers' => array(
            'Authorization' => 'Bearer ' . $key,
            'Content-Type' => 'application/json',
        ),
        'body' => json_encode(array(
            'model' => $provider === 'perplexity' ? 'sonar-pro' : 'gpt-4o',
            'messages' => array(array('role' => 'user', 'content' => 'test')),
            'max_tokens' => 10
        )),
        'timeout' => 30,
    ));
    
    if (is_wp_error($response)) {
        wp_send_json_error('Error: ' . $response->get_error_message());
    }
    
    $code = wp_remote_retrieve_response_code($response);
    
    if ($code === 200) {
        wp_send_json_success('Conexión exitosa con ' . ucfirst($provider));
    } else {
        $body = json_decode(wp_remote_retrieve_body($response), true);
        $error = isset($body['error']['message']) ? $body['error']['message'] : 'Error ' . $code;
        wp_send_json_error($error);
    }
}

// Add AI button to product edit page
add_action('woocommerce_product_options_general_product_data', 'aiwca_add_product_button');
function aiwca_add_product_button() {
    global $post;
    ?>
    <div class="options_group">
        <p class="form-field">
            <label>🤖 AI Optimization</label>
            <button type="button" class="button button-primary" id="aiwca-process-product" data-product-id="<?php echo $post->ID; ?>">
                Procesar con AI
            </button>
            <span class="description">Genera descripción optimizada y precio con AI</span>
        </p>
    </div>
    
    <script>
    jQuery(document).ready(function($) {
        $('#aiwca-process-product').click(function() {
            var productId = $(this).data('product-id');
            var $btn = $(this);
            
            $btn.prop('disabled', true).text('Procesando...');
            
            $.post(ajaxurl, {
                action: 'aiwca_process_product',
                product_id: productId,
                nonce: '<?php echo wp_create_nonce('aiwca_process'); ?>'
            }, function(response) {
                alert(response.data);
                $btn.prop('disabled', false).text('Procesar con AI');
                if (response.success) {
                    location.reload();
                }
            });
        });
    });
    </script>
    <?php
}

// AJAX process product
add_action('wp_ajax_aiwca_process_product', 'aiwca_ajax_process_product');
function aiwca_ajax_process_product() {
    check_ajax_referer('aiwca_process', 'nonce');
    
    $product_id = intval($_POST['product_id']);
    $product = wc_get_product($product_id);
    
    if (!$product) {
        wp_send_json_error('Producto no encontrado');
    }
    
    $provider = get_option('aiwca_ai_provider', 'perplexity');
    $key = $provider === 'perplexity' ? get_option('aiwca_perplexity_api_key') : get_option('aiwca_openai_api_key');
    
    if (empty($key)) {
        wp_send_json_error('Configura tu API key primero en Settings');
    }
    
    $product_name = $product->get_name();
    $prompt = "Genera una descripción SEO optimizada en español para este producto de WooCommerce: {$product_name}. La descripción debe tener 200-300 palabras, ser persuasiva y estar optimizada para motores de búsqueda.";
    
    // Call AI
    $url = $provider === 'perplexity' ? 'https://api.perplexity.ai/chat/completions' : 'https://api.openai.com/v1/chat/completions';
    
    $response = wp_remote_post($url, array(
        'headers' => array(
            'Authorization' => 'Bearer ' . $key,
            'Content-Type' => 'application/json',
        ),
        'body' => json_encode(array(
            'model' => $provider === 'perplexity' ? 'sonar-pro' : 'gpt-4o',
            'messages' => array(array('role' => 'user', 'content' => $prompt)),
            'max_tokens' => 500
        )),
        'timeout' => 60,
    ));
    
    if (is_wp_error($response)) {
        wp_send_json_error('Error AI: ' . $response->get_error_message());
    }
    
    $body = json_decode(wp_remote_retrieve_body($response), true);
    
    if (isset($body['choices'][0]['message']['content'])) {
        $description = $body['choices'][0]['message']['content'];
        
        // Update product
        $product->set_description($description);
        $product->save();
        
        wp_send_json_success('✅ Producto optimizado con AI usando ' . ucfirst($provider));
    } else {
        wp_send_json_error('No se pudo generar descripción');
    }
}

// Success notice
add_action('admin_notices', 'aiwca_activation_notice');
function aiwca_activation_notice() {
    if (get_transient('aiwca_activated')) {
        ?>
        <div class="updated notice is-dismissible">
            <p><strong>🎉 AI WooCommerce Agent activado correctamente!</strong> Ve a <a href="<?php echo admin_url('admin.php?page=ai-woocommerce-agent-settings'); ?>">Settings</a> para configurar.</p>
        </div>
        <?php
        delete_transient('aiwca_activated');
    }
}

// Set activation transient
add_action('activated_plugin', 'aiwca_set_activation_transient');
function aiwca_set_activation_transient($plugin) {
    if ($plugin == plugin_basename(__FILE__)) {
        set_transient('aiwca_activated', true, 30);
    }
}
