<?php
/**
 * Plugin Name: AI Dropshipping Manager
 * Plugin URI: https://herramientasyaccesorios.store
 * Description: Gestión automática de productos dropshipping con IA - Calcula precios óptimos y genera contenido profesional
 * Version: 1.1.0
 * Author: Agente Monetización
 * Author URI: https://emergentagent.com
 * License: GPL v2 or later
 * Text Domain: ai-dropshipping
 * Requires at least: 5.8
 * Requires PHP: 7.4
 * WC requires at least: 5.0
 * WC tested up to: 8.0
 */

// Exit if accessed directly
if (!defined('ABSPATH')) {
    exit;
}

// Define plugin constants
define('AI_DROPSHIP_VERSION', '1.1.0');
define('AI_DROPSHIP_PATH', plugin_dir_path(__FILE__));
define('AI_DROPSHIP_URL', plugin_dir_url(__FILE__));
define('AI_DROPSHIP_FILE', __FILE__);

// API Configuration - CAMBIAR POR TU URL DE API
define('AI_DROPSHIP_API_URL', 'https://agente90.preview.emergentagent.com/api');

/**
 * Main Plugin Class
 */
class AI_Dropshipping_Manager {
    
    private static $instance = null;
    
    public static function get_instance() {
        if (null === self::$instance) {
            self::$instance = new self();
        }
        return self::$instance;
    }
    
    private function __construct() {
        add_action('plugins_loaded', array($this, 'init'));
    }
    
    public function init() {
        // Check if WooCommerce is active
        if (!class_exists('WooCommerce')) {
            add_action('admin_notices', array($this, 'woocommerce_missing_notice'));
            return;
        }
        
        // Load plugin components
        $this->load_includes();
        
        // Admin hooks
        if (is_admin()) {
            add_action('admin_menu', array($this, 'add_admin_menu'));
            add_action('admin_enqueue_scripts', array($this, 'enqueue_admin_assets'));
        }
        
        // Product meta box
        add_action('add_meta_boxes', array($this, 'add_product_meta_box'));
        
        // AJAX handlers
        add_action('wp_ajax_ai_process_product', array($this, 'ajax_process_product'));
        add_action('wp_ajax_ai_generate_content', array($this, 'ajax_generate_content'));
        add_action('wp_ajax_ai_process_all', array($this, 'ajax_process_all'));
        add_action('wp_ajax_ai_get_stats', array($this, 'ajax_get_stats'));
    }
    
    private function load_includes() {
        // Include API client
        require_once AI_DROPSHIP_PATH . 'includes/class-api-client.php';
        require_once AI_DROPSHIP_PATH . 'includes/class-product-processor.php';
    }
    
    public function woocommerce_missing_notice() {
        ?>
        <div class="notice notice-error">
            <p><?php _e('AI Dropshipping Manager requiere WooCommerce para funcionar. Por favor, instala y activa WooCommerce.', 'ai-dropshipping'); ?></p>
        </div>
        <?php
    }
    
    public function add_admin_menu() {
        add_menu_page(
            __('AI Dropshipping', 'ai-dropshipping'),
            __('AI Dropshipping', 'ai-dropshipping'),
            'manage_woocommerce',
            'ai-dropshipping',
            array($this, 'render_admin_page'),
            'dashicons-store',
            56
        );
        
        add_submenu_page(
            'ai-dropshipping',
            __('Dashboard', 'ai-dropshipping'),
            __('Dashboard', 'ai-dropshipping'),
            'manage_woocommerce',
            'ai-dropshipping',
            array($this, 'render_admin_page')
        );
        
        add_submenu_page(
            'ai-dropshipping',
            __('Configuración', 'ai-dropshipping'),
            __('Configuración', 'ai-dropshipping'),
            'manage_options',
            'ai-dropshipping-settings',
            array($this, 'render_settings_page')
        );
    }
    
    public function enqueue_admin_assets($hook) {
        if (strpos($hook, 'ai-dropshipping') === false && $hook !== 'post.php' && $hook !== 'post-new.php') {
            return;
        }
        
        wp_enqueue_style(
            'ai-dropship-admin',
            AI_DROPSHIP_URL . 'assets/css/admin.css',
            array(),
            AI_DROPSHIP_VERSION
        );
        
        wp_enqueue_script(
            'ai-dropship-admin',
            AI_DROPSHIP_URL . 'assets/js/admin.js',
            array('jquery'),
            AI_DROPSHIP_VERSION,
            true
        );
        
        wp_localize_script('ai-dropship-admin', 'aiDropship', array(
            'ajax_url' => admin_url('admin-ajax.php'),
            'nonce' => wp_create_nonce('ai_dropship_nonce'),
            'strings' => array(
                'processing' => __('Procesando...', 'ai-dropshipping'),
                'success' => __('¡Completado!', 'ai-dropshipping'),
                'error' => __('Error', 'ai-dropshipping'),
            )
        ));
    }
    
    public function add_product_meta_box() {
        add_meta_box(
            'ai-dropship-actions',
            __('🤖 AI Dropshipping', 'ai-dropshipping'),
            array($this, 'render_product_meta_box'),
            'product',
            'side',
            'high'
        );
    }
    
    public function render_product_meta_box($post) {
        $product = wc_get_product($post->ID);
        $price = $product->get_regular_price();
        $has_price = !empty($price) && $price > 0;
        
        ?>
        <div class="ai-dropship-meta-box">
            <p class="ai-dropship-status">
                <?php if ($has_price): ?>
                    <span class="dashicons dashicons-yes-alt" style="color: #46b450;"></span>
                    <strong><?php _e('Precio configurado:', 'ai-dropshipping'); ?></strong> €<?php echo esc_html($price); ?>
                <?php else: ?>
                    <span class="dashicons dashicons-warning" style="color: #f56e28;"></span>
                    <strong><?php _e('Sin precio configurado', 'ai-dropshipping'); ?></strong>
                <?php endif; ?>
            </p>
            
            <div class="ai-dropship-actions" style="margin-top: 15px;">
                <button type="button" class="button button-primary button-large ai-process-product" data-product-id="<?php echo esc_attr($post->ID); ?>" style="width: 100%; margin-bottom: 8px;">
                    <span class="dashicons dashicons-update"></span>
                    <?php _e('Calcular Precio Óptimo', 'ai-dropshipping'); ?>
                </button>
                
                <button type="button" class="button button-secondary button-large ai-generate-content" data-product-id="<?php echo esc_attr($post->ID); ?>" style="width: 100%;">
                    <span class="dashicons dashicons-format-image"></span>
                    <?php _e('Generar Contenido IA', 'ai-dropshipping'); ?>
                </button>
            </div>
            
            <p style="margin-top: 12px; font-size: 11px; color: #666;">
                <?php _e('💡 El sistema calcula automáticamente el precio de venta con margen del 50% y genera imágenes profesionales con IA.', 'ai-dropshipping'); ?>
            </p>
        </div>
        <style>
            .ai-dropship-meta-box .ai-dropship-status {
                background: #f0f0f1;
                padding: 10px;
                border-radius: 4px;
                margin: 0 0 10px 0;
            }
            .ai-dropship-actions button {
                transition: all 0.3s ease;
            }
            .ai-dropship-actions button:hover {
                transform: translateY(-2px);
                box-shadow: 0 2px 8px rgba(0,0,0,0.15);
            }
            .ai-dropship-actions button .dashicons {
                margin-right: 5px;
            }
        </style>
        <?php
    }
    
    public function render_admin_page() {
        include AI_DROPSHIP_PATH . 'admin/dashboard.php';
    }
    
    public function render_settings_page() {
        include AI_DROPSHIP_PATH . 'admin/settings.php';
    }
    
    // AJAX Handlers
    public function ajax_process_product() {
        check_ajax_referer('ai_dropship_nonce', 'nonce');
        
        if (!current_user_can('manage_woocommerce')) {
            wp_send_json_error('Unauthorized');
        }
        
        $product_id = intval($_POST['product_id']);
        
        try {
            $processor = new AI_Dropship_Product_Processor();
            $result = $processor->process_product($product_id);
            wp_send_json_success($result);
        } catch (Exception $e) {
            wp_send_json_error($e->getMessage());
        }
    }
    
    public function ajax_generate_content() {
        check_ajax_referer('ai_dropship_nonce', 'nonce');
        
        if (!current_user_can('manage_woocommerce')) {
            wp_send_json_error('Unauthorized');
        }
        
        $product_id = intval($_POST['product_id']);
        
        try {
            $processor = new AI_Dropship_Product_Processor();
            $result = $processor->generate_content($product_id);
            wp_send_json_success($result);
        } catch (Exception $e) {
            wp_send_json_error($e->getMessage());
        }
    }
    
    public function ajax_process_all() {
        check_ajax_referer('ai_dropship_nonce', 'nonce');
        
        if (!current_user_can('manage_woocommerce')) {
            wp_send_json_error('Unauthorized');
        }
        
        try {
            $processor = new AI_Dropship_Product_Processor();
            $result = $processor->process_all_products();
            wp_send_json_success($result);
        } catch (Exception $e) {
            wp_send_json_error($e->getMessage());
        }
    }
    
    public function ajax_get_stats() {
        check_ajax_referer('ai_dropship_nonce', 'nonce');
        
        if (!current_user_can('manage_woocommerce')) {
            wp_send_json_error('Unauthorized');
        }
        
        $api_client = new AI_Dropship_API_Client();
        $stats = $api_client->get_stats();
        wp_send_json_success($stats);
    }
}

// Initialize plugin
function ai_dropshipping_manager_init() {
    return AI_Dropshipping_Manager::get_instance();
}

add_action('plugins_loaded', 'ai_dropshipping_manager_init');

// Activation hook
register_activation_hook(__FILE__, 'ai_dropshipping_activate');
function ai_dropshipping_activate() {
    // Set default options
    add_option('ai_dropship_api_url', AI_DROPSHIP_API_URL);
    add_option('ai_dropship_auto_process', 'yes');
    add_option('ai_dropship_auto_generate_content', 'no');
    
    // Flush rewrite rules
    flush_rewrite_rules();
}

// Deactivation hook
register_deactivation_hook(__FILE__, 'ai_dropshipping_deactivate');
function ai_dropshipping_deactivate() {
    flush_rewrite_rules();
}
