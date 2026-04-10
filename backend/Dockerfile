# ============================================================
#  ENGLISH GRAMMAR CHATBOT — Backend Dockerfile
#  File: backend/Dockerfile
# ============================================================

# ----------------------------------------------------------
# STAGE 1: BASE
# ----------------------------------------------------------
FROM python:3.11-slim AS base

# Set environment Python
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# ----------------------------------------------------------
# STAGE 2: DEVELOPMENT
# Target ini dipakai di docker-compose.dev.yml
# Source code di-mount via volume, tidak di-copy
# ----------------------------------------------------------
FROM base AS development

ENV APP_ENV=development \
    DEBUG=true

# Install dev tools tambahan
RUN pip install pytest pytest-asyncio httpx

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

# ----------------------------------------------------------
# STAGE 3: PRODUCTION
# Target ini dipakai di docker-compose.yml
# Source code di-copy ke dalam image
# ----------------------------------------------------------
FROM base AS production

ENV APP_ENV=production \
    DEBUG=false

# Copy seluruh source code backend
COPY . .

# Buat folder logs
RUN mkdir -p logs

# Jalankan sebagai non-root user (keamanan)
RUN addgroup --system appgroup && \
    adduser --system --ingroup appgroup appuser && \
    chown -R appuser:appgroup /app

USER appuser

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]