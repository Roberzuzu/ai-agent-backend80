# 🚀 Despliegue Backend Completo - herramientasyaccesorios.store

## 📦 Paquete Standalone

Ya tienes el paquete completo creado:
- **Archivo**: `miapp-standalone-20251022-142042.zip` (637 KB)
- **Ubicación**: `/app/miapp-standalone-20251022-142042.zip`

---

## 🎯 Arquitectura del Sistema

```
herramientasyaccesorios.store
│
├── WordPress + WooCommerce (Puerto 80/443)
│   └── https://herramientasyaccesorios.store
│
└── Backend AI Standalone (Puerto 8001)
    └── https://herramientasyaccesorios.store:8001
    │   ├── Backend FastAPI (API + AI Agent)
    │   ├── Frontend React (Interfaz web con chat)
    │   └── Telegram Bot 24/7
```

---

## 📋 Paso 1: Preparar el Servidor

### 1.1 Conectar por SSH

```bash
ssh productos@herramientasyaccesorios.store
# Usa tu contraseña: oFnXqP3(EITAWfd%rUzIkW%i
```

### 1.2 Instalar Dependencias

```bash
# Actualizar sistema
sudo apt update
sudo apt upgrade -y

# Instalar Python 3.10+
sudo apt install -y python3.10 python3.10-venv python3-pip

# Instalar Node.js (para frontend)
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo bash -
sudo apt install -y nodejs

# Verificar instalaciones
python3 --version  # Debe ser 3.10+
node --version     # Debe ser 18+
npm --version
```

---

## 📋 Paso 2: Subir y Descomprimir Paquete

### 2.1 Transferir Paquete

**Opción A: Desde donde está /app**
```bash
# Copiar a tu servidor
scp /app/miapp-standalone-20251022-142042.zip productos@herramientasyaccesorios.store:~/
```

**Opción B: Descargar directo en servidor**
```bash
# En tu servidor
cd ~
wget http://servidor-donde-esta-app:8080/miapp-standalone-20251022-142042.zip
# O usa el script serve_download.sh que creamos
```

### 2.2 Descomprimir

```bash
cd ~
unzip miapp-standalone-20251022-142042.zip
cd miapp-standalone-*
```

---

## 📋 Paso 3: Configurar Variables de Entorno

### 3.1 Configurar Backend

```bash
cd ~/miapp-standalone-*/backend
cp .env.example .env
nano .env
```

**Configuración para herramientasyaccesorios.store:**

```bash
# Base de datos (MongoDB Atlas - GRATIS)
MONGO_URL=mongodb+srv://usuario:password@cluster.mongodb.net/herramientas_db
# O local si prefieres:
# MONGO_URL=mongodb://localhost:27017

DB_NAME=herramientas_woocommerce

# OpenAI (tu key actual)
OPENAI_API_KEY=sk-proj-tu-key-aqui

# Perplexity (recomendado)
PERPLEXITY_API_KEY=pplx-tu-key-aqui

# Telegram Bot
TELEGRAM_BOT_TOKEN=tu-token-de-botfather
TELEGRAM_CHAT_ID=tu-chat-id

# WooCommerce API (de tu tienda)
WC_URL=https://herramientasyaccesorios.store/wp-json/wc/v3
WC_KEY=ck_tu_consumer_key_aqui
WC_SECRET=cs_tu_consumer_secret_aqui

# WordPress API
WP_URL=https://herramientasyaccesorios.store/wp-json/wp/v2
WP_USER=productos@herramientasyaccesorios.store
WP_PASS=oFnXqP3(EITAWfd%rUzIkW%i

# Seguridad
SECRET_KEY=$(openssl rand -hex 32)

# URLs
BACKEND_URL=http://localhost:8001
```

**Guardar**: Ctrl+O, Enter, Ctrl+X

---

## 📋 Paso 4: Obtener API Keys de WooCommerce

### 4.1 Crear Consumer Key

1. WordPress Admin → **WooCommerce → Settings**
2. Tab **"Advanced"** → **"REST API"**
3. Click **"Add key"**
4. Configurar:
   - **Description**: "AI Agent Backend"
   - **User**: productos (o tu usuario admin)
   - **Permissions**: **Read/Write**
5. Click **"Generate API key"**
6. **COPIAR Y GUARDAR**:
   - Consumer key: `ck_...`
   - Consumer secret: `cs_...`
7. Agregar al `.env`

---

## 📋 Paso 5: Configurar MongoDB

**Opción A: MongoDB Atlas (Gratis y Recomendado)**

1. Ve a https://www.mongodb.com/cloud/atlas
2. Crea cuenta gratis
3. Crea cluster (Free tier)
4. Click "Connect" → "Connect your application"
5. Copia la connection string
6. Reemplaza `<password>` con tu contraseña
7. Pega en `.env` como `MONGO_URL`

**Opción B: MongoDB Local**

```bash
# Instalar MongoDB
sudo apt install -y mongodb
sudo systemctl enable mongodb
sudo systemctl start mongodb

# Usar en .env:
MONGO_URL=mongodb://localhost:27017
```

---

## 📋 Paso 6: Instalar Dependencias Python

```bash
cd ~/miapp-standalone-*/backend

# Crear entorno virtual
python3 -m venv venv
source venv/bin/activate

# Instalar dependencias standalone
pip install -r requirements_standalone.txt

# Debería instalar sin errores
```

---

## 📋 Paso 7: Iniciar Backend (Primera Prueba)

```bash
# Con entorno virtual activado
cd ~/miapp-standalone-*/backend
source venv/bin/activate

# Iniciar backend
python3 -m uvicorn server:app --host 0.0.0.0 --port 8001

# Debería mostrar:
# INFO:     Started server process
# INFO:     Uvicorn running on http://0.0.0.0:8001
```

**Probar en navegador:**
- `http://herramientasyaccesorios.store:8001/docs`
- Deberías ver la documentación de la API

**Presiona Ctrl+C para detener**

---

## 📋 Paso 8: Configurar Frontend

### 8.1 Configurar Variables

```bash
cd ~/miapp-standalone-*/frontend
cp .env.example .env
nano .env
```

**Contenido:**
```bash
REACT_APP_BACKEND_URL=http://herramientasyaccesorios.store:8001/api
```

### 8.2 Instalar Dependencias

```bash
cd ~/miapp-standalone-*/frontend

# Instalar con npm (o yarn si prefieres)
npm install

# Si hay errores, prueba:
npm install --legacy-peer-deps
```

### 8.3 Iniciar Frontend (Prueba)

```bash
npm start

# Debería abrir en puerto 3000
```

**Probar:**
- `http://herramientasyaccesorios.store:3000`

**Presiona Ctrl+C para detener**

---

## 📋 Paso 9: Configurar Ejecución Permanente (Systemd)

### 9.1 Crear Servicio Backend

```bash
sudo nano /etc/systemd/system/herramientas-backend.service
```

**Contenido:**
```ini
[Unit]
Description=Herramientas AI Backend
After=network.target

[Service]
Type=simple
User=productos
WorkingDirectory=/home/productos/miapp-standalone-20251022-142042/backend
Environment="PATH=/home/productos/miapp-standalone-20251022-142042/backend/venv/bin"
ExecStart=/home/productos/miapp-standalone-20251022-142042/backend/venv/bin/uvicorn server:app --host 0.0.0.0 --port 8001
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### 9.2 Crear Servicio Telegram Bot

```bash
sudo nano /etc/systemd/system/herramientas-telegram.service
```

**Contenido:**
```ini
[Unit]
Description=Herramientas Telegram Bot
After=network.target herramientas-backend.service

[Service]
Type=simple
User=productos
WorkingDirectory=/home/productos/miapp-standalone-20251022-142042/backend
Environment="PATH=/home/productos/miapp-standalone-20251022-142042/backend/venv/bin"
ExecStart=/home/productos/miapp-standalone-20251022-142042/backend/venv/bin/python telegram_bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### 9.3 Habilitar e Iniciar Servicios

```bash
# Recargar systemd
sudo systemctl daemon-reload

# Habilitar (arranque automático)
sudo systemctl enable herramientas-backend
sudo systemctl enable herramientas-telegram

# Iniciar
sudo systemctl start herramientas-backend
sudo systemctl start herramientas-telegram

# Ver estado
sudo systemctl status herramientas-backend
sudo systemctl status herramientas-telegram

# Ver logs
sudo journalctl -u herramientas-backend -f
```

---

## 📋 Paso 10: Configurar Nginx (Proxy Reverso)

### 10.1 Crear Configuración

```bash
sudo nano /etc/nginx/sites-available/ai-backend
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
    }
}
```

### 10.2 Activar

```bash
sudo ln -s /etc/nginx/sites-available/ai-backend /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### 10.3 Build Frontend

```bash
cd ~/miapp-standalone-*/frontend
npm run build

# El build estará en frontend/build/
```

---

## 📋 Paso 11: Configurar SSL (Opcional pero Recomendado)

```bash
# Instalar certbot
sudo apt install certbot python3-certbot-nginx

# Obtener certificado
sudo certbot --nginx -d ai.herramientasyaccesorios.store

# Renovación automática ya está configurada
```

---

## 📋 Paso 12: Acceder a la Aplicación

Una vez todo configurado:

**Frontend (Interfaz web con chat):**
- http://ai.herramientasyaccesorios.store
- O: http://herramientasyaccesorios.store:3000 (desarrollo)

**Backend API:**
- http://ai.herramientasyaccesorios.store/api/docs
- O: http://herramientasyaccesorios.store:8001/docs

**Telegram Bot:**
- Funciona en background 24/7
- Envía comandos a tu bot

---

## 🎯 Funcionalidades Disponibles

### 1. Interfaz Web (Frontend)
- Chat con AI Agent
- Dashboard con estadísticas
- Gestión de productos
- Análisis de ventas
- 22+ herramientas integradas

### 2. API Backend
- Endpoints REST
- Procesamiento con AI
- Integración WooCommerce
- Sistema de memoria con RAG

### 3. Telegram Bot
- Control remoto de tienda
- Comandos en lenguaje natural
- Notificaciones en tiempo real

---

## 🔧 Comandos Útiles

### Ver Logs
```bash
# Backend
sudo journalctl -u herramientas-backend -f

# Telegram
sudo journalctl -u herramientas-telegram -f

# Nginx
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

### Reiniciar Servicios
```bash
sudo systemctl restart herramientas-backend
sudo systemctl restart herramientas-telegram
sudo systemctl reload nginx
```

### Ver Estado
```bash
sudo systemctl status herramientas-backend
sudo systemctl status herramientas-telegram
```

---

## ⚠️ Abrir Puertos en Firewall

Si usas firewall (ufw):

```bash
sudo ufw allow 8001/tcp
sudo ufw allow 3000/tcp
sudo ufw status
```

---

## 💡 Tips Finales

1. **MongoDB Atlas** es más fácil que local
2. **Usa HTTPS** con certbot para producción
3. **Backup regular** de la base de datos
4. **Monitorea logs** regularmente
5. **Telegram Bot** es opcional pero muy útil

---

## 📞 Problemas Comunes

### Backend no inicia
```bash
# Ver error exacto
sudo journalctl -u herramientas-backend -n 50

# Verificar .env
cat ~/miapp-standalone-*/backend/.env

# Verificar permisos
ls -la ~/miapp-standalone-*/backend/
```

### Frontend no conecta
- Verifica REACT_APP_BACKEND_URL en `.env`
- Debe ser la URL correcta del backend
- Asegura que backend esté corriendo

### MongoDB error
- Verifica MONGO_URL en `.env`
- Si es Atlas, verifica IP whitelist
- Si es local, verifica que esté corriendo

---

**¡Tu backend completo standalone estará funcionando 24/7! 🚀**
