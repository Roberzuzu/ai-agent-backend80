# 🚀 INSTALACIÓN DEL AGENTE COMPLETO - Cerebro AI

## 📦 ARCHIVOS CREADOS:

1. **agent_core.py** - El cerebro del agente con herramientas
2. **agent_endpoint_FULL.py** - Los endpoints actualizados
3. **telegram_bot.py** - Bot de Telegram
4. **INSTRUCCIONES.md** - Este archivo

---

## 🔧 PASOS DE INSTALACIÓN:

### **PASO 1: Subir archivos a Render**

Opción A - Por GitHub:
```bash
1. Ve a tu repo: https://github.com/roberzuzu/ai-agent-backend80
2. Crea los archivos:
   - agent_core.py (contenido del archivo 1)
   - telegram_bot.py (contenido del archivo 3)
3. Commit changes
```

Opción B - Por Shell de Render:
```bash
# Conecta a la Shell
cd /app

# Crea agent_core.py
nano agent_core.py
# Pega el contenido, Ctrl+O, Ctrl+X

# Crea telegram_bot.py  
nano telegram_bot.py
# Pega el contenido, Ctrl+O, Ctrl+X
```

---

### **PASO 2: Modificar server.py**

```bash
nano server.py
```

**2.1 - Agregar imports (línea ~50, después de otros imports):**

```python
from agent_core import CerebroAgent
from telegram_bot import TelegramBot
```

**2.2 - Inicializar el agente (línea ~200, después de `db = client[db_name]`):**

```python
# Inicializar Cerebro AI Agent
ADMIN_TELEGRAM_ID = os.environ.get('ADMIN_TELEGRAM_ID', '7202793910')
agente = CerebroAgent(db, ADMIN_TELEGRAM_ID)
logger.info("✅ Cerebro AI Agent inicializado")

# Inicializar Telegram Bot
telegram_bot = None
if os.environ.get('TELEGRAM_BOT_TOKEN'):
    telegram_bot = TelegramBot(
        token=os.environ.get('TELEGRAM_BOT_TOKEN'),
        admin_id=ADMIN_TELEGRAM_ID,
        agent=agente
    )
    logger.info("✅ Telegram Bot inicializado")
```

**2.3 - Reemplazar el endpoint /agent/execute (línea ~7047):**

BUSCA:
```python
@api_router.post("/agent/execute")
async def agent_execute_command_temp(request: AgentExecuteRequest):
```

REEMPLAZA TODA ESA FUNCIÓN (hasta antes de `@api_router.post("/agent/chat")`) con el contenido de `agent_endpoint_FULL.py`

**2.4 - Agregar endpoint de webhook Telegram (al final de los endpoints de agent):**

```python
@api_router.post("/webhook/telegram")
async def telegram_webhook(request: Request):
    """Webhook para recibir mensajes de Telegram"""
    try:
        if not telegram_bot:
            return {"error": "Bot no configurado"}
        
        update = await request.json()
        await telegram_bot.procesar_webhook(update)
        
        return {"ok": True}
    except Exception as e:
        logger.error(f"Error en webhook Telegram: {str(e)}")
        return {"error": str(e)}
```

---

### **PASO 3: Agregar variables de entorno en Render**

```
Dashboard → Environment → Add Environment Variable
```

Agrega estas:

```bash
# Telegram
TELEGRAM_BOT_TOKEN=7708509018:AAErAOblRAlC587j1QB4k19PAfDgoiZ3kWk
ADMIN_TELEGRAM_ID=7202793910

# Ya tienes estas (verifica que estén):
PERPLEXITY_API_KEY=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
OPENAI_API_KEY=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
OPENROUTER_API_KEY=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
WOOCOMMERCE_URL=https://herramientasyaccesorios.store
WOOCOMMERCE_CONSUMER_KEY=ck_4f50637d85ec404fff441fceb7b113b5050431ea
WOOCOMMERCE_CONSUMER_SECRET=cs_e59ef18ea20d80ffdf835803ad2fdd834a4ba19f
```

---

### **PASO 4: Deploy**

```
Manual Deploy → Deploy latest commit
Espera 3-5 minutos
```

Verifica en los logs:
```
✅ Cerebro AI Agent inicializado
✅ Telegram Bot inicializado
```

---

### **PASO 5: Configurar webhook de Telegram**

Ejecuta este comando UNA VEZ (desde cualquier terminal o navegador):

```bash
curl -X POST "https://api.telegram.org/bot7708509018:AAErAOblRAlC587j1QB4k19PAfDgoiZ3kWk/setWebhook?url=https://ai-agent-backend80.onrender.com/api/webhook/telegram"
```

Deberías ver:
```json
{"ok":true,"result":true,"description":"Webhook was set"}
```

---

## 🧪 PROBAR EL SISTEMA:

### **Prueba 1: Chat en la web**
```
1. Ve a: https://herramientasyaccesorios.store
2. Abre el chat
3. Escribe: "hola cerebro, ¿cuáles son las tendencias de bricolaje en 2025?"
4. Debería responder con información actualizada de internet
```

### **Prueba 2: Telegram**
```
1. Busca el bot en Telegram: @CerebroAI_bot (o usa el link del bot)
2. Envía: /start
3. Envía: /status
4. Envía: "lista los productos de la tienda"
```

### **Prueba 3: Acciones con autorización**
```
1. Desde el chat web (como usuario normal):
   "Crea un producto de taladro inalámbrico por €89"

2. El agente te dirá que necesita autorización

3. Recibirás notificación en Telegram

4. Responde en Telegram para autorizar/rechazar
```

---

## 🎯 CAPACIDADES DEL AGENTE:

### **Conversación:**
- ✅ Respuestas inteligentes con contexto
- ✅ Memoria de conversaciones previas
- ✅ Búsqueda en internet en tiempo real
- ✅ Análisis y recomendaciones

### **Acciones WooCommerce:**
- ✅ Listar productos
- ✅ Crear productos nuevos
- ✅ Modificar productos existentes
- ✅ Crear ofertas y descuentos
- ✅ Analizar ventas

### **Sistema de Autorización:**
- ✅ Acciones simples: ejecuta directamente
- ✅ Acciones críticas: solicita autorización
- ✅ Notificaciones por Telegram
- ✅ Control remoto desde Telegram

### **Telegram Bot:**
- ✅ /status - Estado del sistema
- ✅ /productos - Lista de productos
- ✅ /ventas - Análisis de ventas
- ✅ /pendientes - Acciones pendientes
- ✅ Chat directo con el agente

---

## 🔧 PERSONALIZACIÓN:

### **Cambiar el system_prompt:**

Edita `agent_core.py`, línea ~50:

```python
self.system_prompt = """
TU PROMPT PERSONALIZADO AQUÍ
"""
```

### **Agregar más herramientas:**

En `agent_core.py`, agrega funciones a la clase `CerebroAgent`:

```python
async def mi_nueva_herramienta(self, parametros):
    # Tu código aquí
    pass
```

Y regístrala en `self.tools`:

```python
self.tools = {
    'buscar_internet': self.buscar_internet,
    'mi_nueva_herramienta': self.mi_nueva_herramienta,  # ← Agregar aquí
}
```

---

## 🐛 TROUBLESHOOTING:

### **El agente no responde:**
```bash
# Verifica logs en Render
# Busca errores de import o inicialización
```

### **Telegram no funciona:**
```bash
# Verifica el webhook:
curl "https://api.telegram.org/bot7708509018:AAErAOblRAlC587j1QB4k19PAfDgoiZ3kWk/getWebhookInfo"

# Debería mostrar:
# "url": "https://ai-agent-backend80.onrender.com/api/webhook/telegram"
```

### **WooCommerce no funciona:**
```bash
# Verifica las variables de entorno en Render
# Verifica que las API keys de WooCommerce sean correctas
```

---

## 📊 LOGS IMPORTANTES:

Busca en los logs de Render:

```
✅ Cerebro AI Agent inicializado
✅ Telegram Bot inicializado
✅ MongoDB connection successful
✅ Perplexity API: Configured
✅ OpenAI API: Configured
✅ WooCommerce: Configured
```

---

## 🎉 ¡LISTO!

Tu agente está completo con:
- 🤖 IA conversacional avanzada
- 🛠️ Ejecución de acciones
- 🔐 Sistema de autorización
- 📱 Control por Telegram
- 💾 Memoria persistente
- 🔍 Búsqueda en internet

**¿Dudas o problemas? Revisa los logs o pregunta.**
