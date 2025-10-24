# Compilación de varias etapas para una imagen de producción optimizada

# Etapa 1: Constructor
DESDE python:3.11-slim como constructor

WORKDIR /aplicación

# Instalar dependencias de compilación
EJECUTAR apt-get update && apt-get install -y \
    gcc \
    g++ \
    hacer \
    libffi-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/listas/*

# Copiar requisitos e instalar dependencias
COPIA requisitos.txt .
EJECUTAR pip install --user --no-cache-dir -r requirements.txt

# Etapa 2: Producción
DESDE python:3.11-slim como producción

WORKDIR /aplicación

# Instalar solo dependencias de tiempo de ejecución
EJECUTAR apt-get update && apt-get install -y \
    rizo \
    && rm -rf /var/lib/apt/listas/*

# Crear un usuario no root
EJECUTAR useradd -m -u 1000 appuser && \
    mkdir -p /var/log/app && \
    chown -R appuser:appuser /var/log/app

# Copiar paquetes de Python desde el generador
COPIA --from=builder /root/.local /home/appuser/.local

# Copiar el código de la aplicación
COPIA --chown=appuser:appuser . .

# Establecer variables de entorno
RUTA DE ENV=/home/appuser/.local/bin:$RUTA \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    NIVEL_DE_REGISTRO=INFO

# Cambiar a usuario no root
USUARIO appuser

# Exponer puerto
EXPONER 8001

# Chequeo de salud
CONTROL DE ESTADO --intervalo=30s --tiempo de espera=10s --periodo de inicio=40s --reintentos=3 \
    CMD curl -f http://localhost:8001/api/health/liveness || salida 1

# Ejecutar aplicación
CMD ["uvicorn", "servidor:app", "--host", "0.0.0.0", "--puerto", "8001", "--trabajadores", "4"]
