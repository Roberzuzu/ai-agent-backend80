<?php
/**
 * Plugin Name: AI WooCommerce Agent
 * Plugin URI: https://tu-dominio.com/ai-woocommerce-agent
 * Description: Agente AI potente para WooCommerce con Perplexity, OpenAI, gestión automática de productos, bot de Telegram y 22+ herramientas integradas.
 * Version: 1.0.0
 * Author: Tu Nombre
 * Author URI: https://tu-dominio.com
 * License: GPL v2 or later
 * License URI: https://www.gnu.org/licenses/gpl-2.0.html
 * Text Domain: ai-woocommerce-agent
 * Domain Path: /languages
 * Requires at least: 6.0
 * Tested up to: 6.4
 * Requires PHP: 7.4
 * WC requires at least: 7.0
 * WC tested up to: 8.5
 */

// Exit if accessed directly
if (!defined('ABSPATH')) {
    exit;
}

// Define plugin constants
define('AIWCA_VERSION', '1.0.0');
define('AIWCA_PLUGIN_DIR', plugin_dir_path(__FILE__));
define('AIWCA_PLUGIN_URL', plugin_dir_url(__FILE__));
define('AIWCA_PLUGIN_FILE', __FILE__);

/**
 * Main Plugin Class
 */
class AI_WooCommerce_Agent {
    
    /**
     * Single instance
     */
    private static $instance = null;
    
    /**
     * Get instance
     */
    public static function get_instance() {
        if (null === self::$instance) {
            self::$instance = new self();
        }
        return self::$instance;
    }
    
    /**
     * Constructor
     */
    private function __construct() {
        $this->init_hooks();
        $this->load_dependencies();
    }
    
    /**
     * Initialize hooks
     */
    private function init_hooks() {
        // Activation and deactivation
        register_activation_hook(__FILE__, array($this, 'activate'));
        register_deactivation_hook(__FILE__, array($this, 'deactivate'));
        
        // Admin hooks
        add_action('admin_menu', array($this, 'add_admin_menu'));
        add_action('admin_enqueue_scripts', array($this, 'enqueue_admin_assets'));
        add_action('admin_init', array($this, 'register_settings'));
        
        // AJAX hooks
        add_action('wp_ajax_aiwca_process_product', array($this, 'ajax_process_product'));
        add_action('wp_ajax_aiwca_execute_command', array($this, 'ajax_execute_command'));
        add_action('wp_ajax_aiwca_get_stats', array($this, 'ajax_get_stats'));
        add_action('wp_ajax_aiwca_test_connection', array($this, 'ajax_test_connection'));
        
        // WooCommerce hooks
        add_action('woocommerce_product_options_general_product_data', array($this, 'add_product_ai_button'));
        add_action('woocommerce_process_product_meta', array($this, 'save_product_ai_data'));
        
        // Telegram webhook
        add_action('rest_api_init', array($this, 'register_webhook_endpoint'));
        
        // Cron jobs
        add_action('aiwca_process_telegram_updates', array($this, 'process_telegram_updates'));
    }
    
    /**
     * Load dependencies
     */
    private function load_dependencies() {
        $files = array(
            'includes/class-ai-client.php',
            'includes/class-telegram-bot.php',
            'includes/class-product-processor.php',
            'includes/class-agent-executor.php',
            'includes/functions.php'
        );
        
        foreach ($files as $file) {
            $path = AIWCA_PLUGIN_DIR . $file;
            if (file_exists($path)) {
                require_once $path;
            }
        }
    }
    
    /**
     * Plugin activation
     */
    public function activate() {
        // Create database tables if needed
        $this->create_tables();
        
        // Schedule cron jobs
        if (!wp_next_scheduled('aiwca_process_telegram_updates')) {
            wp_schedule_event(time(), 'every_minute', 'aiwca_process_telegram_updates');
        }
        
        // Set default options
        $default_options = array(
            'backend_url' => '',
            'openai_api_key' => '',
            'perplexity_api_key' => '',
            'telegram_bot_token' => '',
            'telegram_chat_id' => '',
            'stripe_api_key' => '',
            'fal_api_key' => '',
            'auto_optimize_products' => 'no',
            'enable_telegram_bot' => 'yes',
            'ai_provider' => 'perplexity',
        );
        
        foreach ($default_options as $key => $value) {
            if (get_option('aiwca_' . $key) === false) {
                add_option('aiwca_' . $key, $value);
            }
        }
        
        flush_rewrite_rules();
    }
    
    /**
     * Plugin deactivation
     */
    public function deactivate() {
        // Clear scheduled hooks
        $timestamp = wp_next_scheduled('aiwca_process_telegram_updates');
        wp_unschedule_event($timestamp, 'aiwca_process_telegram_updates');
        
        flush_rewrite_rules();
    }
    
    /**
     * Create database tables
     */
    private function create_tables() {
        global $wpdb;
        
        $charset_collate = $wpdb->get_charset_collate();
        
        // AI Agent Memory table
        $table_memory = $wpdb->prefix . 'aiwca_memory';
        $sql_memory = "CREATE TABLE IF NOT EXISTS $table_memory (
            id bigint(20) NOT NULL AUTO_INCREMENT,
            user_id varchar(255) NOT NULL,
            command text NOT NULL,
            response longtext NOT NULL,
            plan text,
            embedding longtext,
            created_at datetime DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (id),
            KEY user_id (user_id),
            KEY created_at (created_at)
        ) $charset_collate;";
        
        // Telegram Messages table
        $table_telegram = $wpdb->prefix . 'aiwca_telegram_messages';
        $sql_telegram = "CREATE TABLE IF NOT EXISTS $table_telegram (
            id bigint(20) NOT NULL AUTO_INCREMENT,
            update_id bigint(20) NOT NULL,
            chat_id bigint(20) NOT NULL,
            message_text text,
            processed tinyint(1) DEFAULT 0,
            response text,
            created_at datetime DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (id),
            UNIQUE KEY update_id (update_id),
            KEY processed (processed),
            KEY created_at (created_at)
        ) $charset_collate;";
        
        require_once(ABSPATH . 'wp-admin/includes/upgrade.php');
        dbDelta($sql_memory);
        dbDelta($sql_telegram);
    }
    
    /**
     * Add admin menu
     */
    public function add_admin_menu() {
        add_menu_page(
            __('AI WooCommerce Agent', 'ai-woocommerce-agent'),
            __('AI Agent', 'ai-woocommerce-agent'),
            'manage_woocommerce',
            'ai-woocommerce-agent',
            array($this, 'render_dashboard_page'),
            'dashicons-superhero',
            56
        );
        
        add_submenu_page(
            'ai-woocommerce-agent',
            __('Dashboard', 'ai-woocommerce-agent'),
            __('Dashboard', 'ai-woocommerce-agent'),
            'manage_woocommerce',
            'ai-woocommerce-agent',
            array($this, 'render_dashboard_page')
        );
        
        add_submenu_page(
            'ai-woocommerce-agent',
            __('Command Center', 'ai-woocommerce-agent'),
            __('Command Center', 'ai-woocommerce-agent'),
            'manage_woocommerce',
            'ai-woocommerce-agent-commands',
            array($this, 'render_commands_page')
        );
        
        add_submenu_page(
            'ai-woocommerce-agent',
            __('Telegram Bot', 'ai-woocommerce-agent'),
            __('Telegram Bot', 'ai-woocommerce-agent'),
            'manage_woocommerce',
            'ai-woocommerce-agent-telegram',
            array($this, 'render_telegram_page')
        );
        
        add_submenu_page(
            'ai-woocommerce-agent',
            __('Settings', 'ai-woocommerce-agent'),
            __('Settings', 'ai-woocommerce-agent'),
            'manage_options',
            'ai-woocommerce-agent-settings',
            array($this, 'render_settings_page')
        );
    }
    
    /**
     * Enqueue admin assets
     */
    public function enqueue_admin_assets($hook) {
        if (strpos($hook, 'ai-woocommerce-agent') === false) {
            return;
        }
        
        wp_enqueue_style(
            'aiwca-admin',
            AIWCA_PLUGIN_URL . 'assets/css/admin.css',
            array(),
            AIWCA_VERSION
        );
        
        wp_enqueue_script(
            'aiwca-admin',
            AIWCA_PLUGIN_URL . 'assets/js/admin.js',
            array('jquery'),
            AIWCA_VERSION,
            true
        );
        
        wp_localize_script('aiwca-admin', 'aiwcaData', array(
            'ajaxUrl' => admin_url('admin-ajax.php'),
            'nonce' => wp_create_nonce('aiwca_nonce'),
            'strings' => array(
                'processing' => __('Processing...', 'ai-woocommerce-agent'),
                'success' => __('Success!', 'ai-woocommerce-agent'),
                'error' => __('Error occurred', 'ai-woocommerce-agent'),
            ),
        ));
    }
    
    /**
     * Register settings
     */
    public function register_settings() {
        register_setting('aiwca_settings', 'aiwca_backend_url');
        register_setting('aiwca_settings', 'aiwca_openai_api_key');
        register_setting('aiwca_settings', 'aiwca_perplexity_api_key');
        register_setting('aiwca_settings', 'aiwca_telegram_bot_token');
        register_setting('aiwca_settings', 'aiwca_telegram_chat_id');
        register_setting('aiwca_settings', 'aiwca_stripe_api_key');
        register_setting('aiwca_settings', 'aiwca_fal_api_key');
        register_setting('aiwca_settings', 'aiwca_auto_optimize_products');
        register_setting('aiwca_settings', 'aiwca_enable_telegram_bot');
        register_setting('aiwca_settings', 'aiwca_ai_provider');
    }
    
    /**
     * Render dashboard page
     */
    public function render_dashboard_page() {
        $file = AIWCA_PLUGIN_DIR . 'templates/admin/dashboard.php';
        if (file_exists($file)) {
            include $file;
        } else {
            echo '<div class="wrap"><h1>Dashboard</h1><p>Template file not found.</p></div>';
        }
    }
    
    /**
     * Render commands page
     */
    public function render_commands_page() {
        $file = AIWCA_PLUGIN_DIR . 'templates/admin/commands.php';
        if (file_exists($file)) {
            include $file;
        } else {
            echo '<div class="wrap"><h1>Commands</h1><p>Template file not found.</p></div>';
        }
    }
    
    /**
     * Render telegram page
     */
    public function render_telegram_page() {
        $file = AIWCA_PLUGIN_DIR . 'templates/admin/telegram.php';
        if (file_exists($file)) {
            include $file;
        } else {
            echo '<div class="wrap"><h1>Telegram Bot</h1><p>Template file not found.</p></div>';
        }
    }
    
    /**
     * Render settings page
     */
    public function render_settings_page() {
        $file = AIWCA_PLUGIN_DIR . 'templates/admin/settings.php';
        if (file_exists($file)) {
            include $file;
        } else {
            echo '<div class="wrap"><h1>Settings</h1><p>Template file not found.</p></div>';
        }
    }
    
    /**
     * Add AI button to product page
     */
    public function add_product_ai_button() {
        global $post;
        ?>
        <div class="options_group">
            <p class="form-field">
                <label><?php _e('AI Optimization', 'ai-woocommerce-agent'); ?></label>
                <button type="button" class="button button-primary aiwca-process-product" data-product-id="<?php echo $post->ID; ?>">
                    <span class="dashicons dashicons-superhero"></span>
                    <?php _e('Process with AI Agent', 'ai-woocommerce-agent'); ?>
                </button>
                <span class="description"><?php _e('Generate optimized description, pricing, and images using AI', 'ai-woocommerce-agent'); ?></span>
            </p>
        </div>
        <?php
    }
    
    /**
     * Save product AI data
     */
    public function save_product_ai_data($post_id) {
        // Auto-process if enabled
        if (get_option('aiwca_auto_optimize_products') === 'yes') {
            $this->process_product_with_ai($post_id);
        }
    }
    
    /**
     * AJAX: Process product
     */
    public function ajax_process_product() {
        check_ajax_referer('aiwca_nonce', 'nonce');
        
        if (!current_user_can('manage_woocommerce')) {
            wp_send_json_error('Insufficient permissions');
        }
        
        $product_id = isset($_POST['product_id']) ? intval($_POST['product_id']) : 0;
        
        if (!$product_id) {
            wp_send_json_error('Invalid product ID');
        }
        
        $result = $this->process_product_with_ai($product_id);
        
        if ($result['success']) {
            wp_send_json_success($result);
        } else {
            wp_send_json_error($result['message']);
        }
    }
    
    /**
     * AJAX: Execute command
     */
    public function ajax_execute_command() {
        check_ajax_referer('aiwca_nonce', 'nonce');
        
        if (!current_user_can('manage_woocommerce')) {
            wp_send_json_error('Insufficient permissions');
        }
        
        $command = isset($_POST['command']) ? sanitize_textarea_field($_POST['command']) : '';
        
        if (empty($command)) {
            wp_send_json_error('Empty command');
        }
        
        $executor = new AIWCA_Agent_Executor();
        $result = $executor->execute($command, get_current_user_id());
        
        wp_send_json($result);
    }
    
    /**
     * AJAX: Get stats
     */
    public function ajax_get_stats() {
        check_ajax_referer('aiwca_nonce', 'nonce');
        
        global $wpdb;
        
        $stats = array(
            'total_products' => wp_count_posts('product')->publish,
            'ai_processed_today' => $wpdb->get_var(
                "SELECT COUNT(*) FROM {$wpdb->prefix}aiwca_memory 
                WHERE DATE(created_at) = CURDATE()"
            ),
            'telegram_messages' => $wpdb->get_var(
                "SELECT COUNT(*) FROM {$wpdb->prefix}aiwca_telegram_messages 
                WHERE processed = 1"
            ),
            'backend_status' => $this->check_backend_status(),
        );
        
        wp_send_json_success($stats);
    }
    
    /**
     * AJAX: Test connection
     */
    public function ajax_test_connection() {
        check_ajax_referer('aiwca_nonce', 'nonce');
        
        $backend_url = get_option('aiwca_backend_url');
        
        if (empty($backend_url)) {
            wp_send_json_error('Backend URL not configured');
        }
        
        $response = wp_remote_get($backend_url . '/api/health', array('timeout' => 10));
        
        if (is_wp_error($response)) {
            wp_send_json_error($response->get_error_message());
        }
        
        $status_code = wp_remote_retrieve_response_code($response);
        
        if ($status_code === 200) {
            wp_send_json_success('Backend is online');
        } else {
            wp_send_json_error('Backend returned status: ' . $status_code);
        }
    }
    
    /**
     * Register webhook endpoint
     */
    public function register_webhook_endpoint() {
        register_rest_route('aiwca/v1', '/telegram/webhook', array(
            'methods' => 'POST',
            'callback' => array($this, 'handle_telegram_webhook'),
            'permission_callback' => '__return_true',
        ));
    }
    
    /**
     * Handle Telegram webhook
     */
    public function handle_telegram_webhook($request) {
        $telegram = new AIWCA_Telegram_Bot();
        return $telegram->handle_webhook($request);
    }
    
    /**
     * Process Telegram updates (cron)
     */
    public function process_telegram_updates() {
        if (get_option('aiwca_enable_telegram_bot') !== 'yes') {
            return;
        }
        
        $telegram = new AIWCA_Telegram_Bot();
        $telegram->process_updates();
    }
    
    /**
     * Process product with AI
     */
    private function process_product_with_ai($product_id) {
        $processor = new AIWCA_Product_Processor();
        return $processor->process($product_id);
    }
    
    /**
     * Check backend status
     */
    private function check_backend_status() {
        $backend_url = get_option('aiwca_backend_url');
        
        if (empty($backend_url)) {
            return 'not_configured';
        }
        
        $response = wp_remote_get($backend_url . '/api/health', array('timeout' => 5));
        
        if (is_wp_error($response)) {
            return 'offline';
        }
        
        $status_code = wp_remote_retrieve_response_code($response);
        
        return $status_code === 200 ? 'online' : 'error';
    }
}

// Initialize plugin
function aiwca_init() {
    return AI_WooCommerce_Agent::get_instance();
}

// Start the plugin
add_action('plugins_loaded', 'aiwca_init');

// Check for WooCommerce
function aiwca_check_woocommerce() {
    if (!class_exists('WooCommerce')) {
        add_action('admin_notices', function() {
            ?>
            <div class="notice notice-error">
                <p><?php _e('AI WooCommerce Agent requires WooCommerce to be installed and active.', 'ai-woocommerce-agent'); ?></p>
            </div>
            <?php
        });
        
        deactivate_plugins(plugin_basename(__FILE__));
    }
}
add_action('admin_init', 'aiwca_check_woocommerce');
