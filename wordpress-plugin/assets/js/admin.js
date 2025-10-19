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

    });

})(jQuery);
