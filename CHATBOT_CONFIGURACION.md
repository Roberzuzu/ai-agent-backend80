# 🤖 CHATBOT AUTOMATIZADO - Configuración

## ✅ INSTALADO

### Plugin Tidio Live Chat
- **Estado:** Instalado y Activado
- **Tipo:** Chatbot con IA + Chat en vivo
- **Funcionalidad:** Respuestas automáticas 24/7

## 📋 CONFIGURACIÓN NECESARIA

### 1. Crear Cuenta Tidio (2 minutos)
1. Ve a: https://www.tidio.com/
2. Registra con email: agenteweb@herramientasyaccesorios.store
3. Conecta con tu WordPress (autodetecta)
4. El widget aparecerá automáticamente en tu sitio

### 2. Configurar Respuestas Automáticas

#### FAQ Automáticas a Configurar:

**Pregunta:** "¿Cuánto tarda el envío?"
**Respuesta:** 
```
¡Hola! 👋 
Nuestros envíos son:
🚚 Península: 3-5 días
🏝️ Islas: 5-7 días
✨ Envío GRATIS en compras +50€

¿Necesitas envío express (24-48h)?
```

**Pregunta:** "¿Puedo devolver?"
**Respuesta:**
```
¡Claro! 🔄
Tienes 30 días para devolver sin problema.
Solo debe estar sin usar y en su caja original.

📧 Escríbenos a devoluciones@herramientasyaccesorios.store
```

**Pregunta:** "¿Qué métodos de pago?"
**Respuesta:**
```
Aceptamos:
💳 Tarjetas (Visa, MasterCard, Amex)
🅿️ PayPal
🔒 100% Seguro con encriptación SSL
```

**Pregunta:** "¿Los productos son originales?"
**Respuesta:**
```
¡100% originales! ✅
- Marcas: Bosch, Makita, DeWalt
- Garantía oficial del fabricante
- Distribuidores autorizados
```

**Pregunta:** "¿Tienen garantía?"
**Respuesta:**
```
Doble garantía:
🛡️ 2 años garantía legal (UE)
🏆 Garantía del fabricante (1-5 años según marca)
```

### 3. Configurar Horarios

**Chat en Vivo:**
- Lunes a Viernes: 9:00 - 18:00
- Fuera de horario: Chatbot automático

**Chatbot 24/7:**
- Respuestas instantáneas
- Deriva a email si es complejo

### 4. Personalización Widget

**Apariencia:**
- Color: #667eea (morado de tu marca)
- Posición: Esquina inferior derecha
- Mensaje bienvenida: "👋 ¡Hola! ¿En qué te ayudamos?"

**Triggers:**
- Mostrar después de 3 segundos
- Si intenta salir: "¿Necesitas ayuda? Estoy aquí 😊"
- Si está 30s en checkout: "¿Alguna duda sobre el pago?"

## 🔗 ALTERNATIVA - Widget HTML Personalizado

Si prefieres un chatbot más personalizado, he creado un código:

```html
<!-- Chatbot Personalizado -->
<div id="custom-chatbot">
    <div id="chat-button" onclick="toggleChat()">
        💬 Chat
    </div>
    
    <div id="chat-window" style="display: none;">
        <div id="chat-header">
            <h3>Chat Automático 24/7</h3>
            <button onclick="toggleChat()">✕</button>
        </div>
        
        <div id="chat-body">
            <div class="chat-message bot">
                👋 ¡Hola! Soy tu asistente virtual.<br>
                ¿En qué puedo ayudarte?
            </div>
            
            <div class="chat-options">
                <button onclick="showAnswer('shipping')">🚚 Envíos</button>
                <button onclick="showAnswer('returns')">🔄 Devoluciones</button>
                <button onclick="showAnswer('payment')">💳 Pagos</button>
                <button onclick="showAnswer('warranty')">🛡️ Garantía</button>
            </div>
        </div>
        
        <div id="chat-footer">
            <a href="mailto:contacto@herramientasyaccesorios.store">
                📧 Email
            </a>
            <a href="https://wa.me/TUNUMERO">
                📱 WhatsApp
            </a>
        </div>
    </div>
</div>

<style>
#chat-button {
    position: fixed;
    bottom: 20px;
    right: 20px;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 15px 25px;
    border-radius: 50px;
    cursor: pointer;
    box-shadow: 0 5px 20px rgba(102,126,234,0.4);
    z-index: 9999;
    font-weight: bold;
    font-size: 1.1em;
}

#chat-window {
    position: fixed;
    bottom: 80px;
    right: 20px;
    width: 350px;
    height: 500px;
    background: white;
    border-radius: 15px;
    box-shadow: 0 10px 40px rgba(0,0,0,0.3);
    z-index: 9999;
    display: flex;
    flex-direction: column;
}

#chat-header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 20px;
    border-radius: 15px 15px 0 0;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

#chat-body {
    flex: 1;
    padding: 20px;
    overflow-y: auto;
}

.chat-message {
    padding: 15px;
    margin: 10px 0;
    border-radius: 10px;
    background: #f8f9fa;
    line-height: 1.6;
}

.chat-options button {
    display: block;
    width: 100%;
    padding: 12px;
    margin: 8px 0;
    background: white;
    border: 2px solid #667eea;
    color: #667eea;
    border-radius: 8px;
    cursor: pointer;
    font-weight: bold;
    transition: all 0.3s;
}

.chat-options button:hover {
    background: #667eea;
    color: white;
}

#chat-footer {
    padding: 15px;
    border-top: 1px solid #eee;
    display: flex;
    gap: 10px;
}

#chat-footer a {
    flex: 1;
    text-align: center;
    padding: 10px;
    background: #f8f9fa;
    border-radius: 8px;
    text-decoration: none;
    color: #333;
}
</style>

<script>
function toggleChat() {
    const chatWindow = document.getElementById('chat-window');
    chatWindow.style.display = chatWindow.style.display === 'none' ? 'block' : 'none';
}

const answers = {
    shipping: `
        <div class="chat-message bot">
            🚚 <strong>Información de Envíos:</strong><br><br>
            📍 Península: 3-5 días hábiles<br>
            🏝️ Islas: 5-7 días hábiles<br>
            ⚡ Express: 1-2 días (+9,99€)<br><br>
            ✨ Envío GRATIS en compras >50€
        </div>
    `,
    returns: `
        <div class="chat-message bot">
            🔄 <strong>Devoluciones:</strong><br><br>
            ✅ 30 días para devolver<br>
            ✅ Reembolso completo<br>
            ✅ Proceso sencillo<br><br>
            📧 Escribe a: devoluciones@herramientasyaccesorios.store
        </div>
    `,
    payment: `
        <div class="chat-message bot">
            💳 <strong>Métodos de Pago:</strong><br><br>
            ✅ Tarjetas (Visa, MC, Amex)<br>
            ✅ PayPal<br>
            ✅ Transferencia (+500€)<br><br>
            🔒 100% Seguro SSL
        </div>
    `,
    warranty: `
        <div class="chat-message bot">
            🛡️ <strong>Garantía:</strong><br><br>
            ✅ 2 años garantía legal<br>
            ✅ Garantía fabricante (1-5 años)<br>
            ✅ Productos 100% originales<br><br>
            Marcas: Bosch, Makita, DeWalt
        </div>
    `
};

function showAnswer(topic) {
    const chatBody = document.getElementById('chat-body');
    chatBody.innerHTML += answers[topic];
    chatBody.scrollTop = chatBody.scrollHeight;
}
</script>
```

## 📱 WHATSAPP DIRECTO

Código para botón flotante de WhatsApp:

```html
<!-- WhatsApp Flotante -->
<a href="https://wa.me/TUNUMERO?text=Hola,%20tengo%20una%20pregunta" 
   target="_blank"
   style="position: fixed; bottom: 90px; right: 20px; background: #25D366; color: white; padding: 15px; border-radius: 50%; width: 60px; height: 60px; display: flex; align-items: center; justify-content: center; font-size: 2em; box-shadow: 0 5px 20px rgba(37,211,102,0.5); z-index: 9998; text-decoration: none;">
    📱
</a>
```

## ✅ RESULTADO

Con Tidio instalado:
- ✅ Chat automático 24/7
- ✅ Respuestas instantáneas a FAQ
- ✅ Captura de leads (emails)
- ✅ Integración con WhatsApp/Messenger
- ✅ Panel analytics incluido
- ✅ GRATIS hasta 100 conversaciones/mes

## 🎯 SIGUIENTE PASO

1. Ve a: https://herramientasyaccesorios.store/wp-admin/admin.php?page=tidio-panel
2. Completa el registro de Tidio (2 min)
3. Configura respuestas automáticas (5 min)
4. ¡Listo! Chatbot funcionando 24/7
