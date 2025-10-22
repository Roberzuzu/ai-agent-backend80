<?php
/**
 * Telegram Bot Handler
 */

if (!defined('ABSPATH')) {
    exit;
}

class AIWCA_Telegram_Bot {
    
    private $token;
    private $chat_id;
    
    public function __construct() {
        $this->token = get_option('aiwca_telegram_bot_token');
        $this->chat_id = get_option('aiwca_telegram_chat_id');
    }
    
    /**
     * Handle webhook
     */
    public function handle_webhook($request) {
        $data = $request->get_json_params();
        
        if (!isset($data['update_id']) || !isset($data['message'])) {
            return new WP_REST_Response(array('status' => 'error'), 400);
        }
        
        $this->process_message($data);
        
        return new WP_REST_Response(array('status' => 'ok'), 200);
    }
    
    /**
     * Process updates via polling
     */
    public function process_updates() {
        if (empty($this->token)) {
            return;
        }
        
        $url = "https://api.telegram.org/bot{$this->token}/getUpdates";
        
        $response = wp_remote_get($url, array('timeout' => 30));
        
        if (is_wp_error($response)) {
            error_log('Telegram polling error: ' . $response->get_error_message());
            return;
        }
        
        $body = json_decode(wp_remote_retrieve_body($response), true);
        
        if (!isset($body['result'])) {
            return;
        }
        
        foreach ($body['result'] as $update) {
            $this->process_message($update);
        }
    }
    
    /**
     * Process single message
     */
    private function process_message($data) {
        global $wpdb;
        
        $update_id = $data['update_id'];
        $message = $data['message'];
        $chat_id = $message['chat']['id'];
        $text = isset($message['text']) ? $message['text'] : '';
        
        // Check if already processed
        $exists = $wpdb->get_var($wpdb->prepare(
            "SELECT id FROM {$wpdb->prefix}aiwca_telegram_messages WHERE update_id = %d",
            $update_id
        ));
        
        if ($exists) {
            return;
        }
        
        // Save message
        $wpdb->insert(
            $wpdb->prefix . 'aiwca_telegram_messages',
            array(
                'update_id' => $update_id,
                'chat_id' => $chat_id,
                'message_text' => $text,
                'processed' => 0,
            ),
            array('%d', '%d', '%s', '%d')
        );
        
        // Process command
        $this->handle_command($chat_id, $text);
        
        // Mark as processed
        $wpdb->update(
            $wpdb->prefix . 'aiwca_telegram_messages',
            array('processed' => 1),
            array('update_id' => $update_id),
            array('%d'),
            array('%d')
        );
    }
    
    /**
     * Handle command
     */
    private function handle_command($chat_id, $text) {
        if (strpos($text, '/procesar') === 0) {
            // Process product command
            preg_match('/\/procesar\s+(\d+)/', $text, $matches);
            if (isset($matches[1])) {
                $product_id = intval($matches[1]);
                $this->process_product_command($chat_id, $product_id);
            }
        } elseif ($text === '/ayuda' || $text === '/start') {
            $this->send_help($chat_id);
        } else {
            // Natural language command
            $this->process_natural_command($chat_id, $text);
        }
    }
    
    /**
     * Process product command
     */
    private function process_product_command($chat_id, $product_id) {
        $processor = new AIWCA_Product_Processor();
        $result = $processor->process($product_id);
        
        if ($result['success']) {
            $message = "✅ Producto {$product_id} procesado con AI\n\n";
            $message .= "✓ Descripción optimizada\n";
            $message .= "✓ Precio calculado\n";
            $message .= "✓ Imágenes generadas\n";
        } else {
            $message = "❌ Error procesando producto: " . $result['message'];
        }
        
        $this->send_message($chat_id, $message);
    }
    
    /**
     * Process natural language command
     */
    private function process_natural_command($chat_id, $text) {
        $executor = new AIWCA_Agent_Executor();
        $result = $executor->execute($text, 'telegram_' . $chat_id);
        
        if ($result['success']) {
            $message = "✅ " . $result['message'];
        } else {
            $message = "❌ Error: " . $result['error'];
        }
        
        $this->send_message($chat_id, $message);
    }
    
    /**
     * Send help message
     */
    private function send_help($chat_id) {
        $message = "🤖 *AI WooCommerce Agent - Comandos*\n\n";
        $message .= "*Comandos básicos:*\n";
        $message .= "• /procesar [ID] - Procesar producto con AI\n";
        $message .= "• /ayuda - Ver esta ayuda\n\n";
        $message .= "*Comandos en lenguaje natural:*\n";
        $message .= "• 'Muéstrame los productos sin precio'\n";
        $message .= "• 'Optimiza el producto 123'\n";
        $message .= "• 'Busca tendencias de herramientas'\n";
        $message .= "• 'Analiza la competencia'\n";
        
        $this->send_message($chat_id, $message);
    }
    
    /**
     * Send message to Telegram
     */
    public function send_message($chat_id, $text) {
        if (empty($this->token)) {
            return false;
        }
        
        $url = "https://api.telegram.org/bot{$this->token}/sendMessage";
        
        $body = array(
            'chat_id' => $chat_id,
            'text' => $text,
            'parse_mode' => 'Markdown'
        );
        
        $response = wp_remote_post($url, array(
            'body' => json_encode($body),
            'headers' => array('Content-Type' => 'application/json'),
            'timeout' => 10,
        ));
        
        return !is_wp_error($response);
    }
}
