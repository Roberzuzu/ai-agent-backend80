<?php
/**
 * Settings Page
 */

if (!defined('ABSPATH')) {
    exit;
}

// Save settings
if (isset($_POST['ai_dropship_save_settings']) && check_admin_referer('ai_dropship_settings', 'ai_dropship_settings_nonce')) {
    update_option('ai_dropship_api_url', sanitize_text_field($_POST['api_url']));
    update_option('ai_dropship_auto_process', isset($_POST['auto_process']) ? 'yes' : 'no');
    update_option('ai_dropship_auto_generate_content', isset($_POST['auto_generate_content']) ? 'yes' : 'no');
    
    echo '<div class="notice notice-success is-dismissible"><p>' . __('Configuración guardada correctamente', 'ai-dropshipping') . '</p></div>';
}

$api_url = get_option('ai_dropship_api_url', AI_DROPSHIP_API_URL);
$auto_process = get_option('ai_dropship_auto_process', 'yes') === 'yes';
$auto_generate_content = get_option('ai_dropship_auto_generate_content', 'no') === 'yes';

?>

<div class="wrap">
    <h1>
        <span class="dashicons dashicons-admin-settings"></span>
        <?php _e('Configuración AI Dropshipping', 'ai-dropshipping'); ?>
    </h1>

    <form method="post" action="">
        <?php wp_nonce_field('ai_dropship_settings', 'ai_dropship_settings_nonce'); ?>
        
        <table class="form-table">
            <tr>
                <th scope="row">
                    <label for="api_url"><?php _e('URL de API', 'ai-dropshipping'); ?></label>
                </th>
                <td>
                    <input type="url" id="api_url" name="api_url" value="<?php echo esc_attr($api_url); ?>" class="regular-text" required>
                    <p class="description">
                        <?php _e('URL del backend de procesamiento (ej: https://backend-verify-6.preview.emergentagent.com/api)', 'ai-dropshipping'); ?>
                    </p>
                </td>
            </tr>

            <tr>
                <th scope="row">
                    <?php _e('Procesamiento automático', 'ai-dropshipping'); ?>
                </th>
                <td>
                    <label>
                        <input type="checkbox" name="auto_process" value="1" <?php checked($auto_process); ?>>
                        <?php _e('Procesar automáticamente productos sin precio', 'ai-dropshipping'); ?>
                    </label>
                    <p class="description">
                        <?php _e('Cuando está activado, los productos sin precio se procesarán automáticamente al guardar', 'ai-dropshipping'); ?>
                    </p>
                </td>
            </tr>

            <tr>
                <th scope="row">
                    <?php _e('Generar contenido IA', 'ai-dropshipping'); ?>
                </th>
                <td>
                    <label>
                        <input type="checkbox" name="auto_generate_content" value="1" <?php checked($auto_generate_content); ?>>
                        <?php _e('Generar imágenes y videos automáticamente', 'ai-dropshipping'); ?>
                    </label>
                    <p class="description">
                        <?php _e('⚠️ Advertencia: Esto consume recursos de IA. Úsalo solo para productos importantes.', 'ai-dropshipping'); ?>
                    </p>
                </td>
            </tr>
        </table>

        <p class="submit">
            <input type="submit" name="ai_dropship_save_settings" class="button button-primary" value="<?php esc_attr_e('Guardar cambios', 'ai-dropshipping'); ?>">
        </p>
    </form>

    <hr>

    <h2><?php _e('Configuración de Webhooks', 'ai-dropshipping'); ?></h2>
    <p><?php _e('Para habilitar el procesamiento automático en tiempo real, configura estos webhooks en WooCommerce:', 'ai-dropshipping'); ?></p>
    
    <div class="card" style="max-width: none; padding: 20px;">
        <h3><?php _e('Paso 1: Ir a WooCommerce → Ajustes → Avanzado → Webhooks', 'ai-dropshipping'); ?></h3>
        
        <h3><?php _e('Paso 2: Crear webhook "Product Created"', 'ai-dropshipping'); ?></h3>
        <table class="widefat">
            <tr>
                <td><strong><?php _e('Nombre:', 'ai-dropshipping'); ?></strong></td>
                <td>Product Created - AI Processing</td>
            </tr>
            <tr>
                <td><strong><?php _e('Estado:', 'ai-dropshipping'); ?></strong></td>
                <td>Activo</td>
            </tr>
            <tr>
                <td><strong><?php _e('Tema:', 'ai-dropshipping'); ?></strong></td>
                <td>product.created</td>
            </tr>
            <tr>
                <td><strong><?php _e('URL de entrega:', 'ai-dropshipping'); ?></strong></td>
                <td>
                    <code style="background: #f0f0f1; padding: 5px 10px; display: inline-block;">
                        <?php echo esc_html($api_url); ?>/webhooks/woocommerce/product-created
                    </code>
                    <button type="button" class="button button-small copy-webhook-url" data-url="<?php echo esc_attr($api_url); ?>/webhooks/woocommerce/product-created">
                        <?php _e('Copiar', 'ai-dropshipping'); ?>
                    </button>
                </td>
            </tr>
            <tr>
                <td><strong><?php _e('Secreto:', 'ai-dropshipping'); ?></strong></td>
                <td>
                    <code style="background: #f0f0f1; padding: 5px 10px; display: inline-block;">
                        wc_webhook_secret_herramientas2024
                    </code>
                    <button type="button" class="button button-small copy-webhook-secret">
                        <?php _e('Copiar', 'ai-dropshipping'); ?>
                    </button>
                </td>
            </tr>
        </table>

        <h3 style="margin-top: 30px;"><?php _e('Paso 3: Crear webhook "Product Updated"', 'ai-dropshipping'); ?></h3>
        <table class="widefat">
            <tr>
                <td><strong><?php _e('Nombre:', 'ai-dropshipping'); ?></strong></td>
                <td>Product Updated - AI Processing</td>
            </tr>
            <tr>
                <td><strong><?php _e('Tema:', 'ai-dropshipping'); ?></strong></td>
                <td>product.updated</td>
            </tr>
            <tr>
                <td><strong><?php _e('URL de entrega:', 'ai-dropshipping'); ?></strong></td>
                <td>
                    <code style="background: #f0f0f1; padding: 5px 10px; display: inline-block;">
                        <?php echo esc_html($api_url); ?>/webhooks/woocommerce/product-updated
                    </code>
                    <button type="button" class="button button-small copy-webhook-url-updated" data-url="<?php echo esc_attr($api_url); ?>/webhooks/woocommerce/product-updated">
                        <?php _e('Copiar', 'ai-dropshipping'); ?>
                    </button>
                </td>
            </tr>
        </table>
    </div>

    <script>
    jQuery(document).ready(function($) {
        $('.copy-webhook-url').on('click', function() {
            var url = $(this).data('url');
            navigator.clipboard.writeText(url).then(function() {
                alert('<?php _e('URL copiada al portapapeles', 'ai-dropshipping'); ?>');
            });
        });

        $('.copy-webhook-url-updated').on('click', function() {
            var url = $(this).data('url');
            navigator.clipboard.writeText(url).then(function() {
                alert('<?php _e('URL copiada al portapapeles', 'ai-dropshipping'); ?>');
            });
        });

        $('.copy-webhook-secret').on('click', function() {
            navigator.clipboard.writeText('wc_webhook_secret_herramientas2024').then(function() {
                alert('<?php _e('Secreto copiado al portapapeles', 'ai-dropshipping'); ?>');
            });
        });
    });
    </script>
</div>
