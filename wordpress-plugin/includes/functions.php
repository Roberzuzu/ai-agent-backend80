<?php
/**
 * Helper Functions
 */

if (!defined('ABSPATH')) {
    exit;
}

/**
 * Get plugin option with default
 */
function aiwca_get_option($key, $default = '') {
    return get_option('aiwca_' . $key, $default);
}

/**
 * Update plugin option
 */
function aiwca_update_option($key, $value) {
    return update_option('aiwca_' . $key, $value);
}

/**
 * Log message
 */
function aiwca_log($message, $level = 'info') {
    if (defined('WP_DEBUG') && WP_DEBUG) {
        error_log("[AI WooCommerce Agent - {$level}] " . $message);
    }
}

/**
 * Format price
 */
function aiwca_format_price($price) {
    return wc_price($price);
}

/**
 * Get backend status
 */
function aiwca_get_backend_status() {
    $backend_url = aiwca_get_option('backend_url');
    
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

/**
 * Send Telegram notification
 */
function aiwca_send_telegram_notification($message) {
    $telegram = new AIWCA_Telegram_Bot();
    $chat_id = aiwca_get_option('telegram_chat_id');
    
    if ($chat_id) {
        return $telegram->send_message($chat_id, $message);
    }
    
    return false;
}
