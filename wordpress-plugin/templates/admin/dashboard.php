<?php
if (!defined('ABSPATH')) exit;
?>

<div class="wrap aiwca-dashboard">
    <h1>
        <span class="dashicons dashicons-superhero"></span>
        <?php _e('AI WooCommerce Agent - Dashboard', 'ai-woocommerce-agent'); ?>
    </h1>
    
    <div class="aiwca-stats-grid">
        <div class="aiwca-stat-card">
            <h3><?php _e('Total Products', 'ai-woocommerce-agent'); ?></h3>
            <div class="aiwca-stat-value" id="total-products">
                <?php echo wp_count_posts('product')->publish; ?>
            </div>
        </div>
        
        <div class="aiwca-stat-card">
            <h3><?php _e('AI Processed Today', 'ai-woocommerce-agent'); ?></h3>
            <div class="aiwca-stat-value" id="ai-processed">0</div>
        </div>
        
        <div class="aiwca-stat-card">
            <h3><?php _e('Telegram Messages', 'ai-woocommerce-agent'); ?></h3>
            <div class="aiwca-stat-value" id="telegram-messages">0</div>
        </div>
        
        <div class="aiwca-stat-card">
            <h3><?php _e('Backend Status', 'ai-woocommerce-agent'); ?></h3>
            <div class="aiwca-stat-value" id="backend-status">
                <span class="dashicons dashicons-update spin"></span>
            </div>
        </div>
    </div>
    
    <div class="aiwca-quick-actions">
        <h2><?php _e('Quick Actions', 'ai-woocommerce-agent'); ?></h2>
        
        <div class="aiwca-action-buttons">
            <a href="<?php echo admin_url('admin.php?page=ai-woocommerce-agent-commands'); ?>" class="button button-primary button-hero">
                <span class="dashicons dashicons-admin-generic"></span>
                <?php _e('Execute Command', 'ai-woocommerce-agent'); ?>
            </a>
            
            <button type="button" class="button button-secondary button-hero" id="process-all-products">
                <span class="dashicons dashicons-update"></span>
                <?php _e('Process All Products', 'ai-woocommerce-agent'); ?>
            </button>
            
            <a href="<?php echo admin_url('admin.php?page=ai-woocommerce-agent-telegram'); ?>" class="button button-secondary button-hero">
                <span class="dashicons dashicons-email"></span>
                <?php _e('View Telegram Bot', 'ai-woocommerce-agent'); ?>
            </a>
        </div>
    </div>
    
    <div class="aiwca-recent-activity">
        <h2><?php _e('Recent Activity', 'ai-woocommerce-agent'); ?></h2>
        <div id="recent-activity-list">
            <p><?php _e('Loading...', 'ai-woocommerce-agent'); ?></p>
        </div>
    </div>
</div>
