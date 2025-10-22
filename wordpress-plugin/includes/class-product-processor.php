<?php
/**
 * Product Processor - AI-powered product optimization
 */

if (!defined('ABSPATH')) {
    exit;
}

class AIWCA_Product_Processor {
    
    private $ai_client;
    
    public function __construct() {
        $this->ai_client = new AIWCA_AI_Client();
    }
    
    /**
     * Process product with AI
     */
    public function process($product_id) {
        $product = wc_get_product($product_id);
        
        if (!$product) {
            return array(
                'success' => false,
                'message' => 'Product not found'
            );
        }
        
        $product_name = $product->get_name();
        $category = $this->get_product_category($product);
        
        // Generate optimized description
        $description_result = $this->generate_description($product_name, $category);
        
        // Calculate optimal price
        $price_result = $this->calculate_optimal_price($product_name, $category, $product->get_regular_price());
        
        // Generate images
        $images_result = $this->generate_product_images($product_name, $category);
        
        // Update product
        if ($description_result['success']) {
            $product->set_description($description_result['description']);
            $product->set_short_description($description_result['short_description']);
        }
        
        if ($price_result['success'] && $price_result['optimal_price'] > 0) {
            $product->set_regular_price($price_result['optimal_price']);
        }
        
        $product->save();
        
        return array(
            'success' => true,
            'message' => 'Product processed successfully',
            'description' => $description_result,
            'pricing' => $price_result,
            'images' => $images_result
        );
    }
    
    /**
     * Generate product description
     */
    private function generate_description($product_name, $category) {
        $prompt = "Genera una descripción de producto optimizada para SEO para WooCommerce:\n\n";
        $prompt .= "Producto: {$product_name}\n";
        $prompt .= "Categoría: {$category}\n\n";
        $prompt .= "Proporciona:\n";
        $prompt .= "1. Descripción completa (200-300 palabras) en HTML\n";
        $prompt .= "2. Descripción corta (50-100 palabras)\n";
        $prompt .= "3. 5 keywords SEO\n";
        $prompt .= "4. Meta descripción (160 caracteres)\n\n";
        $prompt .= "Formato JSON: {\"description\": \"\", \"short_description\": \"\", \"keywords\": [], \"meta_description\": \"\"}";
        
        $result = $this->ai_client->complete($prompt, 1500);
        
        if (!$result['success']) {
            return array(
                'success' => false,
                'error' => $result['error']
            );
        }
        
        // Parse JSON from response
        preg_match('/\{[^}]+\}/s', $result['content'], $matches);
        if (isset($matches[0])) {
            $data = json_decode($matches[0], true);
            if ($data) {
                return array_merge(array('success' => true), $data);
            }
        }
        
        // Fallback: use raw content
        return array(
            'success' => true,
            'description' => $result['content'],
            'short_description' => substr(strip_tags($result['content']), 0, 100),
            'keywords' => array(),
            'meta_description' => ''
        );
    }
    
    /**
     * Calculate optimal price
     */
    private function calculate_optimal_price($product_name, $category, $current_price) {
        $prompt = "Analiza el precio óptimo para este producto en España:\n\n";
        $prompt .= "Producto: {$product_name}\n";
        $prompt .= "Categoría: {$category}\n";
        $prompt .= "Precio actual: €" . ($current_price ?: '50') . "\n\n";
        $prompt .= "Proporciona:\n";
        $prompt .= "1. Precio óptimo recomendado\n";
        $prompt .= "2. Rango de precios del mercado (mínimo-máximo)\n";
        $prompt .= "3. Justificación\n\n";
        $prompt .= "Formato JSON: {\"optimal_price\": 0, \"min_market_price\": 0, \"max_market_price\": 0, \"justification\": \"\"}";
        
        $result = $this->ai_client->complete($prompt, 500);
        
        if (!$result['success']) {
            return array(
                'success' => false,
                'error' => $result['error']
            );
        }
        
        preg_match('/\{[^}]+\}/s', $result['content'], $matches);
        if (isset($matches[0])) {
            $data = json_decode($matches[0], true);
            if ($data && isset($data['optimal_price'])) {
                return array_merge(array('success' => true), $data);
            }
        }
        
        return array(
            'success' => false,
            'error' => 'Could not parse price data'
        );
    }
    
    /**
     * Generate product images
     */
    private function generate_product_images($product_name, $category) {
        $prompt = "Professional product photo: {$product_name}, {$category}, high quality, white background, e-commerce";
        
        return $this->ai_client->generate_images($prompt, 2);
    }
    
    /**
     * Get product category
     */
    private function get_product_category($product) {
        $terms = get_the_terms($product->get_id(), 'product_cat');
        if ($terms && !is_wp_error($terms)) {
            return $terms[0]->name;
        }
        return 'General';
    }
}
