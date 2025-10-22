/**
 * AI WooCommerce Agent - Admin JavaScript
 */

(function($) {
    'use strict';
    
    $(document).ready(function() {
        
        // Load stats on dashboard
        if ($('.aiwca-dashboard').length) {
            loadStats();
            setInterval(loadStats, 30000); // Refresh every 30 seconds
        }
        
        // Execute command
        $('#execute-command').on('click', function() {
            var command = $('#ai-command').val().trim();
            
            if (!command) {
                alert(aiwcaData.strings.error + ': Empty command');
                return;
            }
            
            executeCommand(command);
        });
        
        // Click on example commands
        $('.aiwca-command-examples code').on('click', function() {
            $('#ai-command').val($(this).text());
        });
        
        // Process single product (from product edit page)
        $('.aiwca-process-product').on('click', function() {
            var productId = $(this).data('product-id');
            processProduct(productId);
        });
        
        // Process all products
        $('#process-all-products').on('click', function() {
            if (!confirm('This will process all products with AI. Continue?')) {
                return;
            }
            
            alert('Batch processing started. This may take a while.');
            // TODO: Implement batch processing
        });
        
        // Test connection
        $('#test-connection').on('click', function() {
            testConnection();
        });
    });
    
    /**
     * Load statistics
     */
    function loadStats() {
        $.ajax({
            url: aiwcaData.ajaxUrl,
            type: 'POST',
            data: {
                action: 'aiwca_get_stats',
                nonce: aiwcaData.nonce
            },
            success: function(response) {
                if (response.success) {
                    $('#total-products').text(response.data.total_products);
                    $('#ai-processed').text(response.data.ai_processed_today);
                    $('#telegram-messages').text(response.data.telegram_messages);
                    
                    var statusHtml = '';
                    if (response.data.backend_status === 'online') {
                        statusHtml = '<span class="dashicons dashicons-yes-alt status-online"></span> Online';
                    } else if (response.data.backend_status === 'offline') {
                        statusHtml = '<span class="dashicons dashicons-dismiss status-offline"></span> Offline';
                    } else {
                        statusHtml = '<span class="dashicons dashicons-warning status-loading"></span> Not Configured';
                    }
                    $('#backend-status').html(statusHtml);
                }
            }
        });
    }
    
    /**
     * Execute command
     */
    function executeCommand(command) {
        var $button = $('#execute-command');
        var originalText = $button.html();
        
        $button.prop('disabled', true).html('<span class="dashicons dashicons-update spin"></span> ' + aiwcaData.strings.processing);
        
        $.ajax({
            url: aiwcaData.ajaxUrl,
            type: 'POST',
            data: {
                action: 'aiwca_execute_command',
                nonce: aiwcaData.nonce,
                command: command
            },
            success: function(response) {
                $button.prop('disabled', false).html(originalText);
                
                if (response.success) {
                    $('#command-response').show();
                    $('.aiwca-response-content').html(
                        '<strong>Plan:</strong>\n' + (response.plan || 'N/A') + '\n\n' +
                        '<strong>Response:</strong>\n' + response.message + '\n\n' +
                        (response.results ? '<strong>Results:</strong>\n' + JSON.stringify(response.results, null, 2) : '')
                    );
                } else {
                    alert(aiwcaData.strings.error + ': ' + response.error);
                }
            },
            error: function() {
                $button.prop('disabled', false).html(originalText);
                alert(aiwcaData.strings.error);
            }
        });
    }
    
    /**
     * Process product
     */
    function processProduct(productId) {
        var $button = $('.aiwca-process-product[data-product-id="' + productId + '"]');
        var originalText = $button.html();
        
        $button.prop('disabled', true).html('<span class="dashicons dashicons-update spin"></span> ' + aiwcaData.strings.processing);
        
        $.ajax({
            url: aiwcaData.ajaxUrl,
            type: 'POST',
            data: {
                action: 'aiwca_process_product',
                nonce: aiwcaData.nonce,
                product_id: productId
            },
            success: function(response) {
                $button.prop('disabled', false).html(originalText);
                
                if (response.success) {
                    alert(aiwcaData.strings.success + '\nProduct processed with AI!');
                    location.reload();
                } else {
                    alert(aiwcaData.strings.error + ': ' + response.data);
                }
            },
            error: function() {
                $button.prop('disabled', false).html(originalText);
                alert(aiwcaData.strings.error);
            }
        });
    }
    
    /**
     * Test connection
     */
    function testConnection() {
        var $button = $('#test-connection');
        var originalText = $button.text();
        
        $button.prop('disabled', true).text(aiwcaData.strings.processing);
        
        $.ajax({
            url: aiwcaData.ajaxUrl,
            type: 'POST',
            data: {
                action: 'aiwca_test_connection',
                nonce: aiwcaData.nonce
            },
            success: function(response) {
                $button.prop('disabled', false).text(originalText);
                
                if (response.success) {
                    alert(aiwcaData.strings.success + '\n' + response.data);
                } else {
                    alert(aiwcaData.strings.error + '\n' + response.data);
                }
            },
            error: function() {
                $button.prop('disabled', false).text(originalText);
                alert(aiwcaData.strings.error);
            }
        });
    }
    
})(jQuery);
