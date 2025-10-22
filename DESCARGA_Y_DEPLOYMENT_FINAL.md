# 🚀 DESCARGA Y DEPLOYMENT FINAL - 3 OPCIONES

## ⚠️ IMPORTANTE
No puedo conectarme directamente a tu servidor (SSH puerto 22 cerrado/filtrado).
Te doy 3 opciones para descargar y desplegar:

---

## 📦 ARCHIVO LISTO
- **Ubicación:** `/app/ai-agent-standalone.zip`
- **Tamaño:** 529 KB
- **Contenido:** Backend completo + Frontend + Instalador automático

---

## ✅ OPCIÓN 1: Usar Code-Server (MÁS FÁCIL)

### Paso 1: Descargar desde Code-Server
1. Abre Code-Server en tu navegador
2. En el explorador de archivos, navega a `/app`
3. Click derecho en `ai-agent-standalone.zip`
4. Selecciona "Download"
5. El archivo se descargará a tu computadora

### Paso 2: Subir a tu Servidor
```bash
# Desde tu computadora
scp ai-agent-standalone.zip productos@herramientasyaccesorios.store:~/
```

### Paso 3: Conectar y Desplegar
```bash
ssh productos@herramientasyaccesorios.store
cd ~
unzip ai-agent-standalone.zip
cd standalone-package
chmod +x install.sh
./install.sh
```

---

## ✅ OPCIÓN 2: Descarga Directa con SFTP

### Usando FileZilla (GUI)
1. Descargar FileZilla: https://filezilla-project.org
2. Conectar:
   - Host: herramientasyaccesorios.store
   - Usuario: productos
   - Password: oFnXqP3(EITAWfd%rUzIkW%i
   - Puerto: 22
3. Navegar a `/app`
4. Descargar `ai-agent-standalone.zip` arrastrándolo a tu computadora
5. Subir el archivo al servidor en la carpeta home

### Usando SFTP desde terminal
```bash
sftp productos@herramientasyaccesorios.store
# Contraseña: oFnXqP3(EITAWfd%rUzIkW%i

# Descargar
get /app/ai-agent-standalone.zip

# Salir
exit
```

---

## ✅ OPCIÓN 3: Crear Servidor Temporal AQUÍ

### Desde este servidor (Emergent)
```bash
# Terminal 1: Iniciar servidor HTTP
cd /app
python3 -m http.server 8888

# Aparecerá: Serving HTTP on 0.0.0.0 port 8888
```

### Desde tu computadora
```bash
# Reemplaza IP-DEL-SERVIDOR con la IP de Emergent
wget http://IP-DEL-SERVIDOR:8888/ai-agent-standalone.zip

# O desde navegador:
# http://IP-DEL-SERVIDOR:8888/ai-agent-standalone.zip
```

---

## 🔧 DEPLOYMENT AUTOMÁTICO

Una vez tengas el archivo `ai-agent-standalone.zip` en tu servidor de WordPress:

```bash
# Conectar al servidor
ssh productos@herramientasyaccesorios.store

# Descomprimir
unzip ai-agent-standalone.zip
cd standalone-package

# Ejecutar instalador automático
chmod +x install.sh
./install.sh
```

### El instalador hace TODO automáticamente:
1. ✅ Verifica Python, Node.js
2. ✅ Crea directorio `~/ai-agent-backend`
3. ✅ Instala dependencias Python
4. ✅ Copia archivos `.env` con tus API keys
5. ✅ Crea servicio systemd
6. ✅ Inicia el backend
7. ✅ Verifica que funcione

---

## 📝 DESPUÉS DE LA INSTALACIÓN

### 1. Verificar que el Backend funciona
```bash
curl http://localhost:8001/api/health
```

**Debería responder:**
```json
{"status":"healthy", ...}
```

### 2. Ver logs
```bash
sudo journalctl -u ai-agent-backend -f
```

### 3. Configurar WordPress

**WordPress Admin → AI Chat Admin → Settings**

```
Backend URL: http://localhost:8001
```

✅ Marcar: Mostrar Widget  
✅ Marcar: Solo Administrador

**Click: 🔌 Probar Backend**

Debería mostrar: ✅ Backend conectado correctamente!

---

## 🌐 URLs FINALES

**Backend en tu servidor:**
```
http://localhost:8001              # Local en el servidor
http://herramientasyaccesorios.store:8001  # Acceso externo (si abres puerto)
```

**Para WordPress:**
```
Backend URL: http://localhost:8001
```

---

## 🔑 API KEYS YA CONFIGURADAS

El archivo `.env` incluye TODAS tus API keys:
- ✅ OpenAI
- ✅ Perplexity
- ✅ Stripe
- ✅ Telegram Bot
- ✅ WordPress/WooCommerce
- ✅ FAL AI

**No necesitas configurar nada más, todo está listo.**

---

## 🎯 RESUMEN

1. **Descargar** `ai-agent-standalone.zip` (usa Opción 1, 2 o 3)
2. **Transferir** al servidor de WordPress
3. **Ejecutar** `./install.sh`
4. **Verificar** con `curl http://localhost:8001/api/health`
5. **Configurar** WordPress con URL: `http://localhost:8001`
6. **¡Listo!** Sistema funcionando 24/7

---

## ❓ SI TIENES PROBLEMAS

### Backend no inicia
```bash
sudo journalctl -u ai-agent-backend -n 50
```

### Puerto ocupado
```bash
sudo lsof -i :8001
sudo systemctl restart ai-agent-backend
```

### Ver estado
```bash
sudo systemctl status ai-agent-backend
```

---

## 📞 INFORMACIÓN DEL SERVIDOR

**Tu servidor WordPress:**
- Host: herramientasyaccesorios.store
- Usuario SSH: productos
- Password: oFnXqP3(EITAWfd%rUzIkW%i

**Archivo standalone:**
- Ubicación: `/app/ai-agent-standalone.zip`
- Tamaño: 529 KB

---

**¡Todo listo para desplegar! 🚀**

**El backend funcionará permanentemente en TU servidor, NO en Emergent.**
