# 🚀 GUÍA DE IMPLEMENTACIÓN EN TU N8N EXISTENTE

## 📋 INFORMACIÓN DE TU SISTEMA

**n8n URL:** https://n8n-n8n.pgu12h.easypanel.host
**Email:** bricospeed0@gmail.com
**Password:** Amparo14.18.14

---

## ⚡ PASOS DE INSTALACIÓN (5 minutos)

### **PASO 1: Acceder a tu n8n**

1. Abre: https://n8n-n8n.pgu12h.easypanel.host
2. Login con:
   - Email: `bricospeed0@gmail.com`
   - Password: `Amparo14.18.14`

---

### **PASO 2: Importar el Workflow**

1. En n8n, click en **"+"** (arriba a la izquierda)
2. Selecciona **"Import from File"** o **"Import from URL"**
3. **Opción A - Desde archivo:**
   - Descarga: `/app/n8n-workflow-cerebro-ai-COMPLETO.json`
   - Arrastra el archivo a n8n
   
4. **Opción B - Desde contenido:**
   - Copia TODO el contenido del archivo JSON
   - Pégalo en el campo de importación

5. Click **"Import"**

---

### **PASO 3: Configurar Credenciales de Telegram**

#### **3.1 Crear/Usar tu Bot de Telegram:**

Si NO tienes bot aún:
1. Abre Telegram y busca **@BotFather**
2. Envía: `/newbot`
3. Sigue las instrucciones (nombre y username)
4. **COPIA EL TOKEN** que te da (ejemplo: `7708509018:AAErAOblRAlC587j1QB4k19PAfDgoiZ3kWk`)

Si YA tienes bot:
- Usa el token que ya tienes
- Token actual: `7708509018:AAErAOblRAlC587j1QB4k19PAfDgoiZ3kWk`

#### **3.2 Configurar en n8n:**

1. En n8n, ve a **Settings** (⚙️) → **Credentials**
2. Click **"Add Credential"**
3. Busca y selecciona **"Telegram"**
4. Rellena:
   - **Credential name:** `Telegram Bot Cerebro AI`
   - **Access Token:** Pega tu token del bot
5. Click **"Save"**

#### **3.3 Asignar Credencial a los Nodos:**

Estos nodos necesitan la credencial (click en cada uno y selecciona la credencial):

1. `📱 Telegram Trigger`
2. `💬 Send Help`
3. `📤 Send Status`
4. `📤 Send Memory`
5. `❌ Send Error`
6. `⏳ Send Processing`
7. `📤 Send Result`

**Asignar credencial:**
- Click en el nodo
- En "Credential to connect with"
- Selecciona: `Telegram Bot Cerebro AI`
- Click fuera del nodo para guardar

---

### **PASO 4: Verificar URLs del Backend**

Los siguientes nodos tienen URLs del backend, verifica que sean correctas:

#### Nodo: `📊 Get Agent Status`
```
URL: https://railway-port-config.preview.emergentagent.com/api/agent/status
Method: GET
```

#### Nodo: `🧠 Get Memory`
```
URL: https://railway-port-config.preview.emergentagent.com/api/agent/memory/{{ $json.user_id }}?limit=5
Method: GET
```

#### Nodo: `🤖 Execute Cerebro AI`
```
URL: https://railway-port-config.preview.emergentagent.com/api/agent/execute
Method: POST
Body: JSON
Timeout: 180000ms (3 minutos)
```

**Si tu backend está en otra URL, cambia el dominio en estos 3 nodos.**

---

### **PASO 5: Activar el Workflow**

1. En la esquina superior derecha, hay un toggle **"Inactive"/"Active"**
2. Click para cambiar a **"Active"**
3. El workflow ahora está escuchando mensajes de Telegram ✅

---

## 🧪 TESTING INMEDIATO

### **Test 1: Comando de Ayuda**
```
Abre Telegram → Tu bot
Envía: /ayuda
```
**Resultado esperado:**
```
🧠 Cerebro AI - Control Total desde Telegram

🎯 Comandos Directos:
• /ayuda - Ver esta ayuda
• /status - Estado del sistema AI
• /memoria - Ver tu historial
...
```

### **Test 2: Estado del Sistema**
```
Envía: /status
```
**Resultado esperado:**
```
📊 Estado del Cerebro AI

🤖 Agente: ✅ Activo
🔧 Herramientas: 18
💾 Conversaciones: 0
🧠 Memorias: 0
...
```

### **Test 3: Lenguaje Natural**
```
Envía: Dame las estadísticas del sitio
```
**Resultado esperado:**
```
🧠 Analizando tu solicitud...
"Dame las estadísticas del sitio"

✅ Completado
📋 Plan: Obtener estadísticas...
🔧 Resultados (2):
1. ✅ obtener_estadisticas
2. ✅ analizar_ventas
```

### **Test 4: Ver Memoria**
```
Envía: /memoria
```
**Resultado esperado:**
```
📝 Tus últimas 1 memorias

1. Dame las estadísticas del sitio
   📅 15 ene a las 14:30
```

---

## 🎯 COMANDOS DISPONIBLES

### **Comandos Directos:**
- `/ayuda` o `/start` - Ayuda completa
- `/status` - Estado del Cerebro AI
- `/memoria` - Ver últimas 5 memorias
- `/procesar [ID]` - Procesar producto (ej: `/procesar 4146`)

### **Lenguaje Natural (18 herramientas):**

**📦 Productos:**
```
"Busca 10 herramientas eléctricas tendencia"
"Procesa el producto 4146"
"Actualiza el stock del producto 100 a 50"
"Crea 3 productos nuevos de sierras"
```

**📊 Análisis:**
```
"Dame las estadísticas del sitio"
"Analiza las ventas del último mes"
"Analiza la competencia de taladros"
```

**🎨 Marketing:**
```
"Crea un cupón del 20% para sierras"
"Genera contenido para blog sobre herramientas"
```

**🖼️ Creatividad:**
```
"Genera 2 imágenes de sierra circular profesional"
```

---

## 🔧 ESTRUCTURA DEL WORKFLOW

```
📱 Telegram → 🔀 ¿Es Comando?
                    ↓
        ┌───────────┴───────────┐
        │                       │
    Comando (/)          Lenguaje Natural
        ↓                       ↓
    🔄 Route               ⏳ Processing
    ├─ /ayuda                  ↓
    ├─ /status          🤖 Execute AI
    ├─ /memoria                ↓
    └─ /procesar         ✨ Format Result
        ↓                       ↓
    📤 Telegram           📤 Telegram
```

---

## 🎨 CARACTERÍSTICAS DEL WORKFLOW

✅ **19 Nodos optimizados** con emojis y nombres claros
✅ **Detección automática** de comandos vs lenguaje natural
✅ **Validación de errores** (ejemplo: `/procesar` sin ID)
✅ **Formato Markdown** para respuestas bonitas
✅ **Timeout de 3 minutos** para comandos largos
✅ **Feedback instantáneo** ("Analizando...")
✅ **Resultados estructurados** con emojis
✅ **Memoria persistente** con RAG

---

## 📊 MONITOREO EN N8N

### **Ver Ejecuciones:**
1. En n8n, ve a **"Executions"** (panel izquierdo)
2. Verás todas las ejecuciones del workflow
3. Click en una para ver detalles paso a paso

### **Ver Logs de un Nodo:**
1. Click derecho en cualquier nodo
2. Selecciona **"View Executions"**
3. Ve los datos de entrada/salida

### **Probar Manualmente:**
1. Click en **"Test Workflow"** (arriba)
2. Haz un cambio en un nodo
3. Click **"Execute Node"** para probar solo ese nodo

---

## 🚨 TROUBLESHOOTING

### **Problema: Bot no responde**

**Solución 1:** Verificar que el workflow esté **Active**
- Toggle en esquina superior derecha debe estar en verde

**Solución 2:** Verificar credenciales de Telegram
- Settings → Credentials → Telegram Bot Cerebro AI
- Verificar que el token sea correcto

**Solución 3:** Verificar webhook
- En Telegram, envía cualquier mensaje al bot
- Ve a Executions en n8n
- Si no aparece nada, regenera el webhook:
  1. Desactiva el workflow
  2. Actívalo de nuevo

### **Problema: Error 401 Unauthorized**

**Causa:** Token de Telegram incorrecto

**Solución:**
1. Ve a @BotFather en Telegram
2. Envía: `/mybots`
3. Selecciona tu bot
4. Click en "API Token"
5. Copia el token
6. Actualiza en n8n → Settings → Credentials

### **Problema: Timeout en comandos largos**

**Causa:** Comando tarda más de 3 minutos

**Solución:**
1. Abre el nodo `🤖 Execute Cerebro AI`
2. En "Options" → "Timeout"
3. Cambia de `180000` a `300000` (5 minutos)
4. Guarda

### **Problema: Backend no responde**

**Verificar estado del backend:**
```bash
curl https://railway-port-config.preview.emergentagent.com/api/agent/status
```

**Debe retornar:**
```json
{
  "success": true,
  "agente_activo": true,
  "herramientas_disponibles": 18
}
```

Si no responde:
1. Verificar que el backend esté corriendo
2. Verificar la URL en los nodos HTTP Request

### **Problema: Formato de respuesta roto**

**Causa:** Caracteres especiales en Markdown

**Solución:**
- En los nodos de formato (`✨ Format Memory`, `✨ Format Result`)
- Escapar caracteres especiales: `_`, `*`, `[`, `]`, `(`, `)`
- Ejemplo: `text.replace(/_/g, '\\_')`

---

## 📈 MÉTRICAS Y ANÁLISIS

### **Ver Conversaciones en MongoDB:**
```bash
# Conectar a MongoDB
mongo

# Usar base de datos
use social_media_monetization

# Ver últimas 10 conversaciones
db.conversations.find().sort({timestamp: -1}).limit(10)

# Contar conversaciones por usuario
db.conversations.aggregate([
  {$group: {_id: "$user_id", total: {$sum: 1}}},
  {$sort: {total: -1}}
])
```

### **Ver Memorias con Embeddings:**
```bash
# Ver memorias con búsqueda semántica
db.agent_memory.find().sort({timestamp: -1}).limit(5)

# Contar memorias totales
db.agent_memory.count()
```

---

## 🎯 PRÓXIMOS PASOS

Una vez que funcione todo:

### **1. Personalizar Respuestas**
- Edita los nodos `✨ Format Result` y `✨ Format Memory`
- Cambia los textos, emojis, formato

### **2. Agregar Comandos Nuevos**
- Agrega nuevo case en `🔄 Route Command`
- Crea nodos para el nuevo comando
- Conecta al flujo

### **3. Integrar más Canales**
- Duplica el workflow
- Cambia "Telegram Trigger" por "WhatsApp Trigger" o "Discord Trigger"

### **4. Monitoreo Avanzado**
- Configura alertas en n8n
- Envía notificaciones si hay errores

---

## ✅ CHECKLIST FINAL

Antes de dar por terminado:

- [ ] n8n accesible en https://n8n-n8n.pgu12h.easypanel.host
- [ ] Workflow importado correctamente
- [ ] Bot de Telegram creado/existente
- [ ] Token de Telegram configurado
- [ ] Credencial asignada a todos los nodos Telegram (7 nodos)
- [ ] URLs del backend verificadas (3 nodos HTTP)
- [ ] Workflow activado (toggle verde)
- [ ] Test `/ayuda` exitoso ✅
- [ ] Test `/status` exitoso ✅
- [ ] Test lenguaje natural exitoso ✅
- [ ] Test `/memoria` exitoso ✅

---

## 🎉 SISTEMA COMPLETO FUNCIONANDO

Con esto tendrás:

✅ **Bot de Telegram** conectado a Cerebro AI
✅ **18 herramientas** disponibles por lenguaje natural
✅ **Memoria persistente** con RAG
✅ **Claude 3.5 Sonnet** interpretando comandos
✅ **WooCommerce + WordPress** integrados
✅ **n8n** orquestando todo

**Tu tienda ahora tiene un asistente AI completo controlable desde Telegram** 🚀

---

## 📞 SOPORTE

Si tienes algún problema:
1. Revisa la sección Troubleshooting
2. Ve a Executions en n8n para ver logs
3. Verifica que el backend esté corriendo
4. Prueba los endpoints directamente con curl

**Archivo del workflow:** `/app/n8n-workflow-cerebro-ai-COMPLETO.json`
**Documentación completa:** `/app/CEREBRO_AI_SISTEMA_COMPLETO.md`
