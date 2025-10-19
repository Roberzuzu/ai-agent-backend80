<?php
/**
 * Plugin Name: AI Dropshipping Manager - Super Powered
 * Plugin URI: https://herramientasyaccesorios.store
 * Description: Gestión AUTOMÁTICA de productos con IA avanzada - OpenRouter + Perplexity + Abacus AI para análisis de mercado, precios óptimos y contenido profesional
 * Version: 2.0.0
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
define('AI_DROPSHIP_VERSION', '2.0.0');
define('AI_DROPSHIP_PATH', plugin_dir_path(__FILE__));
define('AI_DROPSHIP_URL', plugin_dir_url(__FILE__));
define('AI_DROPSHIP_FILE', __FILE__);

// API Configuration
define('AI_DROPSHIP_API_URL', 'https://signal-stream.preview.emergentagent.com/api');

// AI Super Powers - APIs Externas
define('OPENROUTER_API_KEY', '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');
define('ABACUS_API_KEY', 's2_3902ed8d205a4c2f95f35e7a361fbb59');
define('PERPLEXITY_API_KEY', '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');

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
        
        // NUEVOS: AI Super Powers
        add_action('wp_ajax_ai_complete_process', array($this, 'ajax_complete_process'));
        add_action('wp_ajax_ai_generate_description', array($this, 'ajax_generate_description'));
        add_action('wp_ajax_ai_generate_images', array($this, 'ajax_generate_images'));
        add_action('wp_ajax_ai_market_analysis', array($this, 'ajax_market_analysis'));
        add_action('wp_ajax_ai_optimal_pricing', array($this, 'ajax_optimal_pricing'));
        add_action('wp_ajax_ai_social_content', array($this, 'ajax_social_content'));
        add_action('wp_ajax_ai_email_campaign', array($this, 'ajax_email_campaign'));
    }
    
    private function load_includes() {
        // Include API client
        require_once AI_DROPSHIP_PATH . 'includes/class-api-client.php';
        require_once AI_DROPSHIP_PATH . 'includes/class-ai-client.php'; // NUEVO: Cliente AI Super Powered
        require_once AI_DROPSHIP_PATH . 'includes/class-product-processor.php';
        require_once AI_DROPSHIP_PATH . 'includes/class-ai-superpowered.php'; // NUEVO: IA Avanzada
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
                <button type="button" class="button button-primary button-large ai-complete-process" data-product-id="<?php echo esc_attr($post->ID); ?>" style="width: 100%; margin-bottom: 8px;">
                    <span class="dashicons dashicons-superhero"></span>
                    <?php _e('🚀 PROCESAMIENTO COMPLETO AI', 'ai-dropshipping'); ?>
                </button>
                
                <button type="button" class="button button-secondary ai-generate-description" data-product-id="<?php echo esc_attr($post->ID); ?>" style="width: 100%; margin-bottom: 8px;">
                    <span class="dashicons dashicons-edit"></span>
                    <?php _e('📝 Descripción SEO', 'ai-dropshipping'); ?>
                </button>
                
                <button type="button" class="button button-secondary ai-generate-images-btn" data-product-id="<?php echo esc_attr($post->ID); ?>" style="width: 100%; margin-bottom: 8px;">
                    <span class="dashicons dashicons-format-image"></span>
                    <?php _e('🖼️ Generar Imágenes', 'ai-dropshipping'); ?>
                </button>
                
                <button type="button" class="button button-secondary ai-optimal-pricing" data-product-id="<?php echo esc_attr($post->ID); ?>" style="width: 100%; margin-bottom: 8px;">
                    <span class="dashicons dashicons-chart-line"></span>
                    <?php _e('💰 Precio Óptimo', 'ai-dropshipping'); ?>
                </button>
                
                <button type="button" class="button button-secondary ai-market-analysis" data-product-id="<?php echo esc_attr($post->ID); ?>" style="width: 100%; margin-bottom: 8px;">
                    <span class="dashicons dashicons-analytics"></span>
                    <?php _e('📊 Análisis de Mercado', 'ai-dropshipping'); ?>
                </button>
                
                <button type="button" class="button button-secondary ai-social-content" data-product-id="<?php echo esc_attr($post->ID); ?>" style="width: 100%; margin-bottom: 8px;">
                    <span class="dashicons dashicons-share"></span>
                    <?php _e('📱 Contenido Social', 'ai-dropshipping'); ?>
                </button>
            </div>
            
            <p style="margin-top: 12px; font-size: 11px; color: #666;">
                <?php _e('🤖 Procesamiento completo incluye: descripción SEO, imágenes AI, precio óptimo, análisis de mercado y contenido social.', 'ai-dropshipping'); ?>
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
    
    // ==========================================
    // NUEVOS AJAX HANDLERS - AI SUPER POWERS
    // ==========================================
    
    public function ajax_complete_process() {
        check_ajax_referer('ai_dropship_nonce', 'nonce');
        
        if (!current_user_can('manage_woocommerce')) {
            wp_send_json_error('Unauthorized');
        }
        
        $product_id = intval($_POST['product_id']);
        $product = wc_get_product($product_id);
        
        if (!$product) {
            wp_send_json_error('Producto no encontrado');
        }
        
        try {
            $ai_client = new AI_SuperPowered_Client();
            
            // Obtener datos del producto
            $product_name = $product->get_name();
            $categories = wp_get_post_terms($product_id, 'product_cat', array('fields' => 'names'));
            $category = !empty($categories) ? $categories[0] : 'general';
            $base_price = floatval($product->get_regular_price()) ?: null;
            
            // Procesar completo
            $result = $ai_client->process_product_complete(
                $product_name,
                $category,
                array(),
                $base_price,
                true
            );
            
            if ($result['success']) {
                // Aplicar descripción
                if (!empty($result['description'])) {
                    $ai_client->apply_description_to_product($product_id, $result['description']);
                }
                
                // Aplicar precio óptimo
                if (!empty($result['pricing'])) {
                    $ai_client->apply_optimal_price($product_id, $result['pricing']);
                }
                
                // Aplicar imágenes
                if (!empty($result['images'])) {
                    $ai_client->apply_images_to_product($product_id, $result['images']);
                }
                
                wp_send_json_success(array(
                    'message' => '✅ Producto procesado completamente con AI',
                    'details' => $result
                ));
            } else {
                wp_send_json_error($result);
            }
            
        } catch (Exception $e) {
            wp_send_json_error($e->getMessage());
        }
    }
    
    public function ajax_generate_description() {
        check_ajax_referer('ai_dropship_nonce', 'nonce');
        
        if (!current_user_can('manage_woocommerce')) {
            wp_send_json_error('Unauthorized');
        }
        
        $product_id = intval($_POST['product_id']);
        $product = wc_get_product($product_id);
        
        if (!$product) {
            wp_send_json_error('Producto no encontrado');
        }
        
        try {
            $ai_client = new AI_SuperPowered_Client();
            
            $product_name = $product->get_name();
            $categories = wp_get_post_terms($product_id, 'product_cat', array('fields' => 'names'));
            $category = !empty($categories) ? $categories[0] : 'general';
            
            $result = $ai_client->generate_description($product_name, $category);
            
            if ($result['success']) {
                // Aplicar al producto
                $ai_client->apply_description_to_product($product_id, $result);
                
                wp_send_json_success(array(
                    'message' => '✅ Descripción SEO generada y aplicada',
                    'data' => $result
                ));
            } else {
                wp_send_json_error($result);
            }
            
        } catch (Exception $e) {
            wp_send_json_error($e->getMessage());
        }
    }
    
    public function ajax_generate_images() {
        check_ajax_referer('ai_dropship_nonce', 'nonce');
        
        if (!current_user_can('manage_woocommerce')) {
            wp_send_json_error('Unauthorized');
        }
        
        $product_id = intval($_POST['product_id']);
        $product = wc_get_product($product_id);
        
        if (!$product) {
            wp_send_json_error('Producto no encontrado');
        }
        
        try {
            $ai_client = new AI_SuperPowered_Client();
            
            $product_name = $product->get_name();
            $categories = wp_get_post_terms($product_id, 'product_cat', array('fields' => 'names'));
            $category = !empty($categories) ? $categories[0] : 'general';
            
            $result = $ai_client->generate_images($product_name, $category, 'professional product photo', 2);
            
            if ($result['success']) {
                // Descargar y aplicar imágenes
                $count = $ai_client->apply_images_to_product($product_id, $result);
                
                wp_send_json_success(array(
                    'message' => "✅ $count imágenes generadas y aplicadas",
                    'data' => $result
                ));
            } else {
                wp_send_json_error($result);
            }
            
        } catch (Exception $e) {
            wp_send_json_error($e->getMessage());
        }
    }
    
    public function ajax_market_analysis() {
        check_ajax_referer('ai_dropship_nonce', 'nonce');
        
        if (!current_user_can('manage_woocommerce')) {
            wp_send_json_error('Unauthorized');
        }
        
        $product_id = intval($_POST['product_id']);
        $product = wc_get_product($product_id);
        
        if (!$product) {
            wp_send_json_error('Producto no encontrado');
        }
        
        try {
            $ai_client = new AI_SuperPowered_Client();
            
            $product_name = $product->get_name();
            $categories = wp_get_post_terms($product_id, 'product_cat', array('fields' => 'names'));
            $category = !empty($categories) ? $categories[0] : 'general';
            
            $result = $ai_client->analyze_market($product_name, $category);
            
            wp_send_json_success(array(
                'message' => '✅ Análisis de mercado completado',
                'data' => $result
            ));
            
        } catch (Exception $e) {
            wp_send_json_error($e->getMessage());
        }
    }
    
    public function ajax_optimal_pricing() {
        check_ajax_referer('ai_dropship_nonce', 'nonce');
        
        if (!current_user_can('manage_woocommerce')) {
            wp_send_json_error('Unauthorized');
        }
        
        $product_id = intval($_POST['product_id']);
        $product = wc_get_product($product_id);
        
        if (!$product) {
            wp_send_json_error('Producto no encontrado');
        }
        
        try {
            $ai_client = new AI_SuperPowered_Client();
            
            $product_name = $product->get_name();
            $categories = wp_get_post_terms($product_id, 'product_cat', array('fields' => 'names'));
            $category = !empty($categories) ? $categories[0] : 'general';
            $base_price = floatval($product->get_regular_price());
            
            if ($base_price <= 0) {
                $base_price = 40.0; // Precio base por defecto
            }
            
            $result = $ai_client->calculate_optimal_price($product_name, $category, $base_price);
            
            if ($result['success']) {
                // Aplicar precio
                $ai_client->apply_optimal_price($product_id, $result);
                
                wp_send_json_success(array(
                    'message' => '✅ Precio óptimo calculado y aplicado: €' . $result['optimal_price'],
                    'data' => $result
                ));
            } else {
                wp_send_json_error($result);
            }
            
        } catch (Exception $e) {
            wp_send_json_error($e->getMessage());
        }
    }
    
    public function ajax_social_content() {
        check_ajax_referer('ai_dropship_nonce', 'nonce');
        
        if (!current_user_can('manage_woocommerce')) {
            wp_send_json_error('Unauthorized');
        }
        
        $product_id = intval($_POST['product_id']);
        $product = wc_get_product($product_id);
        
        if (!$product) {
            wp_send_json_error('Producto no encontrado');
        }
        
        try {
            $ai_client = new AI_SuperPowered_Client();
            
            $product_name = $product->get_name();
            $description = $product->get_short_description() ?: $product->get_description();
            
            $result = $ai_client->generate_social_content(
                $product_name,
                strip_tags($description),
                array('instagram', 'facebook', 'twitter')
            );
            
            wp_send_json_success(array(
                'message' => '✅ Contenido de redes sociales generado',
                'data' => $result
            ));
            
        } catch (Exception $e) {
            wp_send_json_error($e->getMessage());
        }
    }
    
    public function ajax_email_campaign() {
        check_ajax_referer('ai_dropship_nonce', 'nonce');
        
        if (!current_user_can('manage_woocommerce')) {
            wp_send_json_error('Unauthorized');
        }
        
        $product_id = intval($_POST['product_id']);
        $product = wc_get_product($product_id);
        
        if (!$product) {
            wp_send_json_error('Producto no encontrado');
        }
        
        try {
            $ai_client = new AI_SuperPowered_Client();
            
            $product_name = $product->get_name();
            $description = $product->get_short_description() ?: $product->get_description();
            
            $result = $ai_client->generate_email_campaign(
                $product_name,
                strip_tags($description),
                'general'
            );
            
            wp_send_json_success(array(
                'message' => '✅ Campaña de email generada',
                'data' => $result
            ));
            
        } catch (Exception $e) {
            wp_send_json_error($e->getMessage());
        }
    }

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
