# 1. Installer les dépendances

pip install -r requirements.txt

# 2. Créer la base de données MySQL locale

mysql -u root -p
CREATE DATABASE thebail_dev CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

# 3. Configurer .env.local

cp .env.example .env.local

# Éditer .env.local avec DB_HOST=localhost

# 4. Migrations

python manage.py migrate --settings=config.settings.development

# or

python manage_dev.py migrate

# 5. Lancer le serveur

python manage.py runserver --settings=config.settings.development
