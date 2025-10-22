<?php
/**
 * Agent Executor - Execute natural language commands
 */

if (!defined('ABSPATH')) {
    exit;
}

class AIWCA_Agent_Executor {
    
    private $ai_client;
    
    public function __construct() {
        $this->ai_client = new AIWCA_AI_Client();
    }
    
    /**
     * Execute command
     */
    public function execute($command, $user_id) {
        // Save to memory
        $this->save_to_memory($user_id, $command);
        
        // Get relevant context
        $context = $this->get_context($user_id, $command);
        
        // Build prompt
        $prompt = $this->build_execution_prompt($command, $context);
        
        // Get AI response
        $result = $this->ai_client->complete($prompt, 2000);
        
        if (!$result['success']) {
            return array(
                'success' => false,
                'error' => $result['error']
            );
        }
        
        // Parse and execute actions
        $response = $this->parse_response($result['content']);
        
        // Execute tools if needed
        if (isset($response['acciones'])) {
            $results = $this->execute_actions($response['acciones']);
            $response['results'] = $results;
        }
        
        // Update memory
        $this->update_memory($user_id, $command, $response);
        
        return array(
            'success' => true,
            'message' => isset($response['respuesta_usuario']) ? $response['respuesta_usuario'] : 'Comando ejecutado',
            'plan' => isset($response['plan']) ? $response['plan'] : '',
            'results' => isset($response['results']) ? $response['results'] : array()
        );
    }
    
    /**
     * Build execution prompt
     */
    private function build_execution_prompt($command, $context) {
        $prompt = "Eres un experto en gestión de WooCommerce con acceso a estas herramientas:\n\n";
        $prompt .= "PRODUCTOS:\n";
        $prompt .= "- obtener_productos(): Lista productos\n";
        $prompt .= "- procesar_producto(id): Optimiza con AI\n";
        $prompt .= "- actualizar_producto(id, datos): Actualiza\n";
        $prompt .= "\n";
        $prompt .= "ANÁLISIS:\n";
        $prompt .= "- obtener_estadisticas(): Stats del sitio\n";
        $prompt .= "- analizar_ventas(periodo): Reportes\n";
        $prompt .= "- buscar_tendencias(categoria): Tendencias\n";
        $prompt .= "\n";
        $prompt .= "CONTEXTO:\n";
        $prompt .= $context . "\n\n";
        $prompt .= "COMANDO: {$command}\n\n";
        $prompt .= "Responde en JSON con: {\"plan\": \"\", \"respuesta_usuario\": \"\", \"acciones\": [{\"herramienta\": \"\", \"parametros\": {}}]}";
        
        return $prompt;
    }
    
    /**
     * Parse AI response
     */
    private function parse_response($content) {
        preg_match('/\{[^}]+\}/s', $content, $matches);
        if (isset($matches[0])) {
            $data = json_decode($matches[0], true);
            if ($data) {
                return $data;
            }
        }
        
        return array(
            'plan' => 'Ejecutar comando',
            'respuesta_usuario' => $content,
            'acciones' => array()
        );
    }
    
    /**
     * Execute actions
     */
    private function execute_actions($actions) {
        $results = array();
        
        foreach ($actions as $action) {
            $tool = isset($action['herramienta']) ? $action['herramienta'] : '';
            $params = isset($action['parametros']) ? $action['parametros'] : array();
            
            $result = $this->execute_tool($tool, $params);
            $results[] = array(
                'tool' => $tool,
                'result' => $result
            );
        }
        
        return $results;
    }
    
    /**
     * Execute individual tool
     */
    private function execute_tool($tool, $params) {
        switch ($tool) {
            case 'obtener_productos':
                return $this->tool_get_products($params);
            
            case 'procesar_producto':
                return $this->tool_process_product($params);
            
            case 'obtener_estadisticas':
                return $this->tool_get_stats();
            
            default:
                return array('error' => 'Unknown tool: ' . $tool);
        }
    }
    
    /**
     * Tool: Get products
     */
    private function tool_get_products($params) {
        $args = array(
            'post_type' => 'product',
            'posts_per_page' => isset($params['limit']) ? $params['limit'] : 10,
            'post_status' => 'publish',
        );
        
        $products = get_posts($args);
        
        $result = array();
        foreach ($products as $post) {
            $product = wc_get_product($post->ID);
            $result[] = array(
                'id' => $product->get_id(),
                'name' => $product->get_name(),
                'price' => $product->get_regular_price(),
                'stock' => $product->get_stock_quantity()
            );
        }
        
        return $result;
    }
    
    /**
     * Tool: Process product
     */
    private function tool_process_product($params) {
        if (!isset($params['id'])) {
            return array('error' => 'Product ID required');
        }
        
        $processor = new AIWCA_Product_Processor();
        return $processor->process($params['id']);
    }
    
    /**
     * Tool: Get stats
     */
    private function tool_get_stats() {
        return array(
            'total_products' => wp_count_posts('product')->publish,
            'total_orders' => wc_orders_count('completed'),
            'total_revenue' => $this->get_total_revenue()
        );
    }
    
    /**
     * Get total revenue
     */
    private function get_total_revenue() {
        global $wpdb;
        
        $result = $wpdb->get_var(
            "SELECT SUM(meta_value) 
            FROM {$wpdb->postmeta} pm
            INNER JOIN {$wpdb->posts} p ON p.ID = pm.post_id
            WHERE pm.meta_key = '_order_total'
            AND p.post_status = 'wc-completed'"
        );
        
        return floatval($result);
    }
    
    /**
     * Get context
     */
    private function get_context($user_id, $command) {
        global $wpdb;
        
        $memories = $wpdb->get_results($wpdb->prepare(
            "SELECT command, response FROM {$wpdb->prefix}aiwca_memory 
            WHERE user_id = %s 
            ORDER BY created_at DESC 
            LIMIT 3",
            $user_id
        ));
        
        $context = '';
        foreach ($memories as $memory) {
            $context .= "Comando anterior: {$memory->command}\nRespuesta: " . substr($memory->response, 0, 200) . "...\n\n";
        }
        
        return $context;
    }
    
    /**
     * Save to memory
     */
    private function save_to_memory($user_id, $command) {
        global $wpdb;
        
        $wpdb->insert(
            $wpdb->prefix . 'aiwca_memory',
            array(
                'user_id' => $user_id,
                'command' => $command,
                'response' => '',
                'plan' => ''
            ),
            array('%s', '%s', '%s', '%s')
        );
    }
    
    /**
     * Update memory
     */
    private function update_memory($user_id, $command, $response) {
        global $wpdb;
        
        $response_text = isset($response['respuesta_usuario']) ? $response['respuesta_usuario'] : json_encode($response);
        $plan = isset($response['plan']) ? $response['plan'] : '';
        
        $wpdb->update(
            $wpdb->prefix . 'aiwca_memory',
            array(
                'response' => $response_text,
                'plan' => $plan
            ),
            array(
                'user_id' => $user_id,
                'command' => $command
            ),
            array('%s', '%s'),
            array('%s', '%s')
        );
    }
}
