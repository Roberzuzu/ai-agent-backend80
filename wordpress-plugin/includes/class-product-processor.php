<?php
/**
 * Product Processor Class
 * Handles product processing logic
 */

class AI_Dropship_Product_Processor {
    
    private $api_client;
    
    public function __construct() {
        $this->api_client = new AI_Dropship_API_Client();
    }
    
    /**
     * Process a single product
     */
    public function process_product($product_id) {
        $product = wc_get_product($product_id);
        
        if (!$product) {
            throw new Exception(__('Producto no encontrado', 'ai-dropshipping'));
        }
        
        // Check if already has price
        $current_price = $product->get_regular_price();
        
        if (empty($current_price) || $current_price == 0) {
            // Estimate supplier price (default €40)
            $supplier_price = $this->estimate_supplier_price($product);
            
            // Calculate optimal price via API
            $pricing = $this->api_client->calculate_price($supplier_price);
            
            // Update product price
            $selling_price = $pricing['selling_price_rounded'];
            $product->set_regular_price($selling_price);
            $product->set_price($selling_price);
            $product->save();
            
            return array(
                'success' => true,
                'message' => sprintf(
                    __('Precio actualizado: €%s (margen: %s%%)', 'ai-dropshipping'),
                    number_format($selling_price, 2),
                    round($pricing['margin_percentage'] * 100)
                ),
                'price' => $selling_price,
                'margin' => $pricing['margin_percentage'],
                'profit' => $pricing['profit']
            );
        } else {
            return array(
                'success' => true,
                'message' => __('El producto ya tiene precio configurado', 'ai-dropshipping'),
                'price' => $current_price
            );
        }
    }
    
    /**
     * Generate AI content for product
     */
    public function generate_content($product_id) {
        try {
            $result = $this->api_client->generate_content($product_id);
            
            return array(
                'success' => true,
                'message' => __('Contenido IA generado exitosamente', 'ai-dropshipping'),
                'data' => $result
            );
        } catch (Exception $e) {
            return array(
                'success' => false,
                'message' => $e->getMessage()
            );
        }
    }
    
    /**
     * Process all products without price
     */
    public function process_all_products() {
        $args = array(
            'post_type' => 'product',
            'posts_per_page' => -1,
            'post_status' => 'publish',
            'meta_query' => array(
                'relation' => 'OR',
                array(
                    'key' => '_regular_price',
                    'value' => '',
                    'compare' => '='
                ),
                array(
                    'key' => '_regular_price',
                    'value' => '0',
                    'compare' => '='
                ),
                array(
                    'key' => '_regular_price',
                    'compare' => 'NOT EXISTS'
                )
            )
        );
        
        $products = get_posts($args);
        $processed = 0;
        $errors = 0;
        
        foreach ($products as $post) {
            try {
                $this->process_product($post->ID);
                $processed++;
            } catch (Exception $e) {
                $errors++;
                error_log('AI Dropship: Error processing product ' . $post->ID . ': ' . $e->getMessage());
            }
        }
        
        return array(
            'success' => true,
            'total' => count($products),
            'processed' => $processed,
            'errors' => $errors,
            'message' => sprintf(
                __('Procesados %d de %d productos (%d errores)', 'ai-dropshipping'),
                $processed,
                count($products),
                $errors
            )
        );
    }
    
    /**
     * Estimate supplier price based on product info
     */
    private function estimate_supplier_price($product) {
        $name = strtolower($product->get_name());
        $slug = strtolower($product->get_slug());
        $text = $name . ' ' . $slug;
        
        $price_keywords = array(
            'profesional' => 80.0,
            'combo' => 90.0,
            'kit' => 60.0,
            'set' => 50.0,
            'sierra' => 75.0,
            'taladro' => 65.0,
            'bateria' => 55.0,
            'amoladora' => 50.0,
            'multiherramienta' => 45.0,
            'electrica' => 45.0,
            'atornillador' => 40.0,
            'herramienta' => 35.0,
            'mini' => 30.0,
        );
        
        foreach ($price_keywords as $keyword => $price) {
            if (strpos($text, $keyword) !== false) {
                return $price;
            }
        }
        
        return 40.0; // Default price
    }
}
