<?php
/**
 * API Client for communicating with the FastAPI backend
 */

class AI_Dropship_API_Client {
    
    private $api_url;
    private $timeout = 30;
    
    public function __construct() {
        $this->api_url = get_option('ai_dropship_api_url', AI_DROPSHIP_API_URL);
    }
    
    /**
     * Make API request
     */
    private function request($method, $endpoint, $data = null) {
        $url = trailingslashit($this->api_url) . ltrim($endpoint, '/');
        
        $args = array(
            'method' => $method,
            'timeout' => $this->timeout,
            'headers' => array(
                'Content-Type' => 'application/json',
            ),
        );
        
        if ($data !== null) {
            $args['body'] = json_encode($data);
        }
        
        $response = wp_remote_request($url, $args);
        
        if (is_wp_error($response)) {
            throw new Exception($response->get_error_message());
        }
        
        $body = wp_remote_retrieve_body($response);
        $code = wp_remote_retrieve_response_code($response);
        
        if ($code < 200 || $code >= 300) {
            throw new Exception("API Error: HTTP $code - $body");
        }
        
        return json_decode($body, true);
    }
    
    /**
     * Calculate price for a product
     */
    public function calculate_price($supplier_price, $currency = 'EUR') {
        return $this->request('POST', 'dropshipping/calculate-price', array(
            'supplier_price' => $supplier_price,
            'currency' => $currency
        ));
    }
    
    /**
     * Process a single product
     */
    public function process_product($product_id, $supplier_price = null, $generate_content = false) {
        $data = array(
            'generate_content' => $generate_content
        );
        
        if ($supplier_price !== null) {
            $data['supplier_price'] = $supplier_price;
        }
        
        return $this->request('POST', "dropshipping/process-product/$product_id", $data);
    }
    
    /**
     * Generate AI content for product
     */
    public function generate_content($product_id) {
        return $this->request('POST', "dropshipping/generate-content/$product_id");
    }
    
    /**
     * Process all products
     */
    public function process_all_products($generate_content = false) {
        return $this->request('POST', "dropshipping/process-all?generate_content=" . ($generate_content ? 'true' : 'false'));
    }
    
    /**
     * Get dropshipping stats
     */
    public function get_stats() {
        try {
            return $this->request('GET', 'dropshipping/stats');
        } catch (Exception $e) {
            return array(
                'error' => $e->getMessage()
            );
        }
    }
    
    /**
     * Get WooCommerce products from API
     */
    public function get_woocommerce_products() {
        return $this->request('GET', 'woocommerce/products');
    }
}
