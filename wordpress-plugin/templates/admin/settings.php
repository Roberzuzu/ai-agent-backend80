<?php
if (!defined('ABSPATH')) exit;

// Save settings
if (isset($_POST['aiwca_save_settings']) && check_admin_referer('aiwca_settings')) {
    update_option('aiwca_backend_url', sanitize_text_field($_POST['backend_url']));
    update_option('aiwca_openai_api_key', sanitize_text_field($_POST['openai_api_key']));
    update_option('aiwca_perplexity_api_key', sanitize_text_field($_POST['perplexity_api_key']));
    update_option('aiwca_telegram_bot_token', sanitize_text_field($_POST['telegram_bot_token']));
    update_option('aiwca_telegram_chat_id', sanitize_text_field($_POST['telegram_chat_id']));
    update_option('aiwca_stripe_api_key', sanitize_text_field($_POST['stripe_api_key']));
    update_option('aiwca_fal_api_key', sanitize_text_field($_POST['fal_api_key']));
    update_option('aiwca_auto_optimize_products', isset($_POST['auto_optimize_products']) ? 'yes' : 'no');
    update_option('aiwca_enable_telegram_bot', isset($_POST['enable_telegram_bot']) ? 'yes' : 'no');
    update_option('aiwca_ai_provider', sanitize_text_field($_POST['ai_provider']));
    
    echo '<div class="notice notice-success"><p>' . __('Settings saved!', 'ai-woocommerce-agent') . '</p></div>';
}
?>

<div class="wrap aiwca-settings">
    <h1>
        <span class="dashicons dashicons-admin-settings"></span>
        <?php _e('AI WooCommerce Agent - Settings', 'ai-woocommerce-agent'); ?>
    </h1>
    
    <form method="post" action="">
        <?php wp_nonce_field('aiwca_settings'); ?>
        
        <h2 class="title"><?php _e('Backend Configuration', 'ai-woocommerce-agent'); ?></h2>
        <table class="form-table">
            <tr>
                <th scope="row">
                    <label for="backend_url"><?php _e('Backend URL', 'ai-woocommerce-agent'); ?></label>
                </th>
                <td>
                    <input type="url" name="backend_url" id="backend_url" class="regular-text" value="<?php echo esc_attr(get_option('aiwca_backend_url')); ?>" placeholder="https://tu-servidor.com/api">
                    <p class="description"><?php _e('URL of your FastAPI backend (optional if using direct APIs)', 'ai-woocommerce-agent'); ?></p>
                </td>
            </tr>
        </table>
        
        <h2 class="title"><?php _e('AI Provider Settings', 'ai-woocommerce-agent'); ?></h2>
        <table class="form-table">
            <tr>
                <th scope="row">
                    <label for="ai_provider"><?php _e('AI Provider', 'ai-woocommerce-agent'); ?></label>
                </th>
                <td>
                    <select name="ai_provider" id="ai_provider">
                        <option value="perplexity" <?php selected(get_option('aiwca_ai_provider'), 'perplexity'); ?>>Perplexity (Recommended)</option>
                        <option value="openai" <?php selected(get_option('aiwca_ai_provider'), 'openai'); ?>>OpenAI</option>
                    </select>
                </td>
            </tr>
            <tr>
                <th scope="row">
                    <label for="perplexity_api_key"><?php _e('Perplexity API Key', 'ai-woocommerce-agent'); ?></label>
                </th>
                <td>
                    <input type="password" name="perplexity_api_key" id="perplexity_api_key" class="regular-text" value="<?php echo esc_attr(get_option('aiwca_perplexity_api_key')); ?>">
                    <p class="description"><?php _e('Get your key at perplexity.ai', 'ai-woocommerce-agent'); ?></p>
                </td>
            </tr>
            <tr>
                <th scope="row">
                    <label for="openai_api_key"><?php _e('OpenAI API Key', 'ai-woocommerce-agent'); ?></label>
                </th>
                <td>
                    <input type="password" name="openai_api_key" id="openai_api_key" class="regular-text" value="<?php echo esc_attr(get_option('aiwca_openai_api_key')); ?>">
                    <p class="description"><?php _e('Get your key at platform.openai.com', 'ai-woocommerce-agent'); ?></p>
                </td>
            </tr>
        </table>
        
        <h2 class="title"><?php _e('Telegram Bot', 'ai-woocommerce-agent'); ?></h2>
        <table class="form-table">
            <tr>
                <th scope="row">
                    <label for="enable_telegram_bot"><?php _e('Enable Telegram Bot', 'ai-woocommerce-agent'); ?></label>
                </th>
                <td>
                    <input type="checkbox" name="enable_telegram_bot" id="enable_telegram_bot" <?php checked(get_option('aiwca_enable_telegram_bot'), 'yes'); ?>>
                </td>
            </tr>
            <tr>
                <th scope="row">
                    <label for="telegram_bot_token"><?php _e('Bot Token', 'ai-woocommerce-agent'); ?></label>
                </th>
                <td>
                    <input type="text" name="telegram_bot_token" id="telegram_bot_token" class="regular-text" value="<?php echo esc_attr(get_option('aiwca_telegram_bot_token')); ?>">
                    <p class="description"><?php _e('Get from @BotFather on Telegram', 'ai-woocommerce-agent'); ?></p>
                </td>
            </tr>
            <tr>
                <th scope="row">
                    <label for="telegram_chat_id"><?php _e('Chat ID', 'ai-woocommerce-agent'); ?></label>
                </th>
                <td>
                    <input type="text" name="telegram_chat_id" id="telegram_chat_id" class="regular-text" value="<?php echo esc_attr(get_option('aiwca_telegram_chat_id')); ?>">
                    <p class="description"><?php _e('Your Telegram chat ID', 'ai-woocommerce-agent'); ?></p>
                </td>
            </tr>
        </table>
        
        <h2 class="title"><?php _e('Additional Services', 'ai-woocommerce-agent'); ?></h2>
        <table class="form-table">
            <tr>
                <th scope="row">
                    <label for="stripe_api_key"><?php _e('Stripe API Key', 'ai-woocommerce-agent'); ?></label>
                </th>
                <td>
                    <input type="password" name="stripe_api_key" id="stripe_api_key" class="regular-text" value="<?php echo esc_attr(get_option('aiwca_stripe_api_key')); ?>">
                </td>
            </tr>
            <tr>
                <th scope="row">
                    <label for="fal_api_key"><?php _e('Fal AI API Key', 'ai-woocommerce-agent'); ?></label>
                </th>
                <td>
                    <input type="password" name="fal_api_key" id="fal_api_key" class="regular-text" value="<?php echo esc_attr(get_option('aiwca_fal_api_key')); ?>">
                    <p class="description"><?php _e('For AI image generation', 'ai-woocommerce-agent'); ?></p>
                </td>
            </tr>
        </table>
        
        <h2 class="title"><?php _e('Automation', 'ai-woocommerce-agent'); ?></h2>
        <table class="form-table">
            <tr>
                <th scope="row">
                    <label for="auto_optimize_products"><?php _e('Auto-optimize Products', 'ai-woocommerce-agent'); ?></label>
                </th>
                <td>
                    <input type="checkbox" name="auto_optimize_products" id="auto_optimize_products" <?php checked(get_option('aiwca_auto_optimize_products'), 'yes'); ?>>
                    <p class="description"><?php _e('Automatically process new products with AI', 'ai-woocommerce-agent'); ?></p>
                </td>
            </tr>
        </table>
        
        <p class="submit">
            <button type="submit" name="aiwca_save_settings" class="button button-primary button-large">
                <?php _e('Save Settings', 'ai-woocommerce-agent'); ?>
            </button>
            <button type="button" id="test-connection" class="button button-secondary button-large">
                <?php _e('Test Connection', 'ai-woocommerce-agent'); ?>
            </button>
        </p>
    </form>
</div>
