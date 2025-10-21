<?php
/**
 * Template: Chat inline (shortcode)
 */

if (!defined('ABSPATH')) exit;

// Cargar scripts si no están ya cargados
if (!wp_script_is('cerebro-ai-chat', 'enqueued')) {
    wp_enqueue_style('cerebro-ai-chat');
    wp_enqueue_script('cerebro-ai-chat');
}
?>

<div class="cerebro-ai-inline-chat">
    <div class="cerebro-chat-inline-container">
        <!-- Header -->
        <div class="cerebro-chat-header cerebro-inline-header">
            <div class="cerebro-chat-header-content">
                <div class="cerebro-chat-avatar">
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M9.5 2A2.5 2.5 0 0 1 12 4.5v15a2.5 2.5 0 0 1-4.96.44 2.5 2.5 0 0 1-2.96-3.08 3 3 0 0 1-.34-5.58 2.5 2.5 0 0 1 1.32-4.24 2.5 2.5 0 0 1 1.98-3A2.5 2.5 0 0 1 9.5 2Z"/>
                    </svg>
                </div>
                <div>
                    <h3>Cerebro AI</h3>
                    <p>Experto en WooCommerce</p>
                </div>
            </div>
        </div>
        
        <!-- Messages -->
        <div id="cerebro-chat-messages" class="cerebro-chat-messages cerebro-inline-messages">
            <div class="cerebro-welcome-message">
                <div class="cerebro-message cerebro-message-bot">
                    <div class="cerebro-message-content">
                        <p>👋 ¡Hola! Soy <strong>Cerebro AI</strong>.</p>
                        <p>Puedo ayudarte con tu tienda WooCommerce. ¿En qué puedo ayudarte?</p>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Input area -->
        <div class="cerebro-chat-input-area">
            <input 
                type="file" 
                id="cerebro-file-input" 
                accept="image/*,.pdf,.docx,.xlsx,.csv" 
                style="display: none;"
            />
            <div id="cerebro-file-preview" class="cerebro-file-preview" style="display: none;">
                <div class="cerebro-file-preview-content">
                    <span id="cerebro-file-name"></span>
                    <button id="cerebro-file-remove" class="cerebro-file-remove">×</button>
                </div>
            </div>
            <div class="cerebro-chat-input-wrapper">
                <button id="cerebro-attach-btn" class="cerebro-attach-btn" title="Adjuntar archivo">
                    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="m21.44 11.05-9.19 9.19a6 6 0 0 1-8.49-8.49l8.57-8.57A4 4 0 1 1 18 8.84l-8.59 8.57a2 2 0 0 1-2.83-2.83l8.49-8.48"/>
                    </svg>
                </button>
                <input 
                    type="text" 
                    id="cerebro-chat-input" 
                    placeholder="Escribe tu comando..."
                    autocomplete="off"
                />
                <button id="cerebro-send-btn" class="cerebro-send-btn">
                    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <line x1="22" y1="2" x2="11" y2="13"></line>
                        <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
                    </svg>
                </button>
            </div>
            <div class="cerebro-typing-indicator" style="display: none;">
                <span></span><span></span><span></span>
            </div>
        </div>
    </div>
</div>

<style>
.cerebro-ai-inline-chat {
    max-width: 800px;
    margin: 40px auto;
}

.cerebro-chat-inline-container {
    background: white;
    border-radius: 16px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    overflow: hidden;
}

.cerebro-inline-header {
    border-radius: 16px 16px 0 0;
}

.cerebro-inline-messages {
    height: 500px;
    max-height: 60vh;
}
</style>
