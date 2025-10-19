<?php
/**
 * AI Client - Super Powered
 * Maneja todas las integraciones AI del backend
 */

class AI_SuperPowered_Client {
    
    private $api_url;
    private $timeout = 120; // Más tiempo para AI
    
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
     * PROCESAMIENTO COMPLETO DE PRODUCTO
     * Ejecuta todas las funcionalidades AI en un solo llamado
     */
    public function process_product_complete($product_name, $category, $features = array(), $base_price = null, $generate_images = true) {
        return $this->request('POST', 'ai/product/complete', array(
            'product_name' => $product_name,
            'category' => $category,
            'features' => $features,
            'base_price' => $base_price,
            'generate_images' => $generate_images
        ));
    }
    
    /**
     * GENERACIÓN DE DESCRIPCIÓN SEO
     * Genera título, descripción, meta tags y keywords
     */
    public function generate_description($product_name, $category, $features = array(), $language = 'es') {
        // Obtener prompt personalizado si existe
        $custom_prompt = get_option('ai_dropship_prompt_description', '');
        
        $data = array(
            'product_name' => $product_name,
            'category' => $category,
            'features' => $features,
            'language' => $language
        );
        
        // Si hay prompt personalizado, enviarlo
        if (!empty($custom_prompt)) {
            $data['custom_prompt'] = $custom_prompt;
        }
        
        return $this->request('POST', 'ai/product/description', $data);
    }
    
    /**
     * GENERACIÓN DE IMÁGENES
     * Crea imágenes profesionales con Fal AI o DALL-E
     */
    public function generate_images($product_name, $category, $style = 'professional product photo', $num_images = 1) {
        $custom_prompt = get_option('ai_dropship_prompt_images', '');
        
        $data = array(
            'product_name' => $product_name,
            'category' => $category,
            'style' => $style,
            'num_images' => $num_images
        );
        
        if (!empty($custom_prompt)) {
            $data['custom_prompt'] = $custom_prompt;
        }
        
        return $this->request('POST', 'ai/product/images', $data);
    }
    
    /**
     * ANÁLISIS DE MERCADO
     * Investiga competencia y tendencias en tiempo real
     */
    public function analyze_market($product_name, $category) {
        $custom_prompt = get_option('ai_dropship_prompt_market', '');
        
        $data = array(
            'product_name' => $product_name,
            'category' => $category
        );
        
        if (!empty($custom_prompt)) {
            $data['custom_prompt'] = $custom_prompt;
        }
        
        return $this->request('POST', 'ai/product/market-analysis', $data);
    }
    
    /**
     * CÁLCULO DE PRECIO ÓPTIMO
     * Usa Abacus AI para predicción de precio
     */
    public function calculate_optimal_price($product_name, $category, $base_price) {
        return $this->request('POST', 'ai/product/optimal-pricing', array(
            'product_name' => $product_name,
            'category' => $category,
            'base_price' => $base_price
        ));
    }
    
    /**
     * CONTENIDO PARA REDES SOCIALES
     * Genera posts optimizados para cada plataforma
     */
    public function generate_social_content($product_name, $description, $platforms = array('instagram', 'facebook', 'twitter')) {
        $custom_prompt = get_option('ai_dropship_prompt_social', '');
        
        $data = array(
            'product_name' => $product_name,
            'description' => $description,
            'platforms' => $platforms
        );
        
        if (!empty($custom_prompt)) {
            $data['custom_prompt'] = $custom_prompt;
        }
        
        return $this->request('POST', 'ai/content/social-media', $data);
    }
    
    /**
     * CAMPAÑA DE EMAIL MARKETING
     * Crea email completo con asuntos y segmentación
     */
    public function generate_email_campaign($product_name, $description, $target_audience = 'general') {
        $custom_prompt = get_option('ai_dropship_prompt_email', '');
        
        $data = array(
            'product_name' => $product_name,
            'description' => $description,
            'target_audience' => $target_audience
        );
        
        if (!empty($custom_prompt)) {
            $data['custom_prompt'] = $custom_prompt;
        }
        
        return $this->request('POST', 'ai/content/email-campaign', $data);
    }
    
    /**
     * HEALTH CHECK
     * Verifica que todas las APIs AI estén disponibles
     */
    public function check_ai_health() {
        try {
            return $this->request('GET', 'ai/health');
        } catch (Exception $e) {
            return array(
                'success' => false,
                'error' => $e->getMessage()
            );
        }
    }
    
    /**
     * HELPER: Aplicar descripción generada a producto WooCommerce
     */
    public function apply_description_to_product($product_id, $description_data) {
        $product = wc_get_product($product_id);
        
        if (!$product) {
            throw new Exception('Producto no encontrado');
        }
        
        // Actualizar título si está disponible
        if (!empty($description_data['title'])) {
            $product->set_name($description_data['title']);
        }
        
        // Actualizar descripción larga
        if (!empty($description_data['description'])) {
            $product->set_description($description_data['description']);
        }
        
        // Actualizar meta SEO con Yoast o RankMath
        if (!empty($description_data['meta_title'])) {
            update_post_meta($product_id, '_yoast_wpseo_title', $description_data['meta_title']);
        }
        
        if (!empty($description_data['meta_description'])) {
            update_post_meta($product_id, '_yoast_wpseo_metadesc', $description_data['meta_description']);
        }
        
        // Guardar keywords como tags
        if (!empty($description_data['keywords']) && is_array($description_data['keywords'])) {
            wp_set_post_terms($product_id, $description_data['keywords'], 'product_tag');
        }
        
        $product->save();
        
        return true;
    }
    
    /**
     * HELPER: Descargar y aplicar imágenes generadas
     */
    public function apply_images_to_product($product_id, $images_data) {
        $product = wc_get_product($product_id);
        
        if (!$product) {
            throw new Exception('Producto no encontrado');
        }
        
        if (empty($images_data['images']) || !is_array($images_data['images'])) {
            throw new Exception('No hay imágenes para aplicar');
        }
        
        require_once(ABSPATH . 'wp-admin/includes/media.php');
        require_once(ABSPATH . 'wp-admin/includes/file.php');
        require_once(ABSPATH . 'wp-admin/includes/image.php');
        
        $image_ids = array();
        
        foreach ($images_data['images'] as $index => $image_info) {
            $image_url = $image_info['url'];
            
            // Descargar imagen
            $tmp = download_url($image_url);
            
            if (is_wp_error($tmp)) {
                continue;
            }
            
            $file_array = array(
                'name' => sanitize_file_name($product->get_name() . '-' . ($index + 1) . '.jpg'),
                'tmp_name' => $tmp
            );
            
            // Subir a media library
            $id = media_handle_sideload($file_array, $product_id);
            
            if (is_wp_error($id)) {
                @unlink($file_array['tmp_name']);
                continue;
            }
            
            $image_ids[] = $id;
        }
        
        // Asignar imágenes al producto
        if (!empty($image_ids)) {
            // Primera imagen como principal
            $product->set_image_id($image_ids[0]);
            
            // Resto como galería
            if (count($image_ids) > 1) {
                $product->set_gallery_image_ids(array_slice($image_ids, 1));
            }
            
            $product->save();
        }
        
        return count($image_ids);
    }
    
    /**
     * HELPER: Aplicar precio óptimo calculado
     */
    public function apply_optimal_price($product_id, $pricing_data) {
        $product = wc_get_product($product_id);
        
        if (!$product) {
            throw new Exception('Producto no encontrado');
        }
        
        if (empty($pricing_data['optimal_price'])) {
            throw new Exception('No se pudo calcular precio óptimo');
        }
        
        $optimal_price = floatval($pricing_data['optimal_price']);
        
        // Aplicar precio
        $product->set_regular_price($optimal_price);
        $product->set_price($optimal_price);
        
        // Guardar análisis como meta
        update_post_meta($product_id, '_ai_pricing_analysis', $pricing_data);
        update_post_meta($product_id, '_ai_processed_date', current_time('mysql'));
        
        $product->save();
        
        return true;
    }
}
