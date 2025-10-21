# 🤖 Guía de Integración: Cerebro AI + n8n + Telegram

## 📋 RESUMEN

Este workflow de n8n conecta tu bot de Telegram directamente con el sistema **Cerebro AI** para control completo mediante comandos de lenguaje natural.

---

## ✨ CARACTERÍSTICAS DEL WORKFLOW

### **Comandos Soportados:**

#### **1. Comandos Directos**
- `/ayuda` o `/start` - Muestra ayuda completa
- `/status` - Estado del Cerebro AI (herramientas, memoria, RAG)
- `/memoria` - Ver tus últimas 5 memorias guardadas
- `/procesar [ID]` - Procesar producto específico

#### **2. Lenguaje Natural**
Cualquier texto que NO empiece con `/` se envía al Cerebro AI:

```
"Busca 10 herramientas eléctricas tendencia"
"Procesa el producto 4146"
"Dame las estadísticas del sitio"
"Crea un cupón del 20% para sierras"
"Analiza la competencia de taladros"
"Actualiza el stock del producto 100 a 50"
```

---

## 🔧 INSTALACIÓN EN n8n

### **Paso 1: Importar el Workflow**

1. Abre tu instancia de n8n
2. Click en **"+"** → **"Import from File"**
3. Selecciona: `/app/n8n-workflow-cerebro-ai-telegram.json`
4. El workflow se importará con todos los nodos

### **Paso 2: Configurar Credenciales de Telegram**

1. **Crear Bot de Telegram:**
   - Habla con [@BotFather](https://t.me/BotFather)
   - Envía `/newbot`
   - Sigue las instrucciones
   - Copia el **Bot Token**

2. **Configurar en n8n:**
   - En n8n, ve a **Credentials** → **Add Credential**
   - Busca **"Telegram"**
   - Nombre: `Telegram Bot Cerebro AI`
   - Access Token: Pega tu token
   - Guarda

3. **Asignar Credencial al Workflow:**
   - Abre el nodo **"Telegram Trigger"**
   - En "Credential to connect with", selecciona `Telegram Bot Cerebro AI`
   - Repite para los nodos: `Send Help`, `Send Status`, `Send Memory`, `Send Processing`, `Send Result`

### **Paso 3: Verificar URL del Backend**

En los nodos HTTP Request, verifica que la URL sea correcta:

```
https://api-switcher.preview.emergentagent.com/api/agent/...
```

Si tu dominio es diferente, actualiza en estos nodos:
- `Get Agent Status`
- `Get User Memory`
- `Execute with Cerebro AI`

### **Paso 4: Activar el Workflow**

1. Click en **"Active"** en la esquina superior derecha
2. El workflow ahora está escuchando mensajes de Telegram

---

## 🎯 FLUJO DEL WORKFLOW

```
┌─────────────────────┐
│  Usuario Telegram   │
│  Envía mensaje      │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Telegram Trigger   │
│  (n8n recibe)       │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  ¿Es comando?       │
│  (empieza con /)    │
└──────┬──────────────┘
       │
       ├─── SÍ ──→ Parse Command ──→ Route Command
       │                              │
       │                              ├─ /ayuda → Send Help
       │                              ├─ /status → Get Agent Status → Send Status
       │                              └─ /memoria → Get User Memory → Format Memory → Send Memory
       │
       └─── NO ──→ Parse Natural Language
                   │
                   ▼
                   Send Processing ("Analizando...")
                   │
                   ▼
                   Execute with Cerebro AI
                   │
                   ▼
                   Format Result
                   │
                   ▼
                   Send Result
```

---

## 📊 NODOS DEL WORKFLOW

### **1. Telegram Trigger**
- **Tipo:** Trigger
- **Función:** Escucha todos los mensajes del bot
- **Updates:** `message`

### **2. Is Command?**
- **Tipo:** IF
- **Función:** Detecta si el mensaje empieza con `/`
- **Output:** TRUE = comando, FALSE = lenguaje natural

### **3. Parse Command**
- **Tipo:** Code
- **Función:** Extrae comando y argumentos
- **Output:** `command`, `args`, `user_id`, `chat_id`

### **4. Route Command**
- **Tipo:** Switch
- **Función:** Enruta comandos específicos
- **Cases:** `/ayuda`, `/start`, `/status`, `/memoria`

### **5. Send Help**
- **Tipo:** Telegram
- **Función:** Envía mensaje de ayuda
- **Parse Mode:** Markdown

### **6. Get Agent Status**
- **Tipo:** HTTP Request
- **URL:** `GET /api/agent/status`
- **Función:** Obtiene estado del agente

### **7. Send Status**
- **Tipo:** Telegram
- **Función:** Formatea y envía estado

### **8. Get User Memory**
- **Tipo:** HTTP Request
- **URL:** `GET /api/agent/memory/{user_id}?limit=5`
- **Función:** Obtiene memoria del usuario

### **9. Format Memory**
- **Tipo:** Code
- **Función:** Formatea memorias para Telegram
- **Output:** Texto markdown con últimas 5 memorias

### **10. Send Memory**
- **Tipo:** Telegram
- **Función:** Envía memorias al usuario

### **11. Parse Natural Language**
- **Tipo:** Code
- **Función:** Prepara comando de lenguaje natural
- **Output:** `command`, `user_id`, `chat_id`

### **12. Send Processing**
- **Tipo:** Telegram
- **Función:** Notifica que está procesando
- **Mensaje:** "🧠 Analizando tu solicitud..."

### **13. Execute with Cerebro AI**
- **Tipo:** HTTP Request
- **URL:** `POST /api/agent/execute`
- **Body:** `{"command": "...", "user_id": "..."}`
- **Timeout:** 180000ms (3 minutos)

### **14. Format Result**
- **Tipo:** Code
- **Función:** Formatea respuesta del agente
- **Output:** Markdown con resultados estructurados

### **15. Send Result**
- **Tipo:** Telegram
- **Función:** Envía resultado final al usuario

---

## 🔐 VARIABLES DE ENTORNO

Asegúrate de que tu backend tenga estas variables:

```env
# Telegram
TELEGRAM_BOT_TOKEN=7708509018:AAErAOblRAlC587j1QB4k19PAfDgoiZ3kWk
TELEGRAM_CHAT_ID=7202793910

# Backend URL
BACKEND_URL=https://api-switcher.preview.emergentagent.com
```

---

## 🧪 TESTING DEL WORKFLOW

### **Test 1: Comando de Ayuda**
```
Enviar en Telegram: /ayuda
Resultado esperado: Lista de comandos disponibles
```

### **Test 2: Estado del Agente**
```
Enviar en Telegram: /status
Resultado esperado: 
📊 Estado del Cerebro AI
🤖 Agente: ✅ Activo
🔧 Herramientas: 18
💾 Conversaciones: X
🧠 Memorias: Y
```

### **Test 3: Ver Memoria**
```
Enviar en Telegram: /memoria
Resultado esperado: Últimas 5 memorias o mensaje de "No tienes memorias"
```

### **Test 4: Lenguaje Natural**
```
Enviar en Telegram: Dame las estadísticas del sitio
Resultado esperado:
🧠 Analizando tu solicitud...
✅ Completado
📋 Plan: Obtener estadísticas...
*Resultados:*
✅ obtener_estadisticas
```

### **Test 5: Comando Complejo**
```
Enviar en Telegram: Busca 5 herramientas eléctricas tendencia en España
Resultado esperado:
🧠 Analizando tu solicitud...
✅ Voy a realizar una búsqueda completa...
📋 Plan: Buscar y analizar herramientas...
*Resultados:*
✅ buscar_tendencias
✅ analizar_competencia
```

---

## 🎨 PERSONALIZACIÓN

### **Cambiar Formato de Respuestas**

Edita el nodo `Format Result` para cambiar cómo se muestran los resultados.

### **Agregar Nuevos Comandos**

1. Agregar case en el nodo `Route Command`
2. Crear nodos para manejar el nuevo comando
3. Conectar al flujo

### **Cambiar Timeout**

En el nodo `Execute with Cerebro AI`, ajusta el timeout según tus necesidades:
- Default: 180000ms (3 minutos)
- Comandos rápidos: 60000ms (1 minuto)
- Comandos lentos: 300000ms (5 minutos)

---

## 🚨 TROUBLESHOOTING

### **Problema: Bot no responde**
- Verificar que el workflow esté **Active**
- Verificar credenciales de Telegram
- Verificar logs de n8n

### **Problema: Error 401**
- Verificar token del bot de Telegram
- Regenerar token en @BotFather si es necesario

### **Problema: Timeout**
- Aumentar timeout en nodo `Execute with Cerebro AI`
- Verificar que el backend esté funcionando: `curl http://localhost:8001/api/agent/status`

### **Problema: Formato incorrecto**
- Verificar que `parse_mode: "Markdown"` esté configurado
- Escapar caracteres especiales: `_`, `*`, `[`, `]`

---

## 📈 MÉTRICAS Y MONITOREO

### **Ver Ejecuciones en n8n**

1. Ve a **Executions** en n8n
2. Filtra por workflow "🧠 Cerebro AI - Telegram Control Hub"
3. Revisa ejecuciones exitosas/fallidas

### **Ver Logs del Backend**

```bash
# Logs del agente
tail -f /var/log/supervisor/backend.out.log | grep "agent"

# Logs de Telegram
tail -f /var/log/telegram_bot.log
```

### **Ver Memoria en MongoDB**

```bash
# Conectar a MongoDB
mongo

# Usar base de datos
use social_media_monetization

# Ver conversaciones
db.conversations.find().limit(5).sort({timestamp: -1})

# Ver memorias
db.agent_memory.find().limit(5).sort({timestamp: -1})
```

---

## 🔗 RECURSOS

- **Workflow File:** `/app/n8n-workflow-cerebro-ai-telegram.json`
- **Documentación Completa:** `/app/CEREBRO_AI_SISTEMA_COMPLETO.md`
- **Backend:** `https://api-switcher.preview.emergentagent.com`
- **n8n Docs:** https://docs.n8n.io

---

## ✅ CHECKLIST DE IMPLEMENTACIÓN

- [ ] n8n instalado y funcionando
- [ ] Bot de Telegram creado con @BotFather
- [ ] Token de Telegram obtenido
- [ ] Workflow importado en n8n
- [ ] Credenciales de Telegram configuradas
- [ ] URLs del backend verificadas
- [ ] Workflow activado
- [ ] Test de `/ayuda` exitoso
- [ ] Test de `/status` exitoso
- [ ] Test de lenguaje natural exitoso
- [ ] Memoria funcionando correctamente

---

## 🎉 RESULTADO FINAL

Con este workflow, tu bot de Telegram estará completamente integrado con el **Cerebro AI**, permitiendo:

✅ **Control por comandos simples** (`/ayuda`, `/status`, `/memoria`)
✅ **Lenguaje natural completo** (cualquier texto)
✅ **18 herramientas disponibles** (productos, análisis, marketing, creatividad)
✅ **Memoria persistente** con RAG
✅ **Respuestas inteligentes** con Claude 3.5 Sonnet
✅ **Ejecución automática** de acciones

**Tu tienda de dropshipping ahora tiene un asistente AI completo controlable desde Telegram** 🚀
