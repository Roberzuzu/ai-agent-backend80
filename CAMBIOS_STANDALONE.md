# ✅ Tu Aplicación es Ahora COMPLETAMENTE AUTÓNOMA

## 🎉 ¿Qué se ha cambiado?

### ❌ ELIMINADO (Dependencias de Emergent):
1. **emergentintegrations** - Librería propietaria eliminada
2. **Dependencia de plataforma Emergent**
3. **Límites de tiempo/sesión**
4. **URLs hardcodeadas de Emergent**

### ✅ AGREGADO (Funcionalidad Standalone):
1. **llm_client.py** - Cliente LLM nativo (OpenAI + Anthropic)
2. **stripe_client.py** - Cliente Stripe nativo
3. **requirements_standalone.txt** - Dependencias sin Emergent
4. **start_standalone.sh** - Script de inicio autónomo
5. **install_dependencies.sh** - Instalador de sistema
6. **Configuración vía .env** - Variables de entorno configurables
7. **DEPLOYMENT.md** - Guía completa de despliegue

---

## 📁 Archivos Nuevos Creados

```
/app/
├── README_STANDALONE.md          ← Documentación principal
├── DEPLOYMENT.md                 ← Guía de despliegue completo
├── CAMBIOS_STANDALONE.md         ← Este archivo
├── start_standalone.sh           ← Script de inicio (EJECUTAR ESTE)
├── install_dependencies.sh       ← Instalador de dependencias
│
├── backend/
│   ├── llm_client.py            ← Cliente LLM standalone
│   ├── stripe_client.py         ← Cliente Stripe standalone
│   ├── requirements_standalone.txt  ← Dependencias standalone
│   ├── .env.example             ← Plantilla de configuración
│   ├── server.py                ← ACTUALIZADO (sin emergentintegrations)
│   └── telegram_bot.py          ← ACTUALIZADO (configurable vía .env)
│
└── logs/                         ← Directorio de logs (se crea automáticamente)
```

---

## 🚀 Cómo Usar Tu Aplicación Autónoma

### Opción 1: Inicio Rápido (Desarrollo Local)

```bash
# 1. Configurar variables de entorno
cd /app/backend
cp .env.example .env
nano .env  # Edita con tus API keys

# 2. Iniciar todo (Backend + Bot)
cd /app
./start_standalone.sh
```

✅ **Listo!** Tu app estará corriendo:
- Backend: `http://localhost:8001`
- API Docs: `http://localhost:8001/docs`
- Telegram Bot: Activo 24/7

---

### Opción 2: Producción en Servidor VPS

#### 1. Instalar Dependencias del Sistema

```bash
# En tu servidor Ubuntu/Debian
cd /app
sudo ./install_dependencies.sh
```

Esto instalará:
- Python 3.10
- Node.js 18
- MongoDB (opcional, puedes usar MongoDB Atlas)
- Nginx (opcional)

#### 2. Configurar Variables de Entorno

```bash
cd /app/backend
cp .env.example .env
nano .env
```

**Configuración mínima requerida:**

```bash
# Database (local o MongoDB Atlas)
MONGO_URL=mongodb://localhost:27017
# o MongoDB Atlas:
# MONGO_URL=mongodb+srv://usuario:password@cluster.mongodb.net/

DB_NAME=social_media_monetization

# APIs Esenciales
OPENAI_API_KEY=sk-proj-tu-key-aqui
PERPLEXITY_API_KEY=pplx-tu-key-aqui
TELEGRAM_BOT_TOKEN=tu-token-aqui
TELEGRAM_CHAT_ID=tu-chat-id

# Seguridad
SECRET_KEY=$(openssl rand -hex 32)

# Stripe (opcional, para pagos)
STRIPE_API_KEY=sk_test_tu-key
STRIPE_PUBLISHABLE_KEY=pk_test_tu-key
```

#### 3. Crear Servicios Systemd (Ejecución Permanente)

**Backend Service:**

```bash
sudo nano /etc/systemd/system/miapp-backend.service
```

```ini
[Unit]
Description=Mi App Backend
After=network.target mongodb.service

[Service]
Type=simple
User=www-data
WorkingDirectory=/app/backend
Environment="PATH=/app/backend/venv/bin"
ExecStart=/app/backend/venv/bin/uvicorn server:app --host 0.0.0.0 --port 8001
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**Telegram Bot Service:**

```bash
sudo nano /etc/systemd/system/miapp-telegram.service
```

```ini
[Unit]
Description=Mi App Telegram Bot
After=network.target miapp-backend.service

[Service]
Type=simple
User=www-data
WorkingDirectory=/app/backend
Environment="PATH=/app/backend/venv/bin"
ExecStart=/app/backend/venv/bin/python telegram_bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**Habilitar y Iniciar:**

```bash
# Instalar dependencias Python primero
cd /app/backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements_standalone.txt

# Habilitar servicios
sudo systemctl daemon-reload
sudo systemctl enable miapp-backend miapp-telegram
sudo systemctl start miapp-backend miapp-telegram

# Ver estado
sudo systemctl status miapp-backend
sudo systemctl status miapp-telegram

# Ver logs
sudo journalctl -u miapp-backend -f
sudo journalctl -u miapp-telegram -f
```

#### 4. Configurar Nginx (Opcional)

```bash
sudo nano /etc/nginx/sites-available/miapp
```

```nginx
server {
    listen 80;
    server_name tu-dominio.com;

    # Frontend (React build)
    location / {
        root /app/frontend/build;
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
    }
}
```

```bash
sudo ln -s /etc/nginx/sites-available/miapp /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

#### 5. SSL con Let's Encrypt

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d tu-dominio.com
```

---

### Opción 3: Docker

```bash
# Crear Dockerfile backend
cat > /app/backend/Dockerfile << 'EOF'
FROM python:3.10-slim

WORKDIR /app

COPY requirements_standalone.txt .
RUN pip install --no-cache-dir -r requirements_standalone.txt

COPY . .

EXPOSE 8001

CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8001"]
EOF

# Crear docker-compose.yml
cat > /app/docker-compose.yml << 'EOF'
version: '3.8'

services:
  mongodb:
    image: mongo:7
    volumes:
      - mongo-data:/data/db
    ports:
      - "27017:27017"

  backend:
    build:
      context: ./backend
    ports:
      - "8001:8001"
    env_file:
      - backend/.env
    depends_on:
      - mongodb

  telegram-bot:
    build:
      context: ./backend
    command: python telegram_bot.py
    env_file:
      - backend/.env
    depends_on:
      - backend

volumes:
  mongo-data:
EOF

# Ejecutar
docker-compose up -d
```

---

## 🔍 Verificación

### 1. Backend Funcionando

```bash
# Test health endpoint
curl http://localhost:8001/api/health || curl http://localhost:8001

# Ver API docs
open http://localhost:8001/docs
```

### 2. Telegram Bot Activo

```bash
# Ver logs
tail -f /app/logs/telegram.log

# O con systemd
sudo journalctl -u miapp-telegram -f

# Test directo
curl "https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/getMe"
```

### 3. MongoDB Conectado

```bash
# Si es local
sudo systemctl status mongod

# Test conexión
mongo --eval "db.version()"

# O con Python
python3 << EOF
from motor.motor_asyncio import AsyncIOMotorClient
import asyncio

async def test():
    client = AsyncIOMotorClient("mongodb://localhost:27017")
    print(await client.server_info())

asyncio.run(test())
EOF
```

---

## 📊 Diferencias Clave

| Aspecto | ❌ Con Emergent | ✅ Standalone |
|---------|----------------|---------------|
| **Dependencias** | emergentintegrations | SDKs nativos (openai, stripe) |
| **Ejecución** | Limitada por sesión (~10min) | 24/7 sin límites |
| **Backend URL** | URLs de Emergent hardcodeadas | Configurable vía .env |
| **Telegram Bot** | Se desconecta | Proceso permanente |
| **Servidor** | Solo en Emergent | Cualquier servidor |
| **Costos** | Por crédito/tiempo | Solo hosting (~$10/mes) |
| **Escalabilidad** | Limitada | Ilimitada |
| **Control** | Limitado | Total |

---

## 🔧 Cambios Técnicos

### 1. LLM Client (`llm_client.py`)

**Antes:**
```python
from emergentintegrations.llm.chat import LlmChat, UserMessage
```

**Ahora:**
```python
from llm_client import LlmChat, UserMessage  # Standalone

# Soporta:
# - OpenAI nativo
# - Anthropic nativo
# - Cualquier provider HTTP
```

### 2. Stripe Client (`stripe_client.py`)

**Antes:**
```python
from emergentintegrations.payments.stripe.checkout import StripeCheckout
```

**Ahora:**
```python
from stripe_client import StripeCheckout  # Standalone usando SDK de Stripe
```

### 3. Variables de Entorno

**Antes:**
```python
BACKEND_URL = "https://plugin-stability.preview.emergentagent.com/api"  # Hardcoded
```

**Ahora:**
```python
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8001/api")  # Configurable
```

### 4. Telegram Bot

**Antes:**
- Se ejecutaba dentro de supervisor de Emergent
- Se desconectaba cada ~10 minutos

**Ahora:**
- Proceso independiente con systemd
- Se reinicia automáticamente si falla
- Logs persistentes
- Ejecución 24/7

---

## 💰 Costos de Hosting

### Opción Económica (~$5-10/mes)

| Servicio | Proveedor | Costo/Mes |
|----------|-----------|-----------|
| **VPS 1GB RAM** | DigitalOcean, Linode, Vultr | $5 USD |
| **MongoDB** | Atlas Free Tier | $0 USD |
| **Dominio** | Namecheap | ~$1 USD |
| **SSL** | Let's Encrypt | $0 USD |
| **Total** | | **~$6 USD** |

### Opción Media (~$15-25/mes)

| Servicio | Costo/Mes |
|----------|-----------|
| **VPS 2GB RAM** | $12 USD |
| **MongoDB Atlas Shared** | $9 USD |
| **CDN (Cloudflare)** | $0 USD |
| **Total** | **~$21 USD** |

---

## 📝 Comandos Útiles

### Logs

```bash
# Ver todos los logs
tail -f /app/logs/*.log

# Solo backend
tail -f /app/logs/backend.log

# Solo Telegram
tail -f /app/logs/telegram.log

# Con systemd
sudo journalctl -u miapp-backend -f
sudo journalctl -u miapp-telegram -f
```

### Reiniciar Servicios

```bash
# Con script standalone
./start_standalone.sh

# Con systemd
sudo systemctl restart miapp-backend
sudo systemctl restart miapp-telegram
sudo systemctl restart all
```

### Ver Estado

```bash
# Servicios
sudo systemctl status miapp-backend
sudo systemctl status miapp-telegram

# Procesos
ps aux | grep python
ps aux | grep uvicorn

# Puertos
sudo lsof -i :8001  # Backend
sudo lsof -i :3000  # Frontend (si corre)
```

### Backup MongoDB

```bash
# Crear backup
mongodump --out /backups/$(date +%Y%m%d)

# Restaurar
mongorestore /backups/20250101

# Backup automatizado (cron)
echo "0 2 * * * mongodump --out /backups/\$(date +\%Y\%m\%d)" | crontab -
```

---

## ✅ Checklist Final

- [ ] Instalar dependencias del sistema
- [ ] Configurar backend/.env con API keys
- [ ] Instalar dependencias Python (requirements_standalone.txt)
- [ ] Test local con ./start_standalone.sh
- [ ] Crear servicios systemd (producción)
- [ ] Configurar Nginx (opcional)
- [ ] Configurar SSL con certbot
- [ ] Configurar backups automáticos
- [ ] Test Telegram Bot
- [ ] Test API endpoints
- [ ] Monitoreo de logs

---

## 🎯 Próximos Pasos

1. **Ahora**: Configura tu .env y ejecuta `./start_standalone.sh`
2. **Producción**: Sigue DEPLOYMENT.md para servidor VPS
3. **Optimización**: Configura Nginx, SSL, backups
4. **Monitoreo**: Setup alertas y logs centralizados

---

## 📚 Documentación Completa

- **README_STANDALONE.md** - Documentación principal
- **DEPLOYMENT.md** - Guía completa de despliegue
- **Este archivo** - Resumen de cambios

---

## 🎉 ¡Felicidades!

Tu aplicación ahora es **100% autónoma** y puede ejecutarse:

✅ **Sin límites de tiempo**  
✅ **Sin límites de sesión**  
✅ **En tu propio servidor**  
✅ **24/7 sin interrupciones**  
✅ **Sin dependencias de Emergent**  

**Tu aplicación. Tu servidor. Tu control total.**

---

## 💬 ¿Problemas?

### Backend no inicia

```bash
# Ver error
tail -f /app/logs/backend.log

# Verificar puerto
sudo lsof -i :8001

# Matar proceso si existe
sudo kill $(sudo lsof -t -i:8001)

# Reiniciar
./start_standalone.sh
```

### Telegram Bot no responde

```bash
# Ver logs
tail -f /app/logs/telegram.log

# Verificar token
curl "https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/getMe"

# Reiniciar bot
sudo systemctl restart miapp-telegram
```

### MongoDB error

```bash
# Local
sudo systemctl start mongod
sudo systemctl status mongod

# Atlas - verifica en .env:
# 1. MONGO_URL correcto
# 2. IP whitelisted
# 3. Usuario/password correctos
```

---

**¡Disfruta de tu aplicación autónoma! 🚀**
