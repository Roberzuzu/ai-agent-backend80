/**
 * Cerebro AI - Chat Widget JavaScript
 */

(function($) {
    'use strict';
    
    const CerebroAI = {
        init() {
            console.log('🧠 Cerebro AI Iniciando...');
            console.log('API URL configurada:', cerebroAI.apiUrl);
            console.log('User ID:', cerebroAI.userId);
            
            if (!cerebroAI.apiUrl) {
                console.error('❌ ERROR: API URL no configurada en WordPress!');
                console.log('Ve a: WordPress Admin > Cerebro AI > Configuración');
                return;
            }
            
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
            if (!message) return;
            
            this.addMessage('user', message);
            this.$input.val('');
            this.$typing.show();
            
            try {
                const data = await this.sendCommand(message);
                
                console.log('Backend dice:', data);
                
                const msg = data.mensaje || data.message || JSON.stringify(data);
                this.addMessage('bot', msg);
                
            } catch (error) {
                console.error('Error:', error);
                this.addMessage('bot', 'Error: ' + error.message, true);
            }
            
            this.$typing.hide();
        },
        
        async sendCommand(command) {
            const apiUrl = cerebroAI.apiUrl;
            
            const response = await fetch(apiUrl + '/agent/execute', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    command: command,
                    user_id: cerebroAI.userId || 'wp_user'
                })
            });
            
            return await response.json();
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
