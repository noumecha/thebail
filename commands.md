# Construire et démarrer

docker-compose up --build

# En arrière-plan

docker-compose up -d

# Voir les logs

docker-compose logs -f web

# Arrêter

docker-compose down

# Construire et démarrer en production

docker-compose -f docker-compose.prod.yml up --build -d

# Voir les logs

docker-compose -f docker-compose.prod.yml logs -f

# Redémarrer un service

docker-compose -f docker-compose.prod.yml restart web

# Arrêter tout

docker-compose -f docker-compose.prod.yml down
