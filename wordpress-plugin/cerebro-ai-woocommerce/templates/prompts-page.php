<?php
/**
 * Página de Prompts Personalizados
 */

if (!defined('ABSPATH')) exit;

// Guardar prompts
if (isset($_POST['save_prompts']) && check_admin_referer('cerebro_ai_prompts')) {
    $prompts = array(
        'welcome' => sanitize_textarea_field($_POST['prompt_welcome'] ?? ''),
        'product_analysis' => sanitize_textarea_field($_POST['prompt_product'] ?? ''),
        'content_creation' => sanitize_textarea_field($_POST['prompt_content'] ?? ''),
        'custom' => sanitize_textarea_field($_POST['prompt_custom'] ?? ''),
    );
    
    update_option('cerebro_ai_prompts', $prompts);
    echo '<div class="notice notice-success"><p>✅ Prompts guardados correctamente</p></div>';
}

$prompts = get_option('cerebro_ai_prompts', array(
    'welcome' => 'Eres un asistente experto en WooCommerce. Ayuda al usuario con sus consultas de manera profesional y amigable.',
    'product_analysis' => 'Analiza este producto y proporciona sugerencias de mejora para la descripción, precio y categorización.',
    'content_creation' => 'Crea contenido atractivo y optimizado para SEO basado en la información del producto.',
    'custom' => '',
));
?>

<div class="wrap cerebro-ai-prompts">
    <h1>🧠 Prompts Personalizados - Cerebro AI</h1>
    
    <div class="cerebro-info-box">
        <h3>📝 ¿Qué son los Prompts?</h3>
        <p>Los prompts son instrucciones que le das al agente IA para que se comporte de una manera específica. Personaliza estos prompts para adaptar Cerebro AI a tu tienda.</p>
    </div>
    
    <form method="post" action="">
        <?php wp_nonce_field('cerebro_ai_prompts'); ?>
        
        <table class="form-table">
            <tr>
                <th scope="row">
                    <label for="prompt_welcome">Prompt de Bienvenida</label>
                    <p class="description">Define la personalidad y comportamiento general del agente</p>
                </th>
                <td>
                    <textarea 
                        name="prompt_welcome" 
                        id="prompt_welcome" 
                        rows="4" 
                        class="large-text"
                        placeholder="Ej: Eres un asistente experto en WooCommerce..."
                    ><?php echo esc_textarea($prompts['welcome']); ?></textarea>
                </td>
            </tr>
            
            <tr>
                <th scope="row">
                    <label for="prompt_product">Prompt de Análisis de Productos</label>
                    <p class="description">Cómo debe analizar y mejorar productos</p>
                </th>
                <td>
                    <textarea 
                        name="prompt_product" 
                        id="prompt_product" 
                        rows="4" 
                        class="large-text"
                        placeholder="Ej: Analiza este producto y proporciona..."
                    ><?php echo esc_textarea($prompts['product_analysis']); ?></textarea>
                </td>
            </tr>
            
            <tr>
                <th scope="row">
                    <label for="prompt_content">Prompt de Creación de Contenido</label>
                    <p class="description">Instrucciones para generar descripciones y contenido</p>
                </th>
                <td>
                    <textarea 
                        name="prompt_content" 
                        id="prompt_content" 
                        rows="4" 
                        class="large-text"
                        placeholder="Ej: Crea contenido atractivo y optimizado para SEO..."
                    ><?php echo esc_textarea($prompts['content_creation']); ?></textarea>
                </td>
            </tr>
            
            <tr>
                <th scope="row">
                    <label for="prompt_custom">Prompt Personalizado</label>
                    <p class="description">Instrucciones adicionales o especiales</p>
                </th>
                <td>
                    <textarea 
                        name="prompt_custom" 
                        id="prompt_custom" 
                        rows="6" 
                        class="large-text"
                        placeholder="Ej: Siempre responde en español, usa emojis, etc..."
                    ><?php echo esc_textarea($prompts['custom']); ?></textarea>
                </td>
            </tr>
        </table>
        
        <div class="cerebro-examples-box">
            <h3>💡 Ejemplos de Prompts Efectivos</h3>
            
            <h4>Para tienda de tecnología:</h4>
            <code>Eres un experto en tecnología y gadgets. Proporciona análisis técnicos detallados, compara especificaciones y recomienda productos basándote en las necesidades del usuario. Usa lenguaje técnico pero accesible.</code>
            
            <h4>Para tienda de moda:</h4>
            <code>Eres un asesor de moda profesional. Ayuda a los clientes a encontrar el estilo perfecto, sugiere combinaciones y tendencias actuales. Sé entusiasta y creativo en tus respuestas.</code>
            
            <h4>Para dropshipping:</h4>
            <code>Analiza productos considerando: competencia, tendencias de mercado, margen de ganancia óptimo y potencial viral. Prioriza productos con alta demanda y baja competencia.</code>
        </div>
        
        <p class="submit">
            <input type="submit" name="save_prompts" class="button button-primary" value="💾 Guardar Prompts">
        </p>
    </form>
    
    <div class="cerebro-tips-box">
        <h3>🎯 Tips para Mejores Prompts</h3>
        <ul>
            <li>✅ <strong>Sé específico:</strong> Cuanto más detallado, mejores resultados</li>
            <li>✅ <strong>Define el tono:</strong> Profesional, amigable, técnico, etc.</li>
            <li>✅ <strong>Establece límites:</strong> Qué debe y qué no debe hacer</li>
            <li>✅ <strong>Incluye ejemplos:</strong> Muestra el tipo de respuesta que esperas</li>
            <li>✅ <strong>Prueba y ajusta:</strong> Itera hasta encontrar el prompt perfecto</li>
        </ul>
    </div>
</div>

<style>
.cerebro-ai-prompts textarea {
    font-family: monospace;
    font-size: 13px;
}

.cerebro-info-box,
.cerebro-examples-box,
.cerebro-tips-box {
    background: #f0f6fc;
    border-left: 4px solid #4285f4;
    padding: 15px 20px;
    margin: 20px 0;
}

.cerebro-examples-box h4 {
    margin-top: 15px;
    margin-bottom: 5px;
    color: #333;
}

.cerebro-examples-box code {
    display: block;
    background: white;
    padding: 10px;
    margin: 10px 0 20px 0;
    border-radius: 4px;
    font-size: 12px;
    line-height: 1.6;
}

.cerebro-tips-box ul {
    margin: 10px 0 0 20px;
}

.cerebro-tips-box li {
    margin: 8px 0;
}
</style>
