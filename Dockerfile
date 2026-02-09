# Dockerfile
FROM python:3.11-slim

# Variables d'environnement
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    NODE_ENV=production

# Installer Node.js et TOUTES les dépendances système nécessaires
RUN apt-get update && apt-get install -y \
    # Outils de base
    curl \
    gcc \
    g++ \
    make \
    netcat-openbsd \
    pkg-config \
    # MySQL
    default-libmysqlclient-dev \
    # Cairo et dépendances pour pycairo, weasyprint, reportlab
    libcairo2-dev \
    libpango1.0-dev \
    libgdk-pixbuf2.0-dev \
    libffi-dev \
    shared-mime-info \
    # Fonts pour PDF
    fonts-liberation \
    fonts-dejavu-core \
    # Librairies pour Pillow
    libjpeg-dev \
    libpng-dev \
    libtiff-dev \
    libwebp-dev \
    zlib1g-dev \
    # Librairies pour lxml
    libxml2-dev \
    libxslt1-dev \
    # Installer Node.js
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    # Nettoyer le cache
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Créer le répertoire de travail
WORKDIR /app

# Copier les fichiers de dépendances Python
COPY requirements.txt ./

# Installer les dépendances Python
RUN pip install --upgrade pip setuptools wheel && \
    pip install -r requirements.txt

# Copier les fichiers de dépendances Node.js depuis src/
COPY src/package.json src/package-lock.json* ./src/
WORKDIR /app/src
RUN npm install

# Retour au répertoire principal
WORKDIR /app

# Copier tout le projet
COPY . .

# Créer les répertoires pour les fichiers statiques et médias
RUN mkdir -p /app/staticfiles /app/uploads

# Exposer le port
EXPOSE 8000

# Script de démarrage
COPY docker/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
