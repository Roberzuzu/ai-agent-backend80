<?php
if (!defined('ABSPATH')) exit;

$telegram = new AIWCA_Telegram_Bot();
$token = get_option('aiwca_telegram_bot_token');
$chat_id = get_option('aiwca_telegram_chat_id');
$webhook_url = rest_url('aiwca/v1/telegram/webhook');
?>

<div class="wrap aiwca-telegram">
    <h1>
        <span class="dashicons dashicons-email"></span>
        <?php _e('Telegram Bot', 'ai-woocommerce-agent'); ?>
    </h1>
    
    <?php if (empty($token)): ?>
        <div class="notice notice-warning">
            <p>
                <strong><?php _e('Telegram Bot not configured!', 'ai-woocommerce-agent'); ?></strong><br>
                <?php _e('Please configure your Telegram Bot Token in Settings.', 'ai-woocommerce-agent'); ?>
                <a href="<?php echo admin_url('admin.php?page=ai-woocommerce-agent-settings'); ?>" class="button button-primary">
                    <?php _e('Go to Settings', 'ai-woocommerce-agent'); ?>
                </a>
            </p>
        </div>
    <?php else: ?>
        <div class="notice notice-success">
            <p><strong><?php _e('Telegram Bot is active!', 'ai-woocommerce-agent'); ?></strong></p>
        </div>
    <?php endif; ?>
    
    <div class="aiwca-telegram-info">
        <h2><?php _e('Bot Information', 'ai-woocommerce-agent'); ?></h2>
        
        <table class="form-table">
            <tr>
                <th><?php _e('Webhook URL:', 'ai-woocommerce-agent'); ?></th>
                <td>
                    <code><?php echo esc_html($webhook_url); ?></code>
                    <button type="button" class="button button-small" onclick="navigator.clipboard.writeText('<?php echo esc_js($webhook_url); ?>')">
                        <?php _e('Copy', 'ai-woocommerce-agent'); ?>
                    </button>
                </td>
            </tr>
            <tr>
                <th><?php _e('Bot Token:', 'ai-woocommerce-agent'); ?></th>
                <td>
                    <?php if ($token): ?>
                        <code><?php echo substr($token, 0, 10); ?>...<?php echo substr($token, -5); ?></code>
                    <?php else: ?>
                        <em><?php _e('Not configured', 'ai-woocommerce-agent'); ?></em>
                    <?php endif; ?>
                </td>
            </tr>
            <tr>
                <th><?php _e('Chat ID:', 'ai-woocommerce-agent'); ?></th>
                <td>
                    <?php if ($chat_id): ?>
                        <code><?php echo esc_html($chat_id); ?></code>
                    <?php else: ?>
                        <em><?php _e('Not configured', 'ai-woocommerce-agent'); ?></em>
                    <?php endif; ?>
                </td>
            </tr>
        </table>
    </div>
    
    <div class="aiwca-telegram-messages">
        <h2><?php _e('Recent Messages', 'ai-woocommerce-agent'); ?></h2>
        
        <?php
        global $wpdb;
        $messages = $wpdb->get_results(
            "SELECT * FROM {$wpdb->prefix}aiwca_telegram_messages 
            ORDER BY created_at DESC 
            LIMIT 20"
        );
        ?>
        
        <?php if ($messages): ?>
            <table class="wp-list-table widefat fixed striped">
                <thead>
                    <tr>
                        <th><?php _e('Date', 'ai-woocommerce-agent'); ?></th>
                        <th><?php _e('Chat ID', 'ai-woocommerce-agent'); ?></th>
                        <th><?php _e('Message', 'ai-woocommerce-agent'); ?></th>
                        <th><?php _e('Status', 'ai-woocommerce-agent'); ?></th>
                    </tr>
                </thead>
                <tbody>
                    <?php foreach ($messages as $msg): ?>
                        <tr>
                            <td><?php echo esc_html($msg->created_at); ?></td>
                            <td><?php echo esc_html($msg->chat_id); ?></td>
                            <td><?php echo esc_html($msg->message_text); ?></td>
                            <td>
                                <?php if ($msg->processed): ?>
                                    <span class="dashicons dashicons-yes-alt" style="color: green;"></span>
                                <?php else: ?>
                                    <span class="dashicons dashicons-clock" style="color: orange;"></span>
                                <?php endif; ?>
                            </td>
                        </tr>
                    <?php endforeach; ?>
                </tbody>
            </table>
        <?php else: ?>
            <p><?php _e('No messages yet', 'ai-woocommerce-agent'); ?></p>
        <?php endif; ?>
    </div>
</div>
