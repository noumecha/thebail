# Dockerfile
# ============================================
# Stage 1: Builder - Compilation des dépendances
# ============================================
FROM python:3.11-slim AS builder

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

# Installer les dépendances de build
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    make \
    pkg-config \
    default-libmysqlclient-dev \
    libcairo2-dev \
    libpango1.0-dev \
    libffi-dev \
    libjpeg-dev \
    libpng-dev \
    libtiff-dev \
    libwebp-dev \
    zlib1g-dev \
    libxml2-dev \
    libxslt1-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copier et installer les dépendances Python
COPY requirements.txt .
RUN pip install --upgrade pip setuptools wheel && \
    pip install --prefix=/install -r requirements.txt

# ============================================
# Stage 2: Runtime - Image finale
# ============================================
FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    NODE_ENV=production

# Installer uniquement les dépendances runtime
RUN apt-get update && apt-get install -y \
    curl \
    netcat-openbsd \
    default-libmysqlclient-dev \
    libcairo2 \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libffi8 \
    shared-mime-info \
    fonts-liberation \
    fonts-dejavu-core \
    libjpeg62-turbo \
    libpng16-16 \
    libtiff6 \
    libwebp7 \
    libxml2 \
    libxslt1.1 \
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copier les packages Python depuis le builder
COPY --from=builder /install /usr/local

# Copier les fichiers de dépendances Node.js
COPY src/package*.json ./src/
WORKDIR /app/src
RUN npm install

# build prod (génère assets/vendor)
RUN npm run build

# Retour au répertoire principal
WORKDIR /app

# Copier tout le projet
COPY . .

# Créer les répertoires
RUN mkdir -p /app/staticfiles /app/uploads

EXPOSE 8000

COPY docker/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
