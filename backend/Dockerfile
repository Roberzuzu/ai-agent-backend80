# syntax=docker/dockerfile:1
FROM python:3.11-slim AS base
WORKDIR /app
# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*
# Copy and install Python dependencies
COPY requirements_standalone.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt
# Copy application code (copies from backend context)
COPY . /app
# Expose port
EXPOSE 8000
# Health check
HEALTHCHECK --interval=30s --timeout=5s --retries=5 \
    CMD curl -f http://localhost:8000/api/health || exit 1
# Start server
CMD uvicorn server:app --host 0.0.0.0 --port ${PORT:-8000}
