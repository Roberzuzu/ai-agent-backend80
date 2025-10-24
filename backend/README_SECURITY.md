# 🔒 Guía de Seguridad - Gestión de Credenciales

## ⚠️ Información de Seguridad Crítica

Este documento describe cómo gestionar de forma segura las credenciales y tokens de autenticación para el proyecto AI Agent Backend.

---

## 📝 Configuración del Archivo .env

### Paso 1: Crear el Archivo .env

1. **Copiar la plantilla:**
   ```bash
   cp .env.example .env
   ```

2. **Editar el archivo .env** con tus credenciales reales:
   ```bash
   nano .env  # o usa tu editor preferido
   ```

3. **Añadir tus tokens y credenciales:**
   - Reemplaza los valores vacíos con tus credenciales reales
   - No incluyas espacios alrededor del signo igual (=)
   - No uses comillas a menos que sean parte de la credencial

### Paso 2: Verificar .gitignore

El archivo `.gitignore` en la raíz del proyecto **YA INCLUYE** las siguientes entradas:

```
*.env
*.env.*
.env
.env.local
.env.*.local
```

Esto garantiza que tu archivo `.env` **NUNCA** será rastreado por Git ni se subirá al repositorio público.

---

## 🔑 Credenciales Requeridas

### 1. Instagram Access Token
- **Obtener desde:** [Meta for Developers](https://developers.facebook.com/)
- **API:** Instagram Basic Display API o Instagram Graph API
- **Permisos necesarios:** `instagram_basic`, `instagram_content_publish`
- **Duración:** Los tokens de Instagram suelen expirar cada 60 días

### 2. Facebook Access Token
- **Obtener desde:** [Meta for Developers - Graph API Explorer](https://developers.facebook.com/tools/explorer/)
- **Permisos necesarios:** `pages_manage_posts`, `pages_read_engagement`
- **Nota:** Usa tokens de página, no tokens de usuario personal
- **Duración:** Los tokens de larga duración expiran cada 60 días

### 3. Google AI Studio API Key (Gemini)
- **Obtener desde:** [Google AI Studio](https://makersuite.google.com/app/apikey)
- **Servicios:** API de Gemini para procesamiento de IA
- **Límites:** Verifica los límites de cuota en Google Cloud Console

### 4. WordPress Credentials
- **Username:** Tu nombre de usuario de WordPress
- **Password:** **RECOMENDADO** usar Application Password en lugar de tu contraseña principal
  - Ve a: WordPress Admin > Usuarios > Tu perfil > Application Passwords
  - Genera una nueva contraseña específica para esta aplicación
  - Esto es más seguro y te permite revocar el acceso sin cambiar tu contraseña principal

---

## ✅ Mejores Prácticas de Seguridad

### DO ✅
- ✅ **Mantener** el archivo `.env` en tu servidor local/producción
- ✅ **Usar** Application Passwords para WordPress
- ✅ **Rotar** tokens periódicamente (cada 30-60 días)
- ✅ **Verificar** que `.env` está en `.gitignore`
- ✅ **Hacer backup** de tus credenciales en un gestor de contraseñas seguro (1Password, LastPass, Bitwarden)
- ✅ **Usar** variables de entorno en producción (Heroku Config Vars, Railway Variables, etc.)
- ✅ **Documentar** fecha de creación y expiración de tokens
- ✅ **Limitar** permisos de tokens al mínimo necesario

### DON'T ❌
- ❌ **NUNCA** subir el archivo `.env` a GitHub o repositorios públicos
- ❌ **NUNCA** compartir credenciales por email, Slack, o mensajes no cifrados
- ❌ **NUNCA** hardcodear credenciales directamente en el código
- ❌ **NUNCA** usar la misma API key para desarrollo y producción
- ❌ **NUNCA** hacer commits con credenciales en el historial de Git
- ❌ **NO** tomar capturas de pantalla del archivo `.env`

---

## 🛠️ Cómo Usar las Credenciales en el Código

### Python con python-dotenv

```python
import os
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

# Acceder a las credenciales
instagram_token = os.getenv('INSTAGRAM_TOKEN')
facebook_token = os.getenv('FACEBOOK_TOKEN')
google_api_key = os.getenv('GOOGLE_AI_STUDIO_API_KEY')
wordpress_user = os.getenv('WORDPRESS_USERNAME')
wordpress_pass = os.getenv('WORDPRESS_PASSWORD')
```

### Instalación de python-dotenv

```bash
pip install python-dotenv
```

---

## 🚨 Qué Hacer Si Se Exponen Credenciales

Si accidentalmente subes credenciales a GitHub:

1. **Revocar inmediatamente** todos los tokens expuestos:
   - Instagram/Facebook: Ve a Meta for Developers > App Dashboard > Revoke tokens
   - Google AI: Ve a Google Cloud Console > Credentials > Delete key
   - WordPress: Revoca la Application Password

2. **Generar nuevas credenciales** para todos los servicios afectados

3. **Actualizar el archivo .env** con las nuevas credenciales

4. **Limpiar el historial de Git** si las credenciales están en commits anteriores:
   ```bash
   # Usa BFG Repo-Cleaner o git filter-branch
   # Consulta: https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository
   ```

5. **Cambiar todas las contraseñas relacionadas**

6. **Monitorear** las cuentas por actividad sospechosa

---

## 📊 Monitorización y Mantenimiento

### Calendario de Mantenimiento Recomendado

- **Cada 30 días:** Verificar estado de tokens (expiración)
- **Cada 60 días:** Rotar todos los tokens y credenciales
- **Cada 90 días:** Auditar permisos de aplicaciones conectadas
- **Trimestral:** Revisar logs de acceso y actividad sospechosa

### Verificar Estado de Tokens

```python
# Ejemplo para verificar expiración de tokens de Facebook/Instagram
import requests

token = os.getenv('FACEBOOK_TOKEN')
response = requests.get(
    f'https://graph.facebook.com/debug_token?input_token={token}&access_token={token}'
)
token_info = response.json()
print(f"Expira en: {token_info['data']['expires_at']}")
```

---

## 📞 Recursos Adicionales

- [Meta for Developers - Security Best Practices](https://developers.facebook.com/docs/development/release/security-best-practices)
- [Google Cloud Security Best Practices](https://cloud.google.com/security/best-practices)
- [WordPress Application Passwords Documentation](https://make.wordpress.org/core/2020/11/05/application-passwords-integration-guide/)
- [OWASP API Security Top 10](https://owasp.org/www-project-api-security/)

---

## ❓ Preguntas Frecuentes (FAQ)

### ¿Por qué no puedo ver el archivo .env en el repositorio?
El archivo `.env` está intencionalmente excluido del repositorio público por razones de seguridad. Cada desarrollador debe crear su propio archivo `.env` local basado en `.env.example`.

### ¿Cómo comparto credenciales con mi equipo?
Usa un gestor de contraseñas corporativo (1Password Teams, LastPass Enterprise) o un sistema de gestión de secretos (HashiCorp Vault, AWS Secrets Manager).

### ¿Qué hago si olvido mis credenciales?
No hay problema. Simplemente genera nuevas credenciales desde las respectivas plataformas y actualiza tu archivo `.env`.

### ¿Puedo usar el mismo .env en desarrollo y producción?
**NO.** Debes usar credenciales diferentes para desarrollo, staging y producción. Esto limita el daño en caso de exposición.

---

## 📌 Recordatorio Final

> **⚠️ El archivo `.env` contiene credenciales extremadamente sensibles.**
> 
> **NUNCA lo subas a GitHub ni lo compartas públicamente.**
> 
> **Tu seguridad y la de los usuarios depende de mantener estas credenciales protegidas.**

---

Última actualización: Octubre 2025
