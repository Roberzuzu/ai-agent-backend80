# Standalone Deployment Guide

## Tu Aplicación Es Ahora Totalmente Autónoma

Esta aplicación **NO depende de Emergent** y puede ejecutarse en cualquier servidor.

---

## Requisitos del Sistema

- **Python 3.10+**
- **Node.js 18+** (para frontend)
- **MongoDB** (local o remoto como MongoDB Atlas)
- **Servidor Linux/Ubuntu** (recomendado) o Windows/Mac

---

## Opción 1: Servidor Propio (VPS/Dedicated)

### 1. Preparar Servidor

```bash
# Actualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar dependencias
sudo apt install -y python3.10 python3.10-venv python3-pip nodejs npm nginx mongodb

# Habilitar MongoDB
sudo systemctl enable mongodb
sudo systemctl start mongodb
```

### 2. Clonar/Copiar Proyecto

```bash
# Crear directorio
sudo mkdir -p /var/www/miapp
sudo chown $USER:$USER /var/www/miapp

# Copiar archivos (usar scp, rsync, o git)
cd /var/www/miapp
# Copiar todo el contenido de /app a este directorio
```

### 3. Configurar Backend

```bash
cd /var/www/miapp/backend

# Crear entorno virtual
python3 -m venv venv
source venv/bin/activate

# Instalar dependencias STANDALONE
pip install -r requirements_standalone.txt

# Configurar .env
cp .env.example .env
nano .env
```

**Editar `/var/www/miapp/backend/.env`:**

```bash
# MongoDB (local o Atlas)
MONGO_URL=mongodb://localhost:27017
DB_NAME=social_media_monetization

# APIs
OPENAI_API_KEY=tu-api-key-aqui
PERPLEXITY_API_KEY=tu-api-key-aqui
FAL_API_KEY=tu-api-key-aqui
STRIPE_API_KEY=tu-api-key-aqui
STRIPE_PUBLISHABLE_KEY=tu-publishable-key-aqui

# Telegram Bot
TELEGRAM_BOT_TOKEN=tu-token-aqui
TELEGRAM_CHAT_ID=tu-chat-id

# Security
SECRET_KEY=genera-un-secret-key-seguro-aqui
```

### 4. Configurar Frontend

```bash
cd /var/www/miapp/frontend

# Instalar dependencias
npm install
# o yarn install

# Configurar .env
cp .env.example .env
nano .env
```

**Editar `/var/www/miapp/frontend/.env`:**

```bash
REACT_APP_BACKEND_URL=http://tu-servidor.com/api
# o para desarrollo local:
# REACT_APP_BACKEND_URL=http://localhost:8001/api
```

### 5. Crear Servicios Systemd (Ejecución Permanente)

**Backend Service: `/etc/systemd/system/miapp-backend.service`**

```ini
[Unit]
Description=Mi App Backend (FastAPI)
After=network.target mongodb.service

[Service]
Type=simple
User=www-data
WorkingDirectory=/var/www/miapp/backend
Environment="PATH=/var/www/miapp/backend/venv/bin"
ExecStart=/var/www/miapp/backend/venv/bin/uvicorn server:app --host 0.0.0.0 --port 8001 --workers 4
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**Telegram Bot Service: `/etc/systemd/system/miapp-telegram.service`**

```ini
[Unit]
Description=Mi App Telegram Bot
After=network.target miapp-backend.service

[Service]
Type=simple
User=www-data
WorkingDirectory=/var/www/miapp/backend
Environment="PATH=/var/www/miapp/backend/venv/bin"
ExecStart=/var/www/miapp/backend/venv/bin/python telegram_bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**Habilitar servicios:**

```bash
sudo systemctl daemon-reload
sudo systemctl enable miapp-backend miapp-telegram
sudo systemctl start miapp-backend miapp-telegram

# Ver logs
sudo journalctl -u miapp-backend -f
sudo journalctl -u miapp-telegram -f
```

### 6. Configurar Nginx (Reverse Proxy)

**`/etc/nginx/sites-available/miapp`:**

```nginx
server {
    listen 80;
    server_name tu-dominio.com;

    # Frontend (React build)
    location / {
        root /var/www/miapp/frontend/build;
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

**Activar:**

```bash
sudo ln -s /etc/nginx/sites-available/miapp /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### 7. Build Frontend

```bash
cd /var/www/miapp/frontend
npm run build
# El build estará en frontend/build/
```

### 8. SSL con Let's Encrypt (Recomendado)

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d tu-dominio.com
```

---

## Opción 2: Docker (Más Simple)

### Dockerfile Backend

```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements_standalone.txt .
RUN pip install --no-cache-dir -r requirements_standalone.txt

COPY . .

EXPOSE 8001

CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8001"]
```

### Docker Compose

```yaml
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
    environment:
      - MONGO_URL=mongodb://mongodb:27017
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - PERPLEXITY_API_KEY=${PERPLEXITY_API_KEY}
    depends_on:
      - mongodb

  telegram-bot:
    build:
      context: ./backend
    command: python telegram_bot.py
    environment:
      - MONGO_URL=mongodb://mongodb:27017
      - TELEGRAM_BOT_TOKEN=${TELEGRAM_BOT_TOKEN}
    depends_on:
      - backend

  frontend:
    build:
      context: ./frontend
    ports:
      - "3000:3000"
    environment:
      - REACT_APP_BACKEND_URL=http://localhost:8001/api

volumes:
  mongo-data:
```

**Ejecutar:**

```bash
docker-compose up -d
```

---

## Opción 3: Servicios Cloud

### AWS (EC2 + RDS MongoDB)

1. Crear EC2 instance (Ubuntu 22.04)
2. Configurar Security Groups (puertos 80, 443, 22)
3. Seguir pasos de "Opción 1" en el EC2
4. Usar MongoDB Atlas en lugar de local

### DigitalOcean Droplet

1. Crear Droplet (Ubuntu 22.04, mínimo 2GB RAM)
2. Seguir pasos de "Opción 1"
3. Usar MongoDB Atlas

### Heroku (Opción Simple)

```bash
# Crear Procfile
echo "web: uvicorn server:app --host 0.0.0.0 --port \$PORT" > Procfile
echo "worker: python telegram_bot.py" >> Procfile

# Deploy
heroku create miapp
heroku addons:create mongolab:sandbox
git push heroku main
```

---

## Mantenimiento

### Ver Logs

```bash
# Backend
sudo journalctl -u miapp-backend -f

# Telegram Bot
sudo journalctl -u miapp-telegram -f

# Nginx
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

### Reiniciar Servicios

```bash
sudo systemctl restart miapp-backend
sudo systemctl restart miapp-telegram
sudo systemctl reload nginx
```

### Backup MongoDB

```bash
# Backup
mongodump --out /backups/$(date +%Y%m%d)

# Restore
mongorestore /backups/20250101
```

### Actualizar Código

```bash
# Pull cambios
cd /var/www/miapp
git pull

# Backend
cd backend
source venv/bin/activate
pip install -r requirements_standalone.txt
sudo systemctl restart miapp-backend miapp-telegram

# Frontend
cd ../frontend
npm install
npm run build
sudo systemctl reload nginx
```

---

## Costos Estimados (Mensual)

| Opción | Costo Estimado |
|--------|----------------|
| VPS Básico (DigitalOcean/Linode) | $5-12 USD |
| MongoDB Atlas Free Tier | $0 USD |
| Dominio | $10-15 USD/año |
| **Total Mensual** | **~$10 USD** |

---

## Soporte

Tu aplicación ahora es **100% independiente de Emergent**. 

**NO HAY:**
- Límites de tiempo
- Límites de sesión
- Dependencias de plataforma
- Costos ocultos

**TIENES:**
- Control total del código
- Ejecución 24/7
- Escalabilidad
- Tu propio servidor
