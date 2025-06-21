# Dockerfile para Hefest
# Imagen optimizada para producción

# Stage 1: Builder
FROM python:3.10-slim as builder

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    pkg-config \
    libxcb1-dev \
    libxkbcommon-x11-0 \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libxcb-xinerama0 \
    && rm -rf /var/lib/apt/lists/*

# Crear directorio de trabajo
WORKDIR /app

# Copiar archivos de dependencias
COPY requirements.txt pyproject.toml ./

# Instalar dependencias Python
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Stage 2: Production
FROM python:3.10-slim

# Metadatos
LABEL maintainer="Hefest Development Team <dev@hefest.com>"
LABEL version="0.0.10"
LABEL description="Sistema Integral de Hostelería y Hospedería"

# Instalar dependencias runtime
RUN apt-get update && apt-get install -y \
    libxcb1 \
    libxkbcommon-x11-0 \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libxcb-xinerama0 \
    xvfb \
    && rm -rf /var/lib/apt/lists/*

# Crear usuario no-root
RUN useradd --create-home --shell /bin/bash hefest

# Crear directorios de trabajo
WORKDIR /app
RUN mkdir -p /app/data /app/logs /app/config /app/assets && \
    chown -R hefest:hefest /app

# Copiar dependencias instaladas
COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copiar código de la aplicación
COPY --chown=hefest:hefest . .

# Instalar la aplicación
RUN pip install -e .

# Configurar entorno
ENV PYTHONPATH=/app/src
ENV HEFEST_ENV=production
ENV QT_QPA_PLATFORM=offscreen
ENV DISPLAY=:99

# Cambiar a usuario no-root
USER hefest

# Exponer puerto (si se implementa API web)
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import src.main; print('OK')" || exit 1

# Comando por defecto
CMD ["xvfb-run", "-a", "python", "main.py"]
