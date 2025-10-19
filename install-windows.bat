@echo off
REM ====================================
REM INSTALADOR AUTOMATICO - WINDOWS
REM Sistema de Dropshipping con IA
REM ====================================

echo.
echo ========================================
echo   INSTALADOR AUTOMATICO
echo   Sistema de Dropshipping con IA
echo ========================================
echo.

REM Verificar si Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python no esta instalado
    echo Por favor instala Python 3.11+ desde https://www.python.org
    pause
    exit /b 1
)

REM Verificar si Node.js está instalado
node --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Node.js no esta instalado
    echo Por favor instala Node.js 18+ desde https://nodejs.org
    pause
    exit /b 1
)

REM Verificar si MongoDB está instalado
mongod --version >nul 2>&1
if errorlevel 1 (
    echo [ADVERTENCIA] MongoDB no detectado
    echo Puedes instalarlo desde https://www.mongodb.com/try/download/community
    echo O usar Docker (recomendado)
)

echo.
echo [1/5] Configurando variables de entorno...
if not exist .env (
    if exist .env.example (
        copy .env.example .env
        echo [OK] Archivo .env creado desde .env.example
        echo.
        echo IMPORTANTE: Edita el archivo .env con tus credenciales
        echo.
        pause
    ) else (
        echo [ERROR] No se encuentra .env.example
        pause
        exit /b 1
    )
) else (
    echo [OK] Archivo .env ya existe
)

echo.
echo [2/5] Instalando dependencias del Backend...
cd backend
pip install -r requirements.txt
if errorlevel 1 (
    echo [ERROR] Fallo al instalar dependencias del backend
    pause
    exit /b 1
)
echo [OK] Backend instalado correctamente
cd ..

echo.
echo [3/5] Instalando dependencias del Frontend...
cd frontend
call npm install
if errorlevel 1 (
    echo [ERROR] Fallo al instalar dependencias del frontend
    pause
    exit /b 1
)
echo [OK] Frontend instalado correctamente
cd ..

echo.
echo [4/5] Creando directorios necesarios...
if not exist data\db mkdir data\db
if not exist backups mkdir backups
if not exist logs mkdir logs
echo [OK] Directorios creados

echo.
echo [5/5] Inicializando base de datos...
cd backend
python init_db.py
if errorlevel 1 (
    echo [ADVERTENCIA] No se pudo inicializar la BD
    echo Asegurate de que MongoDB este corriendo
)
cd ..

echo.
echo ========================================
echo   INSTALACION COMPLETADA!
echo ========================================
echo.
echo Para iniciar el sistema:
echo.
echo   Opcion 1 - Docker (Recomendado):
echo   docker-compose up -d
echo.
echo   Opcion 2 - Manual:
echo   1. Inicia MongoDB:  mongod --dbpath ./data/db
echo   2. Inicia Backend:  cd backend ^&^& python -m uvicorn server:app --reload
echo   3. Inicia Frontend: cd frontend ^&^& npm start
echo.
echo Accede a:
echo   - Frontend: http://localhost:3000
echo   - Backend:  http://localhost:8001/api
echo   - Docs:     http://localhost:8001/docs
echo.
echo ========================================
echo.
pause
