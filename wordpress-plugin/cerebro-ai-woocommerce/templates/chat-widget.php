<?php
/**
 * Template: Widget de chat flotante
 */

if (!defined('ABSPATH')) exit;

$settings = get_option('cerebro_ai_settings');
$position = $settings['chat_position'] ?? 'bottom-right';
?>

<div id="cerebro-ai-chat-widget" class="cerebro-chat-widget cerebro-position-<?php echo esc_attr($position); ?>">
    <!-- Botón flotante -->
    <button id="cerebro-chat-toggle" class="cerebro-chat-button" aria-label="Abrir Cerebro AI">
        <svg class="cerebro-icon-open" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M9.5 2A2.5 2.5 0 0 1 12 4.5v15a2.5 2.5 0 0 1-4.96.44 2.5 2.5 0 0 1-2.96-3.08 3 3 0 0 1-.34-5.58 2.5 2.5 0 0 1 1.32-4.24 2.5 2.5 0 0 1 1.98-3A2.5 2.5 0 0 1 9.5 2Z"/>
            <path d="M14.5 2A2.5 2.5 0 0 0 12 4.5v15a2.5 2.5 0 0 0 4.96.44 2.5 2.5 0 0 0 2.96-3.08 3 3 0 0 0 .34-5.58 2.5 2.5 0 0 0-1.32-4.24 2.5 2.5 0 0 0-1.98-3A2.5 2.5 0 0 0 14.5 2Z"/>
        </svg>
        <svg class="cerebro-icon-close" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <line x1="18" y1="6" x2="6" y2="18"></line>
            <line x1="6" y1="6" x2="18" y2="18"></line>
        </svg>
        <span class="cerebro-notification-badge">AI</span>
    </button>
    
    <!-- Ventana de chat -->
    <div id="cerebro-chat-window" class="cerebro-chat-window">
        <!-- Header -->
        <div class="cerebro-chat-header">
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
            <button id="cerebro-chat-close" class="cerebro-close-btn" aria-label="Cerrar">
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <line x1="18" y1="6" x2="6" y2="18"></line>
                    <line x1="6" y1="6" x2="18" y2="18"></line>
                </svg>
            </button>
        </div>
        
        <!-- Messages -->
        <div id="cerebro-chat-messages" class="cerebro-chat-messages">
            <div class="cerebro-welcome-message">
                <div class="cerebro-message cerebro-message-bot">
                    <div class="cerebro-message-content">
                        <p>👋 ¡Hola! Soy <strong>Cerebro AI</strong>, tu experto en WooCommerce.</p>
                        <p>Puedo ayudarte a:</p>
                        <ul>
                            <li>📸 Analizar fotos de productos y crearlos automáticamente</li>
                            <li>📊 Gestionar tu catálogo y optimizarlo</li>
                            <li>💰 Crear ofertas y promociones</li>
                            <li>📈 Analizar ventas y tendencias</li>
                            <li>✨ Y mucho más...</li>
                        </ul>
                        <p>¿En qué puedo ayudarte hoy?</p>
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
                    placeholder="Escribe tu comando o sube un archivo..."
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
