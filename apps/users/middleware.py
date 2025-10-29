from django.http import JsonResponse
from rest_framework.authtoken.models import Token
from django.shortcuts import redirect
from django.urls import reverse
from rest_framework_simplejwt.tokens import AccessToken

# Liste des URLs accessibles sans authentification
PUBLIC_PATHS = [
    '/login/',
    '/api/login/',
    '/logout/',
    '/api/logout/',
    '/admin/',
    '/__reload__/',   # utile en dev
    '/static/',
]

class JWTAuthMiddleware:
    """
    Middleware global qui redirige les utilisateurs non authentifiés vers la page de login.
    Il vérifie le token JWT stocké dans les cookies (access_token).
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path_info

        # Autoriser les chemins publics
        if any(path.startswith(p) for p in PUBLIC_PATHS) or path.startswith('/static/'):
            return self.get_response(request)

        # Ne pas interférer avec les appels d’API REST
        if path.startswith('/api/'):
            return self.get_response(request)

        # Vérifie la présence du cookie d’authentification
        token = request.COOKIES.get('access_token')
        if token:
            try:
                AccessToken(token)  # valide le token
                return self.get_response(request)
            except Exception:
                pass  # token expiré ou invalide → redirection login

        # Redirige vers la page de login
        return redirect(reverse('login'))

class TokenAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # exclure les urls d'authentification
        if request.path in ['/api/users/login/']:
            return self.get_response(request)

        # vérifier le token pour les autres urls
        token_key = request.headers.get('Authorization', '').split(' ')[-1]
        if not token_key:
            return JsonResponse(
                {'error', 'Token manquant'},
                status=401
            )

        try:
            token = Token.objects.get(key=token_key)
            request.user = token.user
        except Token.DoesNotExist:
            return JsonResponse(
                {'error' : 'Token invalide'},
                status=401
            )

        return self.get_response(request)
