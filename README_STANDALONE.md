# Aplicación Autónoma - Social Media Monetization AI

## 🎉 Tu App es Ahora 100% Independiente

Esta aplicación **NO tiene dependencias de Emergent** y puede ejecutarse en cualquier lugar:

- ✅ Tu propio servidor VPS
- ✅ AWS, DigitalOcean, Linode, etc.
- ✅ Docker containers
- ✅ Heroku, Render, Railway
- ✅ Tu computadora local

---

## 🚀 Inicio Rápido (5 minutos)

### 1. Requisitos Previos

```bash
# Ubuntu/Debian
sudo ./install_dependencies.sh

# O manualmente:
python3.10+
node.js 18+
mongodb (local o MongoDB Atlas)
```

### 2. Configurar Variables de Entorno

```bash
cd backend
cp .env.example .env
nano .env
```

Configura al menos:
- `MONGO_URL`
- `OPENAI_API_KEY`
- `PERPLEXITY_API_KEY`
- `TELEGRAM_BOT_TOKEN`
- `SECRET_KEY`

### 3. Iniciar Aplicación
```bash
chmod +x start_standalone.sh
./start_standalone.sh
```

¡Listo! Tu aplicación estará corriendo en:
- Backend: `http://localhost:8001`
- API Docs: `http://localhost:8001/docs`
- Telegram Bot: Activo y escuchando

---

## 💻 Arquitectura

```
┌────────────────────────────┐
│   React Frontend (port 3000)  │
└───────────┬────────────────┘
             │
             │ HTTP/REST
             │
┌────────────┴────────────────┐
│   FastAPI Backend (port 8001)  │
│   - AI Agent (Perplexity)       │
│   - Stripe Payments             │
│   - OpenAI Integration          │
│   - WooCommerce API             │
└───────────┬────────┬────────┘
             │          │
             │          │
    ┌────────┼─────────────────────────┐
    │        │                          │
┌───┴────┐   │       ┌───────────┴───────────┐
│ MongoDB  │   │       │ Telegram Bot (24/7)   │
│ Database │   │       │ - Command Processor   │
└──────────┘   │       │ - Natural Language    │
                │       └───────────────────────┘
                │
         External APIs:
         - OpenAI (GPT-4o)
         - Perplexity (sonar-pro)
         - Stripe
         - WooCommerce
         - Fal AI
```

---

## 🔧 Características

### Cerebro AI
- **Perplexity Pro** (sonar-pro) como cerebro principal
- **OpenAI GPT-4o** como fallback automático
- **22 herramientas** integradas
- Sistema de **memoria persistente con RAG**
- Búsqueda semántica con embeddings

### Integraciones
- **Telegram Bot**: Comandos en lenguaje natural
- **WooCommerce**: Gestión completa de productos
- **Stripe**: Pagos y suscripciones
- **WordPress**: Publicación de contenido
- **Fal AI**: Generación de imágenes

### Monetización
- Sistema de pagos con Stripe
- Suscripciones recurrentes
- Programa de afiliados
- Analytics avanzados
- Carritos abandonados
- A/B testing

---

## 📦 Deployment Options

### Opción 1: Servidor Propio (Recomendado)

Ver guía completa: **[DEPLOYMENT.md](DEPLOYMENT.md)**

Pasos rápidos:
```bash
# 1. Instalar dependencias del sistema
sudo ./install_dependencies.sh

# 2. Configurar .env
cp backend/.env.example backend/.env
nano backend/.env

# 3. Crear servicios systemd (ejecución permanente)
sudo cp systemd/* /etc/systemd/system/
sudo systemctl enable miapp-backend miapp-telegram
sudo systemctl start miapp-backend miapp-telegram

# 4. Configurar Nginx
sudo cp nginx.conf /etc/nginx/sites-available/miapp
sudo ln -s /etc/nginx/sites-available/miapp /etc/nginx/sites-enabled/
sudo systemctl reload nginx
```

### Opción 2: Docker

```bash
docker-compose up -d
```

### Opción 3: Heroku

```bash
heroku create miapp
heroku addons:create mongolab:sandbox
git push heroku main
```

---

## 📊 Costos Mensuales

| Servicio | Costo |
|----------|-------|
| VPS (DigitalOcean/Linode) | $5-12 USD |
| MongoDB Atlas (Free Tier) | $0 USD |
| Dominio | ~$1 USD |
| **Total** | **~$6-13 USD/mes** |

---

## 🔒 Seguridad

- Autenticación JWT
- Rate limiting
- CSRF protection
- Security headers
- API key management
- 2FA support
- Audit logging

---

## 📝 Logs

```bash
# Ver logs en tiempo real
tail -f logs/backend.log
tail -f logs/telegram.log

# Con systemd
sudo journalctl -u miapp-backend -f
sudo journalctl -u miapp-telegram -f
```

---

## 🔄 Actualizaciones

```bash
# Pull cambios
git pull

# Actualizar dependencias
cd backend
source venv/bin/activate
pip install -r requirements_standalone.txt

# Reiniciar servicios
sudo systemctl restart miapp-backend miapp-telegram
```

---

## 🌐 Frontend Build

```bash
cd frontend
npm install
npm run build

# El build estará en frontend/build/
# Configurar Nginx para servir estos archivos
```

---

## ❓ Troubleshooting

### Backend no inicia

```bash
# Ver logs
tail -f logs/backend.log

# Verificar puerto
sudo lsof -i :8001

# Verificar MongoDB
sudo systemctl status mongod
```

### Telegram Bot no responde

```bash
# Ver logs
tail -f logs/telegram.log

# Verificar token
echo $TELEGRAM_BOT_TOKEN

# Test manual
curl https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/getMe
```

### MongoDB connection error

```bash
# Si usas MongoDB local
sudo systemctl start mongod

# Si usas MongoDB Atlas, verifica:
# 1. MONGO_URL correcto en .env
# 2. IP whitelisted en Atlas
# 3. Usuario/password correctos
```

---

## 📚 Documentación

- **API Docs**: http://localhost:8001/docs
- **Deployment**: [DEPLOYMENT.md](DEPLOYMENT.md)
- **Architecture**: Este archivo

---

## ✨ Diferencias con Emergent

| Aspecto | Emergent | Standalone |
|---------|----------|------------|
| **Dependencias** | emergentintegrations | SDKs nativos |
| **Ejecución** | Limitada por sesión | 24/7 sin límites |
| **Servidor** | Plataforma Emergent | Tu propio servidor |
| **Costos** | Por crédito/tiempo | Solo hosting (~$10/mes) |
| **Control** | Limitado | Total |
| **Escalabilidad** | Limitada | Ilimitada |

---

## 💬 Soporte

Tu aplicación es **100% tuya**:
- Código fuente completo
- Sin dependencias propietarias
- Ejecutable en cualquier lugar
- Sin límites de tiempo o uso

**¡Disfruta de tu libertad! 🚀**
