<?php
/**
 * Admin Dashboard Page
 */

if (!defined('ABSPATH')) {
    exit;
}

$api_client = new AI_Dropship_API_Client();

// Get products stats
$args = array(
    'post_type' => 'product',
    'posts_per_page' => -1,
    'post_status' => 'publish'
);
$all_products = get_posts($args);
$total_products = count($all_products);

$no_price_args = array(
    'post_type' => 'product',
    'posts_per_page' => -1,
    'post_status' => 'publish',
    'meta_query' => array(
        'relation' => 'OR',
        array(
            'key' => '_regular_price',
            'value' => '',
            'compare' => '='
        ),
        array(
            'key' => '_regular_price',
            'value' => '0',
            'compare' => '='
        ),
        array(
            'key' => '_regular_price',
            'compare' => 'NOT EXISTS'
        )
    )
);
$no_price_products = get_posts($no_price_args);
$no_price_count = count($no_price_products);
$with_price_count = $total_products - $no_price_count;

?>

<div class="wrap ai-dropship-dashboard">
    <h1>
        <span class="dashicons dashicons-store" style="font-size: 32px; margin-right: 10px;"></span>
        <?php _e('AI Dropshipping Manager', 'ai-dropshipping'); ?>
    </h1>
    
    <p class="description" style="font-size: 16px; margin-bottom: 30px;">
        <?php _e('Gestión automática de productos con IA - Calcula precios óptimos y genera contenido profesional', 'ai-dropshipping'); ?>
    </p>

    <!-- Stats Cards -->
    <div class="ai-dropship-stats">
        <div class="stat-card stat-total">
            <div class="stat-icon">
                <span class="dashicons dashicons-products"></span>
            </div>
            <div class="stat-content">
                <h3><?php echo esc_html($total_products); ?></h3>
                <p><?php _e('Total Productos', 'ai-dropshipping'); ?></p>
            </div>
        </div>

        <div class="stat-card stat-success">
            <div class="stat-icon">
                <span class="dashicons dashicons-yes-alt"></span>
            </div>
            <div class="stat-content">
                <h3><?php echo esc_html($with_price_count); ?></h3>
                <p><?php _e('Con Precio', 'ai-dropshipping'); ?></p>
            </div>
        </div>

        <div class="stat-card stat-warning">
            <div class="stat-icon">
                <span class="dashicons dashicons-warning"></span>
            </div>
            <div class="stat-content">
                <h3><?php echo esc_html($no_price_count); ?></h3>
                <p><?php _e('Sin Precio', 'ai-dropshipping'); ?></p>
            </div>
        </div>

        <div class="stat-card stat-info">
            <div class="stat-icon">
                <span class="dashicons dashicons-chart-line"></span>
            </div>
            <div class="stat-content">
                <h3><?php echo $total_products > 0 ? round(($with_price_count / $total_products) * 100) : 0; ?>%</h3>
                <p><?php _e('Completado', 'ai-dropshipping'); ?></p>
            </div>
        </div>
    </div>

    <!-- Action Banner -->
    <?php if ($no_price_count > 0): ?>
    <div class="notice notice-warning is-dismissible" style="margin-top: 30px; padding: 20px; border-left-width: 5px;">
        <div style="display: flex; align-items: center; gap: 20px;">
            <span class="dashicons dashicons-info" style="font-size: 40px; color: #f56e28;"></span>
            <div style="flex: 1;">
                <h3 style="margin: 0 0 10px 0;"><?php _e('¡Atención! Productos sin precio', 'ai-dropshipping'); ?></h3>
                <p style="margin: 0 0 15px 0;">
                    <?php echo sprintf(
                        __('Tienes %d productos sin precio configurado. El sistema puede procesarlos automáticamente.', 'ai-dropshipping'),
                        $no_price_count
                    ); ?>
                </p>
                <button type="button" class="button button-primary button-hero ai-process-all-btn">
                    <span class="dashicons dashicons-update"></span>
                    <?php _e('Procesar Todos los Productos', 'ai-dropshipping'); ?>
                </button>
            </div>
        </div>
    </div>
    <?php endif; ?>

    <!-- How It Works -->
    <div class="card" style="margin-top: 30px; padding: 30px;">
        <h2>
            <span class="dashicons dashicons-lightbulb" style="color: #f0b849;"></span>
            <?php _e('¿Cómo funciona?', 'ai-dropshipping'); ?>
        </h2>
        
        <div class="ai-dropship-steps">
            <div class="step">
                <div class="step-number">1</div>
                <h3><?php _e('Importa productos', 'ai-dropshipping'); ?></h3>
                <p><?php _e('Importa productos con SharkDropship u otra herramienta de dropshipping', 'ai-dropshipping'); ?></p>
            </div>

            <div class="step">
                <div class="step-number">2</div>
                <h3><?php _e('Sistema detecta', 'ai-dropshipping'); ?></h3>
                <p><?php _e('El webhook automáticamente detecta productos nuevos sin precio', 'ai-dropshipping'); ?></p>
            </div>

            <div class="step">
                <div class="step-number">3</div>
                <h3><?php _e('Calcula precio óptimo', 'ai-dropshipping'); ?></h3>
                <p><?php _e('IA calcula el precio de venta con margen del 50% automáticamente', 'ai-dropshipping'); ?></p>
            </div>

            <div class="step">
                <div class="step-number">4</div>
                <h3><?php _e('Actualiza producto', 'ai-dropshipping'); ?></h3>
                <p><?php _e('El producto se actualiza automáticamente y está listo para vender', 'ai-dropshipping'); ?></p>
            </div>
        </div>
    </div>

    <!-- Features -->
    <div class="card" style="margin-top: 20px; padding: 30px;">
        <h2>
            <span class="dashicons dashicons-superhero"></span>
            <?php _e('Características principales', 'ai-dropshipping'); ?>
        </h2>
        
        <div class="ai-dropship-features">
            <div class="feature">
                <span class="dashicons dashicons-money-alt"></span>
                <h4><?php _e('Cálculo automático de precios', 'ai-dropshipping'); ?></h4>
                <p><?php _e('Margen del 50% para productos €1-€50, 45% para €50-€100, etc.', 'ai-dropshipping'); ?></p>
            </div>

            <div class="feature">
                <span class="dashicons dashicons-format-image"></span>
                <h4><?php _e('Generación de contenido IA', 'ai-dropshipping'); ?></h4>
                <p><?php _e('Crea imágenes profesionales y videos demostrativos con FAL AI Wan 2.5', 'ai-dropshipping'); ?></p>
            </div>

            <div class="feature">
                <span class="dashicons dashicons-update"></span>
                <h4><?php _e('Procesamiento en tiempo real', 'ai-dropshipping'); ?></h4>
                <p><?php _e('Webhooks detectan productos nuevos y los procesan en segundos', 'ai-dropshipping'); ?></p>
            </div>

            <div class="feature">
                <span class="dashicons dashicons-clock"></span>
                <h4><?php _e('Cron job de respaldo', 'ai-dropshipping'); ?></h4>
                <p><?php _e('Revisa periódicamente productos sin precio como sistema de seguridad', 'ai-dropshipping'); ?></p>
            </div>
        </div>
    </div>

    <!-- Products List -->
    <?php if ($no_price_count > 0): ?>
    <div class="card" style="margin-top: 20px; padding: 30px;">
        <h2>
            <span class="dashicons dashicons-warning" style="color: #f56e28;"></span>
            <?php _e('Productos sin precio', 'ai-dropshipping'); ?>
        </h2>
        
        <table class="wp-list-table widefat fixed striped">
            <thead>
                <tr>
                    <th><?php _e('ID', 'ai-dropshipping'); ?></th>
                    <th><?php _e('Producto', 'ai-dropshipping'); ?></th>
                    <th><?php _e('SKU', 'ai-dropshipping'); ?></th>
                    <th><?php _e('Estado', 'ai-dropshipping'); ?></th>
                    <th><?php _e('Acciones', 'ai-dropshipping'); ?></th>
                </tr>
            </thead>
            <tbody>
                <?php foreach (array_slice($no_price_products, 0, 10) as $product_post): 
                    $product = wc_get_product($product_post->ID);
                ?>
                <tr>
                    <td><?php echo esc_html($product_post->ID); ?></td>
                    <td>
                        <strong><?php echo esc_html($product->get_name()); ?></strong>
                    </td>
                    <td><?php echo esc_html($product->get_sku() ?: '-'); ?></td>
                    <td>
                        <span class="status-badge status-warning">
                            <?php _e('Sin precio', 'ai-dropshipping'); ?>
                        </span>
                    </td>
                    <td>
                        <button type="button" class="button button-small ai-process-single" data-product-id="<?php echo esc_attr($product_post->ID); ?>">
                            <span class="dashicons dashicons-update"></span>
                            <?php _e('Procesar', 'ai-dropshipping'); ?>
                        </button>
                    </td>
                </tr>
                <?php endforeach; ?>
            </tbody>
        </table>
        
        <?php if ($no_price_count > 10): ?>
        <p style="margin-top: 20px; text-align: center;">
            <?php echo sprintf(
                __('Mostrando 10 de %d productos. Usa el botón "Procesar Todos" para optimizar todos a la vez.', 'ai-dropshipping'),
                $no_price_count
            ); ?>
        </p>
        <?php endif; ?>
    </div>
    <?php endif; ?>

</div>
