# 📥 CÓMO DESCARGAR E INSTALAR EN TU ORDENADOR

## 🎯 OPCIÓN 1: Descarga Todo el Proyecto (RECOMENDADO)

### Paso 1: Descargar el Código

Tienes 3 formas de obtener todo el código:

#### A) **GitHub (Si está en GitHub)**
```bash
git clone https://github.com/tu-usuario/tu-proyecto.git
cd tu-proyecto
```

#### B) **Descargar ZIP**
1. Abre tu navegador
2. Ve a la página del proyecto en GitHub
3. Click en "Code" → "Download ZIP"
4. Extrae el ZIP en tu carpeta deseada

#### C) **Desde esta máquina (Si tienes acceso)**
```bash
# Comprimir todo el proyecto
cd /app
tar -czf proyecto-dropshipping-ia.tar.gz \
  --exclude='node_modules' \
  --exclude='.git' \
  --exclude='__pycache__' \
  --exclude='*.pyc' \
  --exclude='.env' \
  --exclude='data' \
  --exclude='backups' \
  .

# Luego descarga: proyecto-dropshipping-ia.tar.gz
# Y extrae en tu ordenador:
tar -xzf proyecto-dropshipping-ia.tar.gz
```

---

## 🖥️ OPCIÓN 2: Instalación Paso a Paso

### Para Windows:

1. **Instalar Requisitos:**
   - Python 3.11: https://www.python.org/downloads/
   - Node.js 18: https://nodejs.org/
   - Docker Desktop: https://www.docker.com/products/docker-desktop/ (Recomendado)

2. **Descargar el proyecto** (usa una de las formas del Paso 1)

3. **Abrir PowerShell** en la carpeta del proyecto

4. **Ejecutar instalador:**
   ```bash
   install-windows.bat
   ```

5. **Editar `.env`** con tus credenciales

6. **Iniciar:**
   ```bash
   docker-compose up -d
   ```

7. **Acceder a:** http://localhost:3000

---

### Para macOS:

1. **Instalar Requisitos:**
   ```bash
   # Instalar Homebrew si no lo tienes
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   
   # Instalar dependencias
   brew install python@3.11 node mongodb-community docker
   ```

2. **Descargar el proyecto**

3. **Abrir Terminal** en la carpeta del proyecto

4. **Ejecutar instalador:**
   ```bash
   chmod +x install-mac-linux.sh
   ./install-mac-linux.sh
   ```

5. **Editar `.env`:**
   ```bash
   nano .env
   # O usa tu editor favorito
   ```

6. **Iniciar:**
   ```bash
   docker-compose up -d
   ```

7. **Acceder a:** http://localhost:3000

---

### Para Linux (Ubuntu/Debian):

1. **Instalar Requisitos:**
   ```bash
   sudo apt update
   sudo apt install -y python3.11 python3-pip nodejs npm mongodb docker.io docker-compose
   sudo systemctl start mongodb
   sudo systemctl start docker
   ```

2. **Descargar el proyecto**

3. **Abrir Terminal** en la carpeta del proyecto

4. **Ejecutar instalador:**
   ```bash
   chmod +x install-mac-linux.sh
   ./install-mac-linux.sh
   ```

5. **Editar `.env`:**
   ```bash
   nano .env
   ```

6. **Iniciar:**
   ```bash
   sudo docker-compose up -d
   ```

7. **Acceder a:** http://localhost:3000

---

## 📦 OPCIÓN 3: Solo Descargar Archivos Específicos

Si solo quieres ciertos archivos:

### Integración FAL AI:
```
backend/integrations/fal_ai.py
```

### Sistema de Precios:
```
backend/integrations/dropshipping_pricing.py
```

### WooCommerce:
```
backend/integrations/woocommerce.py
```

### Sistema Automatizado:
```
backend/integrations/automated_dropshipping.py
```

---

## 🔑 ARCHIVOS IMPORTANTES A CONFIGURAR

### 1. `.env` (Variables de Entorno)

Copia `.env.example` a `.env` y configura:

```bash
# BÁSICO (Obligatorio)
MONGO_URL=mongodb://localhost:27017
DB_NAME=mi_tienda_db
SECRET_KEY=genera-algo-aleatorio-muy-largo-aqui

# SEGURIDAD (Recomendado)
TRUSTED_IPS=127.0.0.1,tu.ip.aqui
ADMIN_WHITELIST_IPS=127.0.0.1,tu.ip.admin

# FAL AI (Para generar contenido)
FAL_API_KEY=agente90:228b46f927a226c270ece128bfeb95db

# STRIPE (Para pagos)
STRIPE_API_KEY=sk_test_tu_clave
STRIPE_PUBLISHABLE_KEY=pk_test_tu_clave

# WOOCOMMERCE (Para tu tienda)
WORDPRESS_URL=https://tu-tienda.com
WC_CONSUMER_KEY=ck_tu_clave
WC_CONSUMER_SECRET=cs_tu_secreto
```

---

## 🚀 VERIFICAR QUE TODO FUNCIONA

### Test 1: Health Check
```bash
curl http://localhost:8001/api/health
```
**Esperado:** `{"status": "healthy"}`

### Test 2: Calcular Precio
```bash
curl -X POST http://localhost:8001/api/dropshipping/calculate-price \
-H "Content-Type: application/json" \
-d '{"supplier_price": 25.00}'
```
**Esperado:** Precio calculado con margen

### Test 3: Frontend
Abre: http://localhost:3000
**Esperado:** Ver la aplicación cargando

---

## 📁 ESTRUCTURA DEL PROYECTO

```
tu-proyecto/
├── backend/               # API FastAPI
│   ├── integrations/     # FAL AI, WooCommerce, Pricing
│   ├── security/         # Rate limiting, 2FA, etc.
│   ├── database/         # Migraciones, backups
│   ├── monitoring/       # Health checks, metrics
│   ├── server.py         # Servidor principal
│   ├── requirements.txt  # Dependencias Python
│   └── .env             # Variables de entorno
├── frontend/             # React App
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── .env
├── monitoring/           # Prometheus, Grafana configs
├── docker-compose.yml    # Orquestación de servicios
├── install-windows.bat   # Instalador Windows
├── install-mac-linux.sh  # Instalador macOS/Linux
├── start.sh             # Script de inicio
├── README.md            # Documentación principal
├── INSTALACION_COMPLETA.md
├── GUIA_RAPIDA.md
└── INVENTARIO_COMPLETO.md
```

---

## 🎓 RECURSOS DE APRENDIZAJE

### Videos Tutoriales (Proximamente)
1. Instalación en Windows
2. Instalación en macOS
3. Configurar tu primera tienda
4. Importar productos con SharkDropship
5. Generar contenido con IA
6. Configurar pagos con Stripe

### Documentación
- **INSTALACION_COMPLETA.md** - Todo sobre instalación
- **GUIA_RAPIDA.md** - Inicio en 10 minutos
- **INVENTARIO_COMPLETO.md** - Todas las features
- **API Docs** - http://localhost:8001/docs

---

## 🆘 PROBLEMAS COMUNES

### "No puedo descargar el proyecto"
- Usa la opción de ZIP desde GitHub
- O contacta para que te envíe el archivo comprimido

### "Python no está instalado"
- Windows: https://www.python.org/downloads/
- macOS: `brew install python@3.11`
- Linux: `sudo apt install python3.11`

### "Docker no funciona"
- Windows/Mac: Descarga Docker Desktop
- Linux: `sudo apt install docker.io docker-compose`
- Reinicia tu ordenador después de instalar

### "MongoDB no conecta"
- Con Docker: `docker-compose ps mongodb`
- Sin Docker: `mongod --dbpath ./data/db`

### "Frontend no carga"
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
npm start
```

---

## 💬 SOPORTE

¿Problemas con la descarga o instalación?

- **Email:** soporte@tuapp.com
- **Telegram:** @tusistema
- **Discord:** [Unirse al servidor]

---

## ✅ CHECKLIST POST-INSTALACIÓN

Después de instalar, verifica:

- [ ] Backend accesible en http://localhost:8001/api
- [ ] Frontend accesible en http://localhost:3000
- [ ] MongoDB corriendo (docker-compose ps mongodb)
- [ ] Health check OK (http://localhost:8001/api/health)
- [ ] Archivo .env configurado con tus credenciales
- [ ] Puedes hacer login en el frontend
- [ ] Endpoints de API funcionan (http://localhost:8001/docs)

---

## 🎉 ¡LISTO!

Una vez instalado, puedes:

1. **Importar productos** con SharkDropship
2. **Calcular precios** automáticamente
3. **Generar contenido IA** (imágenes + videos)
4. **Configurar pagos** con Stripe
5. **Gestionar afiliados**
6. **Ver analytics**
7. **¡EMPEZAR A VENDER!**

---

**🚀 Tiempo estimado de instalación: 10-15 minutos**

**💰 ROI estimado: €7,500+/mes con 29 productos**

**🎯 ¡Éxito en tu negocio!**
