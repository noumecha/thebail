#!/bin/bash
# docker/entrypoint.sh

set -e

echo "🔄 Waiting for database..."
while ! nc -z $DB_HOST $DB_PORT; do
  sleep 0.1
done
echo "✅ Database is ready!"

echo "🔄 Running migrations..."
python manage.py migrate --noinput

# Déterminer la commande npm selon l'environnement
if [ "$DEBUG" = "True" ]; then
    echo "🔄 Building assets (development mode)..."
    cd /app/src && npm run dev
else
    echo "🔄 Building assets (production mode)..."
    cd /app/src && npm run build
fi

cd /app

echo "🔄 Collecting static files..."
python manage.py collectstatic --noinput

echo "🔄 Creating superuser if not exists..."
python manage.py shell << END
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin')
    print('✅ Superuser created')
else:
    print('ℹ️  Superuser already exists')
END

echo "✅ Starting application..."
exec "$@"
