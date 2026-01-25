from django.shortcuts import redirect
from django.urls import reverse
from rest_framework_simplejwt.tokens import AccessToken

PUBLIC_PATHS = [
    '/login/',
    '/logout/',
    '/admin/',
    '/__reload__/',
    '/static/',
    '/media/',
]

class JWTAuthMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path_info

        # Autoriser chemins publics
        if any(path.startswith(p) for p in PUBLIC_PATHS):
            return self.get_response(request)

        # ✅ PRIORITÉ : session Django
        if request.user.is_authenticated:
            return self.get_response(request)

        # JWT cookie
        token = request.COOKIES.get('access_token')
        if token:
            try:
                AccessToken(token)
                return self.get_response(request)
            except Exception:
                response = redirect(reverse('login'))
                response.delete_cookie('access_token')
                return response

        return redirect(reverse('login'))
