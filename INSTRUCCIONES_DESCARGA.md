# 📦 Descargar Paquete Standalone

## ✅ Archivo Listo

**Nombre:** `ai-agent-standalone.zip`  
**Tamaño:** 529 KB  
**Ubicación:** `/app/ai-agent-standalone.zip`

---

## 📥 Métodos de Descarga

### Método 1: Servidor HTTP Temporal (Más Fácil)

```bash
# En el servidor donde está /app
cd /app
python3 -m http.server 8080
```

Luego en tu navegador:
```
http://IP-DEL-SERVIDOR:8080/ai-agent-standalone.zip
```

**Para detener:** Presiona `Ctrl+C`

---

### Método 2: SCP (Recomendado si tienes SSH)

```bash
# Desde tu computadora local
scp usuario@ip-servidor:/app/ai-agent-standalone.zip ~/Downloads/
```

Ejemplo:
```bash
scp productos@178.16.128.200:/app/ai-agent-standalone.zip ~/Downloads/
```

---

### Método 3: SFTP

```bash
# Conectar con SFTP
sftp usuario@ip-servidor

# Descargar archivo
get /app/ai-agent-standalone.zip

# Salir
exit
```

---

### Método 4: Copiar a ubicación web (si tienes Nginx/Apache)

```bash
# Copiar a directorio web
sudo cp /app/ai-agent-standalone.zip /var/www/html/

# Acceder desde navegador
http://tu-dominio.com/ai-agent-standalone.zip
```

---

## 🚀 Después de Descargar

1. **Transferir al servidor donde está WordPress**
   ```bash
   scp ai-agent-standalone.zip productos@herramientasyaccesorios.store:~/
   ```

2. **Conectar por SSH al servidor**
   ```bash
   ssh productos@herramientasyaccesorios.store
   ```

3. **Descomprimir**
   ```bash
   unzip ai-agent-standalone.zip
   cd standalone-package
   ```

4. **Ejecutar instalador**
   ```bash
   chmod +x install.sh
   ./install.sh
   ```

---

## 📝 Configuración Después de Instalar

### 1. Editar archivo .env

```bash
cd ~/ai-agent-backend/backend
nano .env
```

**Configuración mínima necesaria:**

```bash
# MongoDB (elige una opción)
MONGO_URL="mongodb://localhost:27017"
# O usa MongoDB Atlas (gratis): 
# MONGO_URL="mongodb+srv://user:pass@cluster.mongodb.net"

# OpenAI (necesario para el AI)
OPENAI_API_KEY="sk-proj-..."

# Perplexity (cerebro principal del AI)
PERPLEXITY_API_KEY="pplx-..."

# WordPress
WORDPRESS_URL="https://herramientasyaccesorios.store"
WC_CONSUMER_KEY="ck_..."
WC_CONSUMER_SECRET="cs_..."
```

### 2. Reiniciar backend

```bash
sudo systemctl restart ai-agent-backend
```

### 3. Verificar que funciona

```bash
curl http://localhost:8001/api/health
```

### 4. Configurar en WordPress

**WordPress Admin → AI Chat Admin → Settings**

```
Backend URL: http://localhost:8001
O si tienes Nginx: https://herramientasyaccesorios.store/api
```

---

## 🔑 Obtener API Keys (Si aún no las tienes)

### OpenAI
1. Ir a: https://platform.openai.com/api-keys
2. Crear "New secret key"
3. Copiar: `sk-proj-...`

### Perplexity
1. Ir a: https://www.perplexity.ai/settings/api
2. Generar API key
3. Copiar: `pplx-...`

### WooCommerce
1. WordPress Admin → WooCommerce → Settings → Advanced → REST API
2. Crear nueva key
3. Copiar Consumer Key y Consumer Secret

---

## ❓ Problemas Comunes

### "No puedo descargar el archivo"

Usa el método 1 (servidor HTTP temporal) o método 2 (SCP)

### "Archivo muy grande para descargar"

El archivo es solo 529 KB, debería descargar rápido.

### "No tengo acceso SSH"

Usa el panel de control de tu hosting para acceder por SFTP o File Manager.

---

## 🆘 Ayuda

Si tienes problemas con la descarga o instalación, avísame y te ayudo paso a paso.

---

**¡Todo listo para desplegar! 🚀**
