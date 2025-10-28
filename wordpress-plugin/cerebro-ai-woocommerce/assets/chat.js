/**
 * Cerebro AI - Chat Widget JavaScript
 */

(function($) {
    'use strict';
    
    const CerebroAI = {
        init() {
            this.chatOpen = false;
            this.currentFile = null;
            this.messages = [];
            
            this.cacheDom();
            this.bindEvents();
        },
        
        cacheDom() {
            this.$toggleBtn = $('#cerebro-chat-toggle');
            this.$closeBtn = $('#cerebro-chat-close');
            this.$window = $('#cerebro-chat-window');
            this.$messages = $('#cerebro-chat-messages');
            this.$input = $('#cerebro-chat-input');
            this.$sendBtn = $('#cerebro-send-btn');
            this.$attachBtn = $('#cerebro-attach-btn');
            this.$fileInput = $('#cerebro-file-input');
            this.$filePreview = $('#cerebro-file-preview');
            this.$fileName = $('#cerebro-file-name');
            this.$fileRemove = $('#cerebro-file-remove');
            this.$typing = $('.cerebro-typing-indicator');
        },
        
        bindEvents() {
            this.$toggleBtn.on('click', () => this.toggleChat());
            this.$closeBtn.on('click', () => this.closeChat());
            this.$sendBtn.on('click', () => this.sendMessage());
            this.$input.on('keypress', (e) => {
                if (e.which === 13) this.sendMessage();
            });
            this.$attachBtn.on('click', () => this.$fileInput.click());
            this.$fileInput.on('change', (e) => this.handleFileSelect(e));
            this.$fileRemove.on('click', () => this.removeFile());
        },
        
        toggleChat() {
            this.chatOpen = !this.chatOpen;
            if (this.chatOpen) {
                this.$window.addClass('cerebro-chat-open');
                this.$input.focus();
            } else {
                this.$window.removeClass('cerebro-chat-open');
            }
        },
        
        closeChat() {
            this.chatOpen = false;
            this.$window.removeClass('cerebro-chat-open');
        },
        
        handleFileSelect(e) {
            const file = e.target.files[0];
            if (file) {
                // Validar tamaño (max 10MB)
                const maxSize = 10 * 1024 * 1024; // 10MB
                if (file.size > maxSize) {
                    alert('El archivo es muy grande. Máximo 10MB.');
                    return;
                }
                
                // Tipos permitidos
                const allowedTypes = [
                    'image/jpeg', 'image/png', 'image/gif', 'image/webp',
                    'video/mp4', 'video/mpeg', 'video/quicktime',
                    'application/pdf',
                    'application/msword',
                    'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                    'application/vnd.ms-excel',
                    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                    'text/plain', 'text/csv'
                ];
                
                if (!allowedTypes.includes(file.type)) {
                    alert('Tipo de archivo no permitido. Formatos: Imágenes, Videos, PDF, Word, Excel, CSV');
                    return;
                }
                
                this.currentFile = file;
                
                // Mostrar preview según tipo
                let preview = '';
                if (file.type.startsWith('image/')) {
                    preview = '🖼️ ';
                } else if (file.type.startsWith('video/')) {
                    preview = '🎥 ';
                } else if (file.type === 'application/pdf') {
                    preview = '📄 ';
                } else {
                    preview = '📎 ';
                }
                
                this.$fileName.text(preview + file.name);
                this.$filePreview.show();
            }
        },
        
        removeFile() {
            this.currentFile = null;
            this.$fileInput.val('');
            this.$filePreview.hide();
        },
        
        async sendMessage() {
            const message = this.$input.val().trim();
            
            if (!message && !this.currentFile) return;
            
            // Mostrar mensaje del usuario
            this.addMessage('user', message || `📎 ${this.currentFile.name}`);
            
            this.$input.val('');
            this.$typing.show();
            
            try {
                let response;
                
                if (this.currentFile) {
                    response = await this.sendWithFile(message);
                } else {
                    response = await this.sendCommand(message);
                }
                
                console.log('📡 Respuesta completa:', JSON.stringify(response, null, 2));
                
                // Manejo robusto de la respuesta
                let botMessage = 'Error procesando respuesta';
                
                if (response && response.success) {
                    // WordPress AJAX wrappea en {success: true, data: {...}}
                    const backendData = response.data;
                    
                    if (backendData) {
                        // El backend responde con {success: true, mensaje: "..."}
                        botMessage = backendData.mensaje || backendData.message || backendData.respuesta_usuario || 'Comando ejecutado';
                        
                        // Si hay análisis de archivo
                        if (backendData.file_info && backendData.file_info.analysis) {
                            botMessage += '\n\n📄 Análisis:\n' + backendData.file_info.analysis;
                        }
                        
                        // Si hay resultados
                        if (backendData.resultados && backendData.resultados.length > 0) {
                            botMessage += '\n\n🛠️ Herramientas ejecutadas: ' + backendData.resultados.length;
                        }
                        
                        this.addMessage('bot', botMessage);
                    } else {
                        this.addMessage('bot', '❌ Error: Respuesta vacía del servidor', true);
                    }
                } else {
                    // Error del servidor
                    const errorMsg = response?.data?.error || response?.error || response?.message || 'Error desconocido';
                    this.addMessage('bot', '❌ Error: ' + errorMsg, true);
                    console.error('❌ Error en respuesta:', response);
                }
            } catch (error) {
                console.error('❌ Error capturado:', error);
                this.addMessage('bot', '❌ Error de conexión: ' + error.message + '\n\nVerifica la consola (F12) para más detalles.', true);
            } finally {
                this.$typing.hide();
                this.removeFile();
            }
        },
        
        async sendCommand(command) {
            // Llamada DIRECTA al backend - sin WordPress proxy
            const apiUrl = cerebroAI.apiUrl;
            
            try {
                const response = await fetch(apiUrl + '/agent/execute', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        command: command,
                        user_id: cerebroAI.userId
                    })
                });
                
                const data = await response.json();
                return data; // Retorna directamente la respuesta del backend
                
            } catch (error) {
                console.error('Error directo al backend:', error);
                throw error;
            }
        },
        
        async sendWithFile(command) {
            const formData = new FormData();
            formData.append('file', this.currentFile);
            formData.append('user_id', cerebroAI.userId);
            if (command) formData.append('command', command);
            
            return await $.ajax({
                url: cerebroAI.apiUrl + '/agent/upload',
                method: 'POST',
                data: formData,
                processData: false,
                contentType: false,
            });
        },
        
        addMessage(type, content, isError = false) {
            const messageClass = type === 'user' ? 'cerebro-message-user' : 'cerebro-message-bot';
            const errorClass = isError ? ' cerebro-message-error' : '';
            
            const $message = $(`
                <div class="cerebro-message ${messageClass}${errorClass}">
                    <div class="cerebro-message-content">
                        ${this.formatMessage(content)}
                    </div>
                    <div class="cerebro-message-time">
                        ${this.getTime()}
                    </div>
                </div>
            `);
            
            // Eliminar mensaje de bienvenida si existe
            $('.cerebro-welcome-message').remove();
            
            this.$messages.append($message);
            this.scrollToBottom();
            
            this.messages.push({ type, content, timestamp: Date.now() });
        },
        
        formatMessage(content) {
            // Convertir saltos de línea a <br>
            return content.replace(/\n/g, '<br>');
        },
        
        getTime() {
            const now = new Date();
            return now.getHours().toString().padStart(2, '0') + ':' + 
                   now.getMinutes().toString().padStart(2, '0');
        },
        
        scrollToBottom() {
            this.$messages.scrollTop(this.$messages[0].scrollHeight);
        }
    };
    
    // Inicializar cuando el DOM esté listo
    $(document).ready(function() {
        CerebroAI.init();
    });
    
})(jQuery);
