<?php
/**
 * AI Prompts Settings Page
 */

// Exit if accessed directly
if (!defined('ABSPATH')) {
    exit;
}

// Check user permissions
if (!current_user_can('manage_options')) {
    wp_die(__('No tienes permisos para acceder a esta página.'));
}

// Save settings
if (isset($_POST['ai_dropship_save_prompts']) && check_admin_referer('ai_dropship_prompts_nonce')) {
    update_option('ai_dropship_prompt_description', wp_unslash($_POST['prompt_description']));
    update_option('ai_dropship_prompt_images', wp_unslash($_POST['prompt_images']));
    update_option('ai_dropship_prompt_market', wp_unslash($_POST['prompt_market']));
    update_option('ai_dropship_prompt_social', wp_unslash($_POST['prompt_social']));
    update_option('ai_dropship_prompt_email', wp_unslash($_POST['prompt_email']));
    
    echo '<div class="notice notice-success"><p>✅ ' . __('Prompts guardados correctamente', 'ai-dropshipping') . '</p></div>';
}

// Get current prompts or defaults
$prompt_description = get_option('ai_dropship_prompt_description', 
'Genera una descripción profesional para eCommerce en español.

Producto: {product_name}
Categoría: {category}

La descripción debe incluir:
1. Título atractivo y llamativo (H1)
2. Introducción persuasiva (2-3 párrafos)
3. Lista de características principales con emojis
4. Beneficios clave para el usuario
5. Especificaciones técnicas (si aplica)
6. Llamado a la acción
7. SEO: Meta título (max 60 caracteres)
8. SEO: Meta descripción (max 160 caracteres)

Formato: JSON con las claves: title, description, meta_title, meta_description, keywords');

$prompt_images = get_option('ai_dropship_prompt_images',
'Professional product photography of {product_name}, {category}.
{style}. High quality, well lit, white background, commercial photography.
Product centered, sharp focus, professional lighting.');

$prompt_market = get_option('ai_dropship_prompt_market',
'Analiza el mercado español para: {product_name} en la categoría {category}.

Proporciona:
1. Rango de precios en el mercado (mínimo, promedio, máximo)
2. Top 3 competidores y sus precios
3. Características más valoradas por clientes
4. Tendencias actuales de búsqueda
5. Precio óptimo recomendado para España
6. Keywords SEO recomendadas

Formato: Respuesta estructurada y concisa.');

$prompt_social = get_option('ai_dropship_prompt_social',
'Genera posts para redes sociales sobre este producto:

Producto: {product_name}
Descripción: {description}

Para cada plataforma: {platforms}

Genera:
1. Texto del post (con emojis y hashtags)
2. Mejor hora para publicar
3. 5-10 hashtags relevantes
4. Call to action

Formato JSON con estructura por plataforma.');

$prompt_email = get_option('ai_dropship_prompt_email',
'Crea una campaña de email marketing para:

Producto: {product_name}
Descripción: {description}
Audiencia: {target_audience}

Genera:
1. Asunto del email (3 variaciones A/B test)
2. Preheader text
3. Contenido HTML del email (con estructura)
4. Call to action
5. Recomendaciones de segmentación

Formato JSON estructurado.');

?>

<div class="wrap">
    <h1>🤖 <?php _e('Configuración de Prompts AI', 'ai-dropshipping'); ?></h1>
    
    <p class="description">
        <?php _e('Personaliza los prompts que se envían a las APIs de IA. Usa variables entre llaves {} para datos dinámicos.', 'ai-dropshipping'); ?>
    </p>
    
    <div style="background: #fff3cd; border-left: 4px solid #ffc107; padding: 12px; margin: 20px 0;">
        <strong>💡 Variables disponibles:</strong><br>
        <code>{product_name}</code>, <code>{category}</code>, <code>{features}</code>, <code>{description}</code>, 
        <code>{base_price}</code>, <code>{style}</code>, <code>{platforms}</code>, <code>{target_audience}</code>
    </div>

    <form method="post" action="">
        <?php wp_nonce_field('ai_dropship_prompts_nonce'); ?>
        
        <div class="ai-prompt-section" style="margin-bottom: 30px;">
            <h2>📝 Prompt: Descripción de Producto</h2>
            <p class="description">Usado para generar descripciones SEO completas del producto.</p>
            <textarea 
                name="prompt_description" 
                rows="12" 
                style="width: 100%; font-family: monospace;"
                class="large-text code"
            ><?php echo esc_textarea($prompt_description); ?></textarea>
        </div>
        
        <div class="ai-prompt-section" style="margin-bottom: 30px;">
            <h2>🖼️ Prompt: Generación de Imágenes</h2>
            <p class="description">Usado para generar imágenes con Fal AI y DALL-E.</p>
            <textarea 
                name="prompt_images" 
                rows="6" 
                style="width: 100%; font-family: monospace;"
                class="large-text code"
            ><?php echo esc_textarea($prompt_images); ?></textarea>
        </div>
        
        <div class="ai-prompt-section" style="margin-bottom: 30px;">
            <h2>📊 Prompt: Análisis de Mercado</h2>
            <p class="description">Usado para investigar competencia y tendencias con Perplexity.</p>
            <textarea 
                name="prompt_market" 
                rows="10" 
                style="width: 100%; font-family: monospace;"
                class="large-text code"
            ><?php echo esc_textarea($prompt_market); ?></textarea>
        </div>
        
        <div class="ai-prompt-section" style="margin-bottom: 30px;">
            <h2>📱 Prompt: Contenido de Redes Sociales</h2>
            <p class="description">Usado para generar posts de Instagram, Facebook, Twitter.</p>
            <textarea 
                name="prompt_social" 
                rows="10" 
                style="width: 100%; font-family: monospace;"
                class="large-text code"
            ><?php echo esc_textarea($prompt_social); ?></textarea>
        </div>
        
        <div class="ai-prompt-section" style="margin-bottom: 30px;">
            <h2>📧 Prompt: Campaña de Email</h2>
            <p class="description">Usado para generar campañas de email marketing.</p>
            <textarea 
                name="prompt_email" 
                rows="10" 
                style="width: 100%; font-family: monospace;"
                class="large-text code"
            ><?php echo esc_textarea($prompt_email); ?></textarea>
        </div>
        
        <div style="margin-top: 20px; padding: 20px; background: #e7f5ff; border-left: 4px solid #2196f3;">
            <h3 style="margin-top: 0;">💡 Consejos para Prompts Efectivos:</h3>
            <ul>
                <li>✅ Sé específico y claro en tus instrucciones</li>
                <li>✅ Usa ejemplos cuando sea necesario</li>
                <li>✅ Especifica el formato de salida (JSON, HTML, texto)</li>
                <li>✅ Incluye el tono deseado (profesional, casual, persuasivo)</li>
                <li>✅ Menciona el idioma si es importante</li>
                <li>⚠️ No hagas prompts demasiado largos (max 500 palabras)</li>
                <li>⚠️ Mantén las variables entre llaves {}</li>
            </ul>
        </div>
        
        <p class="submit">
            <input 
                type="submit" 
                name="ai_dropship_save_prompts" 
                class="button button-primary button-large" 
                value="<?php _e('💾 Guardar Prompts', 'ai-dropshipping'); ?>"
            >
            <button 
                type="button" 
                class="button button-secondary" 
                onclick="if(confirm('¿Restaurar prompts por defecto? Esto sobrescribirá tus prompts personalizados.')) location.href='<?php echo admin_url('admin.php?page=ai-dropshipping-prompts&reset=1'); ?>'"
            >
                <?php _e('🔄 Restaurar Valores por Defecto', 'ai-dropshipping'); ?>
            </button>
        </p>
    </form>
    
    <div style="margin-top: 30px; padding: 15px; background: #f0f0f1; border-radius: 4px;">
        <h3 style="margin-top: 0;">🧪 Probar Prompts</h3>
        <p>Para probar tus prompts, edita cualquier producto y usa los botones AI del meta box.</p>
        <p>Los nuevos prompts se aplicarán inmediatamente en la próxima generación.</p>
    </div>
</div>

<style>
.ai-prompt-section {
    background: white;
    padding: 20px;
    border: 1px solid #ddd;
    border-radius: 4px;
}
.ai-prompt-section h2 {
    margin-top: 0;
    color: #2271b1;
}
.ai-prompt-section textarea {
    border: 1px solid #8c8f94;
    box-shadow: inset 0 1px 2px rgba(0,0,0,.07);
    background-color: #fff;
    padding: 10px;
}
.ai-prompt-section textarea:focus {
    border-color: #2271b1;
    box-shadow: 0 0 0 1px #2271b1;
}
</style>

<?php
// Handle reset
if (isset($_GET['reset']) && $_GET['reset'] == '1') {
    delete_option('ai_dropship_prompt_description');
    delete_option('ai_dropship_prompt_images');
    delete_option('ai_dropship_prompt_market');
    delete_option('ai_dropship_prompt_social');
    delete_option('ai_dropship_prompt_email');
    
    echo '<script>alert("✅ Prompts restaurados a valores por defecto"); window.location.href="' . admin_url('admin.php?page=ai-dropshipping-prompts') . '";</script>';
}
