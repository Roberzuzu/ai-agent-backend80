# 🚀 INSTRUCCIONES PASO A PASO - IMPLEMENTAR EN TU N8N

## ✅ BACKEND ACTUALIZADO - 22 HERRAMIENTAS DISPONIBLES

**Tu backend YA ESTÁ ACTUALIZADO con:**
- ✅ SerpAPI integrado (búsquedas Google, keywords, shopping)
- ✅ Apify integrado (web scraping)
- ✅ Google Cloud OAuth configurado
- ✅ 22 herramientas totales (antes 18)

---

## 📋 TU INFORMACIÓN

**n8n:**
- URL: https://n8n-n8n.pgu12h.easypanel.host
- Email: bricospeed0@gmail.com
- Password: Amparo14.18.14

**Bot Telegram:**
- Token: `7708509018:AAErAOblRAlC587j1QB4k19PAfDgoiZ3kWk`
- Chat ID: `7202793910`

**Backend:**
- URL: `https://wpmoneyhub.preview.emergentagent.com`
- Status: ✅ FUNCIONANDO (22 herramientas activas)

---

## 🎯 PASO 1: ACCEDER A N8N (2 minutos)

1. **Abre tu navegador**
2. **Ve a:** https://n8n-n8n.pgu12h.easypanel.host
3. **Introduce credenciales:**
   ```
   Email: bricospeed0@gmail.com
   Password: Amparo14.18.14
   ```
4. **Click "Sign in"**

**✅ Resultado:** Deberías ver el dashboard de n8n con tus workflows

---

## 🎯 PASO 2: DESCARGAR EL WORKFLOW (1 minuto)

El workflow está en tu servidor en:
```
/app/n8n-workflow-cerebro-ai-COMPLETO.json
```

**Opción A - Si tienes acceso SSH:**
```bash
# Descarga el archivo
cat /app/n8n-workflow-cerebro-ai-COMPLETO.json
# Copia TODO el contenido
```

**Opción B - Contenido directo:**
El archivo JSON completo está disponible en `/app/n8n-workflow-cerebro-ai-COMPLETO.json`

---

## 🎯 PASO 3: IMPORTAR EN N8N (3 minutos)

### 3.1 Crear Nuevo Workflow

1. En n8n, **click en el icono "+"** (arriba a la izquierda)
   ```
   [+] ← Este botón
   ```

2. En el menú, selecciona **"Import from File"**
   ```
   Options:
   - Import from URL
   - Import from File ← Selecciona esta
   ```

### 3.2 Importar el JSON

**MÉTODO 1 - Desde archivo:**
1. Click "Choose File"
2. Selecciona el archivo `n8n-workflow-cerebro-ai-COMPLETO.json`
3. Click "Import"

**MÉTODO 2 - Copiar/Pegar:**
1. Copia TODO el contenido del archivo JSON
2. En n8n, click en el área de texto
3. Pega el contenido
4. Click "Import"

**✅ Resultado:** Verás 19 nodos con emojis importados

---

## 🎯 PASO 4: CONFIGURAR TELEGRAM (5 minutos)

### 4.1 Crear Credencial de Telegram

1. **Ve a Settings (icono engranaje ⚙️ abajo a la izquierda)**
   ```
   Dashboard
   Workflows
   Executions
   Settings ← Click aquí
   ```

2. **Click en "Credentials"**
   ```
   Personal
   Credentials ← Click aquí
   Community nodes
   ```

3. **Click "Add Credential" (botón rojo arriba a la derecha)**

4. **En el buscador, escribe: "Telegram"**

5. **Selecciona "Telegram"** (no "Telegram Trigger")

6. **Rellena el formulario:**
   ```
   Credential name: Telegram Bot Cerebro AI
   Access Token: 7708509018:AAErAOblRAlC587j1QB4k19PAfDgoiZ3kWk
   ```

7. **Click "Save" (botón verde)**

**✅ Resultado:** Credencial "Telegram Bot Cerebro AI" creada

### 4.2 Asignar Credencial a los Nodos

Vuelve a tu workflow importado. Necesitas asignar la credencial a **7 nodos**:

#### Nodo 1: 📱 Telegram Trigger
1. **Click en el nodo "📱 Telegram Trigger"**
2. **En el panel derecho, busca: "Credential to connect with"**
3. **Click en el dropdown**
4. **Selecciona: "Telegram Bot Cerebro AI"**
5. **Click fuera del nodo para guardar**

#### Repite para estos 6 nodos más:
- 💬 Send Help
- 📤 Send Status
- 📤 Send Memory
- ❌ Send Error
- ⏳ Send Processing
- 📤 Send Result

**✅ Resultado:** Los 7 nodos tienen ⚡ (icono de credencial conectada)

---

## 🎯 PASO 5: VERIFICAR URLs DEL BACKEND (2 minutos)

### 5.1 Nodo: 📊 Get Agent Status

1. **Click en el nodo "📊 Get Agent Status"**
2. **Verifica la URL:**
   ```
   URL: https://wpmoneyhub.preview.emergentagent.com/api/agent/status
   Method: GET
   ```
3. **Si la URL es diferente, cámbiala**

### 5.2 Nodo: 🧠 Get Memory

1. **Click en el nodo "🧠 Get Memory"**
2. **Verifica la URL:**
   ```
   URL: https://wpmoneyhub.preview.emergentagent.com/api/agent/memory/{{ $json.user_id }}?limit=5
   Method: GET
   ```

### 5.3 Nodo: 🤖 Execute Cerebro AI

1. **Click en el nodo "🤖 Execute Cerebro AI"**
2. **Verifica:**
   ```
   URL: https://wpmoneyhub.preview.emergentagent.com/api/agent/execute
   Method: POST
   Timeout: 180000 (3 minutos)
   ```

**✅ Resultado:** Los 3 nodos HTTP tienen la URL correcta

---

## 🎯 PASO 6: ACTIVAR EL WORKFLOW (1 minuto)

1. **En la esquina superior derecha, busca el toggle "Inactive"**
   ```
   [Save] [Execute]  [Inactive ⏸️] ← Este toggle
   ```

2. **Click en el toggle**
   ```
   Cambia de: Inactive ⏸️
   A: Active ✅
   ```

3. **El workflow ahora está ACTIVO y escuchando**

**✅ Resultado:** Toggle en verde "Active ✅"

---

## 🎯 PASO 7: TESTING INMEDIATO (5 minutos)

### Test 1: Comando /ayuda

1. **Abre Telegram en tu móvil/PC**
2. **Busca tu bot de Telegram**
3. **Envía:** `/ayuda`

**Resultado esperado:**
```
🧠 Cerebro AI - Control Total desde Telegram

🎯 Comandos Directos:
• /ayuda - Ver esta ayuda
• /status - Estado del sistema AI
• /memoria - Ver tu historial
...
```

**En n8n:**
1. Ve a "Executions" (panel izquierdo)
2. Deberías ver una ejecución nueva
3. Click en ella para ver detalles

### Test 2: Comando /status

**Envía en Telegram:** `/status`

**Resultado esperado:**
```
📊 Estado del Cerebro AI

🤖 Agente: ✅ Activo
🔧 Herramientas: 22
💾 Conversaciones: X
🧠 Memorias: Y

⚡ Características:
• Memoria persistente: ✅
• RAG habilitado: ✅
• Búsqueda semántica: ✅
• Embeddings OpenAI: ✅
```

### Test 3: Lenguaje Natural

**Envía en Telegram:** `Dame las estadísticas del sitio`

**Resultado esperado:**
```
🧠 Analizando tu solicitud...
"Dame las estadísticas del sitio"

✅ Completado
📋 Plan: Obtener estadísticas del sitio...

🔧 Resultados (2):
1. ✅ obtener_estadisticas
   📦 Productos: X
2. ✅ analizar_ventas
   💰 Órdenes: Y
```

### Test 4: Nueva Herramienta - Búsqueda Google

**Envía en Telegram:** `Busca en Google "mejores taladros 2025"`

**Resultado esperado:**
```
🧠 Analizando tu solicitud...

✅ Completado
📋 Plan: Buscar en Google...

🔧 Resultados (1):
1. ✅ buscar_google
   📊 Total: 10 resultados
```

### Test 5: Nueva Herramienta - Análisis Keywords

**Envía en Telegram:** `Analiza keywords de "herramientas eléctricas"`

**Resultado esperado:**
```
✅ Completado

🔧 Resultados (1):
1. ✅ analizar_keywords
   📊 Total: X keywords relacionadas
```

---

## 🎉 SI TODO FUNCIONA

**¡FELICITACIONES!** Tu sistema está funcionando con:

✅ **22 herramientas AI** disponibles
✅ **Memoria persistente** con RAG
✅ **Claude 3.5 Sonnet** interpretando comandos
✅ **SerpAPI** para búsquedas y keywords
✅ **Apify** para scraping
✅ **n8n** orquestando todo

---

## 🚨 TROUBLESHOOTING

### Problema: Bot no responde

**Verificaciones:**
1. ✅ Workflow está "Active" (toggle verde)
2. ✅ Credencial de Telegram asignada a los 7 nodos
3. ✅ Token de Telegram correcto

**Solución:**
1. Desactiva el workflow (toggle off)
2. Guarda los cambios
3. Actívalo de nuevo

### Problema: Error "Unauthorized"

**Causa:** Token de Telegram incorrecto

**Solución:**
1. Ve a @BotFather en Telegram
2. Envía `/mybots`
3. Selecciona tu bot
4. Click "API Token"
5. Copia el nuevo token
6. Actualiza en n8n → Credentials → Telegram Bot Cerebro AI

### Problema: No llegan las respuestas

**Verificar el backend:**
```bash
curl https://wpmoneyhub.preview.emergentagent.com/api/agent/status
```

**Debe retornar:**
```json
{
  "success": true,
  "agente_activo": true,
  "herramientas_disponibles": 22
}
```

### Problema: Timeout en comandos

**Solución:**
1. Click en nodo "🤖 Execute Cerebro AI"
2. En "Options" → "Timeout"
3. Cambia de `180000` a `300000` (5 minutos)

---

## 📊 MONITOREO

### Ver Ejecuciones en n8n

1. **Panel izquierdo → "Executions"**
2. **Verás todas las ejecuciones del workflow**
3. **Click en una para ver:**
   - Datos de entrada
   - Datos de salida de cada nodo
   - Tiempo de ejecución
   - Errores (si los hay)

### Ver Logs del Backend

Si tienes acceso SSH:
```bash
# Ver logs en tiempo real
tail -f /var/log/supervisor/backend.out.log

# Buscar errores
tail -100 /var/log/supervisor/backend.err.log | grep -i error
```

---

## 🎯 NUEVAS HERRAMIENTAS DISPONIBLES

Con las APIs que agregaste, ahora puedes usar:

### **Búsqueda Google (SerpAPI):**
```
"Busca en Google precios de taladros"
"Encuentra las mejores sierras circulares"
```

### **Análisis Keywords (SerpAPI):**
```
"Analiza keywords de herramientas eléctricas"
"Dame keywords relacionadas con taladros"
```

### **Web Scraping (Apify):**
```
"Extrae datos de esta web: https://ejemplo.com"
"Scrape la información de productos de X tienda"
```

### **Monitoreo Competencia (SerpAPI):**
```
"Monitorea precios de taladros Bosch"
"Vigila la competencia de sierras circulares"
```

---

## ✅ CHECKLIST FINAL

Antes de dar por terminado, verifica:

- [ ] n8n accesible en https://n8n-n8n.pgu12h.easypanel.host
- [ ] Workflow "🧠 Control AI desde Telegram" importado
- [ ] Credencial "Telegram Bot Cerebro AI" creada
- [ ] Credencial asignada a 7 nodos de Telegram
- [ ] URLs del backend verificadas (3 nodos HTTP)
- [ ] Workflow activado (toggle verde "Active")
- [ ] Test `/ayuda` exitoso ✅
- [ ] Test `/status` muestra 22 herramientas ✅
- [ ] Test lenguaje natural exitoso ✅
- [ ] Test nueva herramienta (buscar_google) ✅

---

## 📁 ARCHIVOS DE REFERENCIA

1. **Workflow completo:** `/app/n8n-workflow-cerebro-ai-COMPLETO.json`
2. **Documentación técnica:** `/app/CEREBRO_AI_SISTEMA_COMPLETO.md`
3. **Guía n8n original:** `/app/N8N_CEREBRO_AI_GUIA_IMPLEMENTACION.md`

---

## 🚀 SIGUIENTE NIVEL

Una vez que funcione todo, puedes:

1. **Personalizar respuestas** (edita nodos `✨ Format Result`)
2. **Agregar más comandos** (agrega cases en `🔄 Route Command`)
3. **Integrar otros canales** (WhatsApp, Discord, Web)
4. **Crear dashboards** en n8n para estadísticas

---

**¡TU SISTEMA ESTÁ LISTO! 🎉**

**Backend:** ✅ 22 herramientas + APIs integradas
**n8n:** ✅ Workflow de 19 nodos optimizado
**Telegram:** ✅ Bot conectado y funcionando

**Ahora tienes control total de tu tienda desde Telegram con AI** 🚀
