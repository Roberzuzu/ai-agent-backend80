<?php
/**
 * AI Dropshipping Manager - Super Powered v2.0
 * Integración con OpenRouter, Abacus y Perplexity
 */

// Configuración de APIs externas
define('OPENROUTER_API_KEY', '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');
define('ABACUS_API_KEY', 's2_3902ed8d205a4c2f95f35e7a361fbb59');
define('PERPLEXITY_API_KEY', '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');

/**
 * Clase de IA Avanzada para Dropshipping
 */
class AI_Dropshipping_SuperPowered {
    
    /**
     * Genera descripción de producto usando OpenRouter (mejores modelos)
     */
    public function generate_product_description($product_name, $category, $features = []) {
        $api_url = 'https://openrouter.ai/api/v1/chat/completions';
        
        $prompt = "Genera una descripción de producto profesional y persuasiva para eCommerce:\n\n";
        $prompt .= "Producto: {$product_name}\n";
        $prompt .= "Categoría: {$category}\n";
        
        if (!empty($features)) {
            $prompt .= "Características: " . implode(', ', $features) . "\n\n";
        }
        
        $prompt .= "La descripción debe incluir:\n";
        $prompt .= "1. Título atractivo con emojis relevantes\n";
        $prompt .= "2. Introducción que capte atención (2-3 líneas)\n";
        $prompt .= "3. Características principales (lista con bullets)\n";
        $prompt .= "4. Beneficios clave para el usuario\n";
        $prompt .= "5. Especificaciones técnicas\n";
        $prompt .= "6. Llamado a la acción persuasivo\n";
        $prompt .= "Formato: HTML con estilos inline para WordPress/WooCommerce";
        
        $data = [
            'model' => 'anthropic/claude-3.5-sonnet', // Mejor modelo disponible
            'messages' => [
                [
                    'role' => 'user',
                    'content' => $prompt
                ]
            ],
            'temperature' => 0.7,
            'max_tokens' => 2000
        ];
        
        $response = wp_remote_post($api_url, [
            'headers' => [
                'Authorization' => 'Bearer ' . OPENROUTER_API_KEY,
                'Content-Type' => 'application/json',
                'HTTP-Referer' => get_site_url(),
            ],
            'body' => json_encode($data),
            'timeout' => 30
        ]);
        
        if (is_wp_error($response)) {
            return ['error' => $response->get_error_message()];
        }
        
        $body = json_decode(wp_remote_retrieve_body($response), true);
        
        if (isset($body['choices'][0]['message']['content'])) {
            return [
                'success' => true,
                'description' => $body['choices'][0]['message']['content']
            ];
        }
        
        return ['error' => 'No se pudo generar descripción'];
    }
    
    /**
     * Investiga mercado y competencia usando Perplexity (búsqueda web en tiempo real)
     */
    public function research_market($product_name, $category) {
        $api_url = 'https://api.perplexity.ai/chat/completions';
        
        $prompt = "Investiga el mercado para este producto:\n\n";
        $prompt .= "Producto: {$product_name}\n";
        $prompt .= "Categoría: {$category}\n\n";
        $prompt .= "Proporciona:\n";
        $prompt .= "1. Rango de precios en el mercado actual\n";
        $prompt .= "2. Principales competidores y sus precios\n";
        $prompt .= "3. Características más valoradas por clientes\n";
        $prompt .= "4. Tendencias de búsqueda y demanda\n";
        $prompt .= "5. Precio óptimo sugerido para máxima conversión\n";
        $prompt .= "6. Keywords SEO recomendadas\n";
        $prompt .= "Formato: JSON estructurado";
        
        $data = [
            'model' => 'llama-3.1-sonar-large-128k-online', // Búsqueda web en tiempo real
            'messages' => [
                [
                    'role' => 'user',
                    'content' => $prompt
                ]
            ],
            'temperature' => 0.3 // Más preciso para datos
        ];
        
        $response = wp_remote_post($api_url, [
            'headers' => [
                'Authorization' => 'Bearer ' . PERPLEXITY_API_KEY,
                'Content-Type' => 'application/json'
            ],
            'body' => json_encode($data),
            'timeout' => 45
        ]);
        
        if (is_wp_error($response)) {
            return ['error' => $response->get_error_message()];
        }
        
        $body = json_decode(wp_remote_retrieve_body($response), true);
        
        if (isset($body['choices'][0]['message']['content'])) {
            return [
                'success' => true,
                'market_data' => $body['choices'][0]['message']['content']
            ];
        }
        
        return ['error' => 'No se pudo investigar mercado'];
    }
    
    /**
     * Genera estrategia de precios inteligente con Abacus AI
     */
    public function calculate_optimal_pricing($cost_price, $category, $market_data = null) {
        $api_url = 'https://api.abacus.ai/v1/predict';
        
        // Análisis de precios competitivos
        $prompt = "Analiza y recomienda estrategia de precios:\n\n";
        $prompt .= "Precio de coste: €{$cost_price}\n";
        $prompt .= "Categoría: {$category}\n";
        
        if ($market_data) {
            $prompt .= "Datos de mercado: {$market_data}\n\n";
        }
        
        $prompt .= "Calcula:\n";
        $prompt .= "1. Precio de venta óptimo (considerando conversión y margen)\n";
        $prompt .= "2. Precio tachado (psicología de descuento)\n";
        $prompt .= "3. Precio mínimo viable\n";
        $prompt .= "4. Margen de beneficio (%)\n";
        $prompt .= "5. Estrategia recomendada (precio premium/competitivo/económico)\n";
        $prompt .= "Responde en JSON: {precio_venta, precio_tachado, precio_minimo, margen, estrategia}";
        
        $data = [
            'input' => $prompt,
            'model_id' => 'pricing_optimizer'
        ];
        
        $response = wp_remote_post($api_url, [
            'headers' => [
                'Authorization' => 'Bearer ' . ABACUS_API_KEY,
                'Content-Type' => 'application/json'
            ],
            'body' => json_encode($data),
            'timeout' => 30
        ]);
        
        if (is_wp_error($response)) {
            // Fallback: cálculo manual con margen 50%
            return [
                'success' => true,
                'precio_venta' => round($cost_price * 1.5, 2),
                'precio_tachado' => round($cost_price * 1.8, 2),
                'margen' => 50,
                'estrategia' => 'Margen estándar aplicado'
            ];
        }
        
        $body = json_decode(wp_remote_retrieve_body($response), true);
        
        if (isset($body['prediction'])) {
            $pricing = json_decode($body['prediction'], true);
            return array_merge(['success' => true], $pricing);
        }
        
        return ['error' => 'No se pudo calcular precios'];
    }
    
    /**
     * Genera contenido SEO completo para el producto
     */
    public function generate_seo_content($product_name, $description) {
        $api_url = 'https://openrouter.ai/api/v1/chat/completions';
        
        $prompt = "Genera contenido SEO optimizado para:\n\n";
        $prompt .= "Producto: {$product_name}\n";
        $prompt .= "Descripción base: {$description}\n\n";
        $prompt .= "Genera:\n";
        $prompt .= "1. Meta Title (60 caracteres max, incluye keyword)\n";
        $prompt .= "2. Meta Description (155 caracteres, persuasiva)\n";
        $prompt .= "3. 10 Keywords principales (separadas por comas)\n";
        $prompt .= "4. 5 Long-tail keywords\n";
        $prompt .= "5. Alt text para imagen principal\n";
        $prompt .= "6. Schema markup sugerido\n";
        $prompt .= "Responde en JSON estructurado";
        
        $data = [
            'model' => 'anthropic/claude-3.5-sonnet',
            'messages' => [
                [
                    'role' => 'user',
                    'content' => $prompt
                ]
            ],
            'temperature' => 0.5
        ];
        
        $response = wp_remote_post($api_url, [
            'headers' => [
                'Authorization' => 'Bearer ' . OPENROUTER_API_KEY,
                'Content-Type' => 'application/json',
                'HTTP-Referer' => get_site_url(),
            ],
            'body' => json_encode($data),
            'timeout' => 30
        ]);
        
        if (is_wp_error($response)) {
            return ['error' => $response->get_error_message()];
        }
        
        $body = json_decode(wp_remote_retrieve_body($response), true);
        
        if (isset($body['choices'][0]['message']['content'])) {
            return [
                'success' => true,
                'seo_data' => $body['choices'][0]['message']['content']
            ];
        }
        
        return ['error' => 'No se pudo generar SEO'];
    }
    
    /**
     * Analiza tendencias y genera recomendaciones de productos
     */
    public function analyze_trends_and_recommend() {
        $api_url = 'https://api.perplexity.ai/chat/completions';
        
        $prompt = "Analiza tendencias actuales en herramientas y bricolaje para eCommerce:\n\n";
        $prompt .= "Proporciona:\n";
        $prompt .= "1. Top 10 productos más buscados en los últimos 30 días\n";
        $prompt .= "2. Categorías con mayor crecimiento\n";
        $prompt .= "3. Rango de precios óptimo por categoría\n";
        $prompt .= "4. Temporalidad (productos estacionales vs todo el año)\n";
        $prompt .= "5. Recomendaciones específicas de productos para añadir al catálogo\n";
        $prompt .= "6. Keywords trending en Google\n";
        $prompt .= "Responde en JSON estructurado con datos actualizados";
        
        $data = [
            'model' => 'llama-3.1-sonar-large-128k-online',
            'messages' => [
                [
                    'role' => 'user',
                    'content' => $prompt
                ]
            ]
        ];
        
        $response = wp_remote_post($api_url, [
            'headers' => [
                'Authorization' => 'Bearer ' . PERPLEXITY_API_KEY,
                'Content-Type' => 'application/json'
            ],
            'body' => json_encode($data),
            'timeout' => 60
        ]);
        
        if (is_wp_error($response)) {
            return ['error' => $response->get_error_message()];
        }
        
        $body = json_decode(wp_remote_retrieve_body($response), true);
        
        if (isset($body['choices'][0]['message']['content'])) {
            return [
                'success' => true,
                'trends' => $body['choices'][0]['message']['content']
            ];
        }
        
        return ['error' => 'No se pudieron analizar tendencias'];
    }
    
    /**
     * Procesa producto completo con IA
     */
    public function process_product_with_ai($product_id) {
        $product = wc_get_product($product_id);
        
        if (!$product) {
            return ['error' => 'Producto no encontrado'];
        }
        
        $product_name = $product->get_name();
        $category = wp_get_post_terms($product_id, 'product_cat', ['fields' => 'names']);
        $category = !empty($category) ? $category[0] : 'Herramientas';
        
        $results = [
            'product_id' => $product_id,
            'product_name' => $product_name,
            'timestamp' => current_time('mysql')
        ];
        
        // 1. Investigar mercado (Perplexity)
        error_log("🔍 Investigando mercado para: {$product_name}");
        $market_research = $this->research_market($product_name, $category);
        $results['market_research'] = $market_research;
        
        // 2. Calcular precios óptimos (Abacus + datos de mercado)
        error_log("💰 Calculando precios óptimos...");
        $current_price = $product->get_regular_price();
        if (empty($current_price)) {
            $current_price = 10; // Precio base si no tiene
        }
        
        $market_data = isset($market_research['market_data']) ? $market_research['market_data'] : null;
        $pricing = $this->calculate_optimal_pricing($current_price, $category, $market_data);
        $results['pricing'] = $pricing;
        
        // Actualizar precios del producto
        if ($pricing['success']) {
            $product->set_regular_price($pricing['precio_venta']);
            if (isset($pricing['precio_tachado'])) {
                $product->set_sale_price($pricing['precio_venta']);
                $product->set_regular_price($pricing['precio_tachado']);
            }
        }
        
        // 3. Generar descripción profesional (OpenRouter)
        error_log("✍️ Generando descripción con IA...");
        $description = $this->generate_product_description($product_name, $category);
        $results['description'] = $description;
        
        if ($description['success']) {
            $product->set_description($description['description']);
        }
        
        // 4. Generar contenido SEO (OpenRouter)
        error_log("🔍 Generando SEO...");
        $seo = $this->generate_seo_content($product_name, $description['description'] ?? '');
        $results['seo'] = $seo;
        
        // Guardar cambios
        $product->save();
        
        // Log del proceso
        update_post_meta($product_id, '_ai_processed', true);
        update_post_meta($product_id, '_ai_processing_date', current_time('mysql'));
        update_post_meta($product_id, '_ai_results', json_encode($results));
        
        return [
            'success' => true,
            'message' => 'Producto procesado con IA avanzada',
            'results' => $results
        ];
    }
    
    /**
     * Procesa todos los productos sin procesar
     */
    public function batch_process_products($limit = 10) {
        $args = [
            'post_type' => 'product',
            'posts_per_page' => $limit,
            'meta_query' => [
                'relation' => 'OR',
                [
                    'key' => '_ai_processed',
                    'compare' => 'NOT EXISTS'
                ],
                [
                    'key' => '_ai_processed',
                    'value' => '0'
                ]
            ]
        ];
        
        $products = get_posts($args);
        $results = [];
        
        foreach ($products as $product_post) {
            $result = $this->process_product_with_ai($product_post->ID);
            $results[] = $result;
            
            // Pausa entre productos para no saturar APIs
            sleep(2);
        }
        
        return [
            'success' => true,
            'processed' => count($results),
            'results' => $results
        ];
    }
}

// Inicializar clase
function get_ai_dropshipping_super() {
    return new AI_Dropshipping_SuperPowered();
}

// Hook para procesar productos automáticamente
add_action('woocommerce_new_product', function($product_id) {
    $ai = get_ai_dropshipping_super();
    $ai->process_product_with_ai($product_id);
});

// Cron job para procesar productos pendientes diariamente
add_action('ai_dropship_daily_processing', function() {
    $ai = get_ai_dropshipping_super();
    $ai->batch_process_products(50); // Procesar 50 productos por día
});

if (!wp_next_scheduled('ai_dropship_daily_processing')) {
    wp_schedule_event(time(), 'daily', 'ai_dropship_daily_processing');
}
