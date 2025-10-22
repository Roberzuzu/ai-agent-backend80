# 🚀 Instalación Rápida - Chat Completo con Upload de Archivos

## 🎯 Objetivo

Tener un chat funcional en tu WordPress donde puedas:
- 💬 Comunicarte con el AI Agent
- 📎 Enviar archivos de cualquier tipo
- 🖼️ Enviar imágenes
- 🤖 Usar Perplexity + OpenAI
- 🛠️ Acceso a 22+ herramientas

---

## 📋 Requisitos

- ✅ Servidor con acceso SSH
- ✅ WordPress funcionando
- ✅ Python 3.10+
- ✅ Node.js 18+
- ✅ MongoDB (local o Atlas)
- ✅ API Keys (OpenAI o Perplexity)

---

## ⚡ Instalación en 7 Pasos

### Paso 1: Conectar a Tu Servidor

```bash
ssh productos@herramientasyaccesorios.store
# Contraseña: oFnXqP3(EITAWfd%rUzIkW%i
```

---

### Paso 2: Transferir Archivos

**Desde el servidor donde está /app:**

```bash
# Transferir paquete standalone
scp /app/miapp-standalone-20251022-142042.zip productos@herramientasyaccesorios.store:~/

# Transferir script de instalación
scp /app/install-herramientas.sh productos@herramientasyaccesorios.store:~/

# Transferir guía
scp /app/DEPLOYMENT_HERRAMIENTAS.md productos@herramientasyaccesorios.store:~/
```

**O usa el servidor HTTP temporal:**

```bash
# En el servidor con /app
cd /app
./serve_download.sh

# Luego desde tu servidor de producción:
cd ~
wget http://servidor-origen:8080/miapp-standalone-20251022-142042.zip
wget http://servidor-origen:8080/install-herramientas.sh
chmod +x install-herramientas.sh
```

---

### Paso 3: Descomprimir y Preparar

```bash
cd ~
unzip miapp-standalone-20251022-142042.zip
cd miapp-standalone-20251022-142042
```

---

### Paso 4: Ejecutar Instalación Automática

```bash
# Copiar script de instalación si no está
cp ~/install-herramientas.sh .

# Ejecutar instalador
./install-herramientas.sh
```

**Esto instalará:**
- Python dependencies
- Entorno virtual
- Servicios systemd
- Configuraciones base

---

### Paso 5: Configurar Variables de Entorno

```bash
cd ~/miapp-standalone-20251022-142042/backend
nano .env
```

**Configuración MÍNIMA necesaria:**

```bash
# ============================================
# MONGODB (Obligatorio)
# ============================================

# Opción A: MongoDB Atlas (Recomendado - GRATIS)
# 1. Ve a https://mongodb.com/cloud/atlas
# 2. Crea cuenta y cluster gratis
# 3. Copia connection string
MONGO_URL=mongodb+srv://usuario:password@cluster.mongodb.net/herramientas

# Opción B: MongoDB Local
# MONGO_URL=mongodb://localhost:27017

DB_NAME=herramientas_woocommerce

# ============================================
# AI PROVIDER (Obligatorio - Al menos UNO)
# ============================================

# Opción A: Perplexity (Recomendado)
PERPLEXITY_API_KEY=pplx-tu-key-aqui

# Opción B: OpenAI
OPENAI_API_KEY=sk-proj-tu-key-aqui

# ============================================
# WOOCOMMERCE (Para integración con tu tienda)
# ============================================

WC_URL=https://herramientasyaccesorios.store/wp-json/wc/v3
WC_KEY=ck_tu_consumer_key_aqui
WC_SECRET=cs_tu_consumer_secret_aqui

# Para obtener WC_KEY y WC_SECRET:
# WordPress Admin → WooCommerce → Settings → Advanced → REST API
# Click "Add key" → Permissions: Read/Write → Generate

# ============================================
# WORDPRESS (Para publicar contenido)
# ============================================

WP_URL=https://herramientasyaccesorios.store/wp-json/wp/v2
WP_USER=productos@herramientasyaccesorios.store
WP_PASS=oFnXqP3(EITAWfd%rUzIkW%i

# ============================================
# TELEGRAM BOT (Opcional)
# ============================================

TELEGRAM_BOT_TOKEN=tu-token-de-botfather
TELEGRAM_CHAT_ID=tu-chat-id

# ============================================
# SEGURIDAD (Auto-generado)
# ============================================

SECRET_KEY=auto-generado-por-instalador

# ============================================
# URLS
# ============================================

BACKEND_URL=http://localhost:8001
```

**Guardar**: Ctrl+O → Enter → Ctrl+X

---

### Paso 6: Configurar Frontend

```bash
cd ~/miapp-standalone-20251022-142042/frontend
nano .env
```

**Contenido:**

```bash
REACT_APP_BACKEND_URL=http://herramientasyaccesorios.store:8001/api
```

**Guardar**: Ctrl+O → Enter → Ctrl+X

---

### Paso 7: Iniciar Servicios

```bash
# Iniciar backend
sudo systemctl start herramientas-backend

# Iniciar telegram bot (opcional)
sudo systemctl start herramientas-telegram

# Verificar que están corriendo
sudo systemctl status herramientas-backend

# Ver logs en tiempo real
sudo journalctl -u herramientas-backend -f
```

**Presiona Ctrl+C para salir de los logs**

---

## 🧪 Verificar Instalación

### Test 1: Backend Funciona

```bash
curl http://localhost:8001/api/health
```

**Debe responder:**
```json
{"status":"ok"}
```

### Test 2: Acceder desde Navegador

Abre en tu navegador:
```
http://herramientasyaccesorios.store:8001/docs
```

Deberías ver la documentación de la API.

---

## 🎨 Iniciar Frontend (React)

### Opción A: Desarrollo (Para Probar)

```bash
cd ~/miapp-standalone-20251022-142042/frontend

# Instalar dependencias
npm install --legacy-peer-deps

# Iniciar
npm start
```

Accede a: `http://herramientasyaccesorios.store:3000`

### Opción B: Producción (Build)

```bash
cd ~/miapp-standalone-20251022-142042/frontend

# Build
npm run build

# Los archivos estarán en: frontend/build/
```

Luego configura Nginx para servir estos archivos.

---

## 🔌 Configurar Plugin WordPress

### 1. Instalar Plugin Chat

1. WordPress Admin → **Plugins → Añadir nuevo → Subir**
2. Sube: `/app/ai-chat-admin-only.zip`
3. **Instalar** y **Activar**

### 2. Configurar URLs

1. Ve a: **AI Chat Admin → Settings**
2. Configurar:
   ```
   Backend URL: http://herramientasyaccesorios.store:8001
   Frontend URL: http://herramientasyaccesorios.store:3000
   ```
3. ✅ Marcar "Mostrar Widget"
4. ✅ Marcar "Solo Administrador"
5. **Guardar Configuración**

### 3. Probar Conexión

1. Click botón **"🔌 Probar Backend"**
2. Debe mostrar: "✅ Backend conectado correctamente!"

### 4. Ver Widget

1. Visita cualquier página de tu tienda (logueado como admin)
2. Busca botón morado flotante abajo derecha
3. Tiene texto "ADMIN" debajo
4. Click para abrir chat

---

## 💡 Funcionalidades del Chat

Una vez funcionando, podrás:

### 💬 Chat con AI
- Escribir mensajes
- Recibir respuestas inteligentes
- Conversaciones contextuales

### 📎 Enviar Archivos
- PDFs
- Documentos Word/Excel
- Archivos ZIP
- Cualquier tipo de archivo

### 🖼️ Enviar Imágenes
- Fotos de productos
- Screenshots
- Imágenes para analizar
- El AI puede "ver" las imágenes

### 🛠️ Herramientas Disponibles
1. Gestión de productos WooCommerce
2. Análisis de ventas
3. Búsqueda en internet
4. Generación de contenido
5. Análisis de imágenes
6. Procesamiento de documentos
7. Y 16+ más herramientas

---

## 🔧 Comandos Útiles

### Ver Logs

```bash
# Backend
sudo journalctl -u herramientas-backend -f

# Telegram Bot
sudo journalctl -u herramientas-telegram -f

# Ver últimas 50 líneas
sudo journalctl -u herramientas-backend -n 50
```

### Reiniciar Servicios

```bash
sudo systemctl restart herramientas-backend
sudo systemctl restart herramientas-telegram
```

### Ver Estado

```bash
sudo systemctl status herramientas-backend
sudo systemctl status herramientas-telegram
```

### Detener Servicios

```bash
sudo systemctl stop herramientas-backend
sudo systemctl stop herramientas-telegram
```

---

## 🌐 Configurar Nginx (Producción)

Para usar dominio en lugar de puerto:

```bash
sudo nano /etc/nginx/sites-available/ai-chat
```

**Contenido:**

```nginx
server {
    listen 80;
    server_name ai.herramientasyaccesorios.store;

    # Frontend React
    location / {
        root /home/productos/miapp-standalone-20251022-142042/frontend/build;
        try_files $uri /index.html;
    }

    # Backend API
    location /api {
        proxy_pass http://localhost:8001;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Para upload de archivos grandes
        client_max_body_size 100M;
    }
}
```

**Activar:**

```bash
sudo ln -s /etc/nginx/sites-available/ai-chat /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

**Usar en plugin:**
```
Frontend URL: https://ai.herramientasyaccesorios.store
```

---

## 🔒 Configurar SSL (Recomendado)

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d ai.herramientasyaccesorios.store
```

---

## 🔥 Abrir Puertos en Firewall

Si usas firewall (ufw):

```bash
sudo ufw allow 8001/tcp
sudo ufw allow 3000/tcp
sudo ufw status
```

---

## ⚠️ Solución de Problemas

### Backend no inicia

```bash
# Ver error
sudo journalctl -u herramientas-backend -n 50

# Verificar .env
cat ~/miapp-standalone-*/backend/.env

# Verificar Python
cd ~/miapp-standalone-*/backend
source venv/bin/activate
python server.py
```

### Frontend no carga

```bash
# Verificar dependencias
cd ~/miapp-standalone-*/frontend
npm install --legacy-peer-deps

# Iniciar manualmente
npm start
```

### Chat no aparece en WordPress

1. **Verificar backend corriendo:**
   ```bash
   curl http://localhost:8001/api/health
   ```

2. **Verificar plugin activado:**
   WordPress → Plugins → "AI Chat Admin"

3. **Verificar configuración:**
   AI Chat Admin → Settings → URLs correctas

4. **Verificar permisos:**
   Debes estar logueado como administrador

---

## 💰 Costos

### APIs
- **Perplexity**: ~$0.001 por 1K tokens
- **OpenAI GPT-4o**: ~$2.50 por 1M tokens
- **MongoDB Atlas**: $0 (free tier 512MB)

### Total Estimado
- Uso ligero: $5-10 USD/mes
- Uso medio: $20-40 USD/mes

---

## 📞 Siguientes Pasos

1. ✅ Seguir esta guía paso a paso
2. ✅ Configurar .env con API keys
3. ✅ Iniciar servicios
4. ✅ Verificar que funciona
5. ✅ Configurar plugin WordPress
6. ✅ Probar chat con archivos e imágenes

---

**¡Tu chat completo con AI estará funcionando! 🚀**
