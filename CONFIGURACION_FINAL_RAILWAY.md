# 🎯 Configuración Final de Railway - 3 Minutos

## Tu URL Final (cuando funcione):
```
https://ai-agent-backend-production-9d42.up.railway.app
```

---

## ✅ HAZ ESTO AHORA EN RAILWAY:

### PASO 1: Configurar Variables

1. **Railway Dashboard** → Tu servicio
2. Tab **"Variables"**
3. Click **"Raw Editor"** (arriba a la derecha)
4. **BORRA TODO** lo que esté ahí
5. **COPIA Y PEGA** esto:

```env
MONGO_URL=mongodb+srv://bricospeed0_db_user:7uCqmOCzZsKBT3Uk@cluster0.5uxiix8.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0
DB_NAME=ai_agent_db
SECRET_KEY=09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7
CORS_ORIGINS=*
OPENAI_API_KEY=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
PERPLEXITY_API_KEY=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
STRIPE_API_KEY=sk_test_51RLguuEIV37qlnK9Fm2mejxSRsSVtfLWRjDbLwTwuZ6vL2XNkjQ0FPWQMhq6LNqbOQ5qsJbhuGzA2tvrCjHf1mmT00AXLet9SG
STRIPE_PUBLISHABLE_KEY=pk_test_51RLguuEIV37qlnK9dfwvGn6IN08Fv1tSKRXtrVv1bwEdiLNU4yQ1KzVOn1Jl0QgyAe96l4S6npdTFE9Bni9jDOI500i9CXuLfQ
TELEGRAM_BOT_TOKEN=7708509018:AAErAOblRAlC587j1QB4k19PAfDgoiZ3kWk
TELEGRAM_CHAT_ID=7202793910
WORDPRESS_URL=https://herramientasyaccesorios.store
WC_CONSUMER_KEY=ck_4f50637d85ec404fff441fceb7b113b5050431ea
WC_CONSUMER_SECRET=cs_e59ef18ea20d80ffdf835803ad2fdd834a4ba19f
FAL_API_KEY=railway-port-config:228b46f927a226c270ece128bfeb95db
PORT=$PORT
PYTHONUNBUFFERED=1
```

6. Click **"Update Variables"** o **"Save"**

---

### PASO 2: Configurar Settings

1. Tab **"Settings"**
2. Verifica:

**A) Builder:**
```
Builder: NIXPACKS  ✅
```

**B) Root Directory:**
```
Root Directory: backend  ✅ (sin barra /)
```

**C) Start Command:** (si hay)
```
Déjalo VACÍO o pon:
uvicorn server:app --host 0.0.0.0 --port $PORT
```

---

### PASO 3: Deploy

1. Tab **"Deployments"**
2. Click **"Deploy"** (arriba derecha)
3. **ESPERA 3-5 minutos**

---

## ✅ VERIFICAR QUE FUNCIONA

Cuando termine el deployment:

### Test 1: Abre en tu navegador
```
https://ai-agent-backend-production-9d42.up.railway.app/api/health
```

**Debe mostrar:**
```json
{
  "status": "healthy",
  "database": "connected"
}
```

✅ **Si ves eso = ¡FUNCIONA!**

---

## 🔌 CONFIGURAR WORDPRESS

Una vez que `/api/health` funcione:

1. **WordPress Admin**
2. Busca tu plugin de **AI Chat** o como se llame
3. **Backend URL:** Pon esto:
   ```
   https://ai-agent-backend-production-9d42.up.railway.app
   ```
   ⚠️ **SIN** `/api` al final

4. Click **"Guardar"**
5. Click **"Probar Conexión"**

✅ **Debe decir: "Backend conectado correctamente"**

---

## 🎉 ¡LISTO!

Tu app funcionará **100% autónoma** sin Emergent:

```
WordPress → Backend Railway → MongoDB Atlas → APIs
```

Todo funcionando 24/7 ✅

---

## 🆘 Si Falla

Después de hacer el deploy, si sigue dando error:

1. Tab **"Deployments"**
2. Click en el deployment
3. **Copia las últimas 30 líneas de los logs**
4. Pégalas aquí y te ayudo

---

**Tiempo total: 3-5 minutos** ⏱️

**¡Hazlo ahora y me dices cómo te fue!** 🚀
