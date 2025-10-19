# 🚨 GUÍA RÁPIDA: ASIGNAR CREDENCIALES EN N8N (3 MINUTOS)

## ⚠️ PROBLEMA
n8n no permite asignar credenciales automáticamente via API. Debes hacerlo manualmente.

---

## ✅ SOLUCIÓN SIMPLE (PASO A PASO CON CAPTURAS VISUALES)

### PASO 1: ACCEDER A N8N (30 segundos)

**1.1** Abre en tu navegador:
```
https://n8n-n8n.pgu12h.easypanel.host
```

**1.2** Login:
```
Email: bricospeed0@gmail.com
Password: Amparo14.18.14
```

---

### PASO 2: ABRIR EL WORKFLOW (30 segundos)

**2.1** En el panel izquierdo, busca:
```
📂 Workflows
```

**2.2** Click en el workflow:
```
🧠 Control AI desde Telegram - Cerebro AI
```

**2.3** Se abrirá el canvas con 18 nodos

---

### PASO 3: ASIGNAR CREDENCIAL (2 MINUTOS)

Tienes que hacer esto **7 VECES** (una vez por cada nodo de Telegram):

#### **NODO 1: 📱 Telegram Trigger**

1. **Click en el nodo** "📱 Telegram Trigger"
2. **En el panel derecho**, busca el dropdown que dice:
   ```
   Credential to connect with: [Selecciona una credencial]
   ```
3. **Click en el dropdown**
4. **Selecciona:** `Telegram Bot Cerebro AI`
5. **Click fuera del nodo** para guardar

#### **NODO 2: 💬 Send Help**
Repite lo mismo:
- Click en "💬 Send Help"
- Credential → "Telegram Bot Cerebro AI"
- Click fuera

#### **NODO 3: 📤 Send Status**
- Click en "📤 Send Status"
- Credential → "Telegram Bot Cerebro AI"
- Click fuera

#### **NODO 4: 📤 Send Memory**
- Click en "📤 Send Memory"
- Credential → "Telegram Bot Cerebro AI"
- Click fuera

#### **NODO 5: ❌ Send Error**
- Click en "❌ Send Error"
- Credential → "Telegram Bot Cerebro AI"
- Click fuera

#### **NODO 6: ⏳ Send Processing**
- Click en "⏳ Send Processing"
- Credential → "Telegram Bot Cerebro AI"
- Click fuera

#### **NODO 7: 📤 Send Result**
- Click en "📤 Send Result"
- Credential → "Telegram Bot Cerebro AI"
- Click fuera

---

### PASO 4: GUARDAR (10 segundos)

**Click en el botón "Save"** (esquina superior derecha)

---

### PASO 5: ACTIVAR (10 segundos)

**Toggle "Inactive" → "Active"**

En la esquina superior derecha verás:
```
[Inactive ⏸️] ← Click aquí
```

Debe cambiar a:
```
[Active ✅]
```

---

## 🎯 VERIFICACIÓN

Una vez activado:

1. **Abre Telegram**
2. **Busca tu bot:** @Rrssnanobanana_bot
3. **Envía:** `/status`

**Debes recibir:**
```
📊 Estado del Cerebro AI

🤖 Agente: ✅ Activo
🔧 Herramientas: 22
💾 Conversaciones: X
🧠 Memorias: X

⚡ Características:
• Memoria persistente: ✅
• RAG habilitado: ✅

Modelo: Perplexity Pro (sonar-pro)
```

---

## 📸 REFERENCIA VISUAL

### Como se ve un nodo SIN credencial:
```
┌─────────────────────────┐
│ 📱 Telegram Trigger     │
│                         │
│ ⚠️ No credentials       │
│                         │
│ Credential: [Select...] │ ← Click aquí
└─────────────────────────┘
```

### Como debe quedar CON credencial:
```
┌─────────────────────────┐
│ 📱 Telegram Trigger     │
│                         │
│ ✅ Telegram Bot Cereb...│
│                         │
│ Credential: [Bot...]    │ ← Ya asignado
└─────────────────────────┘
```

---

## 🚨 ATAJOS RÁPIDOS

### Método Rápido (Si conoces n8n):
1. Login → Workflows
2. Abrir "🧠 Control AI..."
3. Select All (Ctrl+A o Cmd+A)
4. En el panel derecho: Credential → "Telegram Bot Cerebro AI"
5. Save
6. Activate

---

## ❓ TROUBLESHOOTING

### Problema: No veo la credencial "Telegram Bot Cerebro AI"

**Solución:**
1. Ve a Settings (⚙️ abajo izquierda)
2. Click "Credentials"
3. Debes ver: "Telegram Bot Cerebro AI"
4. Si no está, créala manualmente:
   - Click "Add Credential"
   - Busca "Telegram"
   - Name: `Telegram Bot Cerebro AI`
   - Token: `7708509018:AAErAOblRAlC587j1QB4k19PAfDgoiZ3kWk`
   - Save

### Problema: No puedo activar el workflow

**Causa:** Falta asignar algún nodo

**Solución:** Verifica que los 7 nodos tengan ✅ en lugar de ⚠️

---

## ✅ CHECKLIST RÁPIDO

- [ ] Login en n8n
- [ ] Workflow abierto
- [ ] 📱 Telegram Trigger → Credencial asignada
- [ ] 💬 Send Help → Credencial asignada
- [ ] 📤 Send Status → Credencial asignada
- [ ] 📤 Send Memory → Credencial asignada
- [ ] ❌ Send Error → Credencial asignada
- [ ] ⏳ Send Processing → Credencial asignada
- [ ] 📤 Send Result → Credencial asignada
- [ ] Workflow guardado (Save)
- [ ] Workflow activado (Active ✅)
- [ ] Test: Telegram /status funciona

---

## 🎉 UNA VEZ HECHO:

✅ El bot responderá en Telegram
✅ Todos los comandos funcionarán
✅ Perplexity Pro procesará comandos
✅ 22 herramientas disponibles
✅ Memoria persistente con RAG

**Total: 3 minutos de trabajo manual**

---

## 📞 NECESITAS AYUDA?

Escribe "no puedo activarlo" y te ayudo a encontrar otra solución.
