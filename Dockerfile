# Dockerfile
FROM python:3.11-slim

# Variables d'environnement
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Installer Node.js et dépendances système
RUN apt-get update && apt-get install -y \
    curl \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Créer le répertoire de travail
WORKDIR /app

# Copier les fichiers de dépendances
COPY requirements.txt package.json package-lock.json* ./

# Installer les dépendances Python
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Installer les dépendances Node.js
RUN npm install

# Copier le projet
COPY . .

# Créer les répertoires pour les fichiers statiques et médias
RUN mkdir -p /app/staticfiles /app/media

# Collecter les fichiers statiques (sera fait au démarrage)
# RUN python manage.py collectstatic --noinput

# Exposer le port
EXPOSE 8000

# Script de démarrage
COPY docker/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
