<?php
if (!defined('ABSPATH')) exit;
?>

<div class="wrap aiwca-commands">
    <h1>
        <span class="dashicons dashicons-admin-generic"></span>
        <?php _e('Command Center', 'ai-woocommerce-agent'); ?>
    </h1>
    
    <div class="aiwca-command-interface">
        <div class="aiwca-command-input">
            <label for="ai-command">
                <strong><?php _e('Enter Natural Language Command:', 'ai-woocommerce-agent'); ?></strong>
            </label>
            <textarea id="ai-command" rows="4" placeholder="<?php _e('Example: Show me products without prices...', 'ai-woocommerce-agent'); ?>"></textarea>
            
            <button type="button" class="button button-primary button-large" id="execute-command">
                <span class="dashicons dashicons-controls-play"></span>
                <?php _e('Execute Command', 'ai-woocommerce-agent'); ?>
            </button>
        </div>
        
        <div class="aiwca-command-examples">
            <h3><?php _e('Example Commands:', 'ai-woocommerce-agent'); ?></h3>
            <ul>
                <li><code>Muéstrame los productos sin precio</code></li>
                <li><code>Optimiza el producto con ID 123</code></li>
                <li><code>Busca tendencias de herramientas en internet</code></li>
                <li><code>Analiza la competencia de mi producto principal</code></li>
                <li><code>Crea una campaña de marketing para mi nueva categoría</code></li>
            </ul>
        </div>
        
        <div id="command-response" style="display:none;">
            <h3><?php _e('Response:', 'ai-woocommerce-agent'); ?></h3>
            <div class="aiwca-response-content"></div>
        </div>
    </div>
    
    <div class="aiwca-command-history">
        <h2><?php _e('Command History', 'ai-woocommerce-agent'); ?></h2>
        <table class="wp-list-table widefat fixed striped">
            <thead>
                <tr>
                    <th><?php _e('Date', 'ai-woocommerce-agent'); ?></th>
                    <th><?php _e('Command', 'ai-woocommerce-agent'); ?></th>
                    <th><?php _e('Status', 'ai-woocommerce-agent'); ?></th>
                    <th><?php _e('Actions', 'ai-woocommerce-agent'); ?></th>
                </tr>
            </thead>
            <tbody id="command-history-body">
                <tr>
                    <td colspan="4"><?php _e('No commands executed yet', 'ai-woocommerce-agent'); ?></td>
                </tr>
            </tbody>
        </table>
    </div>
</div>
