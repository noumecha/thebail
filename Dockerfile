# Dockerfile
FROM python:3.11-slim

# Variables d'environnement
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    NODE_ENV=production

# Installer Node.js et dépendances système
RUN apt-get update && apt-get install -y \
    curl \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    netcat-openbsd \
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Créer le répertoire de travail
WORKDIR /app

# Copier les fichiers de dépendances Python
COPY requirements.txt ./
RUN pip install -r requirements.txt

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
