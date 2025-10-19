# 🚀 INSTALACIÓN DEL SISTEMA COMPLETO EN TU ORDENADOR

## 📦 CONTENIDO DEL PAQUETE

Este sistema incluye:
- ✅ Backend FastAPI con 83+ endpoints
- ✅ Frontend React con dashboard completo
- ✅ MongoDB como base de datos
- ✅ Sistema de pagos con Stripe
- ✅ Programa de afiliados
- ✅ Analytics avanzados
- ✅ Seguridad enterprise (rate limiting, 2FA, audit logs)
- ✅ DevOps completo (Docker, CI/CD, monitoring)
- ✅ Integración FAL AI para videos/imágenes
- ✅ Sistema de dropshipping automatizado
- ✅ Integración WooCommerce

---

## 💻 REQUISITOS DEL SISTEMA

### Opción 1: Instalación con Docker (RECOMENDADO)
- **Sistema Operativo:** Windows 10/11, macOS 10.15+, o Linux
- **Docker Desktop:** Versión 20.10+
- **RAM:** Mínimo 4GB (recomendado 8GB)
- **Disco:** 10GB libres
- **Conexión a Internet:** Para descargar dependencias

### Opción 2: Instalación Manual
- **Python:** 3.11+
- **Node.js:** 18+
- **MongoDB:** 7.0+
- **RAM:** Mínimo 4GB
- **Disco:** 5GB libres

---

## 🔥 INSTALACIÓN RÁPIDA (5 MINUTOS)

### PASO 1: Descargar el Proyecto

**Opción A - Si tienes Git:**
```bash
git clone https://github.com/tu-usuario/tu-proyecto.git
cd tu-proyecto
```

**Opción B - Descarga directa:**
1. Descarga el archivo ZIP del proyecto
2. Extrae en tu carpeta deseada
3. Abre terminal en esa carpeta

---

### PASO 2: Configurar Variables de Entorno

Copia el archivo de ejemplo:
```bash
# En Windows (PowerShell)
Copy-Item .env.example .env

# En macOS/Linux
cp .env.example .env
```

**Edita el archivo `.env`** con tus credenciales:
```bash
# Mínimo requerido para empezar:
MONGO_URL=mongodb://localhost:27017
DB_NAME=mi_tienda_db
SECRET_KEY=cambia-esto-por-algo-super-seguro-y-aleatorio

# Para usar pagos (opcional):
STRIPE_API_KEY=sk_test_tu_clave_aqui
STRIPE_PUBLISHABLE_KEY=pk_test_tu_clave_aqui

# Para usar IA (opcional):
FAL_API_KEY=tu_clave_fal_ai_aqui
OPENAI_API_KEY=sk-tu_clave_openai_aqui

# Para tu tienda WooCommerce (opcional):
WORDPRESS_URL=https://tu-tienda.com
WC_CONSUMER_KEY=ck_tu_clave
WC_CONSUMER_SECRET=cs_tu_secreto
```

---

### PASO 3: Iniciar el Sistema

#### Con Docker (MÁS FÁCIL):
```bash
# Iniciar todo con un solo comando
docker-compose up -d

# Ver logs
docker-compose logs -f

# Detener todo
docker-compose down
```

#### Sin Docker (Manual):

**Terminal 1 - MongoDB:**
```bash
mongod --dbpath ./data/db
```

**Terminal 2 - Backend:**
```bash
cd backend
pip install -r requirements.txt
uvicorn server:app --reload --host 0.0.0.0 --port 8001
```

**Terminal 3 - Frontend:**
```bash
cd frontend
npm install  # o yarn install
npm start    # o yarn start
```

---

### PASO 4: Verificar Instalación

Abre tu navegador y ve a:

1. **Frontend:** http://localhost:3000
2. **Backend API:** http://localhost:8001/api
3. **Health Check:** http://localhost:8001/api/health
4. **Documentación API:** http://localhost:8001/docs

Si ves las páginas cargando, ¡**FELICIDADES**! 🎉 El sistema está funcionando.

---

## 🎯 PRIMEROS PASOS DESPUÉS DE INSTALAR

### 1. Crear tu Primera Cuenta
```bash
curl -X POST http://localhost:8001/api/auth/register \
-H "Content-Type: application/json" \
-d '{
  "email": "tu@email.com",
  "username": "tuusuario",
  "password": "tu_password_seguro",
  "role": "admin"
}'
```

### 2. Login
Ve a http://localhost:3000 y haz login con tus credenciales.

### 3. Explorar el Dashboard
- Ver analytics
- Configurar productos
- Gestionar afiliados
- Ver estadísticas

---

## 🛠️ CONFIGURACIÓN AVANZADA

### Configurar Stripe (Pagos)
1. Ve a https://stripe.com
2. Crea cuenta o haz login
3. Obtén tus claves de test
4. Agrégalas al `.env`
5. Reinicia el backend

### Configurar FAL AI (Videos IA)
1. Tu clave ya está configurada ✅
2. Probar: http://localhost:8001/api/ai/generate-image

### Configurar WooCommerce
1. Instala WooCommerce en tu WordPress
2. Ve a WooCommerce → Settings → Advanced → REST API
3. Genera claves
4. Agrégalas al `.env`

---

## 📊 COMANDOS ÚTILES

### Ver Estado de Servicios
```bash
docker-compose ps
```

### Ver Logs en Tiempo Real
```bash
# Todos los servicios
docker-compose logs -f

# Solo backend
docker-compose logs -f backend

# Solo frontend
docker-compose logs -f frontend
```

### Reiniciar un Servicio
```bash
docker-compose restart backend
```

### Backup de Base de Datos
```bash
# Crear backup
cd backend
python database/backup.py backup

# Listar backups
python database/backup.py list
```

### Ejecutar Migraciones
```bash
cd backend
python init_db.py
```

---

## 🚨 SOLUCIÓN DE PROBLEMAS

### Error: Puerto 3000 ya en uso
```bash
# Cambiar puerto del frontend
# Editar frontend/package.json
"start": "PORT=3001 react-scripts start"
```

### Error: MongoDB no conecta
```bash
# Verificar que MongoDB está corriendo
docker-compose ps mongodb

# O si es manual:
ps aux | grep mongod
```

### Error: Dependencias no instaladas
```bash
# Backend
cd backend
pip install -r requirements.txt --upgrade

# Frontend
cd frontend
rm -rf node_modules package-lock.json
npm install
```

### Backend no inicia
```bash
# Ver logs de error
tail -n 50 /var/log/supervisor/backend.err.log

# O con Docker
docker-compose logs backend
```

---

## 🔒 SEGURIDAD PARA PRODUCCIÓN

Antes de poner en producción:

1. **Cambiar SECRET_KEY:** Genera uno nuevo aleatorio
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

2. **Usar HTTPS:** Configura SSL/TLS

3. **Cambiar passwords por defecto:**
   - MongoDB
   - Grafana
   - Admin de la app

4. **Configurar CORS correctamente:**
```bash
CORS_ORIGINS=https://tu-dominio.com
```

5. **Habilitar rate limiting:**
```bash
TRUSTED_IPS=tu.ip.de.casa
ADMIN_WHITELIST_IPS=tu.ip.de.oficina
```

---

## 📈 MONITOREO

### Grafana (Métricas)
- URL: http://localhost:3001
- User: admin
- Password: admin (cambiar en producción)

### Prometheus (Métricas detalladas)
- URL: http://localhost:9090

### Health Checks
- Backend: http://localhost:8001/api/health
- Liveness: http://localhost:8001/api/health/liveness
- Readiness: http://localhost:8001/api/health/readiness

---

## 📚 DOCUMENTACIÓN ADICIONAL

Dentro del proyecto encontrarás:
- `README.md` - Este archivo
- `INVENTARIO_COMPLETO.md` - Lista de todas las funcionalidades
- `CONFIGURACION_ENV_COMPLETA.md` - Variables de entorno detalladas
- `backend/README_DATABASE.md` - Documentación de base de datos
- `API_ENDPOINTS.md` - Lista completa de endpoints
- `DROPSHIPPING_GUIDE.md` - Guía de dropshipping

---

## 🎓 TUTORIALES Y RECURSOS

### Videos Tutoriales
1. Instalación paso a paso (proximamente)
2. Configurar tu primera tienda
3. Importar productos con SharkDropship
4. Generar contenido con IA
5. Configurar pagos con Stripe

### Comunidad y Soporte
- Discord: [enlace]
- Telegram: [enlace]
- Email: soporte@tuapp.com

---

## 🚀 PRÓXIMOS PASOS

Una vez instalado:

1. ✅ **Configurar tu tienda:** Agrega productos, configura precios
2. ✅ **Conectar Stripe:** Habilita pagos
3. ✅ **Generar contenido IA:** Crea imágenes y videos de productos
4. ✅ **Configurar afiliados:** Invita personas a promover tus productos
5. ✅ **Marketing automático:** Configura posts en redes sociales
6. ✅ **¡VENDER!** Empieza a generar ingresos

---

## 💡 TIPS PROFESIONALES

1. **Backup automático:** Configura cron job para backups diarios
2. **Monitoreo:** Revisa Grafana diariamente
3. **Logs:** Verifica logs de error semanalmente
4. **Updates:** Mantén dependencias actualizadas
5. **Testing:** Prueba en localhost antes de producción

---

## ❓ PREGUNTAS FRECUENTES

**P: ¿Necesito saber programar?**
R: No, el sistema funciona con interfaces visuales y configuración .env

**P: ¿Puedo usar en Windows?**
R: Sí, con Docker Desktop funciona perfecto

**P: ¿Cuánto cuesta mantenerlo?**
R: Gratis en localhost, ~$20-50/mes en servidor cloud

**P: ¿Necesito servidor dedicado?**
R: No, funciona en tu ordenador o servicios como AWS, DigitalOcean, Heroku

**P: ¿Funciona con mi tienda Shopify/WooCommerce?**
R: Sí, está integrado con WooCommerce. Para Shopify necesitas configuración adicional

---

## 📞 CONTACTO

¿Problemas con la instalación?
- Email: soporte@tuapp.com
- Telegram: @tusistema
- Discord: [servidor]

---

**🎉 ¡Bienvenido al sistema más completo de monetización y dropshipping con IA!**

**Versión:** 4.0.0  
**Última actualización:** 2025  
**Licencia:** MIT (o tu licencia)
