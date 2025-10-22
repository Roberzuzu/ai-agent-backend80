<?php
/**
 * AI Client - Interface with OpenAI and Perplexity
 */

if (!defined('ABSPATH')) {
    exit;
}

class AIWCA_AI_Client {
    
    private $openai_key;
    private $perplexity_key;
    private $provider;
    
    public function __construct() {
        $this->openai_key = get_option('aiwca_openai_api_key');
        $this->perplexity_key = get_option('aiwca_perplexity_api_key');
        $this->provider = get_option('aiwca_ai_provider', 'perplexity');
    }
    
    /**
     * Generate text completion
     */
    public function complete($prompt, $max_tokens = 2000) {
        if ($this->provider === 'perplexity' && !empty($this->perplexity_key)) {
            return $this->complete_perplexity($prompt, $max_tokens);
        } elseif (!empty($this->openai_key)) {
            return $this->complete_openai($prompt, $max_tokens);
        }
        
        return array(
            'success' => false,
            'error' => 'No AI provider configured'
        );
    }
    
    /**
     * Complete with Perplexity
     */
    private function complete_perplexity($prompt, $max_tokens) {
        $url = 'https://api.perplexity.ai/chat/completions';
        
        $body = array(
            'model' => 'sonar-pro',
            'messages' => array(
                array('role' => 'user', 'content' => $prompt)
            ),
            'max_tokens' => $max_tokens,
            'temperature' => 0.7
        );
        
        $response = wp_remote_post($url, array(
            'headers' => array(
                'Authorization' => 'Bearer ' . $this->perplexity_key,
                'Content-Type' => 'application/json',
            ),
            'body' => json_encode($body),
            'timeout' => 60,
        ));
        
        if (is_wp_error($response)) {
            return array(
                'success' => false,
                'error' => $response->get_error_message()
            );
        }
        
        $body = json_decode(wp_remote_retrieve_body($response), true);
        
        if (isset($body['choices'][0]['message']['content'])) {
            return array(
                'success' => true,
                'content' => $body['choices'][0]['message']['content'],
                'provider' => 'perplexity'
            );
        }
        
        return array(
            'success' => false,
            'error' => 'Invalid response from Perplexity'
        );
    }
    
    /**
     * Complete with OpenAI
     */
    private function complete_openai($prompt, $max_tokens) {
        $url = 'https://api.openai.com/v1/chat/completions';
        
        $body = array(
            'model' => 'gpt-4o',
            'messages' => array(
                array('role' => 'user', 'content' => $prompt)
            ),
            'max_tokens' => $max_tokens,
            'temperature' => 0.7
        );
        
        $response = wp_remote_post($url, array(
            'headers' => array(
                'Authorization' => 'Bearer ' . $this->openai_key,
                'Content-Type' => 'application/json',
            ),
            'body' => json_encode($body),
            'timeout' => 60,
        ));
        
        if (is_wp_error($response)) {
            return array(
                'success' => false,
                'error' => $response->get_error_message()
            );
        }
        
        $body = json_decode(wp_remote_retrieve_body($response), true);
        
        if (isset($body['choices'][0]['message']['content'])) {
            return array(
                'success' => true,
                'content' => $body['choices'][0]['message']['content'],
                'provider' => 'openai'
            );
        }
        
        return array(
            'success' => false,
            'error' => 'Invalid response from OpenAI'
        );
    }
    
    /**
     * Generate embeddings
     */
    public function generate_embedding($text) {
        if (empty($this->openai_key)) {
            return false;
        }
        
        $url = 'https://api.openai.com/v1/embeddings';
        
        $body = array(
            'model' => 'text-embedding-3-small',
            'input' => $text
        );
        
        $response = wp_remote_post($url, array(
            'headers' => array(
                'Authorization' => 'Bearer ' . $this->openai_key,
                'Content-Type' => 'application/json',
            ),
            'body' => json_encode($body),
            'timeout' => 30,
        ));
        
        if (is_wp_error($response)) {
            return false;
        }
        
        $body = json_decode(wp_remote_retrieve_body($response), true);
        
        if (isset($body['data'][0]['embedding'])) {
            return $body['data'][0]['embedding'];
        }
        
        return false;
    }
    
    /**
     * Generate images with Fal AI
     */
    public function generate_images($prompt, $num_images = 2) {
        $fal_key = get_option('aiwca_fal_api_key');
        
        if (empty($fal_key)) {
            return array(
                'success' => false,
                'error' => 'Fal AI key not configured'
            );
        }
        
        // TODO: Implement Fal AI integration
        // For now, return placeholder
        return array(
            'success' => true,
            'images' => array()
        );
    }
}
