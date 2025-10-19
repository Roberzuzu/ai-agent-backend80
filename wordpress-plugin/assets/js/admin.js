/**
 * AI Dropshipping Manager - Admin JavaScript
 */

(function($) {
    'use strict';

    $(document).ready(function() {

        /**
         * Process All Products
         */
        $('.ai-process-all-btn').on('click', function() {
            var $btn = $(this);
            
            if (!confirm(aiDropship.strings.processing + '\n\n¿Estás seguro de que quieres procesar todos los productos sin precio?')) {
                return;
            }

            $btn.prop('disabled', true).addClass('ai-processing');
            $btn.find('.dashicons').addClass('dashicons-update-alt').css('animation', 'rotation 2s infinite linear');

            $.ajax({
                url: aiDropship.ajax_url,
                type: 'POST',
                data: {
                    action: 'ai_process_all',
                    nonce: aiDropship.nonce
                },
                success: function(response) {
                    if (response.success) {
                        alert('✅ ' + aiDropship.strings.success + '\n\n' + response.data.message);
                        location.reload();
                    } else {
                        alert('❌ ' + aiDropship.strings.error + ': ' + response.data);
                    }
                },
                error: function(xhr) {
                    alert('❌ ' + aiDropship.strings.error + ': ' + xhr.responseText);
                },
                complete: function() {
                    $btn.prop('disabled', false).removeClass('ai-processing');
                    $btn.find('.dashicons').removeClass('dashicons-update-alt').css('animation', '');
                }
            });
        });

        /**
         * Process Single Product
         */
        $('.ai-process-single, .ai-process-product').on('click', function() {
            var $btn = $(this);
            var productId = $btn.data('product-id');

            $btn.prop('disabled', true).addClass('ai-processing');
            $btn.find('.dashicons').addClass('dashicons-update-alt').css('animation', 'rotation 2s infinite linear');

            $.ajax({
                url: aiDropship.ajax_url,
                type: 'POST',
                data: {
                    action: 'ai_process_product',
                    nonce: aiDropship.nonce,
                    product_id: productId
                },
                success: function(response) {
                    if (response.success) {
                        alert('✅ ' + aiDropship.strings.success + '\n\n' + response.data.message);
                        location.reload();
                    } else {
                        alert('❌ ' + aiDropship.strings.error + ': ' + response.data);
                    }
                },
                error: function(xhr) {
                    alert('❌ ' + aiDropship.strings.error + ': ' + xhr.responseText);
                },
                complete: function() {
                    $btn.prop('disabled', false).removeClass('ai-processing');
                    $btn.find('.dashicons').removeClass('dashicons-update-alt').css('animation', '');
                }
            });
        });

        /**
         * Generate AI Content
         */
        $('.ai-generate-content').on('click', function() {
            var $btn = $(this);
            var productId = $btn.data('product-id');

            if (!confirm('🎨 Generar contenido IA\n\nEsto generará imágenes y videos profesionales para este producto. Puede tardar 1-2 minutos.\n\n¿Continuar?')) {
                return;
            }

            $btn.prop('disabled', true).addClass('ai-processing');
            $btn.find('.dashicons').addClass('dashicons-update-alt').css('animation', 'rotation 2s infinite linear');

            $.ajax({
                url: aiDropship.ajax_url,
                type: 'POST',
                data: {
                    action: 'ai_generate_content',
                    nonce: aiDropship.nonce,
                    product_id: productId
                },
                success: function(response) {
                    if (response.success) {
                        alert('✅ ' + aiDropship.strings.success + '\n\nContenido IA generado exitosamente. El producto ha sido actualizado con nuevas imágenes.');
                        location.reload();
                    } else {
                        alert('❌ ' + aiDropship.strings.error + ': ' + response.data);
                    }
                },
                error: function(xhr) {
                    alert('❌ ' + aiDropship.strings.error + ': ' + xhr.responseText);
                },
                complete: function() {
                    $btn.prop('disabled', false).removeClass('ai-processing');
                    $btn.find('.dashicons').removeClass('dashicons-update-alt').css('animation', '');
                }
            });
        });

        /**
         * Get Stats (for future dashboard updates)
         */
        function updateStats() {
            $.ajax({
                url: aiDropship.ajax_url,
                type: 'POST',
                data: {
                    action: 'ai_get_stats',
                    nonce: aiDropship.nonce
                },
                success: function(response) {
                    if (response.success) {
                        // Update stats display if needed
                        console.log('Stats updated:', response.data);
                    }
                }
            });
        }

        // Add CSS for rotation animation
        $('<style>')
            .prop('type', 'text/css')
            .html('@keyframes rotation { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }')
            .appendTo('head');

        // ==========================================
        // NUEVOS HANDLERS - AI SUPER POWERS
        // ==========================================
        
        /**
         * Procesamiento Completo AI
         */
        $('.ai-complete-process').on('click', function() {
            var $btn = $(this);
            var productId = $btn.data('product-id');
            
            if (!confirm('🚀 PROCESAMIENTO COMPLETO AI\n\nEsto ejecutará:\n- Descripción SEO optimizada\n- Análisis de mercado\n- Precio óptimo\n- Generación de imágenes\n- Contenido para redes sociales\n\nPuede tardar 2-3 minutos.\n\n¿Continuar?')) {
                return;
            }
            
            $btn.prop('disabled', true).addClass('ai-processing');
            $btn.find('.dashicons').addClass('dashicons-update-alt').css('animation', 'rotation 2s infinite linear');
            $btn.html('<span class="dashicons dashicons-update-alt"></span> Procesando...');
            
            $.ajax({
                url: aiDropship.ajax_url,
                type: 'POST',
                data: {
                    action: 'ai_complete_process',
                    nonce: aiDropship.nonce,
                    product_id: productId
                },
                timeout: 180000, // 3 minutos
                success: function(response) {
                    if (response.success) {
                        alert('✅ ' + response.data.message + '\n\nEl producto ha sido actualizado completamente.');
                        location.reload();
                    } else {
                        alert('❌ Error: ' + (response.data || 'Error desconocido'));
                    }
                },
                error: function(xhr) {
                    alert('❌ Error de conexión: ' + xhr.responseText);
                },
                complete: function() {
                    $btn.prop('disabled', false).removeClass('ai-processing');
                    $btn.html('<span class="dashicons dashicons-superhero"></span> 🚀 PROCESAMIENTO COMPLETO AI');
                }
            });
        });
        
        /**
         * Generar Descripción SEO
         */
        $('.ai-generate-description').on('click', function() {
            var $btn = $(this);
            var productId = $btn.data('product-id');
            
            $btn.prop('disabled', true).addClass('ai-processing');
            $btn.html('<span class="dashicons dashicons-update-alt"></span> Generando...');
            
            $.ajax({
                url: aiDropship.ajax_url,
                type: 'POST',
                data: {
                    action: 'ai_generate_description',
                    nonce: aiDropship.nonce,
                    product_id: productId
                },
                timeout: 60000,
                success: function(response) {
                    if (response.success) {
                        alert('✅ ' + response.data.message);
                        location.reload();
                    } else {
                        alert('❌ Error: ' + (response.data || 'Error desconocido'));
                    }
                },
                error: function(xhr) {
                    alert('❌ Error: ' + xhr.responseText);
                },
                complete: function() {
                    $btn.prop('disabled', false).removeClass('ai-processing');
                    $btn.html('<span class="dashicons dashicons-edit"></span> 📝 Descripción SEO');
                }
            });
        });
        
        /**
         * Generar Imágenes AI
         */
        $('.ai-generate-images-btn').on('click', function() {
            var $btn = $(this);
            var productId = $btn.data('product-id');
            
            if (!confirm('🖼️ Generar Imágenes AI\n\nSe generarán 2 imágenes profesionales del producto.\nPuede tardar 1-2 minutos.\n\n¿Continuar?')) {
                return;
            }
            
            $btn.prop('disabled', true).addClass('ai-processing');
            $btn.html('<span class="dashicons dashicons-update-alt"></span> Generando...');
            
            $.ajax({
                url: aiDropship.ajax_url,
                type: 'POST',
                data: {
                    action: 'ai_generate_images',
                    nonce: aiDropship.nonce,
                    product_id: productId
                },
                timeout: 120000,
                success: function(response) {
                    if (response.success) {
                        alert('✅ ' + response.data.message);
                        location.reload();
                    } else {
                        alert('❌ Error: ' + (response.data || 'Error desconocido'));
                    }
                },
                error: function(xhr) {
                    alert('❌ Error: ' + xhr.responseText);
                },
                complete: function() {
                    $btn.prop('disabled', false).removeClass('ai-processing');
                    $btn.html('<span class="dashicons dashicons-format-image"></span> 🖼️ Generar Imágenes');
                }
            });
        });
        
        /**
         * Calcular Precio Óptimo
         */
        $('.ai-optimal-pricing').on('click', function() {
            var $btn = $(this);
            var productId = $btn.data('product-id');
            
            $btn.prop('disabled', true).addClass('ai-processing');
            $btn.html('<span class="dashicons dashicons-update-alt"></span> Calculando...');
            
            $.ajax({
                url: aiDropship.ajax_url,
                type: 'POST',
                data: {
                    action: 'ai_optimal_pricing',
                    nonce: aiDropship.nonce,
                    product_id: productId
                },
                timeout: 30000,
                success: function(response) {
                    if (response.success) {
                        alert('✅ ' + response.data.message);
                        location.reload();
                    } else {
                        alert('❌ Error: ' + (response.data || 'Error desconocido'));
                    }
                },
                error: function(xhr) {
                    alert('❌ Error: ' + xhr.responseText);
                },
                complete: function() {
                    $btn.prop('disabled', false).removeClass('ai-processing');
                    $btn.html('<span class="dashicons dashicons-chart-line"></span> 💰 Precio Óptimo');
                }
            });
        });
        
        /**
         * Análisis de Mercado
         */
        $('.ai-market-analysis').on('click', function() {
            var $btn = $(this);
            var productId = $btn.data('product-id');
            
            $btn.prop('disabled', true).addClass('ai-processing');
            $btn.html('<span class="dashicons dashicons-update-alt"></span> Analizando...');
            
            $.ajax({
                url: aiDropship.ajax_url,
                type: 'POST',
                data: {
                    action: 'ai_market_analysis',
                    nonce: aiDropship.nonce,
                    product_id: productId
                },
                timeout: 60000,
                success: function(response) {
                    if (response.success) {
                        // Mostrar resultados en modal o alert
                        var content = response.data.content || JSON.stringify(response.data, null, 2);
                        alert('✅ Análisis de Mercado Completado\n\n' + content.substring(0, 500) + '...');
                    } else {
                        alert('❌ Error: ' + (response.data || 'Error desconocido'));
                    }
                },
                error: function(xhr) {
                    alert('❌ Error: ' + xhr.responseText);
                },
                complete: function() {
                    $btn.prop('disabled', false).removeClass('ai-processing');
                    $btn.html('<span class="dashicons dashicons-analytics"></span> 📊 Análisis de Mercado');
                }
            });
        });
        
        /**
         * Generar Contenido Social
         */
        $('.ai-social-content').on('click', function() {
            var $btn = $(this);
            var productId = $btn.data('product-id');
            
            $btn.prop('disabled', true).addClass('ai-processing');
            $btn.html('<span class="dashicons dashicons-update-alt"></span> Generando...');
            
            $.ajax({
                url: aiDropship.ajax_url,
                type: 'POST',
                data: {
                    action: 'ai_social_content',
                    nonce: aiDropship.nonce,
                    product_id: productId
                },
                timeout: 60000,
                success: function(response) {
                    if (response.success) {
                        alert('✅ ' + response.data.message + '\n\nContenido generado para Instagram, Facebook y Twitter.');
                    } else {
                        alert('❌ Error: ' + (response.data || 'Error desconocido'));
                    }
                },
                error: function(xhr) {
                    alert('❌ Error: ' + xhr.responseText);
                },
                complete: function() {
                    $btn.prop('disabled', false).removeClass('ai-processing');
                    $btn.html('<span class="dashicons dashicons-share"></span> 📱 Contenido Social');
                }
            });
        });

    });

})(jQuery);
