#!/bin/bash

# ============================================
# Crear Paquete Descargable para Móvil
# ============================================

set -e

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "=========================================="
echo "  Creando Paquete Descargable"
echo "=========================================="
echo ""

# Nombre del paquete
PACKAGE_NAME="miapp-standalone-$(date +%Y%m%d-%H%M%S)"
PACKAGE_DIR="/tmp/$PACKAGE_NAME"
ZIP_FILE="/app/$PACKAGE_NAME.zip"

echo -e "${GREEN}✓${NC} Creando directorio temporal..."
mkdir -p "$PACKAGE_DIR"

echo -e "${GREEN}✓${NC} Copiando archivos necesarios..."

# Copiar estructura principal
cp -r /app/backend "$PACKAGE_DIR/"
cp -r /app/frontend "$PACKAGE_DIR/" 2>/dev/null || echo "  (Frontend no encontrado, omitiendo)"

# Copiar documentación
cp /app/README_STANDALONE.md "$PACKAGE_DIR/"
cp /app/DEPLOYMENT.md "$PACKAGE_DIR/"
cp /app/CAMBIOS_STANDALONE.md "$PACKAGE_DIR/"

# Copiar scripts
cp /app/start_standalone.sh "$PACKAGE_DIR/"
cp /app/install_dependencies.sh "$PACKAGE_DIR/"
cp /app/test_standalone.sh "$PACKAGE_DIR/"

echo -e "${GREEN}✓${NC} Limpiando archivos innecesarios..."

# Limpiar archivos temporales y pesados
rm -rf "$PACKAGE_DIR/backend/venv"
rm -rf "$PACKAGE_DIR/backend/__pycache__"
rm -rf "$PACKAGE_DIR/backend/.pytest_cache"
rm -rf "$PACKAGE_DIR/backend/*.pyc"
rm -rf "$PACKAGE_DIR/frontend/node_modules" 2>/dev/null || true
rm -rf "$PACKAGE_DIR/frontend/build" 2>/dev/null || true
rm -rf "$PACKAGE_DIR"/**/.DS_Store 2>/dev/null || true

# Limpiar datos sensibles (mantener .env.example)
if [ -f "$PACKAGE_DIR/backend/.env" ]; then
    echo -e "${YELLOW}!${NC} Removiendo .env (usar .env.example)"
    rm "$PACKAGE_DIR/backend/.env"
fi

echo -e "${GREEN}✓${NC} Creando README para móvil..."

# Crear README específico para el paquete
cat > "$PACKAGE_DIR/README.md" << 'EOF'
# 📱 Mi Aplicación Standalone - Paquete Descargable

## 🎉 ¡Descarga Exitosa!

Este paquete contiene tu aplicación completamente autónoma, lista para ser desplegada en cualquier servidor.

---

## 📦 Contenido del Paquete

```
📁 miapp-standalone/
├── 📄 README.md                    ← Este archivo
├── 📄 README_STANDALONE.md         ← Documentación completa
├── 📄 DEPLOYMENT.md                ← Guía de despliegue
├── 📄 CAMBIOS_STANDALONE.md        ← Cambios realizados
│
├── 🚀 start_standalone.sh          ← Script de inicio
├── 🔧 install_dependencies.sh      ← Instalador
├── ✅ test_standalone.sh           ← Verificación
│
├── 📁 backend/                     ← Backend FastAPI
│   ├── server.py
│   ├── ai_agent.py
│   ├── telegram_bot.py
│   ├── llm_client.py              ← Cliente LLM standalone
│   ├── stripe_client.py           ← Cliente Stripe standalone
│   ├── requirements_standalone.txt
│   └── .env.example               ← Plantilla de configuración
│
└── 📁 frontend/                    ← Frontend React (si existe)
    ├── src/
    └── package.json
```

---

## 🚀 Inicio Rápido (3 pasos)

### 1. Transferir a tu Servidor

**Desde tu móvil al servidor:**

```bash
# Opción A: Usando SCP
scp miapp-standalone-*.zip usuario@tu-servidor.com:~

# Opción B: Usando rsync
rsync -avz miapp-standalone-*.zip usuario@tu-servidor.com:~

# Opción C: Subir a Google Drive/Dropbox, luego descargar en servidor
```

**En el servidor:**

```bash
# Descomprimir
unzip miapp-standalone-*.zip
cd miapp-standalone-*
```

### 2. Configurar

```bash
# Instalar dependencias del sistema (solo primera vez)
sudo ./install_dependencies.sh

# Configurar variables de entorno
cd backend
cp .env.example .env
nano .env  # Edita con tus API keys
```

**Variables mínimas requeridas en `.env`:**

```bash
MONGO_URL=mongodb://localhost:27017
# o MongoDB Atlas:
# MONGO_URL=mongodb+srv://usuario:password@cluster.mongodb.net/

DB_NAME=social_media_monetization

OPENAI_API_KEY=sk-proj-tu-key-aqui
PERPLEXITY_API_KEY=pplx-tu-key-aqui
TELEGRAM_BOT_TOKEN=tu-token-aqui
TELEGRAM_CHAT_ID=tu-chat-id
SECRET_KEY=$(openssl rand -hex 32)

# Opcional para pagos:
STRIPE_API_KEY=sk_test_tu-key
STRIPE_PUBLISHABLE_KEY=pk_test_tu-key
```

### 3. Iniciar

```bash
cd ..
./start_standalone.sh
```

✅ **¡Listo!** Tu app estará en:
- Backend: `http://localhost:8001`
- API Docs: `http://localhost:8001/docs`
- Telegram Bot: Activo 24/7

---

## 🌐 Despliegue en Producción

### Opción 1: VPS (DigitalOcean, Linode, AWS)

1. **Crear VPS** con Ubuntu 22.04 (mínimo 1GB RAM)

2. **Transferir archivos:**
   ```bash
   scp -r miapp-standalone-* usuario@tu-ip:~/
   ```

3. **En el servidor:**
   ```bash
   cd miapp-standalone-*
   sudo ./install_dependencies.sh
   # Configurar .env
   ./start_standalone.sh
   ```

4. **Para ejecución permanente:**
   
   Ver guía completa en `DEPLOYMENT.md` para configurar:
   - Servicios systemd (auto-restart)
   - Nginx como reverse proxy
   - SSL con Let's Encrypt
   - Backup automático

### Opción 2: Docker

```bash
# Ya incluido en el paquete
docker-compose up -d
```

### Opción 3: Heroku

```bash
heroku create miapp
heroku addons:create mongolab:sandbox
git init
git add .
git commit -m "Deploy"
git push heroku main
```

---

## 💰 Costos Estimados

| Opción | Costo/Mes |
|--------|-----------|
| VPS Básico (1GB) | $5-6 USD |
| MongoDB Atlas Free | $0 USD |
| Dominio | ~$1 USD |
| **Total** | **~$6-7 USD** |

---

## 🔒 Seguridad

**Antes de poner en producción:**

1. Cambia `SECRET_KEY` en `.env`:
   ```bash
   SECRET_KEY=$(openssl rand -hex 32)
   ```

2. Configura firewall:
   ```bash
   sudo ufw allow 22    # SSH
   sudo ufw allow 80    # HTTP
   sudo ufw allow 443   # HTTPS
   sudo ufw enable
   ```

3. Configura SSL (Let's Encrypt):
   ```bash
   sudo certbot --nginx -d tu-dominio.com
   ```

---

## 📖 Documentación Completa

- **README_STANDALONE.md** - Arquitectura y características
- **DEPLOYMENT.md** - Guía completa de despliegue
- **CAMBIOS_STANDALONE.md** - Cambios realizados

---

## 🆘 Soporte

### Verificar que todo funciona:

```bash
./test_standalone.sh
```

### Ver logs:

```bash
tail -f logs/backend.log
tail -f logs/telegram.log
```

### Problemas comunes:

**Backend no inicia:**
```bash
# Ver error
tail -f logs/backend.log

# Verificar puerto
sudo lsof -i :8001
```

**Telegram Bot no responde:**
```bash
# Verificar token
curl "https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/getMe"
```

**MongoDB error:**
```bash
# Si es local
sudo systemctl start mongod

# Si es Atlas, verifica MONGO_URL en .env
```

---

## ✨ Características

### Cerebro AI
- **Perplexity Pro** (sonar-pro) como IA principal
- **OpenAI GPT-4o** como backup automático
- **22 herramientas** integradas
- Sistema de **memoria con RAG**

### Integraciones
- **Telegram Bot** con comandos en lenguaje natural
- **WooCommerce** para gestión de productos
- **Stripe** para pagos y suscripciones
- **WordPress** para publicación
- **Fal AI** para generación de imágenes

### Monetización
- Pagos únicos y suscripciones
- Programa de afiliados
- Analytics avanzados
- A/B testing
- Email marketing

---

## 🎯 ¿Qué es Standalone?

Tu aplicación **NO depende de Emergent**:

✅ **Sin límites de tiempo** - Corre 24/7  
✅ **Sin límites de sesión** - No se desconecta  
✅ **Tu propio servidor** - Control total  
✅ **Sin dependencias propietarias** - SDKs nativos  
✅ **Costos predecibles** - Solo hosting  

---

## 🚀 Próximos Pasos

1. ✅ **Ya descargado** - Tienes el paquete completo
2. 📝 **Configurar** - Edita `backend/.env`
3. 🧪 **Test local** - `./start_standalone.sh`
4. 🌐 **Deploy producción** - Ver `DEPLOYMENT.md`
5. 🎉 **Disfrutar** - Tu app autónoma 24/7

---

**¡Tu aplicación, tu servidor, tu control total! 🚀**

Para más información: `README_STANDALONE.md` y `DEPLOYMENT.md`
EOF

echo -e "${GREEN}✓${NC} Comprimiendo archivos..."

# Comprimir todo
cd /tmp
zip -r "$ZIP_FILE" "$PACKAGE_NAME" -q

# Limpiar temporal
rm -rf "$PACKAGE_DIR"

# Información del archivo
FILE_SIZE=$(du -h "$ZIP_FILE" | cut -f1)

echo ""
echo "=========================================="
echo -e "  ${GREEN}✓ Paquete Creado Exitosamente${NC}"
echo "=========================================="
echo ""
echo "📦 Archivo: $PACKAGE_NAME.zip"
echo "📊 Tamaño: $FILE_SIZE"
echo "📍 Ubicación: $ZIP_FILE"
echo ""
echo "🔽 Para descargar desde tu móvil:"
echo ""
echo "1. Usando navegador web:"
echo "   Accede a tu servidor y descarga desde:"
echo "   http://tu-servidor/$(basename $ZIP_FILE)"
echo ""
echo "2. Usando SSH desde terminal móvil (Termux):"
echo "   scp usuario@tu-servidor:$ZIP_FILE ~/Downloads/"
echo ""
echo "3. Usando app de archivos (si tienes acceso SFTP):"
echo "   Conecta por SFTP y descarga: $ZIP_FILE"
echo ""
echo "=========================================="
echo ""
