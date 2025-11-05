# syntax=docker/dockerfile:1
FROM python:3.11-slim AS base

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY backend/requirements_standalone.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy main.py (entry point)
COPY main.py /app/

# Copy backend code
COPY backend /app/backend

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=5s --retries=5 \
    CMD curl -f http://localhost:8000/api/health || exit 1

# Start unified service (FastAPI + Telegram Bot)
CMD python main.py
