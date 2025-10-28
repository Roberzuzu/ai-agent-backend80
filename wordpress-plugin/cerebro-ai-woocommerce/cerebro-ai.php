<?php
/**
 * Plugin Name: Cerebro AI - Asistente Experto WooCommerce
 * Plugin URI: https://cerebroai.com
 * Description: Asistente de IA avanzado para gestión de WooCommerce. Sube fotos de productos, optimiza catálogos, crea ofertas y mucho más.
 * Version: 1.2.0
 * Author: Cerebro AI Team
 * Author URI: https://cerebroai.com
 * License: GPL v2 or later
 * License URI: https://www.gnu.org/licenses/gpl-2.0.html
 * Text Domain: cerebro-ai
 * Requires at least: 5.8
 * Requires PHP: 7.4
 * WC requires at least: 5.0
 * WC tested up to: 8.5
 */

// Evitar acceso directo
if (!defined('ABSPATH')) {
    exit;
}

// Constantes del plugin
define('CEREBRO_AI_VERSION', '1.1.1');
define('CEREBRO_AI_PLUGIN_DIR', plugin_dir_path(__FILE__));
define('CEREBRO_AI_PLUGIN_URL', plugin_dir_url(__FILE__));
define('CEREBRO_AI_PLUGIN_FILE', __FILE__);

/**
 * Clase principal del plugin
 */
class Cerebro_AI_WooCommerce {
    
    private static $instance = null;
    
    public static function get_instance() {
        if (null === self::$instance) {
            self::$instance = new self();
        }
        return self::$instance;
    }
    
    private function __construct() {
        $this->init_hooks();
    }
    
    private function init_hooks() {
        // Activación del plugin
        register_activation_hook(CEREBRO_AI_PLUGIN_FILE, array($this, 'activate'));
        
        // Admin
        add_action('admin_menu', array($this, 'add_admin_menu'));
        add_action('admin_init', array($this, 'register_settings'));
        add_action('admin_enqueue_scripts', array($this, 'admin_enqueue_scripts'));
        
        // Frontend - Solo para administradores
        if (current_user_can('manage_woocommerce')) {
            add_action('wp_footer', array($this, 'render_chat_widget'));
            add_action('wp_enqueue_scripts', array($this, 'enqueue_scripts'));
        }
        
        // Shortcode
        add_shortcode('cerebro_chat', array($this, 'render_shortcode'));
        
        // AJAX handlers
        add_action('wp_ajax_cerebro_ai_proxy', array($this, 'ajax_proxy'));
    }
    
    /**
     * Activación del plugin
     */
    public function activate() {
        // Configuración por defecto
        $defaults = array(
            'api_url' => 'https://ai-agent-backend80.onrender.com/api',
            'chat_position' => 'bottom-right',
            'chat_enabled' => true,
            'admin_only' => true,
        );
        
        if (!get_option('cerebro_ai_settings')) {
            add_option('cerebro_ai_settings', $defaults);
        } else {
            // Actualizar API URL si existe configuración previa
            $current_settings = get_option('cerebro_ai_settings');
            $current_settings['api_url'] = 'https://ai-agent-backend80.onrender.com/api';
            update_option('cerebro_ai_settings', $current_settings);
        }
    }
    
    /**
     * Agregar menú de administración
     */
    public function add_admin_menu() {
        add_menu_page(
            'Cerebro AI',
            'Cerebro AI',
            'manage_woocommerce',
            'cerebro-ai',
            array($this, 'render_admin_page'),
            'dashicons-brain',
            56
        );
        
        add_submenu_page(
            'cerebro-ai',
            'Configuración',
            'Configuración',
            'manage_woocommerce',
            'cerebro-ai',
            array($this, 'render_admin_page')
        );
        
        add_submenu_page(
            'cerebro-ai',
            'Prompts Personalizados',
            'Prompts',
            'manage_woocommerce',
            'cerebro-ai-prompts',
            array($this, 'render_prompts_page')
        );
    }
    
    /**
     * Registrar configuraciones
     */
    public function register_settings() {
        register_setting('cerebro_ai_settings_group', 'cerebro_ai_settings');
    }
    
    /**
     * Scripts del admin
     */
    public function admin_enqueue_scripts($hook) {
        if ('toplevel_page_cerebro-ai' !== $hook) {
            return;
        }
        
        wp_enqueue_style(
            'cerebro-ai-admin',
            CEREBRO_AI_PLUGIN_URL . 'assets/admin.css',
            array(),
            CEREBRO_AI_VERSION
        );
    }
    
    /**
     * Scripts del frontend
     */
    public function enqueue_scripts() {
        wp_enqueue_style(
            'cerebro-ai-chat',
            CEREBRO_AI_PLUGIN_URL . 'assets/chat.css',
            array(),
            CEREBRO_AI_VERSION
        );
        
        wp_enqueue_script(
            'cerebro-ai-chat',
            CEREBRO_AI_PLUGIN_URL . 'assets/chat.js',
            array('jquery'),
            CEREBRO_AI_VERSION,
            true
        );
        
        $settings = get_option('cerebro_ai_settings');
        
        wp_localize_script('cerebro-ai-chat', 'cerebroAI', array(
            'apiUrl' => $settings['api_url'] ?? '',
            'ajaxUrl' => admin_url('admin-ajax.php'),
            'nonce' => wp_create_nonce('cerebro_ai_nonce'),
            'userId' => 'wp_user_' . get_current_user_id(),
            'userName' => wp_get_current_user()->display_name,
        ));
    }
    
    /**
     * Renderizar widget de chat
     */
    public function render_chat_widget() {
        $settings = get_option('cerebro_ai_settings');
        
        if (!isset($settings['chat_enabled']) || !$settings['chat_enabled']) {
            return;
        }
        
        include CEREBRO_AI_PLUGIN_DIR . 'templates/chat-widget.php';
    }
    
    /**
     * Shortcode [cerebro_chat]
     */
    public function render_shortcode($atts) {
        ob_start();
        include CEREBRO_AI_PLUGIN_DIR . 'templates/chat-inline.php';
        return ob_get_clean();
    }
    
    /**
     * Proxy AJAX para las llamadas a la API
     */
    public function ajax_proxy() {
        check_ajax_referer('cerebro_ai_nonce', 'nonce');
        
        if (!current_user_can('manage_woocommerce')) {
            wp_send_json_error(array('message' => 'Permisos insuficientes'));
            return;
        }
        
        $settings = get_option('cerebro_ai_settings');
        $api_url = $settings['api_url'] ?? '';
        
        if (empty($api_url)) {
            wp_send_json_error(array('message' => 'API URL no configurada'));
            return;
        }
        
        $endpoint = sanitize_text_field($_POST['endpoint'] ?? '');
        $method = sanitize_text_field($_POST['method'] ?? 'POST');
        $data = $_POST['data'] ?? array();
        
        $url = trailingslashit($api_url) . $endpoint;
        
        $args = array(
            'method' => $method,
            'timeout' => 60,
            'headers' => array(
                'Content-Type' => 'application/json',
            ),
        );
        
        if ($method === 'POST' && !empty($data)) {
            $args['body'] = json_encode($data);
        }
        
        // Log para debug (solo en development)
        error_log('Cerebro AI - Llamando a: ' . $url);
        error_log('Cerebro AI - Datos: ' . json_encode($data));
        
        $response = wp_remote_request($url, $args);
        
        if (is_wp_error($response)) {
            error_log('Cerebro AI - Error WP: ' . $response->get_error_message());
            wp_send_json_error(array('message' => $response->get_error_message()));
            return;
        }
        
        $http_code = wp_remote_retrieve_response_code($response);
        $body = wp_remote_retrieve_body($response);
        
        error_log('Cerebro AI - HTTP Code: ' . $http_code);
        error_log('Cerebro AI - Respuesta: ' . $body);
        
        if ($http_code !== 200) {
            wp_send_json_error(array(
                'message' => 'Error del servidor: HTTP ' . $http_code,
                'http_code' => $http_code,
                'body' => $body
            ));
            return;
        }
        
        $decoded = json_decode($body, true);
        
        if (json_last_error() !== JSON_ERROR_NONE) {
            error_log('Cerebro AI - Error JSON: ' . json_last_error_msg());
            wp_send_json_error(array(
                'message' => 'Error decodificando JSON: ' . json_last_error_msg(),
                'raw_body' => substr($body, 0, 200)
            ));
            return;
        }
        
        if ($decoded === null) {
            wp_send_json_error(array('message' => 'Respuesta vacía del servidor'));
            return;
        }
        
        wp_send_json_success($decoded);
    }
    
    /**
     * Página de administración
     */
    public function render_admin_page() {
        include CEREBRO_AI_PLUGIN_DIR . 'templates/admin-page.php';
    }
    
    /**
     * Página de prompts
     */
    public function render_prompts_page() {
        include CEREBRO_AI_PLUGIN_DIR . 'templates/prompts-page.php';
    }
}

// Inicializar el plugin
function cerebro_ai_init() {
    return Cerebro_AI_WooCommerce::get_instance();
}

add_action('plugins_loaded', 'cerebro_ai_init');
