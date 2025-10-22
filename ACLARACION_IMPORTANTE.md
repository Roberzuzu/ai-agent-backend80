# ⚠️ ACLARACIÓN IMPORTANTE - NO Confundir Archivos

## 🚫 ERROR COMÚN

Estás intentando instalar el backend como plugin de WordPress. **NO funciona así.**

---

## 📦 Archivos y Su Uso Correcto

### ✅ PLUGINS de WordPress (Instalar desde WP Admin)

**1. Plugin Chat Widget:**
```
Archivo: ai-chat-admin-only.zip (4.3 KB)
Instalación: WordPress Admin → Plugins → Subir
Propósito: Mostrar el widget de chat en WordPress
```

**2. Plugin Procesador de Productos:**
```
Archivo: ai-woocommerce-agent-minimal.zip (3.7 KB)
Instalación: WordPress Admin → Plugins → Subir
Propósito: Procesar productos con AI desde admin
```

---

### ❌ NO es Plugin de WordPress (Instalar por SSH)

**Backend Standalone:**
```
Archivo: miapp-standalone-20251022-142042.zip (637 KB)
Instalación: SSH en el servidor (NO desde WordPress)
Propósito: Servidor backend completo con todas las funcionalidades
```

**Este archivo contiene:**
- Backend FastAPI (Python)
- Frontend React
- Bot de Telegram
- Todas las herramientas AI

**NO se instala como plugin WordPress!**

---

## ✅ Cómo Instalar Correctamente

### Paso 1: Instalar Plugin Chat en WordPress

```
1. Descarga: ai-chat-admin-only.zip (4.3 KB)
2. WordPress Admin → Plugins → Añadir nuevo → Subir
3. Selecciona: ai-chat-admin-only.zip
4. Instalar y Activar
```

### Paso 2: Desplegar Backend en el Servidor

**Necesitas acceso SSH:**

```bash
# Conectar al servidor
ssh productos@herramientasyaccesorios.store

# Subir el archivo (desde donde está /app)
scp /app/miapp-standalone-20251022-142042.zip productos@herramientasyaccesorios.store:~/

# O descargarlo directamente en el servidor
wget [URL-donde-esté-el-archivo]

# Descomprimir
unzip miapp-standalone-20251022-142042.zip

# Entrar al directorio
cd miapp-standalone-20251022-142042

# Instalar dependencias y configurar
./install-herramientas.sh

# Configurar variables
nano backend/.env

# Iniciar servicios
sudo systemctl start herramientas-backend
```

---

## 🎯 Resumen Visual

```
WordPress Admin (Interfaz Web)
├── Plugin 1: ai-chat-admin-only.zip ✅
├── Plugin 2: ai-woocommerce-agent-minimal.zip ✅
└── ❌ NO: miapp-standalone-*.zip (este NO va aquí)

Servidor SSH (Terminal)
└── ✅ SÍ: miapp-standalone-*.zip (este va aquí)
    ├── Backend FastAPI
    ├── Frontend React
    └── Bot Telegram
```

---

## 💡 ¿Qué Hacer Ahora?

### Opción 1: Tienes Acceso SSH

Si tienes acceso SSH a tu servidor:

1. Conecta por SSH
2. Sube el archivo miapp-standalone-*.zip
3. Sigue la guía de instalación por terminal

### Opción 2: NO Tienes Acceso SSH

Si NO tienes acceso SSH:

1. Solo usa el plugin: **ai-chat-admin-only.zip**
2. Contacta a tu proveedor de hosting para:
   - Solicitar acceso SSH
   - O que ellos instalen el backend por ti

### Opción 3: Usar Solo Procesador Simple

Si no quieres/puedes desplegar el backend:

1. Usa solo: **ai-woocommerce-agent-minimal.zip**
2. Este funciona sin backend
3. Procesa productos con APIs directas
4. Pero NO tendrás chat ni upload de archivos

---

## 🔑 Acceso SSH Requerido

Para el **chat completo con archivos e imágenes**, necesitas:

✅ Acceso SSH al servidor  
✅ Permisos sudo  
✅ Python 3.10+  
✅ Node.js 18+  

Si tu hosting no permite esto, considera:
- Cambiar a VPS (DigitalOcean, Linode)
- O contratar hosting con acceso SSH

---

## 📞 ¿Qué Necesitas?

**Responde:**

A) Tengo acceso SSH → Te guío paso a paso
B) NO tengo SSH pero puedo obtenerlo → Te ayudo a configurarlo
C) NO tengo SSH y no puedo obtenerlo → Usamos solo plugin simple
D) Necesito ayuda para acceder por SSH → Te explico cómo

**Dime cuál es tu caso y continúo desde ahí.**
